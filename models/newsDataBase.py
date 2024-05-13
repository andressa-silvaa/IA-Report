import psycopg2
class NewsDataBase:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                            id SERIAL PRIMARY KEY,
                            title TEXT,
                            content TEXT,
                            age TIMESTAMP,
                            link TEXT,
                            media_img TEXT,
                            media_video TEXT,
                            locality TEXT,
                            category TEXT
                        )''')
        self.conn.commit()

    def insert_news(self, news_list):
        cursor = self.conn.cursor()
        for index, news in enumerate(news_list):
            try:
                cursor.execute('''INSERT INTO news (title, content, age, link, media_img, media_video, locality, category)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                               (news['title'], news['content'], news['age'], news['link'], news['media_img'],
                                news['media_video'], news['locality'], news.get('category', None)))
            except Exception as e:
                print(f"Error processing news at index {index}: {e}")
        self.conn.commit()

    def insert_news_category(self, news_list):
        cursor = self.conn.cursor()
        for index, news in enumerate(news_list):
            try:
                cursor.execute('''UPDATE news SET category = %s WHERE title = %s''',
                               (news.get('category', None), news['title']))
            except Exception as e:
                print(f"Error processing news at index {index}: {e}")
        self.conn.commit()
    def get_all_news(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT n.title,n.content,n.age,n.link,n.media_img,n.media_video,n.locality,n.category FROM news n''')
        rows = cursor.fetchall()
        return rows
    def get_title_content_category(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT n.title,n.content,n.category FROM news n''')
        rows = cursor.fetchall()
        return rows

    def get_news_by_title(self, title):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM news WHERE title = %s''', (title,))
        rows = cursor.fetchall()
        return rows

    def get_news_by_locality(self, locality):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM news WHERE locality = %s''', (locality,))
        rows = cursor.fetchall()
        return rows

    def get_news_by_age(self, days):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM news WHERE age >= NOW() - INTERVAL '%s days' ORDER BY age DESC''', (days,))
        rows = cursor.fetchall()
        return rows

    def get_news_by_title_keyword(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM news WHERE title ILIKE %s''', ('%{}%'.format(keyword),))
        rows = cursor.fetchall()
        return rows

    def get_news_by_content_keyword(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM news WHERE content ILIKE %s''', ('%{}%'.format(keyword),))
        rows = cursor.fetchall()
        return rows

    def update_news(self, news_id, new_data):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE news 
                          SET title=%s, content=%s, age=%s, link=%s, media_img=%s, media_video=%s, locality=%s
                          WHERE id=%s''',
                       (new_data['title'], new_data['content'], new_data['age'], new_data['link'], new_data['media_img'], new_data['media_video'], new_data['locality'], news_id))
        self.conn.commit()

    def delete_news(self, news_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM news WHERE id=%s''', (news_id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()