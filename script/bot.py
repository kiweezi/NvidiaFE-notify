# A bot which notifies the user of selected Nvidia products becoming in stock.
# The bot only functions in the UK region as the API works differently here.
# Currently only support for "Founders Edition" graphics cards.
# 
# This is part of a repository hosted here: https://github.com/RicochetStudios/nvidia-bot
# Created by: 
# - https://github.com/kiweezi
# - https://github.com/HazNut
#



# Shebang
#!/usr/bin/env python3

# -- Imports --

import requests                                         # For requests from the API.
import json                                             # For handling json.
import os                                               # For handling file paths and sizes.
import sys                                              # For arguments and script control.
from time import sleep                                  # For delay interval.
from datetime import datetime                           # For displaying the system time.

# -- End --



# -- Global Variables --

# Get the URL for the API request from the json file.
with open("cfg.json") as json_file:
    config = json.load(json_file)

# Location of the flag file for stopping and starting through commandline.
FLAGFILENAME = os.path.abspath(config["flagFile"])

# -- End --



# Get additional imports used in the code.
# If discord is selected, import it.
if (config["discord"]["enabled"] == True):
    from discord import Webhook, RequestsWebhookAdapter     # For discord notifications.

# If win10toast is selected, import it.
if config["win10toast"]["enabled"] == True:
    from win10toast import ToastNotifier                    # For Windows 10 toast notifications.



def set_file_flag(startorstop):
    # If the flag is to be set to true, create the flag file.
    if startorstop:
        with open(FLAGFILENAME, "w") as f:
            f.write("run")
    # If the flag is to be set to false, delete the flag file.
    else:
        if os.path.isfile(FLAGFILENAME):
            os.unlink(FLAGFILENAME)

def is_flag_set():
    # Return if the file exists.
    return os.path.isfile(FLAGFILENAME)


def check_logsize(log):
    # Get logfile path.
    log_path = os.path.abspath(config["logfile"]["path"])
    # Get current size of log file.
    file_size = (os.stat(log_path).st_size / 1000)

    # If the file size is bigger than specified, delete oldest 25%.
    if file_size >= config["logfile"]["maxSize"]:
        # Close the file.
        log.close()

        # Get the lines to cut from the file.
        with open(log_path, "r") as fin:
            data = fin.read().splitlines(True)
            cut = int(len(data) / 4)
        # Cut 25% of the log file lines.
        with open(log_path, "w") as fout:
            fout.writelines(data[cut:])

        # Open the file back up again.
        log = open(log_path, "a")
    
    # Return the processed or uneditted logs.
    return log


def get_data():
    # Get APIurl from config file.
    api_url = config["APIurl"]
    # Set headers to use API as if from a browser.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    # Get the API response and filter it.
    response = requests.get(api_url, headers=headers)
    data = response.json()["searchedProducts"]["productDetails"]

    # Return the data.
    return data


def alert(name, status, link):
    # If discord is enabled, notify discord.
    if config["discord"]["enabled"] == True:
        # Get discord configuration.
        discord_cfg = config["discord"]

        # Create the message for the notification.
        message = ("**" + name + " status changed! " + " <@&" + str(discord_cfg["roleID"]) + ">**\n"
        + ">>> New status: `" + status + "`\n" + "Retailer link: " + link)

        # Create webhook and send the message.
        webhook = Webhook.from_url(discord_cfg["webhookUrl"], adapter=RequestsWebhookAdapter())
        webhook.send(message)

    # If Windows 10 toast is enabled, create a toast notification.
    if config["win10toast"]["enabled"] == True:
        # Get win10toast configuration.
        icon_file = os.path.abspath(config["win10toast"]["icon"])

        # Show toast notification.
        toaster = ToastNotifier()
        toaster.show_toast(name + "status changed",
        "New status: '" + status + "'\n" + " Retailer link: " + link,
        icon_path=icon_file,
        duration=5,
        threaded=True)



# -- Main --

def main():
    # Open the log file specified and overwrite it.
    log = open(os.path.abspath(config["logfile"]["path"]), "a")

    # If incorrect arguments are provided, display usage and quit.
    if len(sys.argv) < 2:
        message = "Usage: <program> start|stop|test\n"
        log.write(message); log.flush()
        sys.exit()
    
    # Store the argument used.
    instruction = sys.argv[1]
    # If program is called to start, set the start flag.
    if instruction == "start":
        log.write("Starting...\n"); log.flush()
        set_file_flag(True)

        # Initialize default alert status for each product.
        alert_status = {}
        # For each product, set the default alert status.
        for product in get_data():
            alert_status[product["displayName"]] = False

    # If program is called to stop, set the stop flag and exit.
    elif instruction == "stop":
        log.write("Stopping...\n"); log.flush()
        set_file_flag(False)
        sys.exit()

    # If program is called to test, send a test alert.
    elif instruction == "test":
        log.write("Testing...\n"); log.flush()
        alert("Nvidia Test Card", "test_run", "https://github.com/kiweezi/NvidiaFE-notify")

    # While the program is set to start, continue running.
    while is_flag_set():

        # If the API is working as intended, run the main script.
        try:
            # Loop through products from data to find the status.
            for product in get_data():
                # Get the details of the product required.
                name = product["displayName"]
                status = product["prdStatus"]
                link = product["retailers"][0]["purchaseLink"]

                # Get the time and format it.
                time_stamp = str((datetime.now()).strftime("%H:%M:%S"))
                # Output current process and update file.
                log.writelines("[" + time_stamp + "] Checking " + name + "...\n"); log.flush()

                # If the status is not out of stock, notify once, but log until out of stock again.
                if status != "out_of_stock":
                    # Get the time and format it.
                    time_stamp = str((datetime.now()).strftime("%H:%M:%S"))
                    # Output current status and update.
                    log.write ("[" + time_stamp + "] >>> Status for " + name + " changed! New status: " + status + "\n"
                        + "[" + time_stamp + "] >>> Retailer link: " + link + "\n"); log.flush()
                    
                    # Alert once, then disable alert until the item is back in stock
                    if alert_status[name] == False:
                        # Send notification alerts.
                        alert(name, status, link)
                        # Set timeout for alert.
                        alert_status[name] = True
                
                # If the item is out of stock, enable alerts again.
                elif status == "out_of_stock" and alert_status[name] == True:
                    # Disable timeout for alert.
                    alert_status[name] = False

        # If the API is not responding, log this.
        except:
            # Log that the API is not giving a response.
            time_stamp = str((datetime.now()).strftime("%H:%M:%S"))
            log.write("[" + time_stamp + "] Connection failed...\n"); log.flush()
        
        
        # If the file size is bigger than specified, delete oldest 25%.
        log = check_logsize(log)
        # Wait for time interval.
        sleep(config["delay"])
    

    # Log that the program is stopping.
    log.write("Stopped\n")
    # Close the log file.
    log.close()
    


# Call the main code.
if __name__ == "__main__":
    main()

# -- End --
