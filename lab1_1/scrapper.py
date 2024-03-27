from bs4 import BeautifulSoup
import requests
import json

DATE = "2024-02-16"
ROOT = "https://lb.ua/politics/newsfeed?page="

def parse_list():
    news = []
    for page_num in range(10, 16):
        news += parse_list_page(page_num)
    return news
    
def parse_list_page(page_num):
    soup = load_page(ROOT+str(page_num))

    elements = soup.find_all('li', attrs={'class': 'item-news'})
    elements = [element for element in elements if element.find('time') and DATE in element.find('time').get('datetime')]

    print (f"Found {len(elements)} news items for {DATE} on page {page_num}")
   
    news = []
    for element in elements:
        
        news_item = parse_news_page(element.find('a').get('href'))
        news_item['article'] = element.find('div', attrs={'class':'title'}).text

        news.append(news_item)
    return news

def parse_news_page(link):
    news_item = {}
    news_item['link'] = link
     
    soup=load_page(link)

    news_item['header'] = soup.find('h1', attrs={'itemprop':'headline'}).text
    news_item['text'] = soup.find('div', attrs={'itemprop':'articleBody'}).text
    return news_item

def load_page(link):
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def main():
    news = parse_list()
    print(f"Total news items: {len(news)}")
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=3)

if __name__ == "__main__":
    main()