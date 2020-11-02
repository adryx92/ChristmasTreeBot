# ChristmasTreeBot

## About
This is a DIY project to use a Raspberry Pi running a Telegram Bot to turn on and off your Christmas tree.

Yes, this is an old project and a smart plug is simpler... But not that funny!

## Installation

### Automatic Instructions
* Make the setup script executable with <code>chmod +x install.sh</code>.
* Run the script elevated <code>sudo ./install.sh</code>.
* Add a cron to automaticallu start the bot, as explained in the [Manual Instructions](https://github.com/adryx92/ChristmasTreeBot#manual-instructions).

### Manual Instructions
* First of all make sure you have installed Python3 typing <code>python3 --version</code> in the shell. If not, install it with <code>apt install python3</code>.
* Then install pip3 with <code>apt install python3-pip</code>.
* Install the [Telegram bot API for Python](https://github.com/python-telegram-bot/python-telegram-bot) typing <code>pip3 install pyTelegramBotAPI</code>.
* The GPIO Zero API should be installed by default on Raspbian. If not, follow [these instructions](https://gpiozero.readthedocs.io/en/stable/installing.html).
* Install the [emoji library](https://pypi.org/project/emoji/) typing <code>pip3 install emoji</code>.
* Make your script executable with <code>chmod +x src.py</code>.
* Configure a cron to automatilcally start the Bot when the system boots up typing <code>sudo crontab -e</code> and adding <code>@reboot python3 /path/to/mySrcFile.py</code>. 
  * If you're on a Wi-Fi network, the Raspberry may try to launch the script when the connection is not ready yet, terminating it with an exception. A workaround for this issue is to delay the script launch. Use this instead:<br>
  <code>@reboot sleep 30 && python3 /path/to/mySrcFile.py</code>
