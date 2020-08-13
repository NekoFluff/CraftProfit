from pymongo import MongoClient, ReplaceOne
# https://pymongo.readthedocs.io/en/stable/examples/bulk.html (Bulk Writes)
# https://pymongo.readthedocs.io/en/stable/examples/aggregation.html (Aggregation)
# https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.update_many
import datetime
import pprint
import numpy as np

class MarketPriceDAO:
    items = {}
    item_profit_calculator = None

    def __init__(self, connectionURI, databaseName):
        self.client = MongoClient(connectionURI)
        self.marketPrices = self.client[databaseName]['market-price']
        self.recipes = self.client[databaseName]['recipes']
        print('Initialized MarketPriceDAO')
        # sample = datetime.datetime.utcnow()
        # pprint.pprint(self.marketPrices.find_one())


    def getData(self):
        print('[TODO] Retrieving data... ')

    def getAllRecipeNames(self):
        # arr1 = (self.recipes.distinct('Name'))
        # pipeline = [
        #     {'$project': {'_id': 0, 'Recipe': 1}},
        #     {'$unwind': '$Recipe'},
        #     {'$group': {'_id': '$Recipe.Item Name'}}
        # ]
        # arr2 = ([r['_id'] for r in self.recipes.aggregate(pipeline)])

        # return self.unique(arr1 + arr2)

        pipeline = [
            {
                '$unwind': {
                    'path': '$Recipe', 
                    'includeArrayIndex': 'index', 
                    'preserveNullAndEmptyArrays': True
                }
            }, {
                '$project': {
                    'Name': '$Recipe.Item Name'
                }
            }, {
                '$group': {
                    '_id': '$Name'
                }
            }, {
                '$lookup': {
                    'from': 'market-price', 
                    'localField': '_id', 
                    'foreignField': 'Name', 
                    'as': 'Market Data'
                }
            }, {
                '$addFields': {
                    'moreThanZero': {
                        '$gt': [
                            {
                                '$size': '$Market Data'
                            }, 0
                        ]
                    }
                }
            }, {
                '$match': {
                    'moreThanZero': False
                }
            }, {
                '$project': {
                    '_id': 1
                }
            }
        ]
        return [r['_id'] for r in self.recipes.aggregate(pipeline)]

    def unique(self, list1): 
  
        # intilize a null list 
        unique_list = [] 
        
        # traverse for all elements 
        for x in list1: 
            # check if exists in unique_list or not 
            if x not in unique_list: 
                unique_list.append(x) 

        return unique_list

    def update(self, item_data):
        print('Starting update for', item_data['Name'])
        _filter = {
            'Name': item_data['Name']
        }
        
        self.marketPrices.replace_one(_filter, item_data, upsert=True)
        print('Updated', item_data['Name'])

    def update_many(self, item_data_arr):
        print('Started update many')
        def replace_wrapper(item_data):
            return ReplaceOne({'Name': item_data['Name']}, item_data, upsert=True)

        new_list = list(map(replace_wrapper, item_data_arr))
        # print('New List', new_list)
        self.marketPrices.bulk_write(new_list)
        print('Finished update many')
    