[![made-with-python](https://img.shields.io/badge/Made%20with-Python-informational)](https://www.python.org/)
[![Build-Status](https://img.shields.io/github/workflow/status/kiweezi/NvidiaFE-notify/Python%20application)](https://github.com/kiweezi/NvidiaFE-notify/actions?query=workflow%3A%22Python+application%22)

**This is a personal project of mine, it is by no means stable and I have no idea what I'm doing. A much more stable and flexible alternative can be found [HERE](https://github.com/samuelm2/Nvidia-Notify).**

# NvidiaFE-notify

Notify Discord or Win10 of **European** Nvidia Founders Edition card stock. Controlled through command line.

## Index

<!--toc-start-->

- [Requirements](#requirements)
- [Setup](#setup)
- [Configure](#configure)
- [Usage](#usage)
- [Contributors](#contributors)
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
   - `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`
   - If running windows, use `win-requirements.txt` instead.
   - On some Linux/Mac systems, you may need to use `python3` and `pip3` instead of `python` and `pip`, respectively.
3. Configure the `cfg.json` file
   - [Guide here](#configure).
4. Set up a method to control the bot like [tmux](https://www.howtogeek.com/671422/how-to-use-tmux-on-linux-and-why-its-better-than-screen/) or a [systemd service](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267) (optional):

```
# nvidiafe-notify.service
# Put me in /etc/systemd/system/

[Unit]
Description=NvidiaFE-notify bot
After=multi-user.target

[Service]
User=<username>
WorkingDirectory=/home/<username>/NvidiaFE-notify/script
ExecStart=/usr/bin/python3 /home/<username>/NvidiaFE-notify/script/bot.py

[Install]
WantedBy=multi-user.target
```

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
  | ---- |
  - **value**: file path
  - **description**: Path to store the logs from the script. Supports OS paths.
- | maxSize |
  | ------- |
  - **value**: number (integer)
  - **description**: The maximum size the log file can grow to, measured in Kb.

### discord

- | enabled |
  | ------- |
  - **value**: true or false
  - **description**: Determines whether Discord alerts are to be used.
- | webhookUrl |
  | ---------- |
  - **value**: text
  - **description**: The url webhook from Discord collected in the [optional](#optional) requirements.
- | roleID |
  | ------ |
  - **value**: number
  - **description**: The identifying, numerical code for a role to mention on the Discord server in the alert message sent.

### win10toast

- | enabled |
  | ------- |
  - **value**: true or false
  - **description**: Determines whether win10toast alerts are to be used.
- | icon |
  | ---- |
  - **value**: file path
  - **description**: Path to the icon file used in the notification. Supports OS paths.

## Usage

NvidiaFE-notify is a command line tool. It's intended usage is as a linux [systemd service](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267).
The bot can also be executed through the shell, therefore [tmux](https://www.howtogeek.com/671422/how-to-use-tmux-on-linux-and-why-its-better-than-screen/) can also be used.

### Systemd service

In linux, using the systemd service, the bot can be started with the following:

```console
sudo systemctl start nvidiafe-notify
```

### Commandline

The bot can still be executed throught the shell on Windows and Linux systems. This is where you will need to be a bit more creative, however.
The main issue is stopping the bot. This will need to be done by ending the process manually.

In Linux bash the script can be started with the `&` character at the end while the ssh session is active:

```console
python bot.py &
```

In Windows the script can be started in PowerShell by using `pythonw.exe`, which allows the script to run silently.

```powershell
& pythonw .\bot.py
```

## Contributors

- [HazNut](https://github.com/HazNut) - Greatly helped with styling and using requests, modules and general syntax. Fixed slow API requests using User-Agent header.

### Please give me issues, this is just a means of learning for me.
