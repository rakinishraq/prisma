# Prisma  
  
Prisma uses [pywal](https://github.com/dylanaraps/pywal/) to generate color schemes and apply them to Firefox (including websites), Discord, Obsidian, Alacritty, VS Code, WSL GTK/QT, etc. to match [animated](https://wallpaperengine.io) or static wallpapers. It can optionally choose new ones from your library everyday automatically as well.
  
Similar functionality can be found in Linux (using wpgtk), which was the inspiration for the Nyx series of tools. In it's current state, using this requires basic terminal skill.
  
Prisma is released under the [GNU General Public License v3.0](COPYING).
  
  
## Installation  
 
1. Install [ImageMagick](https://imagemagick.org/script/download.php#windows) while making sure "Add application directory to your system path" is enabled then restart your PC.
2. Click "prisma.exe" under Assets in the [Latest Release](https://github.com/rakinishraq/prisma/releases/latest) page to download.  
3. Run the exe once and wait a few seconds to extract resources and templates. Press Enter to exit.  
4. Run the exe again to generate a theme with your current Windows wallpaper.
5. Install any Integrations from the [Integrations section](https://github.com/rakinishraq/prisma#Integrations) right below.  

To make changes to the generated config file, like to enable animated wallpapers or some of the integrations below, use the following [Configuration section](https://github.com/rakinishraq/prisma#configuration).
  
  
## Integrations

- **Wallpaper Engine:** paid
- **Visual Studio Code:** Install the [extension](https://marketplace.visualstudio.com/items?itemName=dlasagno.wal-theme) and enable the theme in the Settings menu.  
- **Firefox/Thunderbird:** Install the Pywalfox [extension](https://addons.mozilla.org/en-US/firefox/addon/pywalfox/) and [application](https://github.com/Frewacom/pywalfox). The process for the latter may be complex for those new to Python/Pip. Tested with Librewolf.  
- **Obsidian:** The theme is temporarily not functional with the newest versions of the template theme, Minimal. When it is, add an entry of your Vault's location in the config file under "obsidian" like the [example config file](https://github.com/rakinishraq/prisma#Configuration) below.  
- **Disclaimer:** _Usage of BetterDiscord to apply themes is subject to user discretion and risk. It's important to note that custom clients are not permitted under Discord's Terms of Service and may result in user penalties, including account bans. As a developer, I bear no responsibility for any repercussions from using BetterDiscord. Please adhere to Discord's Terms of Service._
- **Discord:** If you agree to the above, install [BetterDiscord](https://betterdiscord.app/) and enable the theme in the Settings menu.
- **Neovim:** Use this [Neovim theme](https://github.com/AlphaTechnolog/pywal.nvim) for pywal support in WSL and potentially native Windows as well.
- **Alacritty:** An Alacritty configuration file is included but enabling it means you must make all edits in the templates file and run the tool to update. A line-replacing update method is in progress to prevent this.  
- **WSL GTK/QT:** Set the WSL variable as the name of your WSL OS name if you want [wpgtk](https://github.com/deviantfero/wpgtk) compatibility (more readable terminal color scheme as well as GTK/QT and other Linux GUI app theming). All Pywal supported apps should update automatically, too. If WSL is not installed, leave it empty.  
  - **Zathura:** Install and run [this script](https://github.com/GideonWolfe/Zathura-Pywal) within WSL to generate a new themed zathurarc file.
  - wpgtk depends on the imagemagick and ffmpeg packages
  - There's probably a similar process for many other Linux apps that sync with Linux's pywal theme files, which wpgtk generates. This was tested with GWSL on feh and zathura.
  
  
## Configuration  
  
Edit the new C:\Users\USER\AppData\Local\prisma\config.json file with any text editor. Example:
  
```  
{  
    "templates":  
    {  
        "alacritty.txt": "C:/Users/USER/AppData/Roaming/alacritty/alacritty.yml",  
        "discord.txt": "C:/Users/USER/AppData/Roaming/BetterDiscord/themes/pywal-discord-default.theme.css",  
        "obsidian.txt": "C:/Users/USER/Documents/Notes/.obsidian/themes/Minimal.css"  
    },  
  
    "wallpapers": "D:/Gallery/Wallpapers",  
  
    "wal_engine": "C:/Program Files (x86)/Steam/steamapps/common/Wallpaper Engine",  
    "monitors": ["2560x1080", "1920x1080"],  

    "wsl": "Manjaro"  
}  
```  

### Formatting
- Paths must use "/", not the usual Windows "\\".  
- Each line in the templates section is formatted with the template filename on the left and the target file to replace on the right.  
### Custom Templates
- They default templates (Alacritty, Discord and Obsidian) are located in the "templates" folder next to this config file.
- In the template files, {colorname} is replaced with the hex code for a color or a HSL/RGB component like {colorname.r} for Red.  
- The available color names are color0, color1...color15, background, foreground and cursor. The available components are Hue (0-360), Saturation (0%-100%), Lightness (0%-100%), Red (0-255), Green (0-255) and Blue (0-255).  
### Wallpaper Engine
- Set wal_engine to your Wallpaper Engine installation path. If left blank, Prisma will use win_wallpaper.exe as a fallback to set a single static wallpaper across all monitors (no animated or unique multi-monitor wallpaper support).  
- The monitors variable should contain all your monitors in the order they appear in Wallpaper Engine, represented by their resolutions (so if you have multiple with the same resolution, repeat it). This variable isn't used if Wallpaer Engine isn't installed.  
### Photo/Video Wallpapers
- The wallpapers path should contain photos and videos to be randomly selected from daily. If you want to use different files for different resolution monitors, append \_WIDTHxHEIGHT to the end of the filename (like painter\_1920x1080.png and painter\_2560x1080.png). This currently supports JPGs, PNGs and MP4s. Files starting with exclamation points and all subfolders are ignored.  
- You must include variants for all resolutions if using multiple files. Otherwise, name the single file regularly (like painter.png).  
  
  
  
  
## CLI Usage  
  
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


## Common Uses

- `.\prisma.exe` checks if there's already been a wallpaper saved today and loads it if it exists. Otherwise, it randomly picks one from your library (wallpapers/ and the Prisma Wallpaper Engine playlist) and saves it. Thus, if you placed the exe in C:\Users\USER\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup, you would automatically have a new theme everyday with no manual input (or make a shortcut to the location of the exe, recommended only after having tested it in a different folder manually a few times).  
- `.\prisma.exe -r -s` randomly picks a wallpaper from your library and saves it regardless of if one was already selected today. This is useful for skipping a daily wallpaper.  
- `.\prisma.exe -co` fetches your current Windows wallpaper image and generates a color scheme and themes from it. This is useful if you already have a wallpaper that you want to keep.  
- `.\prisma.exe filename.ext -s` sets all your wallpapers to that single file and saves it as today's wallpaper. Saving is useful for returning to today's selection after experimenting with other choices or refreshing the Wallpaper Engine project generation after restarting your PC.  
- `.\prisma.exe filename_2560x1080.ext filename_1920x1080.ext` sets different wallpapers for different wallpapers without saving. The number of inputs must be equal to the number of monitors if there's more than one input.   
  
  
  
## Credits (licenses distributed with project)  
  
- Discord template from [pywal-discord](https://github.com/FilipLitwora/pywal-discord) d12972d by FilipLitwora (GNU General Public License v3.0)  
  - changes: colors of theme subsituted in theme css file
  - stanadalone installer and alternate theme available [here](https://github.com/rakinishraq/pywal-discord)
- Obsidian template from [Minimal Obsidian](https://github.com/kepano/obsidian-minimal) 4.3.5 by kepano (MIT License)  
- fallback wallpaper binary from [win-wallpaper](https://github.com/sindresorhus/win-wallpaper) by sindresorhus (MIT License)  
- Alacritty template from [alacritty](https://github.com/alacritty/alacritty) by The Alacritty Project (Apache License, Version 2.0)  
  - changes: colors of tomorrow night theme subsituted in default config file
- color scheme file generation from [pywal](https://github.com/dylanaraps/pywal) module by Dylan Araps