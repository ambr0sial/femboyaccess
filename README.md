<p align="center">
  <a href="https://github.com/ambr0sial/femboyaccess"><img src="femboyaccess_logo.png" alt="FemboyAccess" width="128" /></a> 
</p>
<p align="center">
  FemboyAccess is a remote administration trojan that uses Discord as a C2C server.
</p>

## Purpose

FemboyAccess is a RAT (Remote Administration Tool/Trojan) that uses the Discord platform as a C2C (command & control) server. More specifically, it uses your own custom Discord guild and then uses a bot account to send commands from the server to the victim's computer.

## Features

- almost undetectable
- escalate privileges without UAC
- can handle multiple machines at once
- a lot of commands
- silent

Unfortunately, FemboyAccess is not well hidden as of now. It is easily findable by only using the Task Manager. Reminder that you can create pull requests, so if you have any ideas to hide FemboyAccess, give it a shot!

### All Commands

<details>
<summary>Click here to see all current FemboyAccess commands!</summary>

```
help - sends the help message
ping - checks bot latency
cd - navigates through directories
ls - lists files in the current directory
download <file> - download a specific file from the victim's computer
cmd - execute a CMD command
run <file> - run a file
screenshot - take a screenshot of the computer
bsod - blue screen of death
startup - add femboyaccess to startup
furryporn - floods the user's screen with furry porn (e621)
randommousemovements - randomly moves the user's mouse location
randomvolume - changes the volume value randomly
clipboard - fetches the victim's clipboard and sends it [BUGGY]
askescalate - asks the user to escalate privileges
escalate - tries to escalate privileges [DETECTED]
whoami - checks if femboyaccess is running as user or admin
msgbox <message> <title> - sends a message box
background <url> - changes the background to a specific image
playsound <url> - plays a sound using its url
doxx - fetches information from ipapi.co like city, zip..
blockinput - blocks inputs
unblockinput - unblocks inputs
tts - text-to-speech message
windowsphish - sends a fake windows security update pop-up asking for a password
displayoff - turns off screen
displayon - turns on screen
critproc - makes femboyaccess into a critical process
uncritproc - makes femboyaccess into a normal process
idletime - shows how much time the user has been idle
passwords - fetches passwords from the user's browsers
streamscreen - supposed to "stream" the user's screen using several screenshots but still not working
pid - gets the current pid
localtime - fetches the user's local time
timeset <year> <month> <day> <hour> <minute> - changes the system's time to a new one
webcampic - takes a pic from the user's webcam
fuckmbr - overwrites the master boot record
regedit <key_path> <value_name> <new_value> - edits a regedit value
taskkill <name> - kills a process
processes - lists all the running processes
exit - exit this session
```

</details>

## Usage

  1. Download `femboyaccess.py` and Python with the necessary libraries if not already done.
  2. [Create a Discord bot](https://discord.dev/) (make sure to check all intents on) then invite it on a new server.
  3. Edit the `femboyaccess.py` file:
      * Change the `guild_id` variable (line 44) to your server's ID
      * Change the last line of the code with your bot token
  4. Finished! Now, you can obfuscate it yourself if you want to. Whenever someone will open the file, a new channel will be created in your defined server with a custom session ID.

Note: FemboyAccess treats all machines like sessions and attributes them a 8-character long ID with letters and numbers. That's how the bot can manage multiple machines at the same time. The format of the generated channel name is something like:

`<computer_name>-<session_id>`

So if the computer's name is 'ambr0sial', the channel name will be something like:

`ambr0sial-6ef87f83`

## License

FemboyAccess is using the CC BY-NC 4.0 license. You can click on the badge to see what's it's all about! ✨

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-magenta.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
## Contributing

Contributions are always welcome!

You can create pull requests, we're pretty active.


#### Made with ❤ by [ambr0sial](https://www.github.com/ambr0sial) and [kaipicpic](https://www.github.com/kaipicpic).
