# The Random Bot
[![License](https://img.shields.io/badge/license-GNU-red)](LICENSE)
[![Discord](https://img.shields.io/discord/756682912166051851?label=Development%20Discord)](https://discord.gg/3hry5EFuM4)
[![Version](https://img.shields.io/pypi/pyversions/Discord.py)](https://pypi.org/project/discord.py/)
[![Grade](https://img.shields.io/codefactor/grade/github/xarvatium/the-random-project/master)](https://www.codefactor.io/repository/github/xarvatium/the-random-project/branches)
[![Issues](https://img.shields.io/github/issues/xarvatium/the-random-project)](https://github.com/xarvatium/the-random-project/issues)


Hello, and welcome to the GitHub page for the Random Bot. If you're curious as to what all it does, I will include sections that describe the different aspects of the bot.

### General Purpose Commands
These are the general purpose commands:
##### Help
This provides a list of commands (and how to use them properly)
##### Ping
 - This is self-explanatory really. It just provides you the bot's latency.
##### Ask
 - This is basically an 8Ball that gives you 8ball answers.
##### Repeat
 - This repeats whatever you tell it to say (some things have been blacklisted).

### The Random Commands
There are 6 random commands for right now:
##### Article
 - This gives you a random wikipedia article with a title, summary, and url
##### Number
 - This gives you a number from a min/max that you can give, or just use it as `;generate number` and it will give a number from 1-100
##### Video
 - This gives you a random video from YouTube
##### Color
 - This gives you a random color w/ Hex and RGB formatting (might add CMYK for the kicks)
##### Song
 - This gives you a random song from the top 50 songs of the top 50 tags of last.fm
##### Random
 - This gives you a random item from one of the previously listed generators


### Roadmap:
- [x] Incorporate a homebrew Random Wikipedia Article generator
- [x] Include a basic random number generator
- [x] Include a ping command that displays the bot's latency
- [x] Add a random YouTube video generator
- [x] Added a new random color feature
- [x] Streamlined the Help command in order to ensure legibility
- [x] Added a few developer-only commands
- [x] Added a random song generator
- [ ] Maybe add a random Urban Dictionary definition for channels marked nsfw(?)
- [ ] Add a r/all puller for only channels marked nsfw (with a possibility for ignoring nsfw posts in sfw channels)
- [ ] Add automated testing to make error catching easier in beta

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

