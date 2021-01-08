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

import requests
import json

# -- End --



# -- Global Variables --

URL = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&search=nvidia&gpu=RTX%203080,RTX%203070&gpu_filter=RTX%203090~1,RTX%203080~1,RTX%203070~1,RTX%203060%20Ti~1,RTX%202080%20Ti~0,RTX%202080%20SUPER~0,RTX%202080~0,RTX%202070%20SUPER~0,RTX%202070~0,RTX%202060~0,GTX%201660%20Ti~0,GTX%201660%20SUPER~1,GTX%201660~0,GTX%201650%20Ti~0,GTX%201650%20SUPER~0,GTX%201650~5"

# -- End --



def get_status():
    # Define array to store results.
    results = []

    # Get the API response and filter it.
    response = requests.get(url = URL)
    data = response.json()["searchedProducts"]["productDetails"]

    # Loop through products to find status.
    for products in data:
        # Get the details of the product required.
        name = products["displayName"]
        status = products["prdStatus"]
        link = products["retailers"][0]["purchaseLink"]

        # Add to results.
        results.append([name, status, link])

    # Return the results.
    return results



# -- Main --

def main():
    # Get the products and their status.
    status = get_status()
    print (status)


    # result = json.dumps(data, indent= 4)
    #print (result)


# Call the main code.
if __name__ == "__main__":
    main()

# -- End --
