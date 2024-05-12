from models.newsDataBase import NewsDataBase
from models.news import News

class NewsRepository:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def process_and_save_news(self, df):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        news_list = df.to_dict('records')
        try:
            news_database.insert_news(news_list)
        except Exception as e:
            print(f"Error processing and saving news: {e}")

    def get_all_news(self):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        try:
            rows = news_database.get_all_news()
            return(rows)
            #return [self._row_to_news(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving all news: {e}")
            return []

    def get_news_by_title(self, title):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        try:
            rows = news_database.get_news_by_title(title)
            return [self._row_to_news(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving news by title: {e}")
            return []

    def get_news_by_locality(self, locality):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        try:
            rows = news_database.get_news_by_locality(locality)
            return [self._row_to_news(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving news by locality: {e}")
            return []

    def get_news_by_age(self, days):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        try:
            rows = news_database.get_news_by_age(days)
            return [self._row_to_news(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving news by age: {e}")
            return []

    def get_news_by_title_keyword(self, keyword):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        try:
            rows = news_database.get_news_by_title_keyword(keyword)
            return [self._row_to_news(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving news by title keyword: {e}")
            return []

    def get_news_by_content_keyword(self, keyword):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        try:
            rows = news_database.get_news_by_content_keyword(keyword)
            return [self._row_to_news(row) for row in rows]
        except Exception as e:
            print(f"Error retrieving news by content keyword: {e}")
            return []

    def update_news(self, news_id, new_data):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        try:
            news_database.update_news(news_id, new_data)
        except Exception as e:
            print(f"Error updating news: {e}")

    def delete_news(self, news_id):
        news_database = NewsDataBase(self.dbname, self.user, self.password, self.host, self.port)
        try:
            news_database.delete_news(news_id)
        except Exception as e:
            print(f"Error deleting news: {e}")

    def _row_to_news(self, row):
        return News(row[1], row[2], row[3], row[4], row[5], row[6], row[7])