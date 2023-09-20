# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
import traverse

from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration


mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "firefox" # My browser of choice


def audio_device():
    output = subprocess.check_output("sh /home/bushy/.scripts/i3-sink-change/sink_change.sh --device", shell=True).decode("utf-8").strip()
    device, volume = output.split(' ')
    if device == 'Speaker':
        return f'{volume} - 🔈'
    elif device == "Headphone":
        return f'{volume} - 🎧'
    else:
        return f'{volume} - ?'

keys = [
        Key([], "XF86AudioMute", lazy.spawn("sh /home/bushy/.scripts/i3-sink-change/sink_change.sh --change")),
        Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%")),
        Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%")),
        Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
        Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
        Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
        Key([], "XF86AudioPause", lazy.spawn("playerctl play-pause")),
        
        Key([mod, "shift"], "s", lazy.spawn("sh -c 'import png:- | xclip -selection clipboard -t image/png'")),


         ### The essentials
         Key([mod], "T",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod], "D",
             lazy.spawn("rofi -show combi -modes combi -combi-modes 'filebrowser,run' -no-show-icons"),
             desc='Run Launcher'
             ),
         Key([mod], "F1",
             lazy.spawn(myBrowser),
             desc='Firefox'
             ),

         ### shortcuts 
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "Shift"], "Tab",
             lazy.prev_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Exit Qtile'
             ),

         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Treetab controls
          Key([mod, "shift"], "Left",
             lazy.layout.move_left(),
             desc='Move up a section in treetab'
         ),
         Key([mod, "shift"], "Right",
             lazy.layout.move_right(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
        Key([mod], "Down",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),

        Key([mod], "Up",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
      
        Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
        Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),

        Key([mod, "shift"], "up",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "down",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),

        Key([mod, "shift"], "Left",
             lazy.layout.shuffle_left(),
             lazy.layout.section_left(),
             desc='Move windows up in current stack'
             ),

        Key([mod, "shift"], "Right",
                 lazy.layout.shuffle_right(),
                 lazy.layout.section_right(),
             desc='Move windows up in current stack'
             ),

        Key([mod, "shift"], "u",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls

          Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         ### Emacs programs launched using the key chord CTRL+e followed by 'key'
        
]


keys.extend([
        Key([mod], 'up', lazy.function(traverse.up)),
        Key([mod], 'down', lazy.function(traverse.down)),
        Key([mod], 'left', lazy.function(traverse.left)),
        Key([mod], 'right', lazy.function(traverse.right)),
    ])

groups = [Group("1", layout='columns'),
          Group("2", layout='ratiotile', matches=[Match(wm_class=["Spotify","discord","steamwebhelper","crx_cifhbcnohmdccbgoicgdjpfamggdegmo","KeePassXC","Remmina"])]),
          Group("3", layout='monadtall'),
          Group("4", layout='monadtall'),
          Group("5", layout='monadtall'),
          Group("6", layout='monadtall')]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
#from libqtile.dgroups import simple_key_binder
#dgroups_key_binder = simple_key_binder("mod4")

### Switch groups
for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

colors = {
    'darker_background': ["#1c1f24", "#1c1f24"],
    'dark_background': ["#0b0d21", "#0b0d21"],
    'background': ["#989898", "#989898"],
    'light_background': ["#e0e0e0", "#e0e0e0"],
    'red': ["#ff4444", "#ff4444"],
    'green': ["#99cc00", "#99cc00"],
    'orange': ["#ff6600", "#ff6600"],
    'blue': ["#4866d8", "#4866d8"],
    'purple': ["#762ca7", "#762ca7"],
    'cyan': ["#18a7b5", "#33c5ba"],
    'light_purple': ["#c0b6e2", "#c0b6e2"]
}

layout_theme = {"border_width": 5,
                "margin": 0,
                "border_focus": colors['background'],
                "border_normal": colors['dark_background']
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(border_width=0),
    layout.RatioTile(**layout_theme),
    #layout.Stack(num_stacks=2,**layout_theme),
    # layout.TreeTab(
    #      font = "Ubuntu",
    #      fontsize = 10,
    #      sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
    #      section_fontsize = 10,
    #      border_width = 2,
    #      bg_color = "1c1f24",
    #      active_bg = "c678dd",
    #      active_fg = "000000",
    #      inactive_bg = "a9a1e1",
    #      inactive_fg = "1c1f24",
    #      padding_left = 0,
    #      padding_x = 0,
    #      padding_y = 5,
    #      section_top = 10,
    #      section_bottom = 20,
    #      level_shift = 8,
    #      vspace = 3,
    #      panel_width = 200
    #      ),
    layout.Floating(**layout_theme)
]


prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 13,
    padding = 2,
    background=colors['dark_background'],
    foreground=colors['light_background']
)
extension_defaults = widget_defaults.copy()



def init_widgets_list():
    widgets_list = [
            widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors['light_background'],
                       background = colors['dark_background']
                       ),

            widget.GroupBox(
                       font = "Ubuntu Bold",
                       hide_unused = True,
                       fontsize = 10,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 5,
                       highlight_method = "line",
                       this_current_screen_border = colors['red'],
                       this_screen_border = colors['red'],
                       other_current_screen_border = colors['green'],
                       other_screen_border = colors['green'],
                       foreground = colors['light_background'],
                       background = colors['dark_background'],
                      ),

            widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors['dark_background'],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),

            widget.WindowName(
                       foreground = colors['light_background'],
                       background = colors['dark_background'],
                       padding = 0,
                       ),



            widget.Spacer(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors['dark_background'],
                       background = colors['dark_background']
                       ),

            widget.GenPollText(
                update_interval=5,
                func=lambda: subprocess.check_output("python3 /home/bushy/.scripts/spotify.py",shell=True).decode("utf-8").strip(),
                mouse_callbacks = {
                    "Button1": lazy.spawn('playerctl next'),
                    },
                #background = colors['red'],
                decorations=[
                       BorderDecoration(
                           colour = colors['red'],
                           border_width = [0, 0, 2, 0],
                           padding_x = 0,
                           padding_y = None,
                            )
                        ]
            ),

            widget.Spacer(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors['dark_background'],
                       background = colors['dark_background']
                       ),
            widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors['dark_background'],
                       background = colors['dark_background']
                       ),


            widget.TextBox(
                       text = 'O',
                       font = "Ubuntu Mono",
                       background = colors['dark_background'],
                       foreground = colors['light_background'],
                       padding = 2,
                       fontsize = 16,
                        mouse_callbacks = {
                        # 1 - left click
                        # 2 - middle click
                        # 3 - right click
                        # 4 - scroll up
                        # 5 - scroll down
                        "Button1": lambda: subprocess.run("seq 2 | xargs -n 1 -P 2 sh -c 'ddcutil setvcp -d $1 10 0  --sleep-multiplier 0.3 --noverify'  sh",shell=True),
                        "Button2": lambda: subprocess.run("seq 2 | xargs -n 1 -P 2 sh -c 'ddcutil setvcp -d $1 10 25  --sleep-multiplier 0.3 --noverify'  sh",shell=True),
                        "Button3": lambda: subprocess.run("seq 2 | xargs -n 1 -P 2 sh -c 'ddcutil setvcp -d $1 10 50  --sleep-multiplier 0.3 --noverify'  sh",shell=True),

                        "Button4": lambda: subprocess.run("seq 2 | xargs -n 1 -P 2 sh -c 'ddcutil setvcp -d $1 10 + 25  --sleep-multiplier 0.3 --noverify'  sh",shell=True),
                        "Button5": lambda: subprocess.run("seq 2 | xargs -n 1 -P 2 sh -c 'ddcutil setvcp -d $1 10 - 25  --sleep-multiplier 0.3 --noverify'  sh",shell=True),
                        }
                       ),    
            widget.Systray(
                       background = colors['dark_background'],
                       foreground = colors['light_background'],
                       padding = 5,
                       icon_size = 16,

                       ),

            widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors['dark_background'],
                    background = colors['dark_background']
                    ),

            widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       #background = colors['dark_background'],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14,
                       ),

            widget.ThermalSensor(
                    update_interval=5,
                    foreground = colors['light_background'],
                    # background = colors['red'],
                    threshold = 90,
                    tag_sensor='Package id 0',
                    format = 'CPU: {temp:.0f}{unit}',
                    padding = 5,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                    decorations=[
                       BorderDecoration(
                           colour = colors['red'],
                           border_width = [0, 0, 2, 0],
                           padding_x = 5,
                           padding_y = None,
                            )
                        ]
                       
                       ),

            widget.Memory(
                measure_mem='M',
                update_interval=5,
                format="RAM: {MemUsed: .0f} MB",
                foreground = colors['light_background'],
                #background = colors['red'],
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                fmt = '{}',
                padding = 5,
                decorations=[
                   BorderDecoration(
                       colour = colors['red'],
                       border_width = [0, 0, 2, 0],
                       padding_x = 5,
                       padding_y = None,
                        )
                    ]
            ),

            widget.GenPollText(
                update_interval=1,
                func=lambda: audio_device(),
                mouse_callbacks = {'Button1': lambda: subprocess.check_output("sh /home/bushy/.scripts/i3-sink-change/sink_change.sh --change",shell=True)},
                foreground = colors['light_background'],
                #background = colors['red'],
                decorations=[
                       BorderDecoration(
                           colour = colors['red'],
                           border_width = [0, 0, 2, 0],
                           padding_x = 0,
                           padding_y = None,
                            )
                        ]
            ),
             
            widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       #background = colors['dark_background'],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14,
                       ),

            widget.CurrentLayout(
                foreground = colors['light_background'],
                # background = colors['dark_background'],
                padding = 5,
                decorations=[
                BorderDecoration(
                    colour = colors['red'],
                    border_width = [0, 0, 2, 0],
                    padding_x = 0,
                    padding_y = None,
                        )
                        ]
                       ),

            widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors['dark_background'],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),

            widget.Clock(
                       foreground = colors['light_background'],
                       # background = colors['red'],
                       format = "%a, %B %d - %H:%M",
                        decorations=[
                        BorderDecoration(
                            colour = colors['red'],
                            border_width = [0, 0, 2, 0],
                            padding_x = 0,
                            padding_y = None,
                        )
                        ]
                       ),

              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       #foreground = colors['dark_background'],
                       #background = colors['red']
                       ),
              ]

    return widgets_list


    print(device)

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    # del widgets_screen1[9:10]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    widgets_screen2 = widgets_screen2[0:4] + [widgets_screen2[-4]]
    return widgets_screen2               # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=30)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=30)),]
            # Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def autostart():
    autostart = [
        'xrandr --output HDMI-A-0 --rotate inverted',
        'xrandr --output "DisplayPort-0" --primary --mode 1920x1080 --rate 143.60',
        'setxkbmap -layout us -variant intl'
                  ]
    for cmd in autostart:
        subprocess.run(cmd, shell=True) 

# @hook.subscribe.layout_change
# def layout_changed(layout, group):
#     print(layout.name)
#     if layout.name == "max":
#         lazy.window.toggle_fullscreen()

#     elif layout.name != "max" and qtile.current_screen.top.margin == 0:
#         # Reset the margin for other layouts
#         qtile.current_screen.top.margin = 0
#         # Reconfigure the bar
#         qtile.current_screen.top._configure(qtile, qtile.current_screen)
#         # Redraw the layout
#         group.layout_all()

    #elif layout.name != "max" and qtile.current_screen.top.margin == 0:


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

