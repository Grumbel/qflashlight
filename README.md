QFlashlight
===========

QFlashlight is a simple Qt application that will fill the whole screen
with a solid color. The color can be selected via command line with
`--color` optional or interactively via the color picker (press 'C').
Fullscreen can be entered and left with a double click. The mouse
cursor can be hidden by pressing 'M'.

The app can also run as a borderless window and blackout only a
smaller portion of the screen.

Additionally the app can also display a text inside the window. The
text can either be static or be the output of a program that it
refreshed at regular intervals, which can be used to get `watch`-like
functionality, e.g. to display the current date and time use:

    qflashlight -C date -n 1


Usage
-----

    usage: qflashlight [-h] [-c COLOR] [-T COLOR] [-F FONT] [-t TEXT] [-C CMD]
                       [-n SECONDS] [-w] [-m] [-b] [-g WxH+X+Y]
                       [FILE]

    QFlashlight - Fill the screen with a solid color

    positional arguments:
      FILE

    optional arguments:
      -h, --help            show this help message and exit

    Style:
      -c COLOR, --color COLOR
                            Color to use for the background (#FFF, #FFFFFF or
                            name)
      -T COLOR, --text-color COLOR
                            Color to use for text
      -F FONT, --font FONT  Use FONT to display text

    Content:
      -t TEXT, --text TEXT  Display text
      -C CMD, --command CMD
                            Runs CMD and shows the output
      -n SECONDS, --interval SECONDS
                            Refresh the screen and rerun command every SECONDS
                            seconds (default: None)

    Window:
      -w, --window          Start in window mode
      -m, --hide-cursor     Hide the mouse cursor
      -b, --borderless      Run the window without a border
      -g WxH+X+Y, --geometry WxH+X+Y
                            Set the size and position of the window
