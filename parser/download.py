import requests
from bs4 import BeautifulSoup

img_num = 0
# storage_num = 1
link = f'https://zastavok.net/'

resp = requests.get(link).text
soup = BeautifulSoup(resp, 'lxml')
block = soup.find('div', class_='block-photo')
all_img = block.find_all('div', class_='short_full')

for img in all_img:
    if img_num >= 3: break

    img_link = img.find('a').get('href')
    download_storage = requests.get(f'{link}{img_link}').text
    download_soup = BeautifulSoup(download_storage, 'lxml')
    download_block = download_soup.find('div', class_='image_data').find('div', class_='block_down')
    result_link = download_block.find('a').get('href')

    img_bytes = requests.get(f'{link}{result_link}').content

    with open(f'img/{img_num}.jpg', 'wb') as file:
        file.write(img_bytes)
    print(f'Изображение {img_num} записано!')
    img_num += 1


if __name__ == '__main__':
    ...
