# discordMCserverBot
A bot that starts a minecraft server locally via discord messages

## Running the bot yourself
Setting up this bot may seem challenging, and that is because I didn't intend to make it public for everyone to use, so a lot of the parts was coded to fit my own environment only. BUT if you know which arguments to change, i don't see how it wouldn't run on your computer.

### 1. Create a new discord applicaction account
Go to [https://discord.com/developers/applications](https://discord.com/developers/applications) and choose a name yourself ( I can't help u in setting up the account, there are a lot of tutorials online), once you're done, go to the Bot tab, and copy the token, you'll need it later.
### 2. Change the arguments in the python files
Here is the hard part, make sure to read through EVERY comment in the code, stuff that's needed to be changed would be named 'YOUR XXXX HERE', for example: the token you copied earlier, goes into line 146 'YOUR TOKEN HERE' (Single quotation marks included) in bot.py

There are at least 3 parts you MUST change before you run the bot:

 1. The aforementioned TOKEN in bot.py
 2. Arguments for java to launch the server in startmcserver.py (line 12)
 3. Your minecraft directory that contains the server jar in startmcserver.py (line 13)

### 3. Starting up the bot
I made a really simple batch file to start the bot called discordbot.bat, just click it and it'll launch the bot, easy as that.

## Bot Commands
`&server start`  Starts the minecraft server

`&server stop` Stops the minecraft server

`&watchlist enable/disalbe` Enables or disables the watchlist system, if enabled only the users in the watchlist can execute commands

`&watchlist add/remove @user` Adds or Removes a certain user on the list, simply tag the user at the end of the command to specify the user, e.g.: &watchlist add @SomeUserName

