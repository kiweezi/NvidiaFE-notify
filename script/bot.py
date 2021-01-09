# A bot which notifies the user of selected Nvidia products becoming in stock.
# The bot only functions in the UK region as the API works differently here.
# Currently only support for "Founders Edition" graphics cards.
# 
# This is part of a repository hosted here: https://github.com/RicochetStudios/nvidia-bot
# Created by: 
# - https://github.com/kiweezi
# - https://github.com/HazNut
#



# -- Imports --

import requests                                         # For requests from the API.
import json                                             # For handling json.
import os                                               # For handling file paths and sizes.
from discord import Webhook, RequestsWebhookAdapter     # For discord notifications.
from win10toast import ToastNotifier                    # For Windows 10 toast notifications.
from time import sleep                                  # For delay interval.
from datetime import datetime                           # For displaying the system time.

# -- End --



# -- Global Variables --

# DeGet the URL for the API request from the json file.
with open("cfg.json") as json_file:
    config = json.load(json_file)

# -- End --



def check_logsize(log):
    # Get logfile path.
    logPath = config['logfile']['path']
    # Get current size of log file.
    fileSize = (os.stat(logPath).st_size / 1000)

    # If the file size is bigger than specified, delete oldest 25%.
    if fileSize >= config['logfile']['maxSize']:
        # Close the file.
        log.close()

        # Get the lines to cut from the file.
        with open(logPath, 'r') as fin:
            data = fin.read().splitlines(True)
            cut = int(len(data) / 4)
        # Cut 25% of the log file lines.
        with open(logPath, 'w') as fout:
            fout.writelines(data[cut:])

        # Open the file back up again.
        log = open(logPath, "a")
    
    # Return the processed or uneditted logs.
    return log



def get_data():
    # Get APIurl from config file.
    APIurl = config['APIurl']
    # Set headers to use API as if from a browser.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    # Get the API response and filter it.
    response = requests.get(APIurl, headers=headers)
    data = response.json()["searchedProducts"]["productDetails"]

    # Return the data.
    return data


def alert(name, status, link):

    # If discord is enabled, notify discord.
    if config['discord']['enabled'] == True:
        # Get discord configuration.
        discordCfg = config['discord']

        # Create the message for the notification.
        message = ("**" + name + " status changed! " + " <@&" + discordCfg['roleID'] + ">**\n"
        + ">>> New status: `" + status + "`\n" + "Retailer link: " + link)

        # Create webhook and send the message.
        webhook = Webhook.from_url(discordCfg['webhookUrl'], adapter=RequestsWebhookAdapter())
        webhook.send(message)

    # If Windows 10 toast is enabled, create a toast notification.
    if config['win10toast']['enabled'] == True:
        # Get win10toast configuration.
        iconPath = config['win10toast']['icon']

        # Show toast notification.
        toaster = ToastNotifier()
        toaster.show_toast(name + "status changed",
        "New status: '" + status + "'\n" + " Retailer link: " + link,
        icon_path=iconPath,
        duration=5,
        threaded=True)



# -- Main --

def main():
    # Open the log file specified and overwrite it.
    log = open(config['logfile']['path'], "a")

    # Loop as long as keyboard interrupt is not triggered.
    try:
        while True:
            # Get the specified product data.
            data = get_data()

            # Loop through products to find status.
            for products in data:
                # Get the details of the product required.
                name = products["displayName"]
                status = products["prdStatus"]
                link = products["retailers"][0]["purchaseLink"]

                # Get the time and format it.
                timeStamp = (datetime.now()).strftime("%H:%M:%S")
                # Output current process and update file.
                log.writelines("[" + timeStamp + "] Checking " + name + "...\n")
                log.flush()

                if status != "out_of_stock":
                    # Wipe the contents of the file.
                    log.truncate(0)
                    # Get the time and format it.
                    timeStamp = str((datetime.now()).strftime("%H:%M:%S"))
                    # Output current status and update.
                    log.write ("[" + timeStamp + "] >>> Status for " + name + " changed! New status: " + status + " <<<\n"
                        + "[" + timeStamp + "] >>> Retailer link: " + link + " <<<\n")
                    log.flush()

                    # Send notification alerts.
                    alert(name, status, link)
            
            # If the file size is bigger than specified, delete oldest 25%.
            log = check_logsize(log)

            # Wait for time interval.
            sleep(config['delay'])
    

    # Loop as long as keyboard interrupt is not triggered.
    except KeyboardInterrupt:
        # Display an exiting log.
        log.write("Exiting...")
        print ("Exiting...")
        # Close the log file.
        log.close()
        pass

    


# Call the main code.
if __name__ == "__main__":
    main()

# -- End --
