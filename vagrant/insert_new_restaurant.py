from database_setup import Restaurant
from createSessionAndConnectToDB import createSessionAndConnectToDB


def insertNewRestaurant (restaurantName):
    session = createSessionAndConnectToDB()

    newRestaurant = Restaurant(name=restaurantName)

    session.add(newRestaurant)
    session.commit()