import os
from json import loads
from random import choice as rchoice
from subprocess import Popen
import moviepy.video.io.ImageSequenceClip as sequence
from time import sleep
from colors import wal
import cv2
from inspect import cleandoc
from pathlib import Path
from datetime import date as dt
from config import *
from shutil import copyfile

# TODO: double quote where necessary
home = os.path.expanduser("~")
cwd = os.getcwd()
if not os.path.isdir(data_path := home+"\\Appdata\\Local\\prisma"):
    os.mkdir(data_path)
cache = data_path+os.sep+"wallpaper.txt"


def get_playlist():
    with open(wal_engine+"\\config.json", encoding = 'cp850') as f:
        f = loads(f.read())
    f = list(f[list(f.keys())[1]]["general"]["playlists"])
    for p in f:
        if p["name"] == "Prisma":
            return [i[:i.rindex("/")]+"/project.json" for i in p["items"]]
    return []


def random_wal():
    wals = [i for i in os.listdir(wallpapers) if os.path.isfile(i) and not i.endswith(".mp4.png") \
            and not "_alt" in i and not i.startswith("!") and not i.endswith(".json")]
    chosen = rchoice(wals+get_playlist())
    #return wallpapers+"\\"+chosen if "\\" not in chosen else chosen
    return chosen.replace("/", "\\") if "/" in chosen else wallpapers+'\\'+chosen


def daily(cache=cache):
    choice = ""
    if os.path.isfile(cache):
        date, choice = Path(cache).read_text().split("|")
        if date != str(dt.today()):
            choice = ""
    if choice == "":
        choice = random_wal()
        with open(cache, "w") as cache:
            cache.write("|".join([str(dt.today()), choice]))
    return choice

update = lambda m, pj: Popen("\"%s\" -control openWallpaper -monitor %s -file \"%s\\project.json\"" % (wal_engine+"\\wallpaper32.exe", m, pj))
def run(args, cache=cache): 
    if args.reroll:
        os.remove(data_path+os.sep+"wallpaper.txt")
        args.input = daily()
    if not args.skip and not args.daemon:
        # TODO: assume path for pathless inputs using png/mp4=wallpapers and json=wal_engine/projects/myprojects
        if args.input.strip().endswith(".json"):
            thumb = (projectdir := args.input[:args.input.rindex("\\")])+"\\preview.png\""
            if not os.path.isfile(thumb.strip('\"')):
                thumb = '"'+thumb[:-4]+"gif\""
            if not os.path.isfile(thumb.strip('\"')):
                thumb = '"'+thumb[:-4]+"jpg\""
            update(0, projectdir) and update(1, projectdir)
        else:
            projectdir = wallpapers
            os.system("windows-wallpaper.exe %s\\!black.png" % wallpapers)
            os.system("taskkill /f /im wallpaper32.exe")
            sleep(1)
            wide, normal, thumb = args.input, args.input[:-4]+"_alt"+args.input[-4:], args.input+".png"
            if not os.path.exists(normal):
                normal = wide
            if wide.endswith(".png"): # replace with scene.pkg generation
                thumb = wide[:]
                sequence.ImageSequenceClip([wide], fps=1).write_videofile(wallpapers+"\\!wide.mp4")
                sequence.ImageSequenceClip([normal], fps=1).write_videofile(wallpapers+"\\!normal.mp4")
                wide, normal = "\\!wide.mp4", "\\!normal.mp4"
            template = Path("templates\\wallpaper_engine").read_text()
            with open(wallpapers+"\\project.json", "w") as fl:
                fl.write(template.replace("<FILE>", wide[wide.rindex("\\")+1:]).replace("<TITLE>", "wide"))
            update(0, projectdir)
            sleep(1)
            with open(wallpapers+"\\project.json", "w") as fl:
                fl.write(template.replace("<FILE>", normal[normal.rindex("\\")+1:]).replace("<TITLE>", "normal"))
            update(1, projectdir)
        wal(thumb) if os.path.isfile(thumb.strip('\"')) else print(thumb)
        if args.persistent:
            with open(cache, "w") as cache:
                cache.write("|".join([str(dt.today()), args.input]))
