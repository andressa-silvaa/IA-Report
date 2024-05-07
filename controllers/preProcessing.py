import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from datetime import datetime, timedelta
import spacy
from controllers.newsCollection import NewsCollection

class PreProcessing:
    def __init__(self, news_collection):
        self.news_collection = news_collection
        self.stop_words = set(stopwords.words('portuguese'))
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load('pt_core_news_sm')
        self.categories = {
            'agricultura': ['agricultura', 'agricultor', 'plantio', 'lavoura', 'agroindústria', 'agronegócio'],
            'agropecuária': ['agropecuária', 'pecuária', 'fazenda', 'gado', 'criação', 'pecuarista'],
            'garimpo': ['garimpo', 'mineradora', 'mineração', 'extração', 'exploração', 'lavra'],
            'atividades ilegais': ['ilegal', 'crime', 'contrabando', 'tráfico', 'ilegalidade', 'ilegalmente'],
            'outro': []
        }

    def process_data(self):
        content = self.news_collection.load_page()
        news_list = self.news_collection.extract_info(content)

        # Pré-processamento dos dados
        processed_news_list = []
        for news in news_list:
            processed_news = self.preprocess_news(news)
            processed_news_list.append(processed_news)

        # Filtrar as notícias relacionadas ao desmatamento
        filtered_news = [news for news in processed_news_list if self.is_deforestation(news)]

        # Adicionar categorias com base em critérios
        categorized_news = self.add_categories(filtered_news)

        # Converter a lista de notícias filtrada em um DataFrame
        df = pd.DataFrame(categorized_news)

        df['locality'] = df['content'].apply(self.extract_location)

        df.to_excel('news_data.xlsx', index=False)

        # Retornar o DataFrame
        return df

    def preprocess_news(self, news):
        processed_news = {}
        processed_news['title'] = self.preprocess_text(news['title'])
        processed_news['content'] = self.preprocess_text(news['content'])
        processed_news['age'] = self.convert_age_to_date(news['age'])
        processed_news['link'] = news['link']
        processed_news['media_img'] = news['media_img']
        processed_news['media_video'] = news['media_video']
        return processed_news

    def preprocess_text(self, text):
        # Remoção de caracteres especiais e pontuações
        text = re.sub(r'[^\w\s]', '', text)
        # Tokenização
        tokens = word_tokenize(text.lower())
        # Remoção de stopwords
        tokens = [word for word in tokens if word not in self.stop_words]
        # Stemming
        tokens = [self.stemmer.stem(word) for word in tokens]
        return ' '.join(tokens)

    def convert_age_to_date(self, age):
        # Verifica se a idade está no formato "há X dias"
        if 'há' in age:
            days_ago = int(age.split()[1])
            date = datetime.now() - timedelta(days=days_ago)
        else:
            # Se não estiver no formato "há X dias", assume que está no formato "DD/MM/YYYY HH:mm"
            date = datetime.strptime(age, '%d/%m/%Y %Hh%M')
        return date

    def is_deforestation(self, news):
        title = news['title']
        content = news['content']
        return 'desmatamento' in title or 'desmatamento' in content

    def add_categories(self, news_list):
        categorized_news = []
        category_counter = 0
        for news in news_list:
            if category_counter < 3:
                category = self.classify_category(news['title'], news['content'])
                news['category'] = category
                category_counter += 1
            else:
                news['category'] = ''
                category_counter = 0
            categorized_news.append(news)
        return categorized_news

    def classify_category(self, title, content):
        # Convertendo o título e o conteúdo para minúsculas para tornar a comparação insensível a maiúsculas e minúsculas
        text = f"{title.lower()} {content.lower()}"
        for category, keywords in self.categories.items():
            # Aplicando stemming nas palavras-chave de cada categoria
            stemmed_keywords = [self.stemmer.stem(word) for word in keywords]
            # Verifica se alguma palavra-chave ou sinônimo está presente no texto da notícia
            for keyword in stemmed_keywords:
                # Usando expressões regulares para encontrar correspondências de palavras inteiras
                if re.search(rf"\b{keyword}\b", text):
                    return category
        # Se nenhum padrão corresponder, atribui a categoria 'outro'
        return 'outro'

    def extract_location(self, text):
        doc = self.nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ == 'LOC']
        return ', '.join(locations) if locations else None

if __name__ == "__main__":
    url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1y'
    news_collection = NewsCollection(url)

    news_repository = PreProcessing(news_collection)
    news_list = news_repository.process_data()
    print(news_list)
