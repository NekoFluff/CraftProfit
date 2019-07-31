import json
import os
from datetime import datetime


class ItemPriceManager:
    __instance = None
    market_prices = {}

    def __new__(cls):
        if ItemPriceManager.__instance is None:
            ItemPriceManager.__instance = object.__new__(cls)
        return ItemPriceManager.__instance

    def load_market_prices(self):
        try:
            with open('Market_Prices/market_prices.json', 'r') as json_file:
                self.market_prices = json.load(json_file)
        except Exception as ex:
            print('Unable to load market_prices.json. Error: {}'.format(ex))

    def save_market_prices(self):
        print('Saving market prices...')
        with open('Market_Prices/market_prices.json', 'w') as json_file:
            json.dump(self.market_prices, json_file, indent=4, sort_keys=True)
        print('Saved market prices!')

    def ask_user_for_market_price(self, item_name: str):
        market_price = input('What is the price for {}?:\t'.format(item_name))
        count = input('How many {} are there?:\t'.format(item_name))
        self.market_prices[item_name] = {
            'Market Price': int(market_price), 
            'Quantity:': int(count), 
            'Last Updated': datetime.now().__str__()
        }
        print(self.market_prices[item_name])

    def get_market_price_for_item(self, item_name: str) -> int:
        if item_name not in self.market_prices:
            self.ask_user_for_market_price(item_name)
        return self.market_prices[item_name]['Market Price']
