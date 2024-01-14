import argparse
from colorsys import rgb_to_hls
from re import search as re
import pywal.backends.wal
from time import sleep
from subprocess import Popen, check_output, DEVNULL, CalledProcessError
from random import choice as rchoice
from json import loads, dumps
from os import path, mkdir, listdir, remove
import sys
from datetime import date as dt
import pywal
import cv2
import moviepy.video.io.ImageSequenceClip as sequence
from shutil import rmtree, copytree, copy
#from rgb import rgb_keyboard

home = path.expanduser("~").replace("\\", "/")
data_path = home+"/AppData/Local/prisma"
cache_path = data_path+"/wallpaper.txt"
config_path = data_path+"/config.json"
template_path = data_path+"/templates"
licenses_path = data_path+"/licenses"
tmp_path = home+"/AppData/Local/Temp"
batch_path = tmp_path+"/wallpaper.bat"
config = {}

pic_ext = ["png", "jpg"]
vid_ext = ["mp4"]

# silently run command
cmd = lambda c,out=DEVNULL: Popen(c, stderr=DEVNULL, stdout=out, shell=True).wait()
# set Windows wallpaper using fallback binary
fallpaper = lambda f: Popen(["powershell.exe", "&",
    '\"'+resource("wallpaper.exe")+'"', '"'+f+'"'], stderr=DEVNULL)
# convert path to Linux format for WPG
convert = lambda i: "/mnt/"+i[0].lower()+i[2:].replace("\\", "/")


def fatal(msg, parser=None):
    """Prints message then ends program"""
    print(msg+'\n')
    if parser: # print parser help message
        parser.print_help()
    sys.exit(2)


def resource(relative_path):
    """Get absolute path to resource for dev/PyInstaller"""
    try: # PyInstaller temp folder
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = path.abspath(".")
    return "/".join([base_path, "resources", relative_path])


class Parser(argparse.ArgumentParser):
    """Show help menu on argparse error"""
    def error(self, message):
        fatal("error: "+message, self)


def random_wal():
    """Randomly chooses set from "wallpapers" folder and
    "Prisma" Wallpaper Engine playlist.

    Returns (list): wallpaper paths"""

    choices = []
    
    # wallpapers without *.json, !*, double extensions or directories
    if path.exists(config["wallpapers"]):
        wals = []
        for i in listdir(config["wallpapers"]):
            if path.isfile(config["wallpapers"]+'/'+i) and \
                    i.count('.')==1 and not i.startswith("!") and \
                    i[i.rindex(".")+1:] in pic_ext+vid_ext:
                wals.append(i)
        # remove duplicates and resolution/extension suffix
        for i in wals:
            if re(r".*\d*x\d*\..*", i):
                choices.append(i[:i.rindex("_")])
            else:
                choices.append(i[:i.rindex(".")])
        choices = list(dict.fromkeys(choices))

    # get project.json files for prisma playlist items
    if config["wal_engine"]:
        with open(config["wal_engine"]+"/config.json", encoding='cp850') as f:
            f = loads(f.read())
        for u in f.values():
            try:
                for p in u["general"]["playlists"]:
                    if p["name"] == "Prisma":
                        for i in p["items"]:
                            choices.append(i[:i.rindex("/")]+"/project.json")
                        break
            except TypeError:
                pass
            except KeyError:
                pass

    if not choices:
        fatal("No entries in Wallpaper Engine playlist or Wallpaper folder found.")
    choice = rchoice(choices) # choose randomly

    ret = [choice] * len(config["monitors"])
    if not "/" in choice: # is "wallpapers/" item
        for w in wals:
            if not w.startswith(choice+"_"):
                continue
            for i in range(len(config["monitors"])):
                if config["monitors"][i] in w:
                    ret[i] = config["wallpapers"]+'/'+w
            if not choice in ret: # if all resolution variants found
                break
        else: # fallback to non-variant
            for w in wals:
                if w.startswith(choice+"."):
                    ret = [config["wallpapers"]+"/"+w] * \
                        len(config["monitors"])
                    break
    return ret


def daily():
    """Fetches wallpapers from cache if it was updated today
    otherwise randomly choose one.

    Returns (list): wallpaper paths
    """
    choice = ""
    if path.isfile(cache_path):
        with open(cache_path) as c:
            date, *choice = c.read().split("|")
        if date != str(dt.today()):
            choice = ""
    if choice == "":
        choice = random_wal()
    return choice


