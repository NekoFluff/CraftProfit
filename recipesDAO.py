from pymongo import MongoClient, InsertOne
# https://pymongo.readthedocs.io/en/stable/examples/bulk.html (Bulk Writes)
# https://pymongo.readthedocs.io/en/stable/examples/aggregation.html (Aggregation)
# https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.update_many
import datetime
import pprint

class RecipesDAO:
    items = {}
    item_profit_calculator = None

    def __init__(self, connectionURI, databaseName):
        self.client = MongoClient(connectionURI)
        self.recipes = self.client[databaseName]['recipes']
        print('Initialized RecipesDAO')

    def getData(self):
        print('[TODO] Retrieving data... ')

    # def update(self, item_data):
    #     _filter = {
    #         'Name': item_data['Name']
    #     }
        
    #     self.recipes.replace_one(_filter, item_data, upsert=True)

    def insertMany(self, item_data_arr):
        def replace_wrapper(item_data):
            return InsertOne(item_data)

        new_list = list(map(replace_wrapper, item_data_arr))
        self.recipes.bulk_write(new_list)
    