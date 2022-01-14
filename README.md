# Prisma  
  
Prisma uses [pywal](https://github.com/dylanaraps/pywal/) to generate color schemes and apply them to Discord, Obsidian, Alacritty, etc. to match Wallpaper Engine animated wallpapers or static Windows wallpapers. It can automatically choose new ones from your library everyday.  
  
In it's current state, Prisma requires basic terminal skill. If you'd rather use a GUI, Nyx is coming soon and will contain graphical installers and settings for Linux-like tools/WSL.  
  
  
## General Usage  
  
```  
usage: prisma.exe [-h] [-r] [-s] [-co] [input ...]  
  
Generates color scheme and applies to templates. If no inputs are provided: a  
new wallpaper is selected daily and saved (generates colors from the currently  
set Windows wallpaper if Wallpaper Engine isn't set)  
  
positional arguments:  
  input               Input image/video/project.json file. Defaults to today's  
                      wallpaper.  
  
optional arguments:  
  -h, --help          show this help message and exit  
  -r, --random        Load random wallpaper. Input file is then ignored.  
  -s, --save          Save input as today's wallpaper.  
  -co, --colors-only  Ignores all other inputs and sets colors with main  
                      monitor's picture wallpaper.  
```  
  
  
## Configuration  
  
Run the program once then edit C:\Users\USER\AppData\Local\prisma\config.json with any text editor. Here's mine for example.  
  
```  
{  
    "templates":  
    {  
        "alacritty": "C:/Users/USER/AppData/Roaming/alacritty/alacritty.yml",  
        "discord": "C:/Users/USER/AppData/Roaming/BetterDiscord/themes/pywal-discord-default.theme.css",  
        "obsidian": "C:/Projects/Notes/.obsidian/themes/Minimal.css"  
    },  
    "wsl": "Manjaro",  
  
    "wallpapers": "E:/Gallery/Wallpapers",  
  
    "wal_engine": "C:/Program Files (x86)/Steam/steamapps/common/Wallpaper Engine",  
    "monitors": ["2560x1080", "1920x1080"]  
}  
```  
  
- Paths must use "/", not the usual Windows "\".  
- Each line in the templates section is formatted with the template filename on the left (stored in the templates folder next to config.json) and the target file to replace on the right.  
- Alacritty and Obsidian templates are included by default but aren't added to the config file since the Alacritty template will override your existing config if it exists and the Obsidian theme location depends on your Vault's location.  
- In the template files, {colorname} is replaced with the hex code for a color or a HSL/RGB component like {colorname.r} for Red.  
- The available color names are color0, color1...color15, background, foreground and cursor. The available components are Hue (0-360), Saturation (0%-100%), Lightness (0%-100%), Red (0-255), Green (0-255) and Blue (0-255).  
- Set the WSL variable as the name of your WSL OS name if you want [wpgtk](https://github.com/deviantfero/wpgtk) compatibility (more readable color schemes as well as GTK/QT and other Linux GUI app theming). If WSL is not installed, leave it empty.  
- The wallpapers path should contain photos and videos to be randomly selected from daily. If you want to use different files for different resolution monitors, append \_WIDTHxHEIGHT to the end of the filename (like painter\_1920x1080.png and painter\_2560x1080.png). This currently supports JPGs, PNGs and MP4s. Files starting with exclamation points and all subfolders are ignored.  
- You must include variants for all resolutions if using multiple files. Otherwise, name the single file regularly (like painter.png).  
- Set wal_engine to your Wallpaper Engine installation path. If left blank, Prisma will use win_wallpaper.exe as a fallback to set a single static wallpaper across all monitors (no animated or unique multi-monitor wallpaper support).  
- The monitors variable should contain all your monitors in the order they appear in Wallpaper Engine, represented by their resolutions (so if you have multiple with the same resolution, repeat it). This variable is optional if Wallpaer Engine isn't installed.  
  
  
## "Installation"  
  
1. Click Prisma.exe under Assets in the [Latest Release](https://github.com/rakinishraq/prisma/releases/latest) page to download.  
  
  
## Common Uses  
  
- `.\prisma.exe` checks if there's already been a wallpaper saved today and loads it if it exists. Otherwise, it randomly picks one from your library (wallpapers/ and the Prisma Wallpaper Engine playlist) and saves it. Thus, if you placed the exe in C:\Users\USER\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup, you would automatically have a new theme everyday with no manual input (or make a shortcut to the location of the exe, recommended only after having tested it in a different folder manually a few times).  
- `.\prisma.exe -r -s` randomly picks a wallpaper from your library and saves it regardless of if one was already selected today. This is useful for skipping a daily wallpaper.  
- `.\prisma.exe -co` fetches your current Windows wallpaper image and generates a color scheme and themes from it. This is useful if you already have a wallpaper that you want to keep.  
- `.\prisma.exe filename.ext -s` sets all your wallpapers to that single file and saves it as today's wallpaper. Saving is useful for returning to today's selection after experimenting with other choices or refreshing the Wallpaper Engine project generation after restarting your PC.  
- `.\prisma.exe filename_2560x1080.ext filename_1920x1080.ext` sets different wallpapers for different wallpapers without saving. The number of inputs must be equal to the number of monitors if there's more than one input.   
  
  
## Advanced Use Requirements  
  
### WSL and Running from Source  
 -  imagemagick  
 -  python 3.x (pip install pywal wpgtk)  
 -  ffmpeg  
  
### Run from Source  
 -  python 3.x (pip install -r requirements.txt)  
  
  
## Planned Features  
   
- [ ] README demonstration visuals
- [ ] requirements.txt (venv)  
- [ ] alacritty template cleanup
- [ ] list choices flag/implicit paths  
- [ ] handle unsupported encoding in names  
- [ ] debug messages  
- [ ] cache files w/ custom fields  
- [ ] wpgtk symlink  
- [ ] tests/test fresh installs  
- [ ] light mode flag  
- [ ] distribution (gh actions?)  
- [ ] openrgb and firefox support  
- [ ] silence pywal's imagemagick  
  
  
## License  
  
Prisma is released under the [GNU General Public License v3.0](COPYING).  
  
  
## Credits  
  
- Discord template from pywal-discord d12972d by FilipLitwora (GNU General Public License v3.0)  
- Obsidian template from Minimal Obsidian 4.3.5 by kepano (MIT License)  
- fallback wallpaper binary from win-wallpaper by sindresorhus (MIT License)  
- Alacritty template from alacritty by The Alacritty Project (Apache License, Version 2.0)  
