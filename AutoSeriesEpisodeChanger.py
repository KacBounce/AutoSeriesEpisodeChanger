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
from pyautogui import press


class AutoSeriesEpisodeChanger():    

    def __init__(self, start_url, episode_time, key_to_exit, key_to_pause, key_to_skip):
        self.start_url = start_url
        self.episode_time = episode_time * 60
        self.playing = True
        self.paused = False
        self.skipped = False
        self.key_to_exit = key_to_exit
        self.key_to_pause = key_to_pause
        self.key_to_skip = key_to_skip
        self.mutex = threading.Lock()
        self.pausing_thread_running = False
        self.skipping_thread_running = False
        self.stop_thread_running = True
        
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
    
    def start_ending_thread(self):
        # Create and start a thread
        listener_thread = threading.Thread(
            target=self.end_threads)
        listener_thread.daemon = True  # Daemonize thread
        listener_thread.start()
        
        return listener_thread
    
    def end_threads(self):
        time.sleep(10)
        while self.stop_thread_running:
            time.sleep(5)
            if (not self.skipping_thread_running or not self.pausing_thread_running):
                press('a')
                time.sleep(1)
                press('a')
                time.sleep(1)
                
            
            # if Websites.WCOFUN.value in start_url:
        #     self.website = Websites.WCOFUN
    def start_skiping_thread(self, driver, iframe):
        # Create and start a thread
        listener_thread = threading.Thread(
            target=self.skip_episode, args=(driver, iframe))
        listener_thread.daemon = True  # Daemonize thread
        listener_thread.start()

        return listener_thread

    def skip_episode(self, driver, iframe):
        print("Running skipping thread")
        self.skipped = False
        self.playing = True
        while self.skipping_thread_running:
            time.sleep(1)
            event = keyboard.read_event()  # Blocks until an event occurs
            if event.name == self.key_to_skip:  # Only handle key down events
                try:
                    driver.switch_to.default_content()
                    next_ep = driver.find_element(
                        By.XPATH, "/html/body/div[3]/div/div/div[1]/div[2]/div[5]/span[2]")

                    next_ep.click()
                except:
                    print("Next ep not found, trying to quit full screen")
                    try:
                        driver.switch_to.frame(iframe)
                        video = driver.find_element(
                            By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/video")
                        video.send_keys(Keys.ESCAPE)
                        
                        
                        fullscreen = driver.find_element(
                            By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div[4]/button[6]")

                        
                        fullscreen.click()
                        driver.switch_to.default_content()
                        time.sleep(1)
                        
                        next_ep = driver.find_element(
                            By.XPATH, "/html/body/div[3]/div/div/div[1]/div[2]/div[5]/span[2]")

                        
                        next_ep.click()
                        
                    except Exception as e:                        
                        print(f"Can't skip episode : {e}\nTurning fullscreen to previous state")
                        video.send_keys(Keys.ESCAPE)
                        time.sleep(1)
                        fullscreen.click()
                finally:
                    self.skipped = True
                    self.playing = False
                                
                
        # if Websites.WCOFUN.value in start_url:
        #     self.website = Websites.WCOFUN
    def start_pausing_thread(self, video):
        # Create and start a thread
        listener_thread = threading.Thread(
            target=self.pause_playback, args=(video,))
        listener_thread.daemon = True  # Daemonize thread
        listener_thread.start()
        
        return listener_thread
    
    def pause_playback(self, video):
        print("Running pausing thread")
        while self.pausing_thread_running:
            time.sleep(1)
            event = keyboard.read_event()  # Blocks until an event occurs
            if event.name == self.key_to_pause:  # Only handle key down events
                if (self.paused):
                    print(f"Un-pausing video")
                else:
                    print("Pausing video")
                self.paused = not self.paused
                try:
                    video.click()
                except:
                    continue

    
    def start_closing_thread(self, driver):
        # Create and start a thread
        listener_thread = threading.Thread(target=self.stop_playing, args=(driver,))
        listener_thread.daemon = True  # Daemonize thread
        listener_thread.start()
        
        return listener_thread
    
    def stop_playing(self, driver):
        while self.stop_thread_running:
            event = keyboard.read_event()  # Blocks until an event occurs
            if event.name == self.key_to_exit:  # Only handle key down events
                print(f"Closing the driver")
                self.playing = False
                try:
                    last_episode_file = open(
                        "C:\\Users\\kacpe\\Desktop\\Auto Series Episode Changer\\last_episode.txt", "w")
                    last_episode_file.write(driver.current_url)
                    last_episode_file.close()
                    driver.close()
                except:
                    print("Driver already closed")
                    continue
                

    def run_wcofun(self):
        driver = uc.Chrome()
        
        driver.get(self.start_url)

        try:
            first_run = True
            closing_thread = self.start_closing_thread(driver)
            ending_thread = self.start_ending_thread()
            while self.playing:
                time.sleep(1)
                iframe = driver.find_element(
                    By.XPATH, "//iframe[@id='cizgi-js-0']")

                driver.switch_to.frame(iframe)
                if (first_run):
                    print("Starting bot, please wait until message to quit safely...")
                else:
                    print("Starting next episode, please wait for the message to quit safely...")
                
                first_run = False
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
                
                self.pausing_thread_running = True
                pausing_thread = self.start_pausing_thread(video)

                           
                fullscreen = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/div[4]/button[6]")
                
                time.sleep(1.5)
                
                fullscreen.click()
                video = driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[2]/div/div/div[1]/div/video")
                time.sleep(1)
                print("You can quit now by pressing " +
                      self.key_to_exit)
                
                self.skipping_thread_running = True
                skipping_thread = self.start_skiping_thread(driver, iframe)
                
                
                counter = 0
                while(counter != int(math.ceil(self.episode_time))):
                    if (self.playing):
                        time.sleep(1)
                        if (not self.paused):
                            counter += 1    
                    else:
                        if (self.skipped):
                            print("Loop broken")
                            self.playing = True
                            break
                        else:
                            try:
                                driver.close()     
                            finally:  
                                quit()    
                
                if (not self.skipped):
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
                
                self.pausing_thread_running = False
                pausing_thread.join()
                print("Pausing thread closed")
                self.skipping_thread_running = False
                skipping_thread.join()
                print("Skipping thread closed")
                
        except Exception as e:
            print(e)
         
        finally:
            print("Goodbye")
            self.stop_thread_running = False
            closing_thread.join()
            print("Closing thread closed")
            ending_thread.join()
            print("Ending thread closed")
            try:              
                driver.close()
                print("Driver closed")
            except:
                quit(0)

    def run(self):
        if (self.website == Websites.WCOFUN):
            self.run_wcofun()