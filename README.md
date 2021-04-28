# [NOTICE] This repository has been archived, please use the GitLab repository for the most up-to-date releases --> https://gitlab.com/xarvatium/the-random-project
# The Random Bot
[![License](https://img.shields.io/badge/license-GNU-red)](LICENSE)
[![Discord](https://img.shields.io/discord/756682912166051851?label=Development%20Discord)](https://discord.gg/3hry5EFuM4)
[![Version](https://img.shields.io/pypi/pyversions/Discord.py)](https://pypi.org/project/discord.py/)
[![Grade](https://img.shields.io/codefactor/grade/github/xarvatium/the-random-project/master)](https://www.codefactor.io/repository/github/xarvatium/the-random-project/branches)
[![Issues](https://img.shields.io/github/issues/xarvatium/the-random-project)](https://github.com/xarvatium/the-random-project/issues)


Hello, and welcome to the GitHub page for the Random Bot. If you're curious as to what all it does, I will include sections that describe the different aspects of the bot.

Looking for a list of commands? Go to the [Bot Files](https://github.com/xarvatium/the-random-project/tree/master/BotFiles) directory!

### Roadmap:
- [x] Incorporate a homebrew Random Wikipedia Article generator
- [x] Include a basic random number generator
- [x] Include a ping command that displays the bot's latency
- [x] Add a random YouTube video generator (Revision: Added the ability for videos that do not just begin with "IMG" and other default names, but ones that begin/end with any letter of the alphabet + numbers)
- [x] Added a new random color feature
- [x] Streamlined the Help command in order to ensure legibility
- [x] Added a few developer-only commands
- [x] Added a random song generator
- [x] Add an r/all puller for only channels marked nsfw (with a possibility for ignoring nsfw posts in sfw channels)
- [x] Add an Imgur feature that draws from galleries (nsfw feature in development)
- [x] Add a word generator with definitions
- [x] Add a Nth digit in the Pi/Fibonacci sequence
- [ ] Maybe add a random Urban Dictionary definition for channels marked nsfw(?)
- [ ] Add automated testing to make error catching easier in beta
- [ ] Add database support with custom prefixes (sort of functions, still in the works)

### Are you Self-Hosting?
We are completely fine with self-hosting, we just ask that if you do publish to github, to please follow the License and it's terms. <br>
Below are the developer only commands: 
 - ;servers - this lists the servers the bot is in
 - ;status [status]- this changes the status of the bot <br>
 - ;database show|add|remove - This allows you to see, add, or delete entries in the database

Note: You can either make this yourself, or on the first run the console will take you through a wizard to make one. If you don't go through the wizard you will have to make a file called "config.json" in /BotFiles/ with the following layout:
```json
{
    "ytApiKey": "YTKey",
    "lastFmKey": "lastFMkey",
    "lastFmUA": "User Agent",
    "discordToken": "discordTOKEN",
    "bannedWords": [
        "word1",
        "word2",
        "banned word"
    ],
    "developers": {
        "1234567890": "username#1234"
    },
    "reddit": {
        "clientID": "personalUseScript",
        "clientSecret": "appSecret",
        "user_agent": "User Agent (by /u/user)"
    },
    "imgur": {
        "imgurID": "AppID",
        "imgurSecret": "AppSecret",
        "Authorization": "Client-ID <clientID here>"
    }
}
```
### About The Project
This was originally a bot that just generated a Wikipedia article, but I eventually added more and more onto it. I appreciate any help regarding feature requests and bug reports, and fully support open-source technology. I do not get paid for this, and do not accept donations as of now – if the project grows I may have to move to paid hosting.

### References:
[Discord.py Documentation](https://discordpy.readthedocs.io/en/latest/) <br>
[Wikipedia's Python API](https://stackabuse.com/getting-started-with-pythons-wikipedia-api/) <br>
[Google's API](https://console.developers.google.com/getting-started) <br>
[last.fm's API](https://www.last.fm/api) <br>
[Imgur's API](https://apidocs.imgur.com/)
