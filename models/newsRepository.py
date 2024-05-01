from preProcessing import PreProcessing
from newsDataBase import NewsDataBase


class NewsRepository:
    def __init__(self, news_collection, db_file):
        self.preprocessor = PreProcessing(news_collection)
        self.news_database = NewsDataBase(db_file)

    def process_and_save_news(self):
        try:
            news_list = self.preprocessor.process_data()
            self.news_database.insert_news(news_list)
        except Exception as e:
            print(f"Error processing and saving news: {e}")

    def get_all_news(self):
        try:
            return self.news_database.get_all_news()
        except Exception as e:
            print(f"Error retrieving all news: {e}")
            return []

    def get_news_by_title(self, title):
        try:
            return self.news_database.get_news_by_title(title)
        except Exception as e:
            print(f"Error retrieving news by title: {e}")
            return []

    def get_news_by_locality(self, locality):
        try:
            return self.news_database.get_news_by_locality(locality)
        except Exception as e:
            print(f"Error retrieving news by locality: {e}")
            return []

    def get_news_by_age(self, days):
        try:
            return self.news_database.get_news_by_age(days)
        except Exception as e:
            print(f"Error retrieving news by age: {e}")
            return []

    def get_news_by_title_keyword(self, keyword):
        try:
            return self.news_database.get_news_by_title_keyword(keyword)
        except Exception as e:
            print(f"Error retrieving news by title keyword: {e}")
            return []

    def get_news_by_content_keyword(self, keyword):
        try:
            return self.news_database.get_news_by_content_keyword(keyword)
        except Exception as e:
            print(f"Error retrieving news by content keyword: {e}")
            return []

    def update_news(self, news_id, new_data):
        try:
            self.news_database.update_news(news_id, new_data)
        except Exception as e:
            print(f"Error updating news: {e}")

    def delete_news(self, news_id):
        try:
            self.news_database.delete_news(news_id)
        except Exception as e:
            print(f"Error deleting news: {e}")
