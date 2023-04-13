# Your name: Aaron Benyamini
# Your student id: 7901 4001
# Your email: aaronben@umich.edu
# List who you have worked with on this homework: Daniel Kates

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    rest_data = {}
    cur.execute('''SELECT restaurants.name AS restaurant_name, categories.category AS category_name, buildings.building AS building_name, restaurants.rating
              FROM restaurants
              INNER JOIN categories ON restaurants.category_id = categories.id
              INNER JOIN buildings ON restaurants.building_id = buildings.id''')
    rows = cur.fetchall()

    for r in rows:
        rest_name = r[0]
        rest_category = r[1]
        rest_building = r[2]
        rest_rating = r[3]
        rest_data[rest_name] = {"category": rest_category, "building": rest_building, "rating": rest_rating}
    
    conn.close()

    return rest_data

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('''SELECT categories.category, COUNT(restaurants.id)
                   FROM restaurants
                   JOIN categories ON restaurants.category_id = categories.id
                   GROUP BY categories.category
                   ORDER BY COUNT(restaurants.id) DESC''')
    
    cat_data = {}
    for r in cur.fetchall():
        cat_data[r[0]] = r[1]
    conn.close()
    
    plt.barh(list(cat_data.keys()), list(cat_data.values()))
    plt.title('Restaurant Categories')
    plt.xlabel('Count')
    plt.ylabel('Category')
    plt.gca().invert_yaxis()
    plt.show()

    return cat_data

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    restaurant_names = []
    cur.execute('''SELECT restaurants.name, restaurants.rating
                 FROM restaurants
                 INNER JOIN buildings ON restaurants.building_id = buildings.id
                 WHERE buildings.building = ?
                 ORDER BY restaurants.rating DESC''', (building_num,))

    rows = cur.fetchall()
    for r in rows:
        restaurant_names.append(r[0])
    conn.close()

    return restaurant_names

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # highest rated category
    cur.execute('SELECT category, ROUND(AVG(rating), 1) as avg_rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY category ORDER BY avg_rating DESC LIMIT 1')
    high_category = cur.fetchone()

    plt.subplot(211)
    cur.execute('SELECT category, ROUND(AVG(rating), 1) as avg_rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY category ORDER BY avg_rating ASC')
    categories_list = cur.fetchall()
    category_name = [category[0] for category in categories_list]
    avg_rating = [category[1] for category in categories_list]
    plt.barh(category_name, avg_rating)
    plt.title('Average Restaurant Ratings by Category')
    plt.xlabel('Rating')
    plt.ylabel('Category')
    plt.xlim(0, 5)

    #highest rated building
    cur.execute('SELECT building, ROUND(AVG(rating), 1) as avg_rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id GROUP BY building ORDER BY avg_rating DESC LIMIT 1')
    high_building = cur.fetchone()

    plt.subplot(212)
    cur.execute('SELECT building, ROUND(AVG(rating), 1) as avg_rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id GROUP BY building ORDER BY avg_rating ASC')
    buildings_list = cur.fetchall()
    building_name = [str(building[0]) for building in buildings_list]
    avg_rating = [building[1] for building in buildings_list]
    plt.barh(building_name, avg_rating)
    plt.title('Average Restaurant Ratings by Building')
    plt.xlabel('Rating')
    plt.ylabel('Building')
    plt.xlim(0, 5)

    plt.subplots_adjust(hspace=0.4)
    plt.show()

    return [(high_category[0], high_category[1]), (high_building[0], high_building[1])]

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
