# The Random Bot
[![License](https://img.shields.io/badge/license-GNU-red)](LICENSE)
[![Discord](https://img.shields.io/discord/756682912166051851?label=Development%20Discord)](https://discord.gg/3hry5EFuM4)
[![Version](https://img.shields.io/pypi/pyversions/Discord.py)](https://pypi.org/project/discord.py/)
[![Grade](https://img.shields.io/codefactor/grade/github/xarvatium/the-random-project/master)](https://www.codefactor.io/repository/github/xarvatium/the-random-project/branches)
[![Issues](https://img.shields.io/github/issues/xarvatium/the-random-project)](https://github.com/xarvatium/the-random-project/issues)


Hello, and welcome to the GitHub page for the Random Bot. If you're curious as to what all it does, I will include sections that describe the different aspects of the bot.


### Roadmap:
- [x] Incorporate a homebrew Random Wikipedia Article generator
- [x] Include a basic random number generator
- [x] Include a ping command that displays the bot's latency
- [x] Add a random YouTube video generator
- [x] Added a new random color feature
- [x] Streamlined the Help command in order to ensure legibility
- [x] Added a few developer-only commands
- [x] Added a random song generator
- [x] Add a r/all puller for only channels marked nsfw (with a possibility for ignoring nsfw posts in sfw channels)
- [x] Add an Imgur feature that draws from galleries (nsfw feature in development)
- [ ] Maybe add a random Urban Dictionary definition for channels marked nsfw(?)
- [ ] Add automated testing to make error catching easier in beta
- [ ] Add database support with custom prefixes (sort of functions, still in the works)

### Are you Self-Hosting?
We are completely fine with self-hosting, we just ask that if you do publish to github, to please follow the License and it's terms. <br>
Below are the developer only commands: 
 - ;servers - this lists the servers the bot is in
 - ;status [status]- this changes the status of the bot <br>

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
    }
}
```

### Sources:
[Discord.py Documentation](https://discordpy.readthedocs.io/en/latest/) <br>
[Wikipedia's Python API](https://stackabuse.com/getting-started-with-pythons-wikipedia-api/) <br>
[Google's API](https://console.developers.google.com/getting-started) <br>
[last.fm's API](https://www.last.fm/api)

#### Are you curious as to how I made this?
It's simple! All I used was discord.py with a random wiki article generator I made previously and built on it from there!

