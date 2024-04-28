from newsCollection import NewsCollection
import pandas as pd
class NewsRepository:
    def __init__(self, news_collection):
        self.news_collection = news_collection

    def process_data(self):
        content = self.news_collection.load_page()
        news_list = self.news_collection.extract_info(content)

        # Filtrar as notícias relacionadas ao desmatamento
        filtered_news = [news for news in news_list if self.is_deforestation(news)]

        # Converter a lista de notícias filtrada em um DataFrame
        df = pd.DataFrame(filtered_news)
        df.to_excel('news_data.xlsx', index=False)

        # Retornar o DataFrame
        return df

    def is_deforestation(self, news):
        title = news['title']
        content = news['content']
        return 'desmatamento' in title.lower() or 'desmatamento' in content.lower()

    def save_to_database(self, processed_data):
        # Método para salvar os dados processados no banco de dados
        pass

    # Outros métodos necessários podem ser adicionados aqui


if __name__ == "__main__":
    url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1M'
    news_collection = NewsCollection(url)

    news_repository = NewsRepository(news_collection)
    news_list = news_repository.process_data()
    print(news_list)