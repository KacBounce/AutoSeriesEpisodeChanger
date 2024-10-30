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
import threading
import keyboard


class AutoSeriesEpisodeChanger():    

    def __init__(self, start_url, episode_time, key_to_exit):
        self.start_url = start_url
        self.episode_time = episode_time * 60
        self.playing = True
        self.key_to_exit = key_to_exit
    
    def start_closing_thread(self, driver):
        # Create and start a thread
        listener_thread = threading.Thread(target=self.stop_playing, args=(driver,))
        listener_thread.daemon = True  # Daemonize thread
        listener_thread.start()
    
    def stop_playing(self, driver):
        while self.playing:
            try:
                event = keyboard.read_event()  # Blocks until an event occurs
                if event.name == self.key_to_exit:  # Only handle key down events
                    print(f"Key pressed: {event.name}")
                    self.playing = False
                    driver.close()
            except Exception as e:
                print(f"An error occurred: {e}")
        

    def run(self):
        driver = uc.Chrome()
        self.start_closing_thread(driver)
        driver.get(self.start_url)
        
        iframe = driver.find_element(By.XPATH, "//iframe[@id='cizgi-js-0']")

        driver.switch_to.frame(iframe)

        try:
            while self.playing:
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
                
                video = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/video")                
                video.send_keys(Keys.ESCAPE)
                time.sleep(1)
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
                
        except Exception as e:
            driver.close()
            print("Driver closed")
            
        finally:
            driver.close()
            print("Driver closed")
            
