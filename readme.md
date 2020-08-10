# CraftProfit

Start crafting profits on *Black Desert Online* with this tool!

### If you're interested in helping with this project, send me an email at alexnou@gmail.com

This is a small project for automatically calculating profit values for crafting items and selling them on the *Black Desert Online* market. Since the crafting tree is extensive and there are multiple ways of crafting an individual item, four csv files are created to list out the potential profit values for some of the various crafting methods (`market_craft_profit_values.csv, hand_craft_profit_values.csv, optimal_profit_values.csv, and optimal_per_sec_profit_values.csv`) and stored in the local *Profit* folder. Additional recipes can be added in the *Recipe* folder. Cooking and alchemy time reduction buffs are implemented and in the *Buffs* folder.

The most important is **optimal_per_sec_profit_values.csv** since it provides the best profit values that can be generated per second. This involves buying certain pieces of the recipe (if they're cheap) and crafting others (if they're expensive). The details of each csv file are listed in their own subsection below.

## HOW TO USE

Run `python ./ItemMarketPriceUpdater.py</code>` to generate market_prices.json in the Market_Prices folder.

Run `python ./Main.py` to generate the profit csv files.

Type in the item you want to craft.

Type in the number of items you want to craft.

**(All outputed instructions are based on the optimal_per_sec_profit_values.csv for maximum profits)**

Sample Output:

```
What item would you like to craft?      Ship License: Fishing Boat
How many would you like to craft?       10  
In order to craft Ship License: Fishing Boat x 10:
--------------------------------------------------
Usable Scantling                      32,800 Silver   x      250 =  8,200,000  Silver
Birch Plywood [You Craft]                  0 Silver   x      500 =        0.0  Silver    20.00 minutes
Bronze Ingot                          10,500 Silver   x      250 =  2,625,000  Silver
Pine Sap                               4,970 Silver   x      300 =  1,491,000  Silver
Black Stone Powder                     4,340 Silver   x      300 =  1,302,000  Silver
Flax Fabric                           10,200 Silver   x      160 =  1,632,000  Silver
                                                                     15250000  Ingredient Total
Market Price: 5,950,000.00, Crafting Price: 1,525,000.00 (You save 4,425,000.00 silver per item made, not including sub ingredients)

In order to craft Birch Plywood x 500:
--------------------------------------------------
Birch Plank                            1,770 Silver   x    2,000 =  3,540,000  Silver
                                                                      3540000  Ingredient Total
Market Price: 10,500.00, Crafting Price: 7,080.00 (You save 3,420.00 silver per item made, not including sub ingredients)

                                                                    90,000.00  Seconds to Craft 1 x Ship License: Fishing Boat
                                                                    15,000.00  Minutes to Craft 10 x Ship License: Fishing Boat
                                                                    15,020.00  Total Craft Time (Minutes)
                                                                   18,790,000  Shopping Cart Total
                                                                   59,500,000  Market Sell Price (Pre Tax)
                                                                   50,277,500  Market Sell Price (After Tax)
                                                                   31,487,500  Profit
                                                                         1.68  Profit Margin

                                                                    5,950,000  Market Sell Price (Per Item)
                                                                  5,027,750.0  Market Sell Price (Per Item, After Tax)
                                                                  1,879,000.0  Silver Spent (Per Item)
                                                                  3,148,750.0  Profit (Per Item)

                                                                   125,782.29  Profit (Silver/Hour)
------------------------------------------------------------------------------------------------------------------------
```

## market_craft_profit_values.csv:

Buy all necessary items from the market and craft it.

## hand_craft_profit_values.csv:

Hand craft everything from the ground up to the item.

## optimal_profit_values.csv:

Optimize the total amount of money made for an item (No matter how long it takes).

## optimal_per_sec_profit_values.csv:

Optimize the total amount of money made per second for an item
(Time is money. Sometimes buying it from the market will cost more, but it takes too long to craft by hand with minimal gain.)

# Adding a Recipe
First, you can take a look at a sample recipe such as Beer.json

**Beer.json**
```
{
    "Action": "Cooking",
    "Last Updated": "2019-09-07 19:13:08.812676",
    "Name": "Beer",
    "Quantity Produced": 2.66,
    "Recipes": [
        {
            "Leavening Agent": 2,
            "Mineral Water": 6,
            "Sugar": 1,
            "Wheat": 5
        }
    ],
    "Time to Produce": 10.0
}
```

You can copy/paste the content to a new json file (*e.g. NewItem.json*) in the Recipes folder and change the values accordingly. Just make sure all items used in the Recipes list are also json files too. 

# Recipes with Symbolic Item Recipes

Cooking recipes generally allows multiple items as a substitute for an ingredient (e.g. Dough). The Aloe Cookie recipe is an example that uses the symbolic item 'Dough' which encompasses all 7 types of dough. Feel free to create more symbolic items!

**AloeCookie.json**
```
{
  "Action": "Cooking",
  "Name": "Aloe Cookie",
  "Quantity Produced": 2.5,
  "Recipes": [
      {
          "Aloe": 5,
          "Dough": 7,
          "Cooking Honey": 3,
          "Sugar": 4
      }
  ],
  "Time to Produce": 10.0
}
```

**Dough.json**
```
{
  "Action": "Cooking",
  "Name": "Dough",
  "Quantity Produced": 1,
  "Recipes": [
      {
         "Wheat Dough": 1
      },
      {
         "Barley Dough": 1
      },
      {
        "Potato Dough": 1
      },
      {
        "Sweet Potato Dough": 1
      },
      {
        "Corn Dough": 1
      },
      {
        "Teff Flour Dough": 1
      },
      {
        "Freekeh Flour Dough": 1
      }
  ],
  "Time to Produce": 0,
  "Is Symbolic": true
}
```


