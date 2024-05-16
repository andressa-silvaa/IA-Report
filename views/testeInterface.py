import tkinter as tk
from tkinter import ttk, messagebox

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
    messagebox.showinfo("Sucesso", "Notícias apagadas com sucesso!")

def load_news():
    news_repository = initialize_news_repository()
    news_data = news_repository.get_all_news()
    if news_data:
        messagebox.showinfo("Info", "Notícias já carregadas!")
    else:
        url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1y'
        news_collection = NewsCollection(url)
        pre_processor = PreProcessing(news_collection)
        news_data = pre_processor.process_data()
        news_repository.process_and_save_news(news_data)
        messagebox.showinfo("Sucesso", "Notícias carregadas com sucesso!")

def classify_news():
    news_repository = initialize_news_repository()
    if news_repository.check_null_classification():
        messagebox.showinfo("Info", "Notícias já classificadas!")
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
        messagebox.showinfo("Sucesso", "Notícias classificadas com sucesso!")

def categorize_news():
    news_repository = initialize_news_repository()
    if news_repository.check_null_category():
        messagebox.showinfo("Info", "Notícias já categorizadas!")
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
        messagebox.showinfo("Sucesso", f'Test Accuracy: {accuracy}')
        categorizer.predict_missing_categories()
        categorizer.save_category()
        categorizer.display_updated_dataframe()
        messagebox.showinfo("Sucesso", "Notícias categorizadas com sucesso!")

def display_report():
    news_repository = initialize_news_repository()
    visualizer = NewsVisualizer(news_repository)
    visualizer.visualize_data()
    messagebox.showinfo("Sucesso", "Relatório exibido com sucesso!")


def monitor_network():
    monitor = NetworkMonitor()
    monitor.start_monitoring()
    messagebox.showinfo("Sucesso", "Monitoramento de rede salvo!")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("News Management System")
        self.geometry("1200x720")
        self.resizable(True, True)
        self.center_window()
        self.create_widgets()

    def center_window(self):
        # Obtém as dimensões da tela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcula as coordenadas para centralizar a janela
        x_coordinate = int((screen_width - 1200) / 2)
        y_coordinate = int((screen_height - 720) / 2)

        # Define a geometria da janela para que ela seja centralizada na tela
        self.geometry(f"1200x720+{x_coordinate}+{y_coordinate}")

    def create_widgets(self):
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenu, DeleteNews, LoadNews, MonitorNetwork, ClassifyNews, CategorizeNews, DisplayReport):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Centralizando o menu principal
        main_menu_frame = self.frames["MainMenu"]
        main_menu_frame.grid(row=0, column=0, sticky="nsew", columnspan=len(self.frames))
        #main_menu_frame.grid(pady=150)

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Menu Principal", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)

        buttons = [
            ("Apagar Notícias", "DeleteNews"),
            ("Carregar Notícias", "LoadNews"),
            ("Monitorar Rede", "MonitorNetwork"),
            ("Classificar Notícias", "ClassifyNews"),
            ("Categorizar Notícias", "CategorizeNews"),
            ("Exibir Relatório", "DisplayReport"),
        ]
        for (text, page_name) in buttons:
            button = tk.Button(self, text=text, command=lambda page_name=page_name: controller.show_frame(page_name), width=40, height=2, font=('Helvetica', 12))
            button.pack(side="top", pady=5)

        # Centralizar o frame na janela
        self.pack(expand=True, fill='both')




class DeleteNews(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Apagar Notícias", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Apagar", command=delete_news)
        button.pack(pady=20)
        back_button = ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack()

class LoadNews(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Carregar Notícias", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Carregar", command=load_news)
        button.pack(pady=20)
        back_button = ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack()

class MonitorNetwork(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Monitorar Rede", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Monitorar", command=monitor_network)
        button.pack(pady=20)
        back_button = ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack()

class ClassifyNews(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Classificar Notícias", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Classificar", command=classify_news)
        button.pack(pady=20)
        back_button = ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack()

class CategorizeNews(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Categorizar Notícias", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Categorizar", command=categorize_news)
        button.pack(pady=20)
        back_button = ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack()

class DisplayReport(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = tk.Label(self, text="Exibir Relatório", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Exibir", command=display_report)
        button.pack(pady=20)
        back_button = ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()