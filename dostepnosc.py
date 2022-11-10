# import requests
#
# headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#            "Accept - Encoding": "gzip, deflate, br",
#            "Accept-Language": "en-US,en;q=0.5",
#            "Connection": "keep-alive",
#            "Host": "sklep.pgg.pl",
#            "Sec-Fetch-Dest": "document",
#            "Sec-Fetch-Mode": "navigate",
#            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
#            }
#
# x = requests.get('https://sklep.pgg.pl/', headers=headers)
#
# print(x.text)

import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import seleniumwire.undetected_chromedriver as uc

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)

    driver.get("https://browserleaks.com/client-hints")

    time.sleep(999)
