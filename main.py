from controllers.newsCollection import NewsCollection
from controllers.preProcessing import PreProcessing
from controllers.newsRepository import NewsRepository
from models.sentimentAnalysis import SentimentAnalyzer
from models.networkMonitor import NetworkMonitor
from models.newsCategorizer import NewsCategorizer
from models.trainingSet import TextProcessor

# Credenciais do banco
db_name = 'usjlmkja'
db_user = 'usjlmkja'
db_password = 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT'
db_host = 'isabelle.db.elephantsql.com'
db_port = '5432'

def apagar_noticias():
    news_repository = NewsRepository(db_name, db_user, db_password, db_host, db_port)
    news_repository.delete_table()
    print("Notícias apagadas com sucesso!")

def carregar_noticias():
    # Coleta de notícias
    url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1y'
    news_collection = NewsCollection(url)
    pre_processor = PreProcessing(news_collection)
    news_data = pre_processor.process_data()
    # Acesso ao banco de dados
    news_repository = NewsRepository(db_name, db_user, db_password, db_host, db_port)
    news_repository.process_and_save_news(news_data)
    print("Notícias carregadas com sucesso!")
    input("Pressione Enter para continuar...")
    main()

def monitorar_rede():
    # Monitoramento da rede
    monitor = NetworkMonitor()
    monitor.start_monitoring()
    input("Pressione Enter para continuar...")
    main()
def classificar_noticias():
    # Lógica para classificar notícias
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
    input("Pressione Enter para continuar...")
    main()

def categorizar_noticias():
    # Rede Neural de Categoria
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
    print("Notícias categorizadas com sucesso!")
    input("Pressione Enter para continuar...")
    main()

def exibir_relatorio():
    # Lógica para exibir o relatório
    # Aqui você pode incluir a lógica para exibir o relatório de notícias já existente em seu código principal.
    pass

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

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            apagar_noticias()
            input("Pressione Enter para continuar...")
        elif opcao == "2":
            carregar_noticias()
            input("Pressione Enter para continuar...")
        elif opcao == "3":
            monitorar_rede()
            input("Pressione Enter para continuar...")
        elif opcao == "4":
            classificar_noticias()
        elif opcao == "5":
            categorizar_noticias()
        elif opcao == "6":
            exibir_relatorio()
            input("Pressione Enter para continuar...")
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Escolha novamente.")

if __name__ == "__main__":
    main()
