from controllers.newsCollection import NewsCollection
from controllers.preProcessing import PreProcessing
from controllers.newsRepository import NewsRepository
from models.sentimentAnalysis import SentimentAnalysis

def main():
    # URL da página de notícias que você deseja coletar
    url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1y'

    # Inicializa o objeto responsável pela coleta de notícias
    news_collection = NewsCollection(url)

    # Inicializa o objeto responsável pelo pré-processamento das notícias
    pre_processor = PreProcessing(news_collection)

    # Processa os dados das notícias
    news_data = pre_processor.process_data()

    # Inicializa o objeto responsável pelo acesso ao banco de dados
    db_name = 'usjlmkja'
    db_user = 'usjlmkja'
    db_password = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
    db_host = 'isabelle.db.elephantsql.com'
    db_port = '5432'

    news_repository = NewsRepository(db_name, db_user, db_password, db_host, db_port)

    # Salva as notícias no banco de dados
    news_repository.process_and_save_news(news_data)

    sentiment_analyzer = SentimentAnalysis(news_repository)

    # Realiza a análise de sentimento
    sentiment_result = sentiment_analyzer.analyze_sentiment()

    # Imprime o resultado da análise de sentimento
    print("Análise de Sentimento:")
    print(f"Positiva: {sentiment_result['positiva']}%")
    print(f"Negativa: {sentiment_result['negativa']}%")
    print(f"Neutra: {sentiment_result['neutra']}%")

if __name__ == "__main__":
    main()