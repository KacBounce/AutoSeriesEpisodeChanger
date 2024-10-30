from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import  NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time


class AutoSeriesEpisodeChanger():    

    def __init__(self, start_url, episode_time):
        self.start_url = start_url
        self.episode_time = episode_time * 60

    def run(self):
        driver = uc.Chrome()

        driver.get(self.start_url)
        
        iframe = driver.find_element(By.XPATH, "//iframe[@id='cizgi-js-0']")

        driver.switch_to.frame(iframe)

        try:
            while True:
                time.sleep(2)
                start = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]")
                
                time.sleep(2)
                start.click()
                
                time.sleep(1)
                fullscreen = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div[4]/button[6]")
                
                time.sleep(1)
                fullscreen.click()
                
                time.sleep(self.episode_time)
                fullscreen.click()
                
                driver.switch_to.default_content()
                
                time.sleep(5)
                next_ep = driver.find_element(
                    By.XPATH, "/html/body/div[3]/div/div/div[1]/div[2]/div[5]/span[2]")
                
                next_ep.click()
                
                time.sleep(10)
                iframe = driver.find_element(
                    By.XPATH, "//iframe[@id='cizgi-js-0']")
                
                driver.switch_to.frame(iframe)
                
        except KeyboardInterrupt:
            driver.close()
            print("Driver closed")
            
