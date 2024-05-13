import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Concatenate, Dropout
from controllers.newsRepository import NewsRepository

class NewsClassifier:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.model = None
        self.tokenizer = None
        self.label_encoder = None

    def load_data_from_database(self):
        news_repo = NewsRepository(self.db_name, self.db_user, self.db_password, self.db_host, self.db_port)
        news_data = news_repo.get_title_content_category()
        df = pd.DataFrame(news_data, columns=['title', 'content', 'category'])
        return df

    def preprocess_data(self, df):
        df['content'] = df['content'].apply(lambda x: str(x).lower())
        df['title'] = df['title'].apply(lambda x: str(x).lower())
        df['category'].replace('', np.nan, inplace=True)
        df['category'].fillna('unknown', inplace=True)
        df_train = df[df['category'] != 'unknown']
        return df_train

    def tokenize_data(self, X_train, X_test):
        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(X_train['title'] + ' ' + X_train['content'])

        X_train_title_seq = self.tokenizer.texts_to_sequences(X_train['title'])
        X_train_content_seq = self.tokenizer.texts_to_sequences(X_train['content'])
        X_test_title_seq = self.tokenizer.texts_to_sequences(X_test['title'])
        X_test_content_seq = self.tokenizer.texts_to_sequences(X_test['content'])

        max_len = 100
        X_train_title_seq = pad_sequences(X_train_title_seq, maxlen=max_len)
        X_train_content_seq = pad_sequences(X_train_content_seq, maxlen=max_len)
        X_test_title_seq = pad_sequences(X_test_title_seq, maxlen=max_len)
        X_test_content_seq = pad_sequences(X_test_content_seq, maxlen=max_len)

        return X_train_title_seq, X_train_content_seq, X_test_title_seq, X_test_content_seq

    def encode_labels(self, y_train, y_test):
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(y_train)
        y_train_encoded = self.label_encoder.transform(y_train)
        y_test_encoded = self.label_encoder.transform(y_test)
        return y_train_encoded, y_test_encoded

    def build_model(self, vocab_size, embedding_dim, max_len):
        input_title = Input(shape=(max_len,))
        input_content = Input(shape=(max_len,))
        embedding_title = Embedding(vocab_size, embedding_dim)(input_title)
        embedding_content = Embedding(vocab_size, embedding_dim)(input_content)
        lstm_title = LSTM(128, dropout=0.2, recurrent_dropout=0.2)(embedding_title)
        lstm_content = LSTM(128, dropout=0.2, recurrent_dropout=0.2)(embedding_content)
        concatenated = Concatenate()([lstm_title, lstm_content])
        dense_layer = Dense(128, activation='relu')(concatenated)
        dropout_layer = Dropout(0.5)(dense_layer)
        output = Dense(len(self.label_encoder.classes_), activation='softmax')(dropout_layer)
        self.model = Model(inputs=[input_title, input_content], outputs=output)
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    def train_model(self, X_train_title_seq, X_train_content_seq, y_train_encoded, epochs, batch_size, validation_split):
        self.model.fit([X_train_title_seq, X_train_content_seq], y_train_encoded, epochs=epochs, batch_size=batch_size, validation_split=validation_split)

    def evaluate_model(self, X_test_title_seq, X_test_content_seq, y_test_encoded):
        return self.model.evaluate([X_test_title_seq, X_test_content_seq], y_test_encoded)

    def predict_missing_categories(self, df_missing):
        X_missing_title_seq = pad_sequences(self.tokenizer.texts_to_sequences(df_missing['title']), maxlen=100)
        X_missing_content_seq = pad_sequences(self.tokenizer.texts_to_sequences(df_missing['content']), maxlen=100)
        predictions = self.model.predict([X_missing_title_seq, X_missing_content_seq])
        predicted_categories = self.label_encoder.inverse_transform(np.argmax(predictions, axis=1))
        return predicted_categories

    def fill_missing_categories(self, df, predicted_categories):
        df.loc[df['category'] == 'unknown', 'category'] = predicted_categories
        return df

    def save_dataframe_to_excel(self, df, filename):
        df.to_excel(filename, index=False)

if __name__ == "__main__":
    db_name = 'usjlmkja'
    db_user = 'usjlmkja'
    db_password = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
    db_host = 'isabelle.db.elephantsql.com'
    db_port = '5432'

    news_classifier = NewsClassifier(db_name, db_user, db_password, db_host, db_port)
    df = news_classifier.load_data_from_database()
    df_train = news_classifier.preprocess_data(df)

    X_train, X_test, y_train, y_test = train_test_split(df_train[['title', 'content']], df_train['category'], test_size=0.2, random_state=42)

    X_train_title_seq, X_train_content_seq, X_test_title_seq, X_test_content_seq = news_classifier.tokenize_data(X_train, X_test)
    y_train_encoded, y_test_encoded = news_classifier.encode_labels(y_train, y_test)

    vocab_size = len(news_classifier.tokenizer.word_index) + 1
    embedding_dim = 100

    news_classifier.build_model(vocab_size, embedding_dim, max_len=100)
    news_classifier.train_model(X_train_title_seq, X_train_content_seq, y_train_encoded, epochs=10, batch_size=64, validation_split=0.1)

    loss, accuracy = news_classifier.evaluate_model(X_test_title_seq, X_test_content_seq, y_test_encoded)
    print(f'Test Accuracy: {accuracy}')

    df_missing = df[df['category'] == 'unknown']
    predicted_categories = news_classifier.predict_missing_categories(df_missing)
    df_filled = news_classifier.fill_missing_categories(df, predicted_categories)

    news_classifier.save_dataframe_to_excel(df_filled, 'news_data.xlsx')
