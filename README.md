# AlberoDiNatateBot

## Instructions
* First of all make sure you have installed Python3 typing <code>python3 --version</code> in the shell. If not, install it.
* Then install pip following [these instructions](https://pip.pypa.io/en/stable/installing/).
* Install the Telegram bot API for Python with <code>pip install pyTelegramBotAPI</code>.
* The GPIO Zero API should be installed by default on Raspbian. If not, follow [these instructions](https://gpiozero.readthedocs.io/en/stable/installing.html).
* Install the [emoji library](https://pypi.org/project/emoji/) typing <code>pip install emoji --upgrade</code>.
* Make your script executable with the command <code>chmod u+x mySrcFile.py</code>.
* Add a cron to automatilcally start the Bot when the system boots up typing <code>@reboot python3 /path/to/mySrcFile.py &</code>.
