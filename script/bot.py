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
from datetime import datetime, timezone                 # For displaying the system time.

# -- End --



# -- Global Variables --

# Get the URL for the API request from the json file.
with open("cfg.json") as json_file:
    config = json.load(json_file)

# -- End --



# Get additional imports used in the code.
# If discord is selected, import it.
if (config["discord"]["enabled"] == True):
    from discord import Webhook, RequestsWebhookAdapter     # For discord notifications.

# If win10toast is selected, import it.
if config["win10toast"]["enabled"] == True:
    from win10toast import ToastNotifier                    # For Windows 10 toast notifications.



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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
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


def logOut(message, log):
    # Get strftime format.
    logTimeFormat = config["logfile"]["dateFormat"]
    # Get the time and format it.
    time_stamp = str((datetime.now(timezone.utc)).strftime(logTimeFormat))
    # Write the log to the file.
    log.write("[" + time_stamp + "] " + message)
    log.flush()



# -- Main --

def main():
    # Open the log file specified and overwrite it.
    log = open(os.path.abspath(config["logfile"]["path"]), "a")

    # Initialize default alert status for each product.
    alert_status = {}
    # For each product, set the default alert status.
    for product in get_data():
        alert_status[product["displayName"]] = False

    # Log that the program is starting.
    logOut("Starting...\n", log)

    # Loop as long as keyboard interrupt is not triggered.
    try:
        while True:
            # If the API is working as intended, run the get_instruction script.
            try:
                # Loop through products from data to find the status.
                for product in get_data():
                    # Get the details of the product required.
                    name = product["displayName"]
                    status = product["prdStatus"]
                    link = product["retailers"][0]["purchaseLink"]

                    # Log current process.
                    logOut("Checking " + name + "...\n", log)

                    # If the status is not out of stock, notify once, but log until out of stock again.
                    if status != "out_of_stock":
                        # Log that the status has changed.
                        logOut(">>> Status for " + name + " changed! New status: " + status + "\n", log)
                        logOut(">>> Retailer link: " + link + "\n", log)
                        
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
                # Log current process.
                logOut("Connection failed...\n", log)
            
            # If the file size is bigger than specified, delete oldest 25%.
            log = check_logsize(log)
            # Wait for time interval.
            sleep(config["delay"])
    
    # Loop as long as keyboard interrupt is not triggered.
    except KeyboardInterrupt:
        # Log that the program is stopping.
        logOut("Stopped...\n", log)
        # Close the log file.
        log.close()



# Call the get_instruction code.
if __name__ == "__main__":
    main()

# -- End --