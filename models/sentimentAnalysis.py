import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from controllers.newsRepository import NewsRepository

class SentimentAnalyzer:
    def __init__(self):
        np.random.seed(42)
        tf.random.set_seed(42)

    def load_training_data(self, filename):
        return pd.read_excel(filename)

    def balance_classes(self, df):
        print("Balanceamento das classes:")
        print(df['classification'].value_counts())
        return df

    def map_classifications(self, df):
        mapeamento_classificacoes = {'ruim': 1, 'boa': 0}
        df['classification'] = df['classification'].map(mapeamento_classificacoes)
        return df

    def prepare_data(self, content, classification):
        tokenizer = Tokenizer(num_words=5000, oov_token='<OOV>')
        tokenizer.fit_on_texts(content)
        sequences = tokenizer.texts_to_sequences(content)
        padded = pad_sequences(sequences, maxlen=100)
        X_train, X_val, y_train, y_val = train_test_split(padded, classification, test_size=0.2, random_state=42)
        return X_train, X_val, y_train, y_val, tokenizer

    def build_model(self, word_index):
        model = Sequential([
            Embedding(input_dim=len(word_index) + 1, output_dim=200, input_length=100),
            LSTM(128, dropout=0.2, recurrent_dropout=0.2),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def train_model(self, model, X_train, y_train, X_val, y_val):
        history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=64)
        return model

    def save_model(self, model, filename):
        model.save(filename)
        print("Modelo treinado salvo.")

    def analyze_sentiment(self, tokenizer):
        try:
            model = tf.keras.models.load_model('modelo_sentimento.h5')
            news_repo = NewsRepository('usjlmkja', 'usjlmkja', 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT', 'isabelle.db.elephantsql.com', '5432')
            news_data = news_repo.get_all_news()
            df_dados = pd.DataFrame(news_data, columns=['title', 'content', 'age','link','media_img','media_video','locality','category','classification'])
            df = df_dados[['content', 'classification']].copy()
            sequences = tokenizer.texts_to_sequences(df['content'])
            padded = pad_sequences(sequences, maxlen=100)
            predictions = model.predict(padded)
            predicted_classification = np.round(predictions).astype(int)
            mapping = {1: 'ruim', 0: 'boa'}
            predicted_classification = [mapping[prev[0]] for prev in predicted_classification]
            df['predicted_classification'] = predicted_classification
            df.to_excel('resultados_analise_sentimento.xlsx', index=False)
            classification_df = df[['content', 'predicted_classification']].copy()
            classification_df = classification_df.rename(columns={'predicted_classification': 'classification'})
            news_repo.process_and_save_news_classification(classification_df)
            print("Resultados da análise de sentimento salvos em 'resultados_analise_sentimento.xlsx'.")
        except Exception as e:
            print("Erro durante a análise de sentimento:", str(e))

if __name__ == "__main__":
    sentiment_analyzer = SentimentAnalyzer()
    df_treino = sentiment_analyzer.load_training_data('treino.xlsx')
    df_treino = sentiment_analyzer.balance_classes(df_treino)
    df_treino = sentiment_analyzer.map_classifications(df_treino)
    conteudo_treino = df_treino['content'].values
    classificacao_treino = df_treino['classification'].values
    X_train, X_val, y_train, y_val, tokenizer = sentiment_analyzer.prepare_data(conteudo_treino, classificacao_treino)
    model = sentiment_analyzer.build_model(tokenizer.word_index)
    trained_model = sentiment_analyzer.train_model(model, X_train, y_train, X_val, y_val)
    sentiment_analyzer.save_model(trained_model, 'modelo_sentimento.h5')
    sentiment_analyzer.analyze_sentiment(tokenizer)
