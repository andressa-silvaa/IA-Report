import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from controllers.newsRepository import NewsRepository
class SentimentAnalysis:
    def __init__(self, news_repository):
        self.news_repository = news_repository
        nltk.download('vader_lexicon')
        self.sid = SentimentIntensityAnalyzer()

    def analyze_sentiment(self):
        # Obtenha todas as notícias do NewsRepository
        all_news = self.news_repository.get_all_news()

        # Inicialize contadores para os sentimentos
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Loop sobre todas as notícias e conte os sentimentos
        for news in all_news:
            # Obtenha o texto da notícia
            text = news.content

            # Realize a análise de sentimento
            sentiment_score = self.sid.polarity_scores(text)
            compound_score = sentiment_score['compound']

            # Classifique o sentimento com base no score composto
            if compound_score >= 0.05:
                positive_count += 1
            elif compound_score <= -0.05:
                negative_count += 1
            else:
                neutral_count += 1

        # Calcule as porcentagens de cada sentimento
        total_news = len(all_news)
        positive_percentage = round((positive_count / total_news) * 100, 2)
        negative_percentage = round((negative_count / total_news) * 100, 2)
        neutral_percentage = round((neutral_count / total_news) * 100, 2)

        # Retorne as porcentagens de cada sentimento
        return {
            'positiva': positive_percentage,
            'negativa': negative_percentage,
            'neutra': neutral_percentage
        }
if __name__ == "__main__":

    db_name = 'usjlmkja'
    db_user = 'usjlmkja'
    db_password = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
    db_host = 'isabelle.db.elephantsql.com'
    db_port = '5432'

    news_repository = NewsRepository(db_name, db_user, db_password, db_host, db_port)

    # Inicializa a análise de sentimento
    sentiment_analyzer = SentimentAnalysis(news_repository)

    # Realiza a análise de sentimento
    sentiment_result = sentiment_analyzer.analyze_sentiment()

    # Imprime o resultado da análise de sentimento
    print("Análise de Sentimento:")
    print(f"Positiva: {sentiment_result['positiva']}%")
    print(f"Negativa: {sentiment_result['negativa']}%")
    print(f"Neutra: {sentiment_result['neutra']}%")