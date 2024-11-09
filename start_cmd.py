from AutoSeriesEpisodeChanger import AutoSeriesEpisodeChanger
import os

# os.system("pip install -r requirements.txt")
start_url = input("Enter the url of the episode to start with : ")
episode_time = float(input("Enter the time of a single episode in minutes (eg: 11.2 = 11 minutes and 12 seconds) : "))  # minutes
key_to_exit = input("Enter the key you with to use to exit the program (Event names from keyboard library): ")
asec = AutoSeriesEpisodeChanger(start_url, episode_time, key_to_exit)
asec.run()
