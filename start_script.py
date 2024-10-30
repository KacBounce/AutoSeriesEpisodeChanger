from AutoSeriesEpisodeChanger import AutoSeriesEpisodeChanger
import os

#os.system("pip install -r requirements.txt")
start_url = "https://www.wcofun.net/regular-show-season-2-episode-13-this-is-my-jam"
episode_time = 12 #minutes

asec = AutoSeriesEpisodeChanger(start_url, episode_time)
asec.run()