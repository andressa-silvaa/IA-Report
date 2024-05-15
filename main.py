# Importações
from controllers.newsCollection import NewsCollection
from controllers.preProcessing import PreProcessing
from controllers.newsRepository import NewsRepository
from models.sentimentAnalysis import SentimentAnalyzer
from models.networkMonitor import NetworkMonitor
from models.newsCategorizer import NewsCategorizer
from models.trainingSet import TextProcessor
from views.Dashboard import NewsVisualizer

# Credenciais do banco
DB_NAME = 'usjlmkja'
DB_USER = 'usjlmkja'
DB_PASSWORD = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
DB_HOST = 'isabelle.db.elephantsql.com'
DB_PORT = '5432'

# Função para inicializar a conexão com o banco de dados
def initialize_news_repository():
    return NewsRepository(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

# Funções para operações específicas
def delete_news():
    news_repository = initialize_news_repository()
    news_repository.delete_table()
    print("Notícias apagadas com sucesso!")

def load_news():
    news_repository = initialize_news_repository()
    news_data = news_repository.get_all_news()
    if news_data:
        print("Notícias já carregadas!")
    else:
        url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1y'
        news_collection = NewsCollection(url)
        pre_processor = PreProcessing(news_collection)
        news_data = pre_processor.process_data()
        news_repository.process_and_save_news(news_data)
        print("Notícias carregadas com sucesso!")

def classify_news():
    news_repository = initialize_news_repository()
    if news_repository.check_null_classification():
        print ("Notícias já classificadas!")
    else:
        text_processor = TextProcessor()
        text_processor.process_texts()
        text_processor.save_to_excel('treino.xlsx')
        sentiment_analyzer = SentimentAnalyzer()
        df_treino = sentiment_analyzer.load_training_data('treino.xlsx')
        df_treino = sentiment_analyzer.balance_classes(df_treino)
        df_treino = sentiment_analyzer.map_classifications(df_treino)
        conteudo_treino = df_treino['content'].values
        classificacao_treino = df_treino['classification'].values
        X_train, X_val, y_train, y_val, tokenizer = sentiment_analyzer.prepare_data(conteudo_treino, classificacao_treino)
        model = sentiment_analyzer.build_model(tokenizer.word_index)
        trained_model = sentiment_analyzer.train_model(model, X_train, y_train, X_val, y_val)
        sentiment_analyzer.save_model(trained_model, 'modelo_sentimento.h5')
        sentiment_analyzer.analyze_sentiment(tokenizer)
        print("Notícias classificadas com sucesso!")

def categorize_news():
    news_repository = initialize_news_repository()
    if news_repository.check_null_category():
        print ("Notícias já categorizadas!")
    else:
        categorizer = NewsCategorizer(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
        categorizer.fetch_data()
        categorizer.preprocess_data()
        X_train, X_test, y_train, y_test = categorizer.split_data()
        X_train_seq, X_test_seq = categorizer.tokenize_data(X_train, X_test)
        y_train_encoded, y_test_encoded = categorizer.encode_labels(y_train, y_test)
        vocab_size = len(categorizer.tokenizer.word_index) + 1
        embedding_dim = 100
        categorizer.model = categorizer.build_model(vocab_size, embedding_dim, 100, len(categorizer.label_encoder.classes_))
        categorizer.train_model(categorizer.model, X_train_seq, y_train_encoded)
        loss, accuracy = categorizer.evaluate_model(categorizer.model, X_test_seq, y_test_encoded)
        print(f'Test Accuracy: {accuracy}')
        categorizer.predict_missing_categories()
        categorizer.save_category()
        categorizer.display_updated_dataframe()
        print("Notícias categorizadas com sucesso!")

def display_report():
    news_repository = initialize_news_repository()
    visualizer = NewsVisualizer(news_repository)
    visualizer.visualize_data()
    print("Relatório exibido com sucesso!")

def monitor_network():
    monitor = NetworkMonitor()
    monitor.start_monitoring()


def main():
    while True:
        print("Menu:")
        print("1. Apagar Notícias")
        print("2. Carregar Notícias")
        print("3. Monitorar Rede")
        print("4. Classificar Notícias")
        print("5. Categorizar Notícias")
        print("6. Exibir Relatório")
        print("0. Sair")

        option = input("Escolha uma opção: ")

        if option == "1":
            delete_news()
            input("Pressione Enter para continuar...")
        elif option == "2":
            load_news()
            input("Pressione Enter para continuar...")
        elif option == "3":
            monitor_network()
            input("Pressione Enter para continuar...")
        elif option == "4":
            classify_news()
            input("Pressione Enter para continuar...")
        elif option == "5":
            categorize_news()
            input("Pressione Enter para continuar...")
        elif option == "6":
            display_report()
            input("Pressione Enter para continuar...")
        elif option == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Escolha novamente.")

if __name__ == "__main__":
    main()
