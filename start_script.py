from AutoSeriesEpisodeChanger import AutoSeriesEpisodeChanger

start_url = "https://www.wcofun.net/regular-show-season-3-episode-13-weekend-at-benson-s"

# "https://www.wcofun.net/batman-the-brave-and-the-bold-season-1-episode-15-trials-of-the-demon"
# "https://www.wcofun.net/regular-show-season-3-episode-12-under-the-hood"
try:
    last_episode_file= open(
        'C:\\Users\\kacpe\\Desktop\\Auto Series Episode Changer\\last_episode.txt', "r")
    last_episode = last_episode_file.readline()
    last_episode_file.close()
    print(last_episode + " Found episode")
    if (last_episode != ""):
        start_url = last_episode
    else:
        print("No episode in file")
except:
    print("File not found")
    


episode_time = 11.2 # minutes/
key_to_exit = "/"  # Event names from keyboard library//
key_to_pause = ","
key_to_skip = "."

asec = AutoSeriesEpisodeChanger(start_url, episode_time, key_to_exit, key_to_pause, key_to_skip)
asec.run()