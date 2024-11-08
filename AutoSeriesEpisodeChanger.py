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
import math
from Websites import Websites


class AutoSeriesEpisodeChanger():    

    def __init__(self, start_url, episode_time, key_to_exit):
        self.start_url = start_url
        self.episode_time = episode_time * 60
        self.playing = True
        self.key_to_exit = key_to_exit
        
        self.website = None
        for website in Websites:
            if website.value in start_url:
                print(f"Website found : {website.value}")
                self.website = website
                break
            else:
                print("Website not supported")
        
        if (self.website == None):
            print("Website not found in the Websites enum")
                
        # if Websites.WCOFUN.value in start_url:
        #     self.website = Websites.WCOFUN
   
    
    def start_closing_thread(self, driver):
        # Create and start a thread
        listener_thread = threading.Thread(target=self.stop_playing, args=(driver,))
        listener_thread.daemon = True  # Daemonize thread
        listener_thread.start()
    
    def stop_playing(self, driver):
        while self.playing:
            event = keyboard.read_event()  # Blocks until an event occurs
            if event.name == self.key_to_exit:  # Only handle key down events
                print(f"Closing the driver")
                self.playing = False
                try:
                    driver.close()
                except:
                    print("Driver already closed")
                    continue
                

    def run_wcofun(self):
        driver = uc.Chrome()
        
        driver.get(self.start_url)
        
        iframe = driver.find_element(By.XPATH, "//iframe[@id='cizgi-js-0']")

        driver.switch_to.frame(iframe)

        try:
            first_run = True
            self.start_closing_thread(driver)
            while self.playing:
                if (first_run):
                    print("Starting bot, please wait until message to quit safely...")
                else:
                    print("Starting next episode, please wait for the message to quit safely...")
                time.sleep(1)
               
                start = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]")
                
                time.sleep(1)
                start.click()
                try:
                    time.sleep(1)
                    quality = driver.find_element(
                        By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div[4]/div[14]/button")
                    if (quality.is_displayed()):
                        quality.click()
                        time.sleep(1)
                        try:
                            hd = driver.find_element(
                            By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div[4]/div[14]/div/ul/li[1]/a")
                            hd.click()
                            time.sleep(1)
                            try:
                                start.click()

                            except:
                                print("Start button not found")
                        except:
                            print("HD not found")
                except:
                    print("Quality not found")
    
                time.sleep(1)
                video = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/video")
                video.send_keys(Keys.ESCAPE)
                
                fullscreen = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div[4]/button[6]")
                
                time.sleep(1)
                
                fullscreen.click()
                video = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/video")
                time.sleep(1)
                print("You can quit now by pressing " + self.key_to_exit)
                for i in range(math.ceil(int(self.episode_time))):
                    if (self.playing):
                        time.sleep(1)
                    else:
                        quit(0)                
                
                
                video.send_keys(Keys.ESCAPE)
                time.sleep(1)
                fullscreen.click()
                
                driver.switch_to.default_content()
                
                time.sleep(1)
                next_ep = driver.find_element(
                    By.XPATH, "/html/body/div[3]/div/div/div[1]/div[2]/div[5]/span[2]")
                
                next_ep.click()
                
                time.sleep(1)
                iframe = driver.find_element(
                    By.XPATH, "//iframe[@id='cizgi-js-0']")
                
                driver.switch_to.frame(iframe)
                
        finally:
            print("Goodbye")
            try:              
                driver.close()
                print("Driver closed")
            except:
                print()

    def run(self):
        if (self.website == Websites.WCOFUN):
            self.run_wcofun()