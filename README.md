[![made-with-python](https://img.shields.io/badge/Made%20with-Python-informational)](https://www.python.org/)
[![Build-Status](https://img.shields.io/github/workflow/status/kiweezi/NvidiaFE-notify/Python%20application)](https://github.com/kiweezi/NvidiaFE-notify/actions?query=workflow%3A%22Python+application%22)

**This is a personal project of mine, it is by no means stable and I have no idea what I'm doing. A much more stable and flexible alternative can be found [HERE](https://github.com/samuelm2/Nvidia-Notify).**

# NvidiaFE-notify
Notify Discord or Win10 of **European** Nvidia Founders Edition card stock. Controlled through command line.


## Index
<!--toc-start-->
* [Requirements](#requirements)
* [Setup](#setup)
* [Configure](#configure)
* [Usage](#usage)
* [Testing](#testing)
* [Contributors](#contributors)
<!--toc-end-->


## Requirements
### Essential
- [Python 3](https://www.python.org/downloads/) (not python 2.x)
- [pip](https://pip.pypa.io/en/stable/installing/) (for dependencies)

### Optional
- Discord Notifications via [Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)


## Setup
1. Clone/Download the /script folder to your prefered location
2. Install dependancies with pip
    -  `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`
    - If running windows, use `win-requirements.txt` instead.
    - On some Linux/Mac systems, you may need to use `python3` and `pip3` instead of `python` and `pip`, respectively.
3. Configure the `cfg.json` file
    - [Guide here](#configure).


## Configure
Change the behaviour of the program with the `cfg.json` file. The program will run without any additional configuration, but alerts are disabled by default.

It is recommended that you enable at least one notification method, as the program serves almost no purpose without it. See the settings below:

### APIurl
- **value**: valid url
- **description**: API url to query Nvidia's product page. You can get your own with this guide.
### delay
- **value**: number (can be decimal)
- **description**: The time paused before the next query to the API specified. This can be set to anything above zero.
### logfile
- | path |
  |------|
    - **value**: file path
    - **description**: Path to store the logs from the script. Supports OS paths.
- | maxSize |
  |---------|
    - **value**: number (integer)
    - **description**: The maximum size the log file can grow to, measured in Kb.
### discord
- | enabled |
  |---------|
    - **value**: true or false
    - **description**: Determines whether Discord alerts are to be used.
- | webhookUrl |
  |------------|
    - **value**: text
    - **description**: The url webhook from Discord collected in the [optional](#optional) requirements.
- | roleID |
  |--------|
    - **value**: number
    - **description**: The identifying, numerical code for a role to mention on the Discord server in the alert message sent.
### win10toast
- | enabled |
  |---------|
    - **value**: true or false
    - **description**: Determines whether win10toast alerts are to be used.
- | icon |
  |------|
    - **value**: file path
    - **description**: Path to the icon file used in the notification. Supports OS paths.


## Usage
NvidiaFE-notify is a command line tool. Use arguments `start` and `stop` to start and stop the script from running.
The script must be run in the background on a separate thread as to not pause the command line.

In Linux bash the script can be started with the `&` character at the end:
```console
python bot.py start &
```
In Windows the script can be stopped in PowerShell by using `pythonw.exe`, which allows the script to run silently.
```powershell
& pythonw.exe .\bot.py stop
```


## Testing
The `test` argument can be provided to the script to test the alerts currently configured in `cfg.json`.

For Linux bash:
```console
python bot.py test &
```
For Windows PowerShell:
```powershell
& pythonw.exe .\bot.py test
```


## Contributors
* [HazNut](https://github.com/HazNut) - Greatly helped with styling and using requests, modules and general syntax. Fixed slow API requests using User-Agent header.

### Please give me issues, this is just a means of learning for me.
