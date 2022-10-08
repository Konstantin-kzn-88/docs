import requests
from bs4 import BeautifulSoup
import fake_useragent

num = 1
link = f'https://zastavok.net/{num}'

resp = requests.get(link).text
soup = BeautifulSoup(resp, 'lxml')
block = soup.find('div', class_ = 'block-photo')
all_img = block.find_all('div', class_ = 'short_full')

for img in all_img:
    img_link = img.find('a').get('href')
    print(img_link)

if __name__ == '__main__':
    ...