import bs4
from urllib.request import urlopen

url = "https://news.google.com/news/rss"
client = urlopen(url)
xml_page = client.read()
client.close()
page = bs4.BeautifulSoup(xml_page, 'xml')
news_list = page.findAll("item")
print("Kabul Airport")
try:
    for news in news_list:
        print(news.title.text)
        # print(news.pubDate.text)
        print()

except Exception as e:
    pass
