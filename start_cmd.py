from AutoSeriesEpisodeChanger import AutoSeriesEpisodeChanger
import os

# os.system("pip install -r requirements.txt")
start_url = input("Enter the url of the episode to start with : ")
episode_time = float(input("Enter the time of a single episode in minutes (eg: 11.2 = 11 minutes and 12 seconds)"))  # minutes

asec = AutoSeriesEpisodeChanger(start_url, episode_time)
asec.run()