def gen_colors(img):
    """Generates color scheme from image and applies to templates.

    Parameters:
        img (string): path leading to input image
    """
    
    # get/create color scheme
    # TODO: add json with custom fields for openrgb
    wal = pywal.colors.colors_to_dict(
            pywal.colors.saturate_colors(
                getattr(sys.modules["pywal.backends.wal"], "get")(img, False),
                ""), img)
    print("Generated Windows pywal colors.json")

    # pywalfox update
    print("Full color scheme in: " + (json_path := home+"/.cache/wal/colors.json"))
    with open(json_path, "w") as cj:
        print("Updated pywal's colors.json path format for Pywalfox")
        cj.write(dumps(wal, indent=4))
    try:
        Popen(["python", "-m", "pywalfox", "update"])
        print("Pywalfox updated")
    except Exception:
        print("Pywalfox not updated")

    # process color scheme
    wal["colors"].update(wal["special"])
    wal = wal["colors"]
    print("Processed color scheme")
    print("\n\tBackground: %s\n\tForeground: %s\n" % (wal["background"], wal["foreground"]))

    # OpenRGB
    try:
        #rgb_keyboard(wal["foreground"], wal["background"], wal["color4"], port)
        #print("Applied OpenRGB colors")
        print("OpenRGB integration temporarily disabled")
    except Exception as e:
        print("OpenRGB error: " + str(e))

    # WSL / wpgtk
    if config["wsl"]: # wpgtk
        wsl = "wsl -d " + config["wsl"]
        cmd(wsl + " -- wpg -s \"%s\"" % (img := convert(img)))
        img = img.replace("/", "_").replace(" ", "\\ ")
        Popen(wsl + " -- rm ~/.config/wpg/schemes/" + img[:img.rfind('.')] + '*')


    # apply templates
    for (base_name,output) in config["templates"].items():
        if not path.exists(template := (template_path+'/'+base_name)):
            print("Skipped %s template (either template file or output folder is missing)" % base_name)
            print(path.exists(output[output.rindex('/'):]))
            continue
        with open(template, encoding='cp850') as base:
            base = base.read()
            for k in wal.keys():
                # process replacement of base, ex. {color0}
                base = base.replace("{%s}"%k, wal[k])
                if '{'+k+'.' in base:
                    # process replacement of component, ex. {color0.r}/{color0.h}
                    rgb = tuple(int(wal[k].strip("#")[i:i+2], 16) for i in (0, 2, 4))
                    hls = rgb_to_hls(*[j/255.0 for j in rgb])
                    hls = [str(hls[i]*100)+"%" if i > 0 else hls[i]*360 for i in range(3)]
                    for c in range(3):
                        base = base.replace("{%s.%s}" % (k, "rgb"[c]), str(rgb[c]))
                        base = base.replace("{%s.%s}" % (k, "hls"[c]), str(hls[c]))
            with open(output, "w", encoding='cp850') as output:
                output.write(base)
        print("Applied %s template" % base_name)


def wal_engine(wals):
    """Apply wallpapers to Wallpaper Engine and pass first one's
    file/still/thumbnail path to gen_colors()
    """

    print("\n\t".join(["Selected wallpapers:"]+wals))
    img = None
    if config["wal_engine_black"]: fallpaper(resource("black.png"))
    cmd("taskkill /im wallpaper32.exe")

    for w in range(len(wals)):
        wal = path.abspath(wals[w])
        parent, filename = wal.rsplit('\\', 1)
        source = None

        # video
        if wal.endswith(vid_ext):
            source = filename
            if w == 0: # extract first frame
                vidcap = cv2.VideoCapture(wal)
                success, image = vidcap.read()
                if success:
                    cv2.imwrite(img := wals[0]+".png", image)
                else:
                    fatal("Video cannot be read: "+wals[0])
            project = config["wallpapers"]+"/project.json"

        # picture
        elif wal.endswith(pic_ext):
            if w == 0:
                img = wals[0]
            rand = str(rchoice(range(100)))
            folder = tmp_path+"/picture/"+rand
            copytree(resource("project_template"), folder) # duplicate project
            copy(wal, folder+"/materials/picture.png") # TODO: jpg/bmp
            _h, _w, _ = cv2.imread(wal).shape
            with open(folder+"/scene.json", "r+") as f: # modify scene.json
                t = f.read().replace("W2", str(_w/2)).replace("H2", str(_h/2))
                f.seek(0)
                f.write(t.replace("W", str(_w)).replace("H", str(_h)))
                f.truncate()
            project = folder+"/project.json"
        
        # wallpaper engine
        else:
            if w == 0:
                img = parent+"/thumbnail.png"
                if not path.exists(img):
                    for ext in pic_ext+["gif"]:
                        if path.exists(img := parent+"/preview."+ext):
                            break
                    else:
                        fatal("No image found for: "+wal)
                print("Using image for color scheme: "+img.replace('\\', '/'))
            project = wal


        if not path.exists(project): # temporary project.json for video
            with open(resource("project_template.json")) as t:
                t = t.read()
            with open(project, "w") as p:
                p.write(t.replace("FILE", source))

        if img: # set colors
            gen_colors(img)
            img = None
        
        print("\nWallpaper Engine: Setting wallpaper for monitor ", w)
        _c = ['"'+config["wal_engine"]+"/wallpaper32.exe\"", "-control", "openWallpaper",
              "-monitor", str(w), "-file", '"'+project+'"']
        with open(batch_path, "w") as bf:
            bf.write(' '.join(_c))
        Popen(["cmd", "/c", batch_path])
        sleep(3)
        print("Done")
        if source: # delete temp project.json for video
            remove(project)



