# keyboard.zones[1].leds[0].set_color(RGBColor(0, 0, 0))
#from multiprocessing import Process, Array
#from pynput import keyboard as kb
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor# DeviceType, ZoneType
#from ctypes import c_bool


# config
FAST = False
accent, normal = RGBColor(255, 0, 0), RGBColor(0, 0, 255)
wave = RGBColor(0, 255, 0)
underglow = RGBColor(0, 0, 0)
total_keys = range(89)
secondary_keys = [
    0, 16, 33, 50, 64, # esc, tilda, tab, caps, lshift
    *range(5, 9), # f5-f8
    *range(13, 16), # prtsc, scrlk, pause
    *range(29, 33), # backspace, ins, home, pgup
    *range(47, 50), # del, end, pgdn
    63, 76, # enter, rshift
    *range(78, 81), # lctrl, win, lalt
    *range(82, 86), # ralt, fn, context, rctrl
    
]
accent_keys = [
    35, *range(51, 54), # WASD
    *range(56, 60), # HJKL
    77, *range(86, 89) # arrows
]
# 62 empty...



#keyboard.zones[0].set_colors([wave if False else c for i,c in enumerate(base)], fast=FAST)
def rgb_keyboard(col1, col2, col3, port):
    #print(col1, col2, col3, port)
    # init
    client = OpenRGBClient("127.0.0.1", port)
    #print("PORT: "+str(port))
    #print(client)
    keyboard = client.get_devices_by_name("K87")[0]
    keyboard.set_mode("direct")
    #mouse = client.get_devices_by_name("Razer Viper Mini")[0]
    #mouse.set_mode("direct")
    base = [accent if k in secondary_keys else normal for k in total_keys]

    # set
    keyboard.zones[1].set_color(underglow)
    keyboard.zones[0].set_colors([
        RGBColor.fromHEX(col1) if k in secondary_keys else \
        (RGBColor.fromHEX(col3) if k in accent_keys else RGBColor.fromHEX(col2)) \
        for k in total_keys], fast=FAST)

    # razer
    keyboard = client.get_devices_by_name("Razer Blade 15 (2021 Base)")[0]
    keyboard.set_mode("direct")
    keyboard.set_color(RGBColor.fromHEX(col3))
#mouse.set_color(accent, fast=FAST)

if __name__ == "__main__":
    rgb_keyboard("#ff0000", "#ffffff", "#00ff00")


# pressed = []
# def listener(k):
#    with keyboard.Listener(on_press=lambda x: k[ord(key.char)] = True,
#            on_release=lambda x: k[ord(key.char)] = False) as listener:
#        listener.join()

# def key_update(key, release=False):
#     global pressed
#     try:
#         key = ord(key.char)
#         if key not in pressed:
#             print(key)
#     except AttributeError:
#         print(key)
#     if release and key in pressed:
#         pressed.remove(key)
#     elif not key in pressed:
#         pressed.append(key)
#         print(pressed)
# 
# if __name__ == "__main__":
#     #keys_pressed = Array(c_bool, [False] * g
#     #p_listener = Process(target=listener, args=(keys_pressed))
#     #p_listener.start()
#     #p_listener.join()
#     listener = kb.Listener(on_press=lambda x: key_update(x, False),
#                            on_release=lambda x: key_update(x, True))
#     listener.start()
#     while True:
#         #print(pressed)
#         pass
