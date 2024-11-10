from AutoSeriesEpisodeChanger import AutoSeriesEpisodeChanger
import os

start_url = ""
try:
    last_episode_file = open(
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

if (start_url == "" or start_url == None):
    # os.system("pip install -r requirements.txt")
    start_url = input("Enter the url of the episode to start with : ")


    

episode_time = float(input("Enter the time of a single episode in minutes (eg: 11.2 = 11 minutes and 12 seconds) : "))  # minutes
key_to_exit = input("Enter the key you with to use to exit the program (Event names from keyboard library): ")

asec = AutoSeriesEpisodeChanger(start_url, episode_time, key_to_exit)
asec.run()
