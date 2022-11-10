import os
import random
import traceback
import bezier
import pyautogui as pyautogui
import requests
import time
import threading
import substring as substring
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, \
    RemoteDriverServerException
from selenium.webdriver import DesiredCapabilities
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire.utils import decode as sw_decode
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
import re
import requests
import brotli
from pypasser import reCaptchaV3
from pypasser import reCaptchaV2
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from python_ghost_cursor import path
import string
from threading import Thread
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import traceback, sys
import datetime


def slow_type(pageInput):ed

    backspace = random.randint(1, 10)
    counter = 1
    for letter in pageInput:
        pyautogui.PAUSE = float(random.uniform(.1, .4))
        if letter.isupper():
            pyautogui.keyDown('shift')
            time.sleep(float(random.uniform(.1, .3)))
            pyautogui.press(letter)
            time.sleep(float(random.uniform(.1, .3)))
            pyautogui.keyUp('shift')
        elif counter == backspace:
            pyautogui.write(random.choice(string.ascii_letters))
            pyautogui.press('backspace')
            time.sleep(float(random.uniform(.5, 1.4)))
            pyautogui.write(letter)
        else:
            pyautogui.write(letter)

        counter += 1

        lotery = random.randint(1, 20)
        if lotery % 3 == 0:
            pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll


def mouse_hc():
    pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll
    time.sleep(float(random.uniform(0.3, 0.7)))
    pyautogui.mouseDown()
    pyautogui.moveRel(random.randint(-2, 2), random.randint(-2, 2))  ##mouse jitter on scroll
    time.sleep(float(random.uniform(0.02, 0.05)))
    pyautogui.mouseUp()
    pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll
    time.sleep(float(random.uniform(0.4, 0.8)))


def resting_mouse(big):  # move mouse to right of screen

    start = pyautogui.position()

    startPos = {
        "x": start.x,
        "y": start.y,
    }

    if big == True:
        end = {
            "x": start.x + random.randint(-100, 100),
            "y": start.y + random.randint(-100, 100),
        }
    else:
        end = {
            "x": start.x + random.randint(-25, 25),
            "y": start.y + random.randint(-25, 25),
        }

    route = path(startPos, end)

    for item in route:  # tranformacja z float64 na int
        for key, value in item.items():
            try:
                item[key] = int(value)
            except ValueError:
                item[key] = float(value)

    pyautogui.PAUSE = float(random.uniform(0.004, 0.007))

    # Move the mouse
    for j in route:
        pyautogui.moveTo(j['x'], j['y'])  # Move to point in curve
        print(j)
        # pyautogui.sleep(delay)  # Wait delay


