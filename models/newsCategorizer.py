import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Supondo que a classe NewsRepository já esteja definida e importada corretamente
news_repo = NewsRepository('usjlmkja', 'usjlmkja', 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT', 'isabelle.db.elephantsql.com', '5432')

# Recuperar os dados do banco de dados
news_data = news_repo.get_all_news()

# Criar um DataFrame com os dados
df_dados = pd.DataFrame(news_data, columns=['title', 'content', 'age', 'link', 'media_img', 'media_video', 'locality', 'category', 'classification'])

# Criar uma janela do Tkinter
root = tk.Tk()
root.title("Dashboard")

# Criar uma guia para os gráficos
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Criar as figuras para os gráficos
fig1, ax1 = plt.subplots(figsize=(8, 6))
fig2, ax2 = plt.subplots(figsize=(8, 6))
fig3, ax3 = plt.subplots(figsize=(8, 6))

# Gráfico de barras: quantidade de categorias por notícias
sns.countplot(x='category', data=df_dados, palette='viridis', ax=ax1)
ax1.set_title('Quantidade de Notícias por Categoria')
ax1.set_xlabel('Categoria')
ax1.set_ylabel('Quantidade de Notícias')
ax1.tick_params(axis='x', rotation=45)

# Gráfico de pizza: quantidade de notícias por classificação
classification_counts = df_dados['classification'].value_counts()
if not classification_counts.empty:
    classification_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax2, textprops={'fontsize': 12})
    ax2.set_title('Distribuição de Notícias por Classificação')
    ax2.set_ylabel('')  # Remover o rótulo do eixo y

# Gráfico de linha: quantidade de notícias por período
df_dados['age'] = pd.to_datetime(df_dados['age'])
df_dados.set_index('age', inplace=True)
news_by_date = df_dados.resample('M').size()
news_by_date.plot(ax=ax3)
ax3.set_title('Quantidade de Notícias ao Longo do Tempo')
ax3.set_xlabel('Data')
ax3.set_ylabel('Quantidade de Notícias')

# Adicionar as figuras às guias
canvas1 = FigureCanvasTkAgg(fig1, master=notebook)
canvas2 = FigureCanvasTkAgg(fig2, master=notebook)
canvas3 = FigureCanvasTkAgg(fig3, master=notebook)

tab1 = canvas1.get_tk_widget()
tab2 = canvas2.get_tk_widget()
tab3 = canvas3.get_tk_widget()

notebook.add(tab1, text='Categoria')
notebook.add(tab2, text='Classificação')
notebook.add(tab3, text='Tempo')

# Adicionar a barra de ferramentas de navegação para cada guia
toolbar1 = NavigationToolbar2Tk(canvas1, root)
toolbar2 = NavigationToolbar2Tk(canvas2, root)
toolbar3 = NavigationToolbar2Tk(canvas3, root)

canvas1.get_tk_widget().pack()
toolbar1.pack()
canvas2.get_tk_widget().pack()
toolbar2.pack()
canvas3.get_tk_widget().pack()
toolbar3.pack()

root.mainloop()
