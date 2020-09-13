from pymongo import MongoClient, InsertOne, DeleteMany
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

    def deleteIngredients(self, ingredient_names_arr):
        def replace_wrapper(item_data):
            return DeleteMany(item_data)

        new_list = list(map(replace_wrapper, ingredient_names_arr))
        result = self.recipes.bulk_write(new_list, ordered=False)
        pprint.pprint(result)
    
    def deleteBaseIngredients(self):
        self.recipes.delete_many({'Action': 'Gather/Purchase'})
    
    def insertBaseIngredients(self):
        result = self.recipes.aggregate([
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
                    'from': 'recipes', 
                    'localField': '_id', 
                    'foreignField': 'Name', 
                    'as': 'All Recipes'
                }
            }, {
                '$addFields': {
                    'moreThanZero': {
                        '$gt': [
                            {
                                '$size': '$All Recipes'
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
        ])

        data_arr = [{
            'Name': x['_id'],
            'Action': 'Gather/Purchase',
            # 'Recipe': [],
            # 'Quantity Produced': 1,
            # 'Time to Produce': 0
        } for x in result]
        print(data_arr)

        # Finally update the data on the backend
        self.insertMany(data_arr)