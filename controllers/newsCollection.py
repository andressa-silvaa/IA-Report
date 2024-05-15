from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class NewsCollection:
    def __init__(self, url):
        self.url = url

    def load_page(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        while True:
            try:
                ver_mais_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'pagination__load-more'))
                )
                old_news_count = len(driver.find_elements(By.CLASS_NAME, 'widget--card'))
                driver.execute_script("arguments[0].click();", ver_mais_button)
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(ver_mais_button)
                )
                new_news_count = len(driver.find_elements(By.CLASS_NAME, 'widget--card'))
                if new_news_count == old_news_count:
                    break
            except:
                break

        content = driver.page_source
        driver.quit()
        return content

    def extract_info(self, content):
        site = BeautifulSoup(content, 'html.parser')
        news = site.find_all('li', class_="widget widget--card widget--info")
        news_list = []
        for notice in news:
            title = notice.find('div', class_='widget--info__title product-color')
            description = notice.find('p', class_="widget--info__description")
            new_age = notice.find('div', class_="widget--info__meta")
            media_video = notice.find('a', class_="widget--info_media widget--info_media--video")
            media_video = media_video['href'] if media_video else None
            media_img = notice.find('img', class_="")
            media_img = media_img['src'] if media_img else None
            link = notice.find('a', class_="")
            link = link['href'] if link else None
            if description:
                title_text = title.text.strip() if title else None
                content_text = description.text.strip()
                age = new_age.text.strip() if new_age else None
                if title_text and title_text != "Assista a seguir":
                    news_list.append(
                        {'title': title_text, 'content': content_text, 'age': age, 'link': link, 'media_img': media_img,
                         'media_video': media_video})
        return news_list

if __name__ == "__main__":
    url = 'https://g1.globo.com/busca/?q=desmatamento&ps=on&order=recent&from=now-1y'
    repository = NewsCollection(url)
    content = repository.load_page()
    news_list = repository.extract_info(content)
    for news in news_list:
        print(f"Título: {news['title']}")
        print(f"Conteúdo: {news['content']}")
        print(f"Idade: {news['age']}")
        print(f"Link: {news['link']}")
        print(f"Mídia de Imagem: {news['media_img']}")
        print(f"Mídia de Vídeo: {news['media_video']}")
        print()
