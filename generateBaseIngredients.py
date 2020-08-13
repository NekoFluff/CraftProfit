from pymongo import MongoClient, InsertOne
import os

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

client = MongoClient('mongodb+srv://alex:rsDYNqZo0gYxM5ZH@cluster0.kfm1c.mongodb.net/test?authSource=admin&replicaSet=atlas-2r0smn-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true')
result = client['bdo-craft-profit']['recipes'].aggregate([
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
  'Action': 'Gather/Produce',
  'Recipe': []
 } for x in result]
print(data_arr)
# Finally update the data on the backend
from dotenv import load_dotenv
load_dotenv()
from recipesDAO import RecipesDAO
rDAO = RecipesDAO(os.getenv('BDO_DB_URI'), os.getenv('BDO_NS'))
# rDAO.insertMany(data_arr)