def wind_mouse(location, size, panelHeight):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    '''
    start_x = pyautogui.position().x
    start_y = pyautogui.position().y
    x = location["x"]  # abs X and relative Y
    w = size["width"]
    wCenter = w / 2 + (random.randint(int(-w / 3), int(w / 3)))
    dest_x = int(wCenter + x)

    relY = location["y"]  # abs X and relative Y
    absY = relY + panelHeight
    h = size["height"]
    hCenter = h / 2 + (random.randint(int(-h / 3), int(h / 3)))
    dest_y = int(hCenter + absY)
    G_0 = random.randint(7, 11)
    W_0 = random.randint(2, 4)
    M_0 = random.randint(12, 18)
    D_0 = random.randint(9, 15)
    move_mouse = lambda x, y: None

    sqrt3 = np.sqrt(3)
    sqrt5 = np.sqrt(5)

    current_x, current_y = start_x, start_y
    v_x = v_y = W_x = W_y = 0
    while (dist := np.hypot(dest_x - start_x, dest_y - start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
            W_y = W_y / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random() * 3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0 * (dest_x - start_x) / dist
        v_y += W_y + G_0 * (dest_y - start_y) / dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0 / 2 + np.random.random() * M_0 / 2
            v_x = (v_x / v_mag) * v_clip
            v_y = (v_y / v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            # This should wait for the mouse polling interval
            move_mouse(current_x := move_x, current_y := move_y)
        pyautogui.PAUSE = float(random.uniform(0.007, 0.01))
        pyautogui.moveTo(current_x, current_y)


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("loginForm.ui", self)

        # self.dodajDoKoszyka.clicked.connect(self.zmientext)
        green = QColor(0, 255, 127)
        self.logi.setTextColor(green)

        self.loginbutton.clicked.connect(self.start)
        self.startbutton.clicked.connect(self.startFunkcji)

        # self.loginbutton.clicked.connect(lambda: self.addItem())

    def addItem(self, text):
        self.lista_wungli.addItem(text)

    def start(self):
        threading.Thread(target=self.loginfunction, args=(), daemon=True).start()

    def sprawdzProdukty(self, driver):
        page_html = driver.page_source

        soup = BeautifulSoup(page_html, 'html.parser', multi_valued_attributes=None)
        produkty = []  # lista wungli

        for row in soup.find_all('div', attrs={'class': 'row mt-4 justify-content-center'}):  # produkty
            id = 0
            rodzaj = row.findNext('div', attrs={'class': ' col-8 col-md-2 text-4 pt-3 text-center'})  # div w divie
            dostep = row.findNext('div', attrs={'class': 'col-12 col-md-3 col-lg-2 pt-3 text-sm-center'})

            nazwa = rodzaj.findNext('a')  # nazwa produktu
            kopalnia = rodzaj.findNext('div')  # nazwa kopalni

            produkt = {}
            produkt['id'] = id
            produkt['nazwa'] = nazwa.getText(" | ", strip=True)
            produkt['kopalnia'] = kopalnia.getText(" | ", strip=True)

            przycisk = dostep.findNext('button')
            if przycisk.has_attr('disabled'):
                produkt['dostepny'] = 'Niedostepny'
            else:
                produkt['dostepny'] = 'Dostepny'

            produkty.append(produkt)
            self.addItem(produkt['nazwa'] + ' z ' + produkt['kopalnia'])
            id += 1

    def startFunkcji(self):
        self.startbutton.setEnabled(False)

    def dodajDoKoszyka(self, driver, panelHeight):

        self.startbutton.setEnabled(False)

        godzina = 16
        minuta = 4
        sekunda = 5

        # godzina = 16
        # minuta = random.randint(2, 3)
        # sekunda = random.randint(2, 59)

        czasStart = 3600 * (godzina - datetime.datetime.now().hour) + 60 * (minuta - datetime.datetime.now().minute) + (
                sekunda - datetime.datetime.now().second)
        self.logi.append(f'Start o {godzina}:{minuta}:{sekunda}')

        if czasStart < 0:
            czasStart = 5

        time.sleep(czasStart)

        while True:
            try:
                pyautogui.hotkey('f5')
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()
                except TimeoutException:
                    print("no alert")

                try:
                    quote = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'mainMenu')))
                except NoSuchElementException:
                    continue
                except RemoteDriverServerException:
                    continue

                przyciski = driver.find_elements(By.CSS_SELECTOR, '.btn.btn-primary')
                przyciski.pop(0)

                wyborID = self.lista_wungli.currentIndex()

                print(wyborID)

                page_html = driver.page_source

                soup = BeautifulSoup(page_html, 'html.parser', multi_valued_attributes=None)
                wybor = soup.find_all('div', attrs={'class': 'row mt-4 justify-content-center'})[wyborID]  # produkt
                dostep = wybor.findNext('div', attrs={'class': 'col-12 col-md-3 col-lg-2 pt-3 text-sm-center'})

                przycisk = dostep.findNext('button')
                # if przycisk.has_attr('disabled'):
                if przycisk.has_attr('enabled'):
                    time.sleep(float(random.uniform(12, 18)))
                    driver.refresh()
                else:
                    loc = przyciski[wyborID].location
                    size = przyciski[wyborID].size

                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center'});",
                                          przyciski[wyborID])
                    windowHeight = driver.execute_script('return window.innerHeight;')

                    time.sleep(float(random.uniform(2, 3)))

                    newloc = {"x": loc['x'], "y": round(windowHeight / 2 - size['height'] / 2)}
                    wind_mouse(newloc, size, panelHeight)

                    mouse_hc()

                    newloc['x'] = newloc['x'] + random.randint(-30, 30)
                    newloc['y'] = newloc['y'] + random.randint(-30, 30)

                    wind_mouse(newloc, size, panelHeight)
                    try:
                        quote = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mainMenu')))
                        self.logi.append("DODANO DO KOSZYKA!")
                        break
                    except NoSuchElementException:
                        pyautogui.hotkey('f5')
                        try:
                            WebDriverWait(driver, 3).until(EC.alert_is_present())
                            driver.switch_to.alert.accept()
                        except TimeoutException:
                            print("no alert")
            except NoSuchElementException:
                continue
            except RemoteDriverServerException:
                continue

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        self.logi.append("Proba logowania, czekaj...")

        self.loginbutton.setEnabled(False)

        try:
            # Zaladowanie webdriver
            options = webdriver.ChromeOptions()
            options.add_argument("--incognito")
            options.add_argument("--disable-gpu")
            options.add_argument("--start-maximized")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(r'--load-extension=C:\Users\Komputer\PycharmProjects\sklep\uBlock')
            # options.add_argument(r'--load-extension=C:\Users\Komputer\PycharmProjects\sklep\ghostery')

            # options.add_argument("--headless=chrome")
            # generowanie losowego USER AGENT
            # ua = UserAgent()
            # userAgent = ua.random

            # ustawienie user agent
            # options.add_argument(f'--user-agent={userAgent}')

            driver = uc.Chrome(options=options)
            # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
            driver.delete_all_cookies()

            time.sleep(2)
            driver.get('chrome://extensions/?id=hpbkalbaefljfondbkaipmmjihafaefa')  # ublock
            # driver.get('chrome://extensions/?id=dlgonfikbbgfhbfiojgpddlehhaacikp')  # ghostery
            time.sleep(2)

            # wlaczenie wtycznki w incognto
            driver.execute_script(
                "return document.querySelector('extensions-manager').shadowRoot.querySelector('#viewManager > extensions-detail-view.active').shadowRoot.querySelector('div#container.page-container > div.page-content > div#options-section extensions-toggle-row#allow-incognito').shadowRoot.querySelector('label#label input').click()");

            panelHeight = driver.execute_script('return window.outerHeight - window.innerHeight;')

            time.sleep(3)

            driver.get("https://sklep.pgg.pl/login")

            # driver.get("https://sklep.pgg.pl")

            time.sleep(float(random.uniform(8, 9)))

            # ============= LOGOWANIE ===================

            # coockie = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/button")  # coockie
            # ghost_mouse(coockie.location, coockie.size, panelHeight, 30)
            # time.sleep(float(random.uniform(0.2, 0.5)))
            # pyautogui.click()
            # resting_mouse(True)
            # time.sleep(float(random.uniform(0.2, 0.5)))

            while True:
                try:
                    emailInput = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "email")))

                    wind_mouse(emailInput.location, emailInput.size, panelHeight)

                    mouse_hc()

                    emailInput.location["x"] = emailInput.location["x"] + random.randint(-50, 50)
                    emailInput.location["y"] = emailInput.location["y"] + random.randint(-25, 25)
                    wind_mouse(emailInput.location, emailInput.size, panelHeight)

                    slow_type(email)

                    time.sleep(float(random.uniform(1, 1.5)))

                    passwordInput = driver.find_element(By.ID, "password")
                    wind_mouse(passwordInput.location, passwordInput.size, panelHeight)

                    mouse_hc()

                    passwordInput.location["x"] = passwordInput.location["x"] + random.randint(-50, 50)
                    passwordInput.location["y"] = passwordInput.location["y"] + random.randint(-25, 25)
                    wind_mouse(passwordInput.location, passwordInput.size, panelHeight)

                    slow_type(password)

                    time.sleep(float(random.uniform(1, 2)))

                    # Solve reCaptcha v2 via PyPasser
                    is_checked = reCaptchaV2(driver=driver, play=False, panelHeight=panelHeight)
                    if is_checked == True:
                        zaloujButton = driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
                        wind_mouse(zaloujButton.location, zaloujButton.size, panelHeight)
                        mouse_hc()
                        self.logi.append("Udane logowanie!")
                        break

                except NoSuchElementException:
                    driver.refresh()
                    time.sleep(10)
                    continue

            # ========== Dodawanie produktow do listy ================

            self.sprawdzProdukty(driver)

            self.logi.append('Wybierz produkt z listy i wcisnij "START" !')
            self.startbutton.setEnabled(True)

            # ============= Dodawanie do koszyka ===================

            while True:
                if self.startbutton.isEnabled() == True:
                    time.sleep(2)
                else:
                    self.dodajDoKoszyka(driver, panelHeight)
                    break

        except NoSuchElementException as ex:
            print("Exception has been thrown. " + str(ex))

    # driver.close()
    # driver.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(587)
    widget.setFixedHeight(748)
    widget.show()
    app.exec()
    sys.exit(app.quit())

    # try:
    # # szukanie tokenu sesji potrzebnego do logowania
    #     for request in driver.requests:
    #         substring = "https://sklep.pgg.pl/login"
    #         if request.url.find(substring) != -1:
    #             data = sw_decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
    #             data = data.decode("utf8")
    #             print(type(data))
    #             csrfmiddlewaretoken = re.findall(r'name="csrf-token" value="(.*?)"', data)[0]
    #             print("token:" + csrfmiddlewaretoken)
    #             break
    # except:
    #     print("Cos poszlo nie tak")
    #     driver.quit()

    # payload = {
    #     'csrfmiddlewaretoken': csrfmiddlewaretoken,
    #     'g-recaptcha-response': reCaptcha_response,
    #     'hidden_username': email,
    #     'password': password
    # }

# try:
#     req = requests.session()
#
#     selenium_user_agent = driver.execute_script("return navigator.userAgent;")
#     req.headers.update({"user-agent": selenium_user_agent})
#
#     for cookie in driver.get_cookies():
#         req.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
#
#     response = req.get("https://linkedin/example_page.com")
#
#     session_cookies = req.cookies
#     cookies_dictionary = session_cookies.get_dict()
#     print(cookies_dictionary)
#     print(req.text)
#
# except Exception as error: \
#     print(error)


# =================================================================

# headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#             "Accept - Encoding": "gzip, deflate, br",
#             "Accept-Language": "en-US,en;q=0.5",
#             "Connection": "keep-alive",
#             "Host":	"sklep.pgg.pl",
#             "Sec-Fetch-Dest": "document",
#             "Sec-Fetch-Mode": "navigate",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
#             }


# # blokowanie ruchu
# driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ["www.google.com"]})
# driver.execute_cdp_cmd('Network.enable', {})
# driver.execute_cdp_cmd('Network.setUserAgentOverride', {
#     "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})


# for request in driver.requests:
#     # szukanie requestu z ReCaptchaV3
#     substring = "https://www.google.com/recaptcha/api2/anchor"
#     if request.url.find(substring) != -1:
#         print(request.url)
#         print(type(request.url))
#         reCaptcha_response = reCaptchaV3(request.url)
#         print(reCaptcha_response)
#         break

# =================================================================
#   browser.execute_script("arguments[0].click();", element)
#  time.sleep(5)
#     email = browser.find_element(By.XPATH, "//*[@id=\"fe_text\"]").get_attribute('value')
#
#     # Open a new window
#     browser.switch_to.new_window('tab')
#     time.sleep(3)
#     # Store the ID of the original window
#     original_window = browser.current_window_handle
#     browser.get("https://h5.iearnbot.com")
#     time.sleep(5)
#
#
#     # Switch back to the first tab
#     browser.switch_to.window(original_window)
#
