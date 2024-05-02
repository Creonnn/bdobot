
from gsheets import read_gsheet, read_market
import pandas as pd

help = "!item or !i: Displays summary of item. Recipe, market price, and whether it is worth to craft.\n"\
"!price or !p: Displays amount listed on market, base price, and daily volume."

def get_recipe(name: str, df):
    i = -1
    for _, row in df.iterrows():

        if pd.notna(row["Name"]) and name in row["Name"].lower():
            i = row["ID"]

        if i >= 0:
            ingredient = list(df[df["ID"] == i]["Ingredient"])
            quantity = list(df[df["ID"] == i]["Quantity"])
            recipe = {ingredient[j]: quantity[j] for j in range(len(ingredient))}
            name = row["Name"]
            break

    return recipe, name

def get_worthit(name: str, df):
    
    for _, row in df.iterrows():
        if name in row["Name"].lower():
            str_val = row["Market - Ingredient"]
            str_val = str_val.replace(",", "")
            return  int(str_val)

def format_item_summary(recipe, worthit, name):
    str = f"Item: {name}\n"\
          f"Recipe:\n"
    
    for ingredient in recipe:
        str += f"        {recipe[ingredient]} {ingredient}\n"

    str += f"\nProfit: {worthit}"
    return str

def check_existence(df, name):
    match = []
    for _, row in df.iterrows():
        if pd.notna(row["Name"]) and name in row["Name"].lower():
            match.append(row["Name"])

    return match

def ask_clarification(lst):
    str = "Based on your input, I got more than 1 match. Please be more precise:\n"
    for item in lst:
        str += f"        {item}\n"
    return str

def item_summary(message: str):
    df_worthit, df_recipes = read_gsheet()

    recipe, name = get_recipe(message, df_recipes)
    worthit = get_worthit(message, df_worthit)

    matches = check_existence(df_recipes, message)
    if len(matches) == 0:
        return "Recipe not found!"

    if len(matches) > 1:
        return ask_clarification(matches)
    
    return format_item_summary(recipe, worthit, name)

def get_market_info(df, name):
    for _, row in df.iterrows():
        if name == row["Name"].lower():
            item_name = row["Name"]
            listed = row["Count"]
            base_price = row["BasePrice"]
            daily_volume = row["DailyVolume"]
    return item_name, listed, base_price, daily_volume

def format_price_summary(item_name, listed, base_price, daily_volume):
    return f"Item: {item_name}\n"\
    f"Available: {listed}\n"\
    f"Base Price = {base_price}\n"\
    f"Daily Volume = {daily_volume}"

def price(message: str):
    #ToDo add enhancement level for gear
    df_market = read_market()

    match = []
    for _, row in df_market.iterrows():
        if pd.notna(row["Name"]) and message == row["Name"].lower():
            match.append(row["Name"])

    if len(match) == 0:
        matches = check_existence(df_market, message)
        return ask_clarification2(matches)
    
    item_name, listed, base_price, daily_volume = get_market_info(df_market, message)
    return format_price_summary(item_name, listed, base_price, daily_volume)


def ask_clarification2(lst):
    str = "Item not found! Either it does not exist or you should use precise spelling.\n"\
        'e.g. To find item called "Concentrated Magical Black Gem", it is not enough to type "Concentrated Black Gem"\n'\
        "Some of the similar items that were found:\n"
    for item in lst[:10]:
        str += f"        {item}\n"
    return str