# 📲 IA - REPORT

Bem-vindo ao IA-Report!👋 Este projeto foi desenvolvido como parte de um estudo sobre redes neurais, utilizando a linguagem Python devido à sua facilidade de manipulação dessas redes através de bibliotecas especializadas. 
O projeto realiza web scraping de notícias sobre desmatamento do site G1, processa essas notícias e as armazena em um banco de dados remoto. Em seguida, duas redes neurais são usadas para categorizar e classificar as notícias.


## 📌 Funcionalidades

- **Web Scraping:** Coleta notícias sobre desmatamento da página do G1.
- **Processamento e Armazenamento:** Processa as notícias coletadas e as armazena em um banco de dados remoto.
- **Redes Neurais:**
  - CNN (Convolutional Neural Network): Categoriza as notícias.
  - LSTM (Long Short-Term Memory): Classifica as notícias como boas ou ruins.
- **Dashboard:** Exibe os resultados finais das notícias em um formato visual.

## 🔍 Interface
<img align="center" alt="Andressa" height="500em" width="1000em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243656024574132255/image.png?ex=6652446e&is=6650f2ee&hm=f2ec64d6b76638375d39fd658be655db24a31934e542d898cd2908358e1cdda9&" />

- **Apagar Notícias:** Este botão apaga todas as notícias atualmente armazenadas no banco de dados. Útil para reiniciar o processo de coleta e categorização/classificação das notícias.
  
  <table>
  <tr>
  <td>
  <img alt="Andressa" height="140em" width="220em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243656813862326293/image.png?ex=6652452a&is=6650f3aa&hm=2e81c94c34be8b6a1653c0d741481d8acc9b29c39437b4600e12f3caed7ae749&" />
  </td>
  </tr>
  </table>
  
- **Carregar Notícias:** Realiza o web scraping das notícias sobre desmatamento da página do G1. As notícias coletadas são processadas e armazenadas no banco de dados remoto.
  
  <table>
  <tr>
  <td>
  <img alt="Andressa" height="140em" width="220em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243656858401505341/image.png?ex=66524535&is=6650f3b5&hm=3e73a46b7c6d426df04e9fb1d71099d0bb5c0a4bc5b65dedf75b8d2dfa715db7&" />
  </td>
  </tr>
  </table>

- **Monitorar Rede:** Gera um arquivo Excel com informações detalhadas sobre a rede, como processos, PID e protocolos usados. O arquivo é salvo na pasta Downloads do computador.
  
  <table>
  <tr>
  <td>
  <img alt="Andressa" height="140em" width="220em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243656901628264519/image.png?ex=6652453f&is=6650f3bf&hm=82f95430171d9987dd3a086b84d52e9560500eadc9df81c1531b7a62e5cb0e32&" />
  </td>
  </tr>
  </table>
  <table>
  <tr>
  <td>
  <img alt="Andressa" height="140em" width="220em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243662192356757564/image.png?ex=66524a2c&is=6650f8ac&hm=21c13e48325ef1751d5a50159ca2d0da1c5002b54cbdd2fd52b0d0ca7c1e5dc0&" />
  </td>
  </tr>
  </table>

- **Classificar Notícias:** Executa a rede neural LSTM para classificar as notícias como boas ou ruins. Após a classificação, as informações são atualizadas no banco de dados.
  
  <table>
  <tr>
  <td>
  <img alt="Andressa" height="140em" width="220em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243656972188909608/image.png?ex=66524550&is=6650f3d0&hm=5e01d47e9d2ffed8c8753ae40028ae5a748ad9198b4cd18ad718b1bb6fa0f6d1&" />
  </td>
  </tr>
  </table>

- **Categorizar Notícias:** Executa a rede neural CNN para categorizar as notícias. Utiliza a base de dados previamente categorizada para treinar o modelo e categoriza as notícias sem categoria. As informações categorizadas são então atualizadas no banco de dados.
  
  <table>
  <tr>
  <td>
  <img alt="Andressa" height="140em" width="220em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243657016107466862/image.png?ex=6652455a&is=6650f3da&hm=f5c3cb63d60c234a60c8fcad18a6a1da7af4d34eb8b1e2d2ef8d4698ee030b9f&" />
  </td>
  </tr>
  </table>

- **Exibir Relatório:** Exibe um dashboard com os resultados finais das notícias. O relatório inclui as classificações e categorizações feitas pelas redes neurais, oferecendo uma visualização clara e intuitiva dos dados processados.
  
  <table>
  <tr>
  <td>
  <img alt="Andressa" height="140em" width="220em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243657061301227643/image.png?ex=66524565&is=6650f3e5&hm=e75b6225d0c1aa7d6dfd59658ab8679b32b12b06db19702652a26e51314d10c9&" />
  </td>
  </tr>
  </table>
  <table>
  <tr>
  <td>
  <img align="center" alt="Andressa" height="500em" width="1000em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243659152899702894/Imagem_do_WhatsApp_de_2024-05-24_as_17.17.12_2bd9995f.jpg?ex=66524758&is=6650f5d8&hm=da174fb5507754ac06b83d917fe69f7af68370b31d611762bf8fdc99270413aa&" />
  </td>
  </tr>
  </table>


## 🕹 Executando Localmente

1. Clone o repositório: `git clone https://github.com/seu-usuario/seu-projeto.git`
2. Instale o python: `https://www.python.org/downloads/`
3. Instale a IDE de sua preferência `Exemplo: PyCharm`
4. Instale as libs: `pip install selenium beautifulsoup4 pandas nltk spacy psutil numpy tensorflow scikit-learn psycopg2`
5. Execute a aplicação: `RUN main(na pasta views)`

## ⚠️ Observação

- Para acessar e entender a estrutura do banco de dados, você pode utilizar as credenciais fornecidas no arquivo config.py e inserir essas informações no Beekeeper Studio (ou qualquer outro cliente SQL de sua preferência).

<table>
<tr>
<td>
<img alt="Andressa" height="400em" width="400em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243664432501096478/image.png?ex=66524c42&is=6650fac2&hm=2777be6563b104579184864944323ee06dab4f3f3170adfa71cf9100b82e41ab&" />
</td>
</tr>
</table>

## 💻 Tecnologias Utilizadas
  
PYTHON | POSTGRESQL
:------:  | :------: 
<img align="center" alt="Python" height="40em" width="40em" src="https://cdn.discordapp.com/attachments/805220480566165514/1243666524133134491/1200px-Python.png?ex=66524e35&is=6650fcb5&hm=ebc7e9f5e46d78f865306bbdd80e6676fd9fee835fe5c382b1d78eb3b25fbfb1&" /> | <img align="center" alt="PostegreSQL" height="45em" width="50em" src="https://cdn.discordapp.com/attachments/805220480566165514/1219030797286379571/postgresql_plain_wordmark_logo_icon_146390.png?ex=6651aba6&is=66505a26&hm=b2a4956ef9ff5c180d6aa66ef467293cbfc70c9c5facd6c29fadcb9b321a253f&" /> 

## 💡 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.


## 👩Autor
>Andressa Silva

