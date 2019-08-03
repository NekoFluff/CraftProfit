import json
import os
from datetime import datetime


class ItemMarketPriceManager:
    __instance = None
    market_prices = {}  # Market prices for the item
    hand_crafted_prices = {}

    def __new__(cls):
        if ItemMarketPriceManager.__instance is None:
            ItemMarketPriceManager.__instance = object.__new__(cls)
        return ItemMarketPriceManager.__instance

    def __init__(self):
        self.load_market_prices()

    def load_market_prices(self):
        try:
            with open('Market_Prices/market_prices.json', 'r') as json_file:
                self.market_prices = json.load(json_file)
        except Exception as ex:
            print('Unable to load market_prices.json. Error: {}'.format(ex))

    def save_market_prices(self):
        # print('Saving market prices...')
        with open('Market_Prices/market_prices.json', 'w') as json_file:
            json.dump(self.market_prices, json_file, indent=4, sort_keys=True)
        # print('Saved market prices!')

    def ask_user_for_market_price(self, item_name: str):
        market_price = input('What is the price for {}?:\t'.format(item_name))
        # count = input('How many {} are there?:\t'.format(item_name))
        self.update_item_market_price(item_name, market_price)
    
    def update_item_market_price(self, item_name: str, market_price: int):
        self.market_prices[item_name] = {
            'Market Price': int(market_price), 
            # 'Quantity:': int(count), 
            'Last Updated': datetime.now().__str__()
        }
        self.save_market_prices()

    def get_market_price_for_item(self, item_name: str, ask_user=True) -> int:
        if item_name not in self.market_prices:
            if ask_user:
                self.ask_user_for_market_price(item_name)
            else:
                raise Exception('There is no market price for {}'.format(item_name))
        return self.market_prices[item_name]['Market Price']
    
    