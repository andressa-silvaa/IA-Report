import pandas as pd
import numpy as np
import random
import tensorflow as tf
from controllers.newsRepository import NewsRepository
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout

class NewsCategorizer:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        np.random.seed(42)
        tf.random.set_seed(42)
        random.seed(42)

        self.news_repo = NewsRepository(db_name, db_user, db_password, db_host, db_port)
        self.df = None
        self.tokenizer = Tokenizer()
        self.label_encoder = LabelEncoder()

    def fetch_data(self):
        news_data = self.news_repo.get_title_content_category()
        self.df = pd.DataFrame(news_data, columns=['title', 'content', 'category'])
        self.df.to_excel('original.xlsx', index=False)

    def preprocess_data(self):
        self.df['content'] = self.df['content'].str.lower()
        self.df['title'] = self.df['title'].str.lower()
        self.df['category'].replace('', np.nan, inplace=True)
        self.df['category'].fillna('unknown', inplace=True)

    def split_data(self):
        df_train = self.df[self.df['category'] != 'unknown']
        X_train, X_test, y_train, y_test = train_test_split(df_train[['title', 'content']], df_train['category'], test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def tokenize_data(self, X_train, X_test):
        self.tokenizer.fit_on_texts(X_train['title'] + ' ' + X_train['content'])
        max_len = 100
        X_train_seq = pad_sequences(self.tokenizer.texts_to_sequences(X_train['title'] + ' ' + X_train['content']), maxlen=max_len)
        X_test_seq = pad_sequences(self.tokenizer.texts_to_sequences(X_test['title'] + ' ' + X_test['content']), maxlen=max_len)
        return X_train_seq, X_test_seq

    def encode_labels(self, y_train, y_test):
        self.label_encoder.fit(y_train)
        y_train_encoded = self.label_encoder.transform(y_train)
        y_test_encoded = self.label_encoder.transform(y_test)
        return y_train_encoded, y_test_encoded

    def build_model(self, vocab_size, embedding_dim, max_len, num_classes):
        model = Sequential([
            Embedding(vocab_size, embedding_dim, input_length=max_len),
            Conv1D(256, 5, activation='relu'),
            GlobalMaxPooling1D(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(num_classes, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def train_model(self, model, X_train, y_train_encoded):
        model.fit(X_train, y_train_encoded, epochs=20, batch_size=128, validation_split=0.1)

    def evaluate_model(self, model, X_test, y_test_encoded):
        return model.evaluate(X_test, y_test_encoded)

    def predict_missing_categories(self):
        df_missing = self.df[self.df['category'] == 'unknown']
        X_missing_seq = pad_sequences(self.tokenizer.texts_to_sequences(df_missing['title'] + ' ' + df_missing['content']), maxlen=100)
        predictions = self.model.predict(X_missing_seq)
        predicted_categories = self.label_encoder.inverse_transform(np.argmax(predictions, axis=1))
        self.df.loc[self.df['category'] == 'unknown', 'category'] = predicted_categories

    def display_updated_dataframe(self):
        print(self.df)
        self.df.to_excel('news_data.xlsx', index=False)

    def save_category(self, filename='category_data.xlsx'):
        category_df = self.df[['title', 'category']].copy()
        self.news_repo.process_and_save_news_category(category_df)


if __name__ == "__main__":
    # Example of usage
    db_name = 'usjlmkja'
    db_user = 'usjlmkja'
    db_password = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
    db_host = 'isabelle.db.elephantsql.com'
    db_port = '5432'

    categorizer = NewsCategorizer(db_name, db_user, db_password, db_host, db_port)
    categorizer.fetch_data()
    categorizer.preprocess_data()
    X_train, X_test, y_train, y_test = categorizer.split_data()
    X_train_seq, X_test_seq = categorizer.tokenize_data(X_train, X_test)
    y_train_encoded, y_test_encoded = categorizer.encode_labels(y_train, y_test)
    vocab_size = len(categorizer.tokenizer.word_index) + 1
    embedding_dim = 100
    categorizer.model = categorizer.build_model(vocab_size, embedding_dim, 100, len(categorizer.label_encoder.classes_))
    categorizer.train_model(categorizer.model, X_train_seq, y_train_encoded)
    loss, accuracy = categorizer.evaluate_model(categorizer.model, X_test_seq, y_test_encoded)
    print(f'Test Accuracy: {accuracy}')
    categorizer.predict_missing_categories()
    categorizer.save_category()
    categorizer.display_updated_dataframe()

