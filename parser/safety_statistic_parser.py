from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


import time

browser = webdriver.Firefox()
# 1. Переход по страницам
# browser.get('https://www.yandex.ru/')
# time.sleep(5)
# browser.get('https://zastavok.net/2/')

# 2. Скриншот
# browser.get('https://zastavok.net/2/')
# browser.save_screenshot('save.png')
# browser.quit() # перезагрузка
# browser.quit() # выход

# 3. Работа в браузере
# browser.get('https://pk.mipt.ru/bachelor/list/')
# Select(browser.find_element(By.XPATH,'/html/body/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/div/div[2]/div[2]/select')).select_by_index(1)
# Select(browser.find_element(By.XPATH, '/html/body/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/div/div[3]/div[2]/select')).select_by_index(2)
# Select(browser.find_element(By.XPATH, '/html/body/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/div/div[4]/div[2]/select')).select_by_index(1)
# Select(browser.find_element(By.XPATH, '/html/body/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/div/div[5]/div[2]/select')).select_by_index(1)
# Select(browser.find_element(By.XPATH, '/html/body/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/div/div[7]/div[2]/select')).select_by_index(1)
#
# browser.find_element(By.XPATH, '/html/body/div/div[3]/div[3]/div/div[2]/div[1]/div[2]/div/div[1]/div/div').click()
# time.sleep(3)
#
# html = browser.page_source
# print(html)
# time.sleep(5)
#
#
browser.get('https://www.safety.ru/accidents/#/')

# for i in range(1,5):
#     element = browser.find_element(By.LINK_TEXT, f'{i}')
#     element.click()
#     time.sleep(3)
#     print(i)

list_ = browser.find_elements(By.LINK_TEXT, f'Подробнее ...')
for item in list_:
    print(item.get_attribute('href'))


browser.close()



if __name__ == '__main__':
    ...
