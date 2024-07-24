import time
from selenium import webdriver
import requests
import smtplib
from bs4 import BeautifulSoup

# old_price = 1450.0
FROM = 'pyautomationpostman@gmail.com'
PW = # Use your password
URL = 'https://www.amazon.de/-/en/Samsung-Smartphone-Android-Contract-Titanium/dp/B0CNH6RHV6/ref=sr_1_4?crid=374CTKCQMRNK&dib=eyJ2IjoiMSJ9.MyOd-3ZOrqa4HC9QDbcFS15XsQ5mvPmNlotbGKIYqpeWErnMgps8mrqh6L7tKgHBNkmf7AyIJs4zv_hsTCvI-Mme9kozFadBXIrXy-_ycAK9F5KV3kIDDwtL578p9xrB99fEP48arv8XRsty2vmczqEDdr61bws8OQga9NN_rgMyRRccLzPnWOrjuIrWlnc9GqbXTYOXqZD4oDez4Mxx1vQvMC6MmHzKthiigJ4H5Lg.RsH18X2N0AseG9zXTKDBlgrDLXQU9FeH7xzXQ0SMJXg&dib_tag=se&keywords=s24+ultra&qid=1713954443&sprefix=s24%2Caps%2C103&sr=8-4&ufe=app_do%3Aamzn1.fos.d9ce03e4-bad8-42e1-835e-4c276296325a'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'content-encoding': 'utf-8'}


def check_price(threshold_price: float):
    '''Function to check the price'''
    # global old_price
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)
    # page = requests.get(URL, headers=headers)
    # page.encoding = 'UTF-8'
    # cont = page.text
    time.sleep(5)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.find('span', {'id': 'productTitle',
                               'class': 'a-size-large product-title-word-break'}).getText()
    price = soup.find('span', {'class': 'a-price-whole'}).getText().replace(',', '')
    price = float(price)
    print(price)

    if (price < threshold_price):
        old_price = price
        sendemail(FROM, PW, 'denofdreamz@gmail.com', 'AMZN PRICE TRACKER NOTIFICATION',
                  f'Hey, Price of \"{title}\" has been reduced to {price} euros.')


def sendemail(from_id: str, pwd: str, to_id: str, subject: str, body: str):
    '''Function called when email needs to be send'''
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(from_id, pwd)
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(from_id, to_id, message)
        print('Email sent')
    except Exception:
        print(f'Email not sent due to the exception {Exception}')


if __name__ == '__main__':
    while (True):
        check_price(1350.)
        time.sleep(3600)
