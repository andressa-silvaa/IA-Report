from controllers.newsRepository import NewsRepository
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

class DesmatamentoClassifier:
    def __init__(self, news_repository):
        self.news_repository = news_repository
        self.vectorizer = TfidfVectorizer(stop_words='portuguese')  # Ignora palavras comuns em português
        self.model = MultinomialNB()

    def train_model(self):
        # Obter os dados do banco de dados
        news_data = self.news_repository.get_all_news()
        X = []
        y = []
        for news in news_data:
            print(news.category)

        # Filtrar os documentos não vazios com categoria
        for news in news_data:
            if news.content and news.category:
                X.append(news.content)
                y.append(news.category)

        # Verifica se há documentos não vazios com categoria
        if X:
            # Vetorização dos dados de texto
            X = self.vectorizer.fit_transform(X)

            # Treinamento do modelo Naive Bayes
            self.model.fit(X, y)
        else:
            print("Nenhum documento não vazio com categoria encontrado para treinar o modelo.")

    def predict_category(self, news_content):
        # Verifica se o conteúdo da notícia não está vazio
        if news_content:
            # Vetorização do conteúdo da notícia
            X = self.vectorizer.transform([news_content])

            # Predição da categoria
            predicted_category = self.model.predict(X)

            return predicted_category[0]
        else:
            print("O conteúdo da notícia está vazio. Não é possível fazer uma previsão.")

if __name__ == "__main__":
    db_name = 'usjlmkja'
    db_user = 'usjlmkja'
    db_password = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
    db_host = 'isabelle.db.elephantsql.com'
    db_port = '5432'

    news_repository = NewsRepository(db_name, db_user, db_password, db_host, db_port)

    classifier = DesmatamentoClassifier(news_repository)
    classifier.train_model()
