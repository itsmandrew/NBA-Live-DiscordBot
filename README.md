# NBA Live Discord Bot

The main functionality is to bring aggregated statistics of real-time NBA game statistics directly into a discord server. 
This functionality is designed to cater to basketball enthusiasts, sports analysts, and fantasy league players who seek up-to-the-minute information from the NBA world. Looking for aggregated statistics is slow. I wanted to make it more convenient and faster.


## Set Up

This is running in Python 3.10!

1. Clone the repository via HTTPS
2. Initialize a virtual environment with this command if using MacOS/Linux
    - ` python3.10 -m venv venv `
3. Activate the virtual environment using the following command if using MacOS/Linux:
    - ` source venv/bin/activate `
4. Install Dependencies 
    - ` pip install -r requirements.txt `
5. Run the "bot.py" file via command line (make sure the venv is activated!!!)
    NOTE: Need a "creds.json" in directory before running command below
    - ` python bot.py `

    After running command, you can test commands in whichever server the bot is in!


## Features

Right now one of the main features is:

!daily - returns the "top 5 fantasy players (most points based off ESPN's system)"  for each game played on the current date

