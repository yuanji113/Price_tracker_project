import requests
from bs4 import BeautifulSoup
import smtplib
import time

#Amazon US doesn't work
# url = 'https://www.amazon.de/Sony-Vollformat-Digitalkamera-Megapixel-LC-Display/dp/B00Q2KEVA2/ref=sr_1_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=sony+a72&qid=1634314045&sr=8-1'
bestbuy_url = 'https://www.bestbuy.com/site/sony-65-class-bravia-xr-x90j-series-led-4k-uhd-smart-google-tv/6453208.p?skuId=6453208'
natasha_url = 'https://www.sephora.com/product/natasha-denona-glam-eyeshadow-palette-P461188?icid2=recommended%20for%20you:p461188:product'
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

def check_bestbuy_price():
    page = requests.get(bestbuy_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
  
    bestbuy_title = soup.find('h1', class_='heading-5 v-fw-regular').get_text()
    bestbuy_price = soup.find('div', class_='priceView-hero-price priceView-customer-price')
    # need to find next level because of aria-hidden
    bestbuy_price = bestbuy_price.find('span', attrs={'aria-hidden': True}).get_text()
    print('The item you are looking for is, ' + bestbuy_title)
    print('The price is, ' + bestbuy_price)
    neat_price = str()
    for char in bestbuy_price:
        #only check number before the dot
        if char == '.':
            break
        if char.isalnum():
            neat_price += char
    neat_price = int(neat_price)    #convert the digits before ',' to an integer
    print('The current neat price is: ', neat_price)

    target_price = 1000
    if neat_price < target_price:
        send_email()

def check_natasha_price():
    page = requests.get(natasha_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    natasha_title = soup.find('h1', class_='css-11zrkxf e65zztl0')
    natasha_title = natasha_title.find('a', class_='css-1gyh3op e65zztl0').get_text()
    natasha_price = soup.find('span', class_='css-1oz9qb')
    # need to find next level because of aria-hidden
    natasha_price = natasha_price.find('b', class_='css-0').get_text()
    print('The item you are looking for is: ' + natasha_title)
    print('The price is: ' + natasha_price)
    neat_price = str()
    for char in natasha_price:
        #only check number before the dot
        if char == '.':
            break
        if char.isalnum():
            neat_price += char
    neat_price = int(neat_price)    #convert the digits before ',' to an integer
    print('The current neat price is: ', neat_price)
    
    target_price = 40
    if neat_price < target_price:
        send_email()

def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('xxxxxx@gmail.com', 'ebzekkecybdnbqls')
    subject = 'Natasha Price down'
    body = 'This message is sent from Yuan Ji. \n Do you like this item? \n Check the Natasha link now: https://www.sephora.com/product/natasha-denona-glam-eyeshadow-palette-P461188?icid2=recommended%20for%20you:p461188:product'
    message = f"""Subject: {subject}\n\n{body}"""
    server.sendmail(
        'xxxxxx@gmail.com',
        'yyyyyyyyy@gmail.com',
        message
    )
    print('Email has been sent!')
    server.quit()

# test single check_price function only
check_natasha_price()

# check the price using a loop
# while True:
#     check_natasha_price()
#     time.sleep(3600)  #check every xx seconds




