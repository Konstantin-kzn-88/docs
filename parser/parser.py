import requests
from bs4 import BeautifulSoup
import fake_useragent

# Подмена юзер-агента
# без него возвращает User-agent: python-requests/2.28.1
user = fake_useragent.UserAgent().random
header = {'user-agent' : user}


link = 'https://browser-info.ru/'
resp = requests.get(link, headers = header).text
soup = BeautifulSoup(resp, 'lxml')
block = soup.find('div', id = 'tool_padding')
# print(block)

check_js = block.find('div', id = 'javascript_check')
# print(chesk_js)
result_js = check_js.find_all('span')
# print(result_js)
# print(result_js[1])
# print(type(result_js[1]))
print(result_js[1].text)

# Check User agent
check_user = block.find('div', id = 'user_agent').text
result_user = f'user agent: {check_user}'
print(result_user)


# POST - отправляет данные на страницу
# GET - получить данные со страницы
# content - получить данные в байтах (напр., при скачивании картинки)
# text - получить html разметку в виде строки

if __name__ == '__main__':
    ...