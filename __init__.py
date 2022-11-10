import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from python_ghost_cursor import path
import os
import speech_recognition as sr
from time import sleep
from typing import Type
import bezier
import pyautogui as pyautogui
import numpy as np
import random
import string

from pypasser.exceptions import IpBlock
from pypasser.utils import download_audio, convert_to_wav


def slow_type(pageInput):
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
            time.sleep(float(random.uniform(.5, 1.2)))
            pyautogui.write(letter)
        else:
            pyautogui.write(letter)

        counter += 1
        lotery = random.randint(1, 20)
        if lotery % 3 == 0:
            pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll

def ghost_mouse(location, size, panelHeight, steps):  # move mouse to middle of element

    x, relY = location["x"], location["y"]  # abs X and relative Y
    absY = relY + panelHeight
    w, h = size["width"], size["height"]
    wCenter = w / 3 + random.randint(1, 10)
    hCenter = h / 3 + random.randint(1, 10)
    xCenter = int(wCenter + x)
    yCenter = int(hCenter + absY)

    start = pyautogui.position()
    end = xCenter, yCenter

    start = {
        "x": start.x,
        "y": start.y,
    }

    end = {
        "x": xCenter,
        "y": yCenter,
    }

    route = path(start, end)

    for item in route:  # tranformacja z float64 na int
        for key, value in item.items():
            try:
                item[key] = int(value)
            except ValueError:
                item[key] = float(value)

    if steps > 15:
        pyautogui.PAUSE = float(random.uniform(0.03, 0.05))
    else:
        pyautogui.PAUSE = float(random.uniform(0.01, 0.02))

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
    wCenter = w / 2 + (random.randint(int(-w/3), int(w/3)))
    dest_x = int(wCenter + x)

    relY = location["y"]  # abs X and relative Y
    absY = relY + panelHeight
    h = size["height"]
    hCenter = h / 2 + (random.randint(int(-h/3), int(h/3)))
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

def mouse_hc():
    pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll
    time.sleep(float(random.uniform(0.3, 0.7)))
    pyautogui.mouseDown()
    pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll
    time.sleep(float(random.uniform(0.02, 0.05)))
    pyautogui.mouseUp()
    pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll
    time.sleep(float(random.uniform(0.4, 0.8)))

def mouse_shake():
    pyautogui.PAUSE = float(random.uniform(0.2, 0.5))
    pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll
    pyautogui.PAUSE = float(random.uniform(0.02, 0.15))
    pyautogui.moveRel(random.randint(-3, 2), random.randint(-2, 3))  ##mouse jitter on scroll


