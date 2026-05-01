import pandas as pd

def load_all_data():

    users = pd.read_excel("data/users.xlsx")
    products = pd.read_excel("data/products.xlsx")
    ratings = pd.read_excel("data/ratings.xlsx")
    behavior = pd.read_excel("data/behavior_15500.xlsx")

    return users, products, ratings, behavior