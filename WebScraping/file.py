import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "MyLearningBot/0.1 (https://example.com/contact)"
}

url = "https://en.wikipedia.org/wiki/Web_scraping"
responseonse = requests.get(url, headers=headers)

bs = BeautifulSoup(responseonse.text, "lxml")
print(bs.find("p").text)


'''responseonse = requests.get("https://en.wikipedia.org/wiki/Web_scraping")
bs = BeautifulSoup(responseonse.text, "lxml")
print(bs.find("p").text)'''

