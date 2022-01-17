

from database_setup import Restaurant
from createSessionAndConnectToDB import createSessionAndConnectToDB


def selectAllRestaurants ():
    session = createSessionAndConnectToDB()

    # Let's do a query
    allRestaurants = session.query(Restaurant).all()

    restaurantList = []
    for restaurant in allRestaurants:
        restaurantList.append(restaurant)

    return restaurantList

