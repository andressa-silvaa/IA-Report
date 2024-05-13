from controllers.newsCollection import NewsCollection
from controllers.preProcessing import PreProcessing
from controllers.newsRepository import NewsRepository
from models.sentimentAnalysis import SentimentAnalysis
from models.networkMonitor import NetworkMonitor
from models.newsCategorizer import NewsCategorizer

def main():

    # Coleta de notícias
    url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1y'
    news_collection = NewsCollection(url)
    pre_processor = PreProcessing(news_collection)
    news_data = pre_processor.process_data()

    #credenciais do banco
    db_name = 'usjlmkja'
    db_user = 'usjlmkja'
    db_password = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
    db_host = 'isabelle.db.elephantsql.com'
    db_port = '5432'
    #acesso ao dataBase
    news_repository = NewsRepository(db_name, db_user, db_password, db_host, db_port)
    news_repository.process_and_save_news(news_data)


    #Rede Neural de Categoria
    categorizer = NewsCategorizer(db_name, db_user, db_password, db_host, db_port)
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

    #Monitoramento da rede
    monitor = NetworkMonitor()
    monitor.start_monitoring()


if __name__ == "__main__":
    main()