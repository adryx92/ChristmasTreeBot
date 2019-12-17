# AlberoDiNatateBot

## Instructions
* First of all make sure you have installed Python3 typing <code>python3 --version</code> in the shell. If not, install it.
* Then install pip following [these instructions](https://pip.pypa.io/en/stable/installing/).
* Install the [Telegram bot API for Python](https://github.com/python-telegram-bot/python-telegram-bot) typing <code>pip install pyTelegramBotAPI</code>.
* The GPIO Zero API should be installed by default on Raspbian. If not, follow [these instructions](https://gpiozero.readthedocs.io/en/stable/installing.html).
* Install the [emoji library](https://pypi.org/project/emoji/) typing <code>pip install emoji --upgrade</code>.
* Add <code>#!/usr/bin/python3</code> at the beginning of the script.
* Make your script executable with <code>chmod</code>.
* Configure a cron to automatilcally start the Bot when the system boots up typing <code>sudo crontab -e</code> and adding <code>@reboot python3 /path/to/mySrcFile.py</code>. 
  * If you're on a Wi-Fi network, the Raspberry may try to launch the script when the connection is not ready yet, terminating it with an exception. A workaround for this issue is to delay the script launch. Use this instead:<br>
  <code>@reboot sleep 30 && python3 /path/to/mySrcFile.py</code>
