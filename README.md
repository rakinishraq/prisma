# Prisma  
  
Prisma uses [pywal](https://github.com/dylanaraps/pywal/) to generate color schemes and apply them to Firefox (including websites), Discord, Obsidian, Alacritty, VS Code, WSL GTK/QT, etc. to match [animated](https://wallpaperengine.io) or static wallpapers. It can optionally choose new ones from your library everyday automatically as well.
  
This tool was inspired by wpgtk which provides similar functionality in Linux. In it's current state, using Prisma requires basic terminal skill.
  
Prisma is released under the [GNU General Public License v3.0](COPYING).
  - The author is not responsible for any damage, loss, or issues arising from the use or misuse of this GPL3 licensed software.  
The summary below is from [tl;drLegal](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3).
  - You may copy, distribute and modify the software as long as you track changes/dates in source files.
  - Any modifications to or software including (via compiler) GPL-licensed code must also be made available under the GPL along with build & install instructions.
  
  
## Installation  
 
1. Install [ImageMagick](https://imagemagick.org/script/download.php#windows) while making sure "Add application directory to your system path" is enabled then restart your PC.
2. Click "prisma.exe" under Assets in the [Latest Release](https://github.com/rakinishraq/prisma/releases/latest) page to download.  
3. Run the exe once and wait a few seconds to extract resources and templates. Press Enter to exit.  
4. Run the exe again to generate a theme with your current Windows wallpaper.
5. Install any Integrations from the [Integrations section](https://github.com/rakinishraq/prisma#Integrations) right below.  

To make changes to the generated config file, like to enable animated wallpapers or some of the integrations below, use the following [Configuration section](https://github.com/rakinishraq/prisma#configuration).

This is optional if you just want to generate colors for Discord from your static Windows wallpaper. However, Prisma is overkill for this use case so check out my fork of [pywal-discord](https://github.com/rakinishraq/pywal-discord).
  
  
## Integrations

- **OpenRGB:** An RGB perpipheral integration is in progress. Currently testing with the Wormier K87 ([SonixQMK firmware](https://sonixqmk.github.io//SonixDocs/compatible_kb/) supports many brands), Razer Blade 15 keyboard and Viper Mini. For now, iCue and Chroma support is available in Wallpaper Engine.
- **Visual Studio Code:** Install the [extension](https://marketplace.visualstudio.com/items?itemName=dlasagno.wal-theme) and enable the theme in the Settings menu.  
- **Websites:** Install the Dark Reader extension from the [Chrome Web Store](https://chrome.google.com/webstore/detail/dark-reader/eimadpbcbfnmbkopoojfekhnkhdbieeh) or [Firefox add-ons](https://addons.mozilla.org/en-US/firefox/addon/darkreader/). You can set the background and foreground colors in `See more options > Colors` section.  
  - Get the colors for these fields as detailed in the "And More!" integration below.  
  - An automation like Pywalfox's native messenger is in progress.
- **Firefox/Thunderbird:** Install the Pywalfox [extension](https://addons.mozilla.org/en-US/firefox/addon/pywalfox/) and [application](https://github.com/Frewacom/pywalfox). The process for the latter may be complex for those new to Python/Pip. Tested with Librewolf.  
- **Chrome:** Use [wal-to-crx](https://github.com/mike-u/wal-to-crx) to generate a theme file. Unfortunately, this process is not seamless like Pywalfox and untested.  
- **Obsidian:** Edit the entry of your Vault's location in the config file under "obsidian" like the [example config file](https://github.com/rakinishraq/prisma#Configuration) below. For unsupported themes, edit the BG/FG colors using the Style Settings plugin usually (details in the "And More!" integration below).  
- **Disclaimer:** _Usage of BetterDiscord to apply themes is subject to user discretion and risk. It's important to note that custom clients are not permitted under Discord's Terms of Service and may result in user penalties, including account bans. As a developer, I bear no responsibility for any repercussions from using BetterDiscord or any other custom client. Please adhere to Discord's Terms of Service._
- **Discord:** If you agree to the above, install [BetterDiscord](https://betterdiscord.app/) and enable the theme in the Settings menu.
  - Standalone installer and alternate theme available [here](https://github.com/rakinishraq/pywal-discord).
- **Neovim:** Use this [Neovim theme](https://github.com/AlphaTechnolog/pywal.nvim) for pywal support in WSL and potentially native Windows as well.
- **Windows 10/11 Theme:** The color scheme of Windows can be set to automatically adapt in `Settings > Colors > Accent color (set to Automatic)`.
- **Alacritty:** An Alacritty configuration file is included but enabling it means you must make all edits in the templates file and run the tool to update. A line-replacing update method is in progress to prevent this.  
- **Wallpaper Engine:** This paid tool is used for animated (sometimes interactive and audio-reactive) wallpapers as well as setting seperate image wallpapers per monitor automatically. See the last two parts of the [Configuration section](https://github.com/rakinishraq/prisma#configuration).
  - **Disclaimer:** _There are dangerous amounts of anime and NSFW content in the Wallpaper Engine workshop. As a developer, I bear no responsibility for any potential loss of brain cells. Proceed with caution._
  - **"Prisma" Playlist:** Save all your Wallpaper Engine favorites into a playlist named "Prisma" and the random/daily functions will add them to the random choice pool/collective library.
  - **Wallpaper folder:** Use a folder of photo/video sets of wallpapers for different monitor resolutions. For video files, the first frame is used for scheme generation and used with a skeleton WE project. For images, they're converted into full WE projects.
    - Do not add these to Prisma playlist as they are replaced and this folder's contents are part of the random choice pool already.
- **WSL GTK/QT:** Set the WSL variable as the name of your WSL OS name if you want [wpgtk](https://github.com/deviantfero/wpgtk) compatibility (more readable terminal color scheme as well as GTK/QT and other Linux GUI app theming). All Pywal supported apps should update automatically, too. If WSL is not installed, leave it empty.  
  - **Zathura:** Install and run [this script](https://github.com/GideonWolfe/Zathura-Pywal) within WSL to generate a new themed zathurarc file.
  - There's probably a similar process for many other Linux apps that sync with Linux's pywal theme files, which wpgtk generates. This was tested with GWSL on feh and zathura.
  - wpgtk depends on the imagemagick and ffmpeg packages
- **And More!** The background and foreground colors are shown in the command line output and the full color scheme is available in `C:/Users/USER/.cache/wal/colors.json` to manually input in any app.
  
  
## Configuration  
  
Edit the new C:/Users/USER/AppData/Local/prisma/config.json file with any text editor. Example:
  
```  
{  
    "templates":  
    {  
        "alacritty.txt": "C:/Users/USER/AppData/Roaming/alacritty/alacritty.yml",  
        "discord.txt": "C:/Users/USER/AppData/Roaming/BetterDiscord/themes/pywal-discord-default.theme.css",  
        "obsidian.txt": "C:/Users/USER/Documents/Notes/.obsidian/themes/pywal.css"  
    },  
  
    "wallpapers": "D:/Gallery/Wallpapers",  
  
    "wal_engine": "C:/Program Files (x86)/Steam/steamapps/common/wallpaper_engine",
    "wal_engine_black": false,  
    "monitors": ["2560x1080", "1920x1080"],  

    "wsl": "Manjaro"  
}  
```  

### Formatting
- Paths must use "/", not the usual Windows "\\".  
- Each line in the templates section is formatted with the template filename on the left and the target file to replace on the right.  
- Every line except the last one must end with a comma, including within curly brackets.
### Custom Templates
- They default templates (Alacritty, Discord and Obsidian) are located in the "templates" folder next to this config file.
- In the template files, {colorname} is replaced with the hex code for a color or a HSL/RGB component like {colorname.r} for Red.  
- The available color names are color0, color1...color15, background, foreground and cursor. The available components are Hue (0-360), Saturation (0%-100%), Lightness (0%-100%), Red (0-255), Green (0-255) and Blue (0-255).  
### Wallpaper Engine
- The provided value in the config above is the default installation path if purchased from Steam.
- Set wal_engine to your Wallpaper Engine installation path. If left blank, Prisma will use win_wallpaper.exe as a fallback to set a single static wallpaper across all monitors (no animated or unique multi-monitor wallpaper support without Wallpaper Engine).  
- The monitors variable should contain all your monitors in the order they appear in Wallpaper Engine, represented by their resolutions (so if you have multiple with the same resolution, repeat it). This variable isn't used if Wallpaper Engine isn't installed.  
- This tool sets the wallpaper behind Wallpaper Engine as all-black if "wal_engine_black" is enabled. This is to prevent a different wallpaper showing before Wallpaper Engine has time to start. An alternative is in progress since this (a) causes Window's automatic accent color (details in the "Windows 10/11 Theme" integration below) to be all-black and (b) running the tool again sets the template-based schemes as all-black. If you want ot enable this option:
  1. For now, use the "Start with Windows in High Priority" and "Adjust Windows color" options in Wallpaper Engine's General tab in Settings to combat the former issue.  
  2. To prevent the latter issue, use the "--save" argument and "saved" variables (further details in the [CLI Usage section](https://github.com/rakinishraq/prisma#cli-usage) below) or only run once.  
### Photo/Video Wallpapers
- The wallpapers path should contain photos and videos to be randomly selected from daily. If you want to use different files for different resolution monitors, append \_WIDTHxHEIGHT to the end of the filename (like painter\_1920x1080.png and painter\_2560x1080.png).
- JPGs, PNGs and MP4s are currently supported. More details in the [Common Uses section](https://github.com/rakinishraq/prisma#common-uses) below.  
- You must include variants for all resolutions of your different monitors if using multiple files. Otherwise, name the single file regularly (like painter.png).  
- Any files with a "!" at the start will be ignored.
- If you don't want to use Wallpaper Engine but want to set seperate image wallpapers per monitor, you'd need to manually do so in the Windows settings. This seems to be a limitation not with the wallpaper binary but with Windows' command line abilities. However, you can easily use the "--colors-only" argument after.  
  
  
  
## CLI Usage  
  

```
Generates color scheme from animated (Wallpaper Engine) or static (Windows) wallpapers and applies 
to templates. Defaults to --colors-only if no arguments provided.

positional arguments:
  input                 Input image/video/project.json file or "saved" keyword.

options:
  -h, --help            show this help message and exit
  -r, --random          load random wallpaper; input file is then ignored
  -s, --save            save inputs as wallpaper set; retrieve with "saved" keyword
  -co, --colors-only    ignores all other inputs and sets colors with current Windows wallpaper
  -d, --daily           select a random wallpaper if new day and save it
  -p PORT, --port PORT  port for OpenRGB communication (default is 6742)
```


## Common Uses

- `.\prisma.exe -co` fetches your current Windows wallpaper image and generates a color scheme and themes from it. This is useful if you already have a wallpaper that you want to keep.  
- `.\prisma.exe` is the same as `.\prisma.exe -co`
- `.\prisma.exe -d` checks if there's already been a wallpaper saved today and loads it if it exists. Otherwise, it randomly picks one from your library (wallpapers folder and the Prisma Wallpaper Engine playlist) then then save it.
- `.\prisma.exe -r -s` randomly picks a wallpaper from your library and saves it regardless of if one was already selected today.  
- `.\prisma.exe filename.ext -s` sets all your wallpapers to that single file and saves it as today's wallpaper. Saving is useful for returning to today's selection after experimenting with other choices.  
- `.\prisma.exe saved` retrieves your saved wallpaper regardless of how long ago you saved it. This is useful for reverting your wallpaper/color schemes after experimenting with other choices.
- `.\prisma.exe filename_2560x1080.ext filename_1920x1080.ext` sets different wallpapers for different wallpapers without saving. The number of inputs must be equal to the number of monitors if there's more than one input.   

For example, if you want to just set all your themes as the wallpaper you have (non-Wallpaper Engine), then simply run the exe or execute `.\prisma.exe` in the command line.

If you want to get a new wallpaper automatically everyday, run `.\prisma.exe -d` at startup. One way to do this is:  
1. Click Windows+R and enter `shell:startup` to open your Startup folder.
2. Right-click an empty area in this folder, hover over New and click Shortcut.
3. Enter `<path to prisma>\prisma.exe -d`, press Next, enter any name and click Finish.

Note: Since Prisma will open Wallpaper Engine if it's not already running, enabling "Start with Windows" in it's Settings is optional. It will just reduce the time you see the static Windows wallpaper running underneath it.

  

## Build Instructions

This is an optional section for those who want to modify the code and execute using a virtual environment:
1. Clone the repo then open a terminal session in the folder or use `cd <path-to-Prisma>/Prisma`
   - For the former, shift-right click in an empty area in the folder, click Open Powershell window here 
2. Execute `python -m venv .venv` to create a virtual environment
3. Install all the required modules with `./.venv/Scripts/pip.exe install -r requirements.txt`
4. To run from source: Execute `./LAUNCH.ps1 <arguments>` or `./.venv/Scripts/python.exe main.py <ARGUMENTS>`
5. To build into .exe: Execute `./COMPILE.ps1` or `./.venv/Scripts/pyinstaller --noconfirm --onefile --console --name "Prisma" --clean --add-data "./resources;resources/" "./main.py"`
  
  
## Credits  
  
The respective licenses are in the [repo resources folder](https://github.com/rakinishraq/prisma/tree/main/resources/licenses) and copied into the Local Appdata folder.

- Discord template from [pywal-discord](https://github.com/FilipLitwora/pywal-discord) d12972d by FilipLitwora (GNU General Public License v3.0)  
  - changes: colors of theme subsituted in theme css file
- Obsidian template from [pywal-obsidianmd](https://github.com/poach3r/pywal-obsidianmd) by poach3r (unlicensed)  
  - changed formatting and some background colors
- fallback wallpaper binary from [win-wallpaper](https://github.com/sindresorhus/win-wallpaper) by sindresorhus (MIT License)  
- Alacritty template from [alacritty](https://github.com/alacritty/alacritty) by The Alacritty Project (Apache License, Version 2.0)  
  - changes: colors of tomorrow night theme subsituted in default config file
- color scheme file generation from [pywal](https://github.com/dylanaraps/pywal) module by Dylan Araps