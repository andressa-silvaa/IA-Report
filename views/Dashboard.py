import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from controllers.newsRepository import NewsRepository

class NewsVisualizer:
    def __init__(self, repository):
        self.repo = repository

    def visualize_data(self):
        news_data = self.repo.get_all_news()
        df_dados = pd.DataFrame(news_data, columns=['title', 'content', 'age','link','media_img','media_video','locality','category','classification'])
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        sns.countplot(ax=axes[0, 0], x='category', data=df_dados, palette='Set2', hue='category', legend=False)
        axes[0, 0].set_title('Quantidade de Notícias por Categoria')
        axes[0, 0].set_xlabel('')
        axes[0, 0].set_ylabel('Quantidade de Notícias')
        axes[0, 0].tick_params(axis='x', rotation=45)

        classification_counts = df_dados['classification'].value_counts()
        if not classification_counts.empty:
            classification_counts.plot(kind='pie', autopct='%1.1f%%', ax=axes[0, 1], textprops={'fontsize': 12}, colors=sns.color_palette('Set2'))
            axes[0, 1].set_title('Distribuição de Notícias por Classificação')
            axes[0, 1].set_ylabel('')
            axes[0, 1].axis('equal')
        else:
            axes[0, 1].axis('off')

        df_dados['age'] = pd.to_datetime(df_dados['age'])
        df_dados.set_index('age', inplace=True)
        news_by_month = df_dados.resample('M').size()
        news_by_month.plot(ax=axes[1, 0], color='gray')
        axes[1, 0].set_title('Quantidade de Notícias ao Longo do Tempo')
        axes[1, 0].set_xlabel('')
        axes[1, 0].set_ylabel('Quantidade de Notícias')
        axes[1, 0].tick_params(axis='x', rotation=45)

        axes[1, 1].set_title('Maior Ocorrência das Notícias')
        mapa = Basemap(projection='merc', llcrnrlat=-35, urcrnrlat=5,
                       llcrnrlon=-80, urcrnrlon=-35, resolution='l', ax=axes[1, 1])

        mapa.drawcoastlines()
        mapa.drawcountries()
        mapa.drawstates(color='gray')

        coordenadas = {
            'Rondônia': (-11.22, -62.80),
            'Amazonas': (-3.47, -65.10)
        }

        for estado, (lat, lon) in coordenadas.items():
            x, y = mapa(lon, lat)
            mapa.plot(x, y, 'ro', markersize=50, alpha=0.6)
            axes[1, 1].text(x, y, estado, fontsize=8, ha='center', va='center', color='black')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    news_repo = NewsRepository('usjlmkja', 'usjlmkja', 'QKJgujyxlBSINpQBd8Gc3-rsc8S0_fiT', 'isabelle.db.elephantsql.com', '5432')
    visualizer = NewsVisualizer(news_repo)
    visualizer.visualize_data()
