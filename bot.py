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

import requests     # Import requests for API.
import json         # Import json for handling json.

# -- End --



# -- Global Variables --

# DeGet the URL for the API request from the json file.
with open("cfg.json") as json_file:
    config = json.load(json_file)

# -- End --



def get_data():
    # Get APIurl from config file.
    APIurl = config['APIurl']

    # Get the API response and filter it.
    response = requests.get(url = APIurl)
    data = response.json()["searchedProducts"]["productDetails"]

    # Return the data.
    return data


def alert(name, status, link):

    # If discord hook is enabled, notify discord.
    if config['discord']['enabled'] == True:
        # Get discord configuration.
        discordCfg = config['discord']
        # Import discord library.
        from discord import Webhook, RequestsWebhookAdapter

        # Create the message for the notification.
        message = ("**" + name + " status changed! " + " <@&" + discordCfg['roleID'] + ">**\n"
        + ">>> New status: `" + status + "`\n" + ">>> Retailer link: " + link)

        # Create webhook and send the message.
        webhook = Webhook.from_url(discordCfg['webhookUrl'], adapter=RequestsWebhookAdapter())
        webhook.send(message)



# -- Main --

def main():
    # Loop forever.
    while True:

        # Get the specified product data.
        data = get_data()

        # Loop through products to find status.
        for products in data:
            # Get the details of the product required.
            name = products["displayName"]
            status = products["prdStatus"]
            link = products["retailers"][0]["purchaseLink"]
            # Output current process.
            print ("Checking " + name + "...")

            if status != "out_of_stock":
                # Output current status.
                print ("~~~ Status for " + name + " changed! New status: " + status + " ~~~")
                print ("~~~ Possible purchase link: " + link + " ~~~")
                alert(name, status, link)


# Call the main code.
if __name__ == "__main__":
    main()

# -- End --
