import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from controllers.newsRepository import NewsRepository

# Supondo que a classe NewsRepository já esteja definida e importada corretamente
news_repo = NewsRepository('usjlmkja', 'usjlmkja', 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT', 'isabelle.db.elephantsql.com', '5432')

# Recuperar os dados do banco de dados
news_data = news_repo.get_all_news()

# Criar um DataFrame com os dados
df_dados = pd.DataFrame(news_data, columns=['title', 'content', 'age','link','media_img','media_video','locality','category','classification'])

# Gráfico de barras: quantidade de categorias por notícias
plt.figure(figsize=(10, 6))
sns.countplot(x='category', data=df_dados, palette='viridis', hue='category', legend=False)
plt.title('Quantidade de Notícias por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Quantidade de Notícias')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Verificar os dados de classificação
print("Dados de Classificação:")
print(df_dados['classification'].value_counts())

# Gráfico de pizza: quantidade de notícias por classificação
plt.figure(figsize=(8, 8))
classification_counts = df_dados['classification'].value_counts()
if not classification_counts.empty:
    classification_counts.plot(kind='pie', autopct='%1.1f%%', textprops={'fontsize': 12})
    plt.title('Distribuição de Notícias por Classificação')
    plt.ylabel('')  # Remover o rótulo do eixo y
    plt.tight_layout()
    plt.show()
else:
    print("Não há dados de classificação para exibir.")

# Gráfico de linha: quantidade de notícias por período
plt.figure(figsize=(10, 6))
df_dados['age'] = pd.to_datetime(df_dados['age'])
df_dados.set_index('age', inplace=True)
news_by_date = df_dados.resample('ME').size()
news_by_date.plot()
plt.title('Quantidade de Notícias ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Quantidade de Notícias')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Texto de agradecimento
agradecimento = "Obrigado por acompanhar nossas notícias!"
