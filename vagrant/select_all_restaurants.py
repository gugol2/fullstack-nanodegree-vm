from database_setup import Restaurant

def selectAllRestaurants (session):
    # Let's do a query
    allRestaurants = session.query(Restaurant).all()

    restaurantList = []
    for restaurant in allRestaurants:
        restaurantList.append(restaurant)

    return restaurantList

