from ItemMarketPriceManager import ItemMarketPriceManager
import os
import json
import requests
from requests.exceptions import HTTPError
import threading
import logging
import time


class MongoDBItemMarketPriceUpdater:
    __instance = None
    updated = set()
    item_market_price_manager = ItemMarketPriceManager()
    threads = []

    def __new__(cls):
        if ItemMarketPriceUpdater.__instance is None:
            ItemMarketPriceUpdater.__instance = object.__new__(cls)
        return ItemMarketPriceUpdater.__instance

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                            )

    def get_item(self, item_name):
        try:
            self.item_market_price_manager.mark_update_attempt(item_name)

            response = requests.get(
                'https://omegapepega.com/na/'+item_name+'/0')

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')  # Python 3.6

        except Exception as err:
            logging.error(f'Other error occurred: {err}')  # Python 3.6

        else:
            logging.debug(response.json())
            return response.json()

    def update_item(self, item_name):
        if item_name not in self.updated:
            self.updated.add(item_name)
            item_json = self.get_item(item_name)
            if (item_json is not None):
                self.item_market_price_manager.update_item(item_json)
                return True
        return False
        
    def update_all(self):
        for recipe_filename in os.listdir('Recipes'):
            try:
                with open('./Recipes/'+recipe_filename, 'r') as json_file:
                    item = json.load(json_file)
                    # t = threading.Thread(
                    #     name=item["Name"],
                    #     target=self.update_item, args=(item["Name"],))
                    # self.threads.append(t)
                    # t.start()
                    self.update_item(item["Name"])

                    if "Recipes" in item:
                        for recipe in item["Recipes"]:
                            for key in recipe.keys():
                                # update_item(key)
                                # t = threading.Thread(
                                #     name=key,
                                #     target=self.update_item, args=(key,))
                                # self.threads.append(t)
                                # t.start()
                                self.update_item(key)

            except Exception as ex:
                logging.error(ex)


if __name__ == "__main__":

    # while True:
    #     item = input("What item would you like to update the price of?\t")

    #     try:
    #         print("Current price of the item: {}".format(
    #             item_market_price_manager.get_market_price_for_item(item)))
    #         item_market_price_manager.ask_user_for_market_price(item_name=item)
    #     except Exception as ex:
    #         print(ex)

# ---------------------------------------------------------------------
    # updater = ItemMarketPriceUpdater()
    # updater.update_all()

# ---------------------------------------------------------------------
    from dotenv import load_dotenv
    load_dotenv()
    test = os.getenv("MEANING_OF_LIFE")
    print(test)

    import marketPriceDAO
    from marketPriceDAO import MarketPriceDAO
    mpDAO = MarketPriceDAO(os.getenv('BDO_DB_URI'), os.getenv('BDO_NS'))
    mpDAO.getData()
