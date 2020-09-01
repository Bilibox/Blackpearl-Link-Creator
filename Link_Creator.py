###############################
###      Author: Bilibox    ###
###      Modder: Cocee      ###
###############################

import os
import sys
import time
import subprocess
import argparse
import pkg_resources
from concurrent.futures import ThreadPoolExecutor
required = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

__version__ = '1.0.3'

def RcloneLink(path):
    # Runs command "rclone link source:path"
    link = subprocess.run([
        "rclone",
        "link",
        path],
        encoding='utf-8',
        stdout=subprocess.PIPE)
    return link.stdout


def RcloneList(path):
    # Runs command "rclone lsf source:path"
    filelist = subprocess.run([
        "rclone",
        "lsf",
        path],
        encoding='utf-8',
        stdout=subprocess.PIPE)
    return filelist.stdout.strip().split("\n")


def Updater():
    print(""" ____  _            _    _____                _   _      _       _       _____                _             
 |  _ \| |          | |  |  __ \              | | | |    (_)     | |     / ____|              | |            
 | |_) | | __ _  ___| | _| |__) ___  __ _ _ __| | | |     _ _ __ | | __ | |     _ __ ___  __ _| |_ ___  _ __ 
 |  _ <| |/ _` |/ __| |/ |  ___/ _ \/ _` | '__| | | |    | | '_ \| |/ / | |    | '__/ _ \/ _` | __/ _ \| '__|
 | |_) | | (_| | (__|   <| |  |  __| (_| | |  | | | |____| | | | |   <  | |____| | |  __| (_| | || (_) | |   
 |____/__|\__,_|\___|_|\_|__   ____|\__,_|_|  |_| |________|_| |_|_|\_\  \_____|_| _____|\__,_|___\____|_|   
 | |  | |         | |     | | (_)                   |  __ \| |                     \ \        / /  (_| |     
 | |  | |_ __   __| | __ _| |_ _ _ __   __ _        | |__) | | ___  __ _ ___  ___   \ \  /\  / __ _ _| |_    
 | |  | | '_ \ / _` |/ _` | __| | '_ \ / _` |       |  ___/| |/ _ \/ _` / __|/ _ \   \ \/  \/ / _` | | __|   
 | |__| | |_) | (_| | (_| | |_| | | | | (_| |_ _ _  | |    | |  __| (_| \__ |  __/    \  /\  | (_| | | |_    
  \____/| .__/ \__,_|\__,_|\__|_|_| |_|\__, (_(_(_) |_|    |_|\___|\__,_|___/\___|     \/  \/ \__,_|_|\__|   
        | |                             __/ |                                                             """)
    time.sleep(10)
    updateURL = 'https://raw.githubusercontent.com/BlackPearl-Forum/Blackpearl-Link-Creator/master/links.py'
    latestFile = requests.get(updateURL)
    with open('links.py', 'wb') as script:
        script.write(latestFile.content)
    sys.exit("Script has been updated")


# Enable arg parser for bools and remote
parser = argparse.ArgumentParser(description='Get them infos')

parser.add_argument('--remote', '-r', type=str, default=None,
                    help='Set The Rclone Remote Path Ex: Gdrive:folder/path')
parser.add_argument('--hidereact', '-hr', default=False, action='store_true',
                    help='Use Hidereact BBCode With Link Output')
parser.add_argument('--downcloud', '-dc', default=False, action='store_true',
                    help='Use Downcloud BBCode With Link Output')
parser.add_argument('--nolinks', '-nl', default=False, action='store_true',
                    help='Print Out File Names Only')
parser.add_argument('--update', default=False, action='store_true',
                    help='Update Script To The Newest Version')

args = parser.parse_args()

if (args.update == True):
    Updater()

    # Check Remote string
path = input(
    "Input Your Rclone Remote: ") if args.remote is None else args.remote

# Runs RcloneList w/ path to grab all file names
files = RcloneList(path)

# Add arg.remote to beginning of every file name grabbed from RcloneList(path)
filesPath = [os.path.join(path, fl) for fl in files]

# Counter to list each iteration of variable "files" which is the file names
count = 0
hidebbcode = ["[Hidereact=1,2,3,4,5,6,7,8]",
              "[/hidereact]"] if args.hidereact is True else ["", ""]
downcloudBBcode = ["[Downcloud]",
                   "[/downcloud]"] if args.downcloud is True else ["", ""]
# makes ThreadPoolExecutor() run when we say executor
with ThreadPoolExecutor() as executor:
    # link in ThreadPoolExecutor().map() This creates a queue to push the
    # strings from filesPath to Def RcloneLink
    for result in executor.map(RcloneLink, filesPath):
        # use Count to grab each file name that is for each link print current
        # iteration in list
        print(files[count])
        count += 1
        # Print Link
        print(hidebbcode[0] + downcloudBBcode[0] +
              result + downcloudBBcode[1] + hidebbcode[1])
