from pymongo import MongoClient, InsertOne
import os

# Requires the PyMongo package.
# https://api.mongodb.com/python/current

from dotenv import load_dotenv
load_dotenv()
from recipesDAO import RecipesDAO
rDAO = RecipesDAO(os.getenv('BDO_DB_URI'), os.getenv('BDO_NS'))
rDAO.deleteBaseIngredients()
rDAO.insertBaseIngredients()