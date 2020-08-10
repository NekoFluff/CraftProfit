from pymongo import MongoClient, ReplaceOne
# https://pymongo.readthedocs.io/en/stable/examples/bulk.html (Bulk Writes)
# https://pymongo.readthedocs.io/en/stable/examples/aggregation.html (Aggregation)
# https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.update_many
import datetime
import pprint

class MarketPriceDAO:
    items = {}
    item_profit_calculator = None

    def __init__(self, connectionURI, databaseName):
        self.client = MongoClient(connectionURI)
        self.marketPrices = self.client[databaseName]['market-price']
        print('Initialized MarketPriceDAO')
        sample = datetime.datetime.utcnow()
        pprint.pprint(self.marketPrices.find_one())

        self.update({
            'Name': 'test'
        })
        self.update_many([{
            'Name': 'test'
        }, {
            'Name': 'test2'
        }])

    def getData(self):
        print('Retrieving data')

    def update(self, item_data):
        _filter = {
            'Name': item_data['Name']
        }
        
        self.marketPrices.replace_one(_filter, item_data, upsert=True)

    def update_many(self, item_data_arr):
        def replace_wrapper(item_data):
            return ReplaceOne({'Name': item_data['Name']}, item_data, upsert=True)

        new_list = list(map(replace_wrapper, item_data_arr))
        # print('New List', new_list)
        self.marketPrices.bulk_write(new_list)
    