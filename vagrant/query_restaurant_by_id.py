from database_setup import Restaurant
from createSessionAndConnectToDB import createSessionAndConnectToDB

def createSession (): 
    session = createSessionAndConnectToDB()
    return session

def queryRestaurantById (restaurantId):
    session = createSession()

    restaurantToEdit = session.query(Restaurant).filter_by(id = restaurantId).one()

    return restaurantToEdit

def updateRestaurantById (restaurantId, newRestaurantName):
    print('restaurantId', restaurantId)
    print('newRestaurantName', newRestaurantName)

    session = createSession()

    restaurantToEdit = queryRestaurantById(restaurantId)

    print('restaurantToEdit', restaurantToEdit)

    if restaurantToEdit != []:
        print(' restaurantToEdit != []',  restaurantToEdit != [])
        restaurantToEdit.name = newRestaurantName
        session.add(restaurantToEdit)
        session.commit()