def main(test_args=None, test_config=None):
    """Process flags and inputs."""

    # check if imagemagick installed to path
    try:
        check_output(["where", "magick"])
    except CalledProcessError:
        try:
            check_output(["where", "montage"])
        except CalledProcessError:
            fatal("Imagemagick isn't installed to system path. Check README.")


    global config
    if not test_config:
        # make data folder and config if not exist
        if not path.isdir(data_path):
            mkdir(data_path)
        if not path.isdir(template_path):
            copytree(resource("templates"), template_path)
        if not path.isdir(licenses_path):
            copytree(resource("licenses"), licenses_path)
        if not path.isfile(config_path):
            with open(resource("config_template.json")) as c:
                config_content = c.read().replace("HOME", home)
            with open(config_path, "w") as c:
                c.write(config_content)
            print("Config file created in %s.\n"
                  "Edit if desired then run this tool again.\n" % config_path)
            input("Press Enter to exit.")
        else:
            with open(config_path) as c:
                config_content = c.read()
        config = loads(config_content)
        # TODO: config validity checks
    else:
        config = test_config

    # parse arguments
    parser = Parser()
    parser.description = "Generates color scheme from animated (Wallpaper Engine) or static" \
        "(Windows) wallpapers and applies to templates.\nDefaults to --colors-only if no arguments provided."
    parser.add_argument("-r", "--random", action="store_true",
            help="load random wallpaper; input file is then ignored")
    parser.add_argument("-s", "--save", action="store_true",
            help="save inputs as wallpaper set; retrieve with \"saved\" keyword")
    parser.add_argument("input", default=[], nargs="*",
            help="input image/video/project.json file or \"saved\" keyword")
    parser.add_argument("-co", "--colors-only", action="store_true",
            help="ignores all other inputs and sets colors with "
                "current Windows wallpaper")
    parser.add_argument("-d", "--daily", action="store_true",
            help="select a random wallpaper if new day and save it")
    parser.add_argument("-p", "--port", type=int, default=6742,
            help="port for OpenRGB communication (default is 6742)")
    args = parser.parse_args(test_args)

    # handle arguments
    inputs = [s.replace("\\", "/").strip() for s in args.input]
    if "saved" in inputs: # retrieve saved
        if path.isfile(cache_path):
            with open(cache_path) as c:
                _, *inputs = c.read().split("|")
    current_wal = home+"/AppData/Roaming/Microsoft/Windows/Themes/TranscodedWallpaper"
    if args.colors_only: # if colors_only, ignore all other args
        gen_colors(current_wal)
        fatal("Done.")
    elif args.random: # if colors_only false and random true, ignore all other args
        inputs = random_wal()
    elif args.daily: # if colors_only/random false, ignore all other args
        inputs = daily()
        args.save = True
    elif not inputs: # no args and no inputs = same as colors_only
        gen_colors(current_wal)
        fatal("Done.")
    else: # no args, only inputs
        for fl in inputs:
            # supports all entries in pic_ext,vid_ext and .json if using WE
            ext = fl[fl.rfind(".")+1:]
            if not path.isfile(fl): # file exists?
                fatal("Invalid file input: " + fl, parser)
            elif ext in vid_ext+["json"] and not config["wal_engine"]: # WE installed?
                fatal("Wallpaper Engine needs to be configured for video/live inputs.")
            elif not ext in pic_ext+vid_ext+["json"]: # file supported?
                fatal("Unsupported file input: " + fl, parser)

    # create/clear temp directory
    if path.isdir(rm := tmp_path+"/picture"):
        for i in listdir(rm):
            rmtree(rm+'/'+i)
    else:
        mkdir(rm)
    
    # process inputs
    if len(inputs) == 1:
        if config["wal_engine"]:
            inputs *= len(config["monitors"])
            wal_engine(inputs)
        else:
            print("Using fallback wallpaper binary")
            fallpaper(inputs[0])
            gen_colors(inputs[0])
    else:
        if not config["wal_engine"]:
            fatal("Wallpaper Engine required for multiple inputs.", parser)
        if len(inputs) != len(config["monitors"]):
            fatal("Input one wallpaper or equal to number of monitors.", parser)
        wal_engine(inputs)

    # save
    if args.save:
        if not args.colors_only and inputs or args.daily:
            with open(cache_path, "w") as c:
                c.write("|".join([str(dt.today())]+inputs))
            print("Saved wallpapers to: "+cache_path)
        else:
            print("Save flag ignored in this case")
    
    exit()

if __name__ == "__main__":
    main()