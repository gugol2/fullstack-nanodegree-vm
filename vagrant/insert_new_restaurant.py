from database_setup import Restaurant

def insertNewRestaurant (session, restaurantName):
    newRestaurant = Restaurant(name=restaurantName)

    session.add(newRestaurant)
    session.commit()