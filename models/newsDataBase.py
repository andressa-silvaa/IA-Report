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
                            category TEXT,
                            classification TEXT
                        )''')
        self.conn.commit()

    def insert_news(self, news_list):
        cursor = self.conn.cursor()
        rows_inserted = 0  # Inicializa o contador de linhas inseridas
        for index, news in enumerate(news_list):
            try:
                cursor.execute('''INSERT INTO news (title, content, age, link, media_img, media_video, locality, category, classification)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                               (news['title'], news['content'], news['age'], news['link'], news['media_img'],
                                news['media_video'], news['locality'], news.get('category', None),
                                news.get('classification', None)))
                rows_inserted += 1  # Incrementa o contador de linhas inseridas
            except Exception as e:
                print(f"Error processing news at index {index}: {e}")
        self.conn.commit()
        return rows_inserted  # Retorna o número total de linhas inseridas

    def insert_news_category(self, news_list):
        cursor = self.conn.cursor()
        for index, news in enumerate(news_list):
            try:
                cursor.execute('''UPDATE news SET category = %s WHERE title = %s''',
                               (news.get('category', None), news['title']))
            except Exception as e:
                print(f"Error processing news at index {index}: {e}")
        self.conn.commit()

    def insert_news_classification(self, news_list):
        cursor = self.conn.cursor()
        for index, news in enumerate(news_list):
            try:
                cursor.execute('''UPDATE news SET classification = %s WHERE content = %s''',
                               (news.get('classification', None), news['content']))
            except Exception as e:
                print(f"Error processing news at index {index}: {e}")
        self.conn.commit()
    def get_all_news(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT n.title,n.content,n.age,n.link,n.media_img,n.media_video,n.locality,n.category,n.classification FROM news n''')
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

    def delete_table(self):
        cursor = self.conn.cursor()
        try:
            # Define autocommit como True para desabilitar o controle de transação
            self.conn.autocommit = True
            cursor.execute('''DROP TABLE news''')
            return True
        except Exception as e:
            print(f"Error deleting database: {e}")
            return False
        finally:
            # Retorna ao modo de transação padrão após a execução
            self.conn.autocommit = False

    def check_null_category(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT n.category FROM news n WHERE n.category IS NULL or n.category = ''")
            result = cursor.fetchone()
            if result is not None:
                count = result[0]
                return count == 0
            else:
                return True
        except Exception as e:
            print(f"Error checking for null values: {e}")
            return True
    def check_null_classification(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT n.classification FROM news n WHERE n.classification IS NULL")
            result = cursor.fetchone()
            if result is not None:
                count = result[0]
                return count == 0
            else:
                return True
        except Exception as e:
            print(f"Error checking for null values: {e}")
            return True


    def close_connection(self):
        self.conn.close()