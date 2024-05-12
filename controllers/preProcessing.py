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
            'multas': ['multas', 'autuações', 'penalidades', 'sanções', 'infrações', 'coimas'],
            'alertas': ['alertas', 'avisos', 'notificações', 'alarmes', 'advertências', 'sinalizações'],
            'agricultura': ['agricultura', 'agricultor', 'plantio', 'lavoura', 'agroindústria', 'agronegócio','agrícola'],
            'agropecuária': ['agropecuária', 'pecuária', 'fazenda', 'gado', 'criação', 'pecuarista'],
            'garimpo': ['garimpo', 'mineradora', 'mineração', 'extração', 'exploração', 'lavra'],
            'fiscalização': ['fiscalização', 'fiscalizar', 'inspeção', 'auditoria', 'regulação', 'polícia',
                             'fiscalizam', 'prende', 'acusado', 'operação', 'coordenadoria', 'flagram', 'flagrou',
                             'polícia', 'flagra','flagrado','preso'],
            'ação governamental': ['governo', 'governamental', 'política pública', 'medidas governamentais',
                                   'gestão pública','programa','combate'],
            'atividades ilegais': ['ilegal', 'contrabando', 'tráfico', 'ilegalidade', 'ilegalmente'],
            'estatísticas': ['estatísticas', 'dados', 'indicadores', 'análise estatística', 'pesquisas','índice','rank','%','área','estudo','tendência','redução','queda','cai','taxa','aponta','levantamento','cresce','caiu'],
            'conscientização pública': ['conscientização', 'educação ambiental', 'mobilização social',
                                        'campanhas educativas', 'sensibilização', 'consciência ambiental','ambientalista','protestam','dúvida','promotor']
        }

        self.forbidden_locations = ['crime ambient','polícia feder combat, airão interior amazona divulgaçãopf','registr',
                                    'oest, instituto nacion','maracanã','sobrevoo região','urbana rurai edificaçõ nova','polícia','combat','estado','secretaria estado meio ambient registr','confira','g1',
                                    'cerrado','projeto','reunião batalhão ambient brigada militar','barreira combat','feder, airão interior amazona divulgação','ambient indenfic 7500',
                                    'proprietário','polícia ambient indenfic 7500','polícia ambient', 'mp','proprietário licença ambient','união',', brasil, guarda','oest, instituto nacion',
                                    'fundação so mata atlântica','conceição mato, ond','terçafeira','polícia feder prend suspeito','ilha banan','engenheiro ambient',
                                    'semana','sc','polícia militar ambient idenfitif','militar ambient, barro branco joão paraíso','polícia militar localiz atravé',
                                    'cidad','polícia feder','informaçõ','polícia militar ambient identific irregularidad','glasgow, brasil','informaçõ','informaçõ, instituto nacion pesquisa',
                                    'vale jequitinhonha balanço','instituto nacion pesquisa','pf','piauí, instituto nacion pesquisa','viraliz banquet ave','sei pessoa','comentarista andré trigueiro analisa',
                                    'abordagem ibama','milhõ durant operaçõ gerência','levantamento','polícia feder acr','grand proporçõ','mapbioma',
                                    'via portavoz','militar ambient, barro branco joão paraíso','conceição mato, ond']

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
        if locations:
            filtered_locations = []
            for location in locations:
                if any(forbidden in location.lower() for forbidden in self.forbidden_locations):
                    for forbidden in self.forbidden_locations:
                        if forbidden in location.lower():
                            location = location.replace(forbidden, "")
                    filtered_locations.append(location.strip())
                else:
                    filtered_locations.append(location)

            # Substituir localizações específicas
            replacements = {
                'ministério meio ambient, amazônia': 'amazônia',
                'confira destaqu g1, rondônia': 'rondônia',
                'estado rondônia amazona ruan gabriel rede amazônica': 'rondônia',
                'combat, amazônia, rondônia': 'rondônia',
                'rondônia amazona ruan gabriel rede amazônica':'rondônia',
                'imazon': 'amazônia',
                'amazônia, instituto nacion pesquisa espaciai, amazônia': 'amazônia',
                'amazônia menor': 'amazônia',
                'mata atlântica, paraná, mata atlântica, mata atlântica': 'paraná',
                'pantan so pantan, mato grosso sul': 'mato grosso do sul'
            }

            for i, location in enumerate(filtered_locations):
                if location in replacements:
                    filtered_locations[i] = replacements[location]

            return ', '.join(filtered_locations) if filtered_locations else None
        else:
            return None


if __name__ == "__main__":
    url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1y'
    news_collection = NewsCollection(url)

    news_repository = PreProcessing(news_collection)
    news_list = news_repository.process_data()
    print(news_list)
