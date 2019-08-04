from ItemMarketPriceManager import ItemMarketPriceManager

if __name__ == "__main__":
    item_market_price_manager = ItemMarketPriceManager()

    while True:
        item = input("What item would you like to update the price of?\t")

        try:
            print("Current price of the item: {}".format(
                item_market_price_manager.get_market_price_for_item(item)))
            item_market_price_manager.ask_user_for_market_price(item_name=item)
        except Exception as ex:
            print(ex)