class reCaptchaV2(object):
    """
    reCaptchaV2 bypass
    -----------------
    Solving reCaptcha V2 using speech to text

    Attributes
    ----------
    driver: webdriver

    play: bool
        default is True

    attempts: int
        default is 3 times

    Returns
    ----------
    bool: result of solver
    """

    def __new__(cls, panelHeight, *args, **kwargs) -> bool:
        instance = super(reCaptchaV2, cls).__new__(cls)
        instance.__init__(*args, **kwargs)

        remaining_attempts = instance.attempts
        file_path = None

        try:
            cls.__click_check_box__(instance.driver, panelHeight=panelHeight)

            if cls.__is_checked__(instance.driver):
                return True

            cls.__click_audio_button__(instance.driver, panelHeight=panelHeight)

            while remaining_attempts:
                remaining_attempts -= 1

                link = cls.__get_audio_link__(instance.driver, instance.play, panelHeight=panelHeight)
                file_path = convert_to_wav(download_audio(link))
                cls.__type_text__(instance.driver, cls.speech_to_text(file_path), panelHeight=panelHeight)
                os.remove(file_path)

                checked = cls.__is_checked__(instance.driver)
                if checked or not remaining_attempts:
                    return checked

        except Exception as e:
            if file_path:
                os.remove(file_path)

            if 'rc-doscaptcha-header' in instance.driver.page_source:
                raise IpBlock()
            else:
                raise e

    def __init__(self, driver: Type[Chrome], play: bool = True, attempts: int = 3, panelHeight: int = 0):
        self.driver = driver
        self.play = play
        self.attempts = attempts
        self.panelHeight = panelHeight

    def __click_check_box__(driver, panelHeight):

        ramka = driver.find_elements(By.TAG_NAME, "iframe")[0]
        lokalizacja = ramka.location

        driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
        check_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR ,"#recaptcha-anchor")))
        # check_box.click()

        dictFin = {'x': 0, 'y': 0}
        dictFin['x'] = lokalizacja['x'] + check_box.location['x']
        dictFin['y'] = lokalizacja['y'] + check_box.location['y']

        wind_mouse(dictFin, check_box.size, panelHeight)
        mouse_hc()

        dictFin['x'] = dictFin['x'] + random.randint(-30, 30)
        dictFin['y'] = dictFin['y'] + random.randint(-25, 25)
        wind_mouse(dictFin, check_box.size, panelHeight)

        mouse_shake()

        driver.switch_to.default_content()

    def __click_audio_button__(driver, panelHeight):
        ramka = driver.find_elements(By.TAG_NAME, "iframe")[2]
        lokalizacja = ramka.location
        driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[2])
        audio_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR ,"#recaptcha-audio-button")))
        # audio_btn.click()

        dictFin = {'x': 0, 'y': 0}
        dictFin['x'] = lokalizacja['x'] + audio_btn.location['x']
        dictFin['y'] = lokalizacja['y'] + audio_btn.location['y']
        dictFin2 = {'x': 0, 'y': 0}
        dictFin2['x'] = dictFin['x'] + random.randint(-30, 30)
        dictFin2['y'] = dictFin['y'] + random.randint(-25, 25)
        audio_btn2 = audio_btn.size

        wind_mouse(dictFin, audio_btn.size, panelHeight)
        mouse_hc()

        wind_mouse(dictFin2, audio_btn2, panelHeight)

        mouse_shake()

        time.sleep(float(random.uniform(0.5, 1)))

        driver.switch_to.default_content()

    def __get_audio_link__(driver, play, panelHeight):
        voice = driver.find_elements(By.TAG_NAME, "iframe")[2]
        lokalizacja = voice.location

        driver.switch_to.frame(voice)
        download_btn = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rc-audiochallenge-tdownload-link")))
        link = download_btn.get_attribute('href')

        play_button = driver.find_element(By.CSS_SELECTOR, ".rc-audiochallenge-play-button > button")

        dictFin = {'x': 0, 'y': 0}
        dictFin['x'] = lokalizacja['x'] + play_button.location['x']
        dictFin['y'] = lokalizacja['y'] + play_button.location['y']

        wind_mouse(dictFin, play_button.size, panelHeight)
        mouse_hc()

        dictFin2 = {'x': 0, 'y': 0}
        dictFin2['x'] = dictFin['x'] + random.randint(-40, 40)
        dictFin2['y'] = dictFin['y'] + random.randint(-25, 25)

        wind_mouse(dictFin2, play_button.size, panelHeight)

        mouse_shake()

        time.sleep(float(random.uniform(0.5, 1)))

        mouse_shake()

        time.sleep(float(random.uniform(1, 2)))

        driver.switch_to.default_content()
        if play:
            play_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rc-audiochallenge-play-button > button")))
            # play_button.click()
            time.sleep(float(random.uniform(1, 2)))
        return link

    def __type_text__(driver, text, panelHeight):

        voice = driver.find_elements(By.TAG_NAME, "iframe")[2]
        lokalizacja = voice.location

        driver.switch_to.frame(voice)

        text_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "audio-response")))

        dictFin = {'x': 0, 'y': 0}
        dictFin['x'] = lokalizacja['x'] + text_field.location['x']
        dictFin['y'] = lokalizacja['y'] + text_field.location['y']

        wind_mouse(dictFin, text_field.size, panelHeight)
        mouse_hc()
        text_field.location["x"] = text_field.location["x"] + random.randint(-50, 50)
        text_field.location["y"] = text_field.location["y"] + random.randint(-25, 25)
        wind_mouse(dictFin, text_field.size, panelHeight)

        slow_type(text)

        time.sleep(float(random.uniform(0.5, 1.5)))
        
        mouse_shake()

        pyautogui.press('enter')
        driver.switch_to.default_content()

    def __is_checked__(driver):
        sleep(3)
        driver.switch_to.frame(
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[name^=a]'))))
        try:
            driver.find_element(By.CSS_SELECTOR, '.recaptcha-checkbox-checked')
            driver.switch_to.default_content()
            return True
        except NoSuchElementException:
            driver.switch_to.default_content()
            return False

    def speech_to_text(audio_path: str) -> str:
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)

        return r.recognize_sphinx(audio)
