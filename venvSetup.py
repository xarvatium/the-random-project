# This is the file to be used to setup a virtual env for those who want one
from sys import platform
from os import system as cmd
import os

if platform == "linux" or platform == "linux32":
    modules = ['pymongo', 'wikipedia', 'discord', 'praw', 'imgurpython', 'random', 'google-api-python-client', 'Pillow',
               'os', 'requests', 'json', 'time']
    cmdOut = cmd("python -m venv random_bot")
    if cmdOut is 0:
        cmd("the-random-bot/Scripts/activate")
        for i in modules:
            cmd("python -m pip install " + i)
    elif cmdOut != 0:
        consent = input(
            "An error occurred with making the virtual environment, attempting to install virtualenv. Would you like to install virtualenv (Y/N) ?").lower()
        if consent == "y":
            cmd("the-random-bot/Scripts/activate")
            for i in modules:
                cmd("python -m pip install " + i)

        elif consent != "n":
            print("Quitting...")
            quit()
    cmd("source random_bot/bin/activate")
    alphabet = list('abcdefghijklmnopqrstuvwxyz')  # create a list out of the alphabet
    modDict = {}
    l = 0  # iteration variable
    for i in modules:  # map each module to a letter of the alphabet
        modDict[l] = i
        l += 1
    for i in modDict:  # print out the letter and module for each thing
        print(str(i) + ": " + modDict[i])
    thing = list(input('\nThe modules above are required to be installed.\nIf you wish to install all of the above, leave it blank and press Enter.\nIf you wish to pick and choose, then please use the corresponding letter of the alphabet (a = 1, b = 2, c = 3, etc.)\nIf you already have some of these installed, pip will automatically mark it as installed.\nPlease list your choice: ').lower())  # get user input and convert to a list
    for i in thing:  # install what's mapped to each letter typed
        os.system("pip install " + modDict[i])
    if len(thing) == 0:  # if there's nothing entered, install everything
        for i in modules:
            os.system('pip install modules')

elif platform == "win32":
    modules = ['pymongo', 'wikipedia', 'discord', 'praw', 'imgurpython', 'random', 'google-api-python-client', 'Pillow',
               'os', 'requests', 'json', 'time']
    cmdOut = cmd("python -m venv random_bot")
    if cmdOut is 0:
        cmd(r"the-random-bot\Scripts\activate.bat")
        for i in modules:
            cmd("python -m pip install " + i)
    elif cmdOut != 0:
        consent = input("An error occurred with making the virtual environment, attempting to install virtualenv. Would you like to install virtualenv (Y/N) ?").lower()
        if consent == "y":
            cmd(r"the-random-bot\Scripts\activate.bat")
            for i in modules:
                cmd("python -m pip install " + i)

        elif consent != "n":
            print("Quitting...")
            quit()
    cmd("source random_bot/bin/activate")
    alphabet = list('abcdefghijklmnopqrstuvwxyz')  # create a list out of the alphabet
    modDict = {}
    l = 0  # iteration variable
    for i in modules:  # map each module to a letter of the alphabet
        modDict[l] = i
        l += 1
    for i in modDict:  # print out the letter and module for each thing
        print(str(i) + ": " + modDict[i])
    thing = list(input(
        '\nThe modules above are required to be installed.\nIf you wish to install all of the above, leave it blank and press Enter.\nIf you wish to pick and choose, then please use the corresponding letter of the alphabet (a = 1, b = 2, c = 3, etc.)\nIf you already have some of these installed, pip will automatically mark it as installed.\nPlease list your choice: ').lower())  # get user input and convert to a list
    for i in thing:  # install what's mapped to each letter typed
        os.system("pip install " + modDict[i])
    if len(thing) == 0:  # if there's nothing entered, install everything
        for i in modules:
            os.system('pip install modules')

elif platform == "darwin":
    print("---------------------------\nSorry! It looks like you're using MacOS which isn't currently supported by us, you'll have to set it up manually.\n---------------------------")