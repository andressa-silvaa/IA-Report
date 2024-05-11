import pandas as pd
import numpy as np
from controllers.newsRepository import NewsRepository
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Concatenate

# Conectar ao banco de dados e recuperar os dados
db_name = 'usjlmkja'
db_user = 'usjlmkja'
db_password = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
db_host = 'isabelle.db.elephantsql.com'
db_port = '5432'

news_repo = NewsRepository(db_name, db_user, db_password, db_host, db_port)
news_data = news_repo.get_all_news()

# Criar DataFrame diretamente dos dados com os nomes das colunas especificados
df = pd.DataFrame(news_data, columns=['title', 'content', 'category'])
df.to_excel('original.xlsx', index=False)
# Pré-processamento dos dados
df['content'] = df['content'].apply(lambda x: str(x).lower())  # Converte para minúsculas
df['title'] = df['title'].apply(lambda x: str(x).lower())      # Converte para minúsculas

# Substituindo categorias vazias por NaN
df['category'].replace('', np.nan, inplace=True)

# Preenchendo valores ausentes na coluna 'category' com uma tag especial
df['category'].fillna('unknown', inplace=True)

# Filtrando exemplos com categorias válidas para treinamento
df_train = df[df['category'] != 'unknown']

# Dividindo os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(df_train[['title', 'content']], df_train['category'], test_size=0.2, random_state=42)

# Tokenização dos dados de entrada
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train['title'] + ' ' + X_train['content'])

X_train_title_seq = tokenizer.texts_to_sequences(X_train['title'])
X_train_content_seq = tokenizer.texts_to_sequences(X_train['content'])
X_test_title_seq = tokenizer.texts_to_sequences(X_test['title'])
X_test_content_seq = tokenizer.texts_to_sequences(X_test['content'])

# Preenchendo sequências para ter o mesmo comprimento
max_len = 100
X_train_title_seq = pad_sequences(X_train_title_seq, maxlen=max_len)
X_train_content_seq = pad_sequences(X_train_content_seq, maxlen=max_len)
X_test_title_seq = pad_sequences(X_test_title_seq, maxlen=max_len)
X_test_content_seq = pad_sequences(X_test_content_seq, maxlen=max_len)

# Codificação das categorias
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
y_train_encoded = label_encoder.transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Construindo o modelo
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 100

# Inputs separados para título e conteúdo
input_title = Input(shape=(max_len,))
input_content = Input(shape=(max_len,))

# Camadas de embedding separadas para título e conteúdo
embedding_title = Embedding(vocab_size, embedding_dim)(input_title)
embedding_content = Embedding(vocab_size, embedding_dim)(input_content)

# Camadas LSTM separadas para título e conteúdo
lstm_title = LSTM(128)(embedding_title)
lstm_content = LSTM(128)(embedding_content)

# Concatenando as saídas das camadas LSTM
concatenated = Concatenate()([lstm_title, lstm_content])

# Camada densa para previsão da categoria
output = Dense(len(label_encoder.classes_), activation='softmax')(concatenated)

# Definindo o modelo
model = Model(inputs=[input_title, input_content], outputs=output)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Treinamento do modelo
model.fit([X_train_title_seq, X_train_content_seq], y_train_encoded, epochs=10, batch_size=64, validation_split=0.1)

# Avaliação do modelo
loss, accuracy = model.evaluate([X_test_title_seq, X_test_content_seq], y_test_encoded)
print(f'Test Accuracy: {accuracy}')

# Preenchimento dos valores ausentes na coluna 'category'
df_missing = df[df['category'] == 'unknown']
X_missing_title_seq = pad_sequences(tokenizer.texts_to_sequences(df_missing['title']), maxlen=max_len)
X_missing_content_seq = pad_sequences(tokenizer.texts_to_sequences(df_missing['content']), maxlen=max_len)

predictions = model.predict([X_missing_title_seq, X_missing_content_seq])
predicted_categories = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

# Preenchendo os valores previstos de categoria de volta ao DataFrame original
df.loc[df['category'] == 'unknown', 'category'] = predicted_categories

# Exibindo o DataFrame atualizado
print(df)
df.to_excel('news_data.xlsx', index=False)