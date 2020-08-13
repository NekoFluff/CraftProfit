# https://docs.google.com/document/d/1ztp0bOYOL4sApJfZnk7qY0Y1nHm0oN5dz9aoq1fd9Vw/edit
from ItemMarketPriceUpdater import ItemMarketPriceUpdater
import os 
import time
import datetime

already_failed = []

def readFile():
    try:
        file = open('failed_market_updates.txt', 'r') 
        for line in file:
            already_failed.append(line.strip())
        file.close()
        print(already_failed)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    readFile()

    from dotenv import load_dotenv
    load_dotenv()

    from marketPriceDAO import MarketPriceDAO
    mpDAO = MarketPriceDAO(os.getenv('BDO_DB_URI'), os.getenv('BDO_NS'))
    

    # Get all recipe names
    # pipeline = [
    #     {'$project': {'_id': 0, 'Name': 1}},
    # ]
    allNames = mpDAO.getAllRecipeNames()
    print('# Recipes without Market Price:', len(allNames))

    # File output for failed updates
    f = open('failed_market_updates.txt', 'a')

    # Get all updates
    mpUpdater = ItemMarketPriceUpdater()
    for idx, item_name in enumerate(allNames):
        if (item_name in already_failed): continue
        print('Recipes #', idx, '/', len(allNames), ":", item_name)
        
        data = mpUpdater.get_item(item_name)
        # print('data', data)
        now = datetime.datetime.now()

        if (data != None):
            formatted_data = {
                'Name': data['name'],
                'ID': data['mainKey'],
                'Market Price': data['pricePerOne'],
                'Quantity': data['count'],
                'Total Trade Count': data['totalTradeCount'],
                'Last Updated': now,
                'Last Update Attempt': now,
            }

            # print('formatted data', formatted_data)
            mpDAO.update(formatted_data)
        else:
            print('Error occured with item: ', item_name)
            try:
                f.write(item_name+"\n")
            except Exception as err:
                print(f'Error occurred: {err}')  # Python 3.6

        time.sleep(2)

    f.close()


