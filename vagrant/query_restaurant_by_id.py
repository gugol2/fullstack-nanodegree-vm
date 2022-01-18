from database_setup import Restaurant

def queryRestaurantById (session, restaurantId):
    restaurantQueried = session.query(Restaurant).filter_by(id = restaurantId).one()

    return restaurantQueried

def updateRestaurantById (session, restaurantId, newRestaurantName):
    restaurantToEdit = queryRestaurantById(session, restaurantId)

    if restaurantToEdit != []:
        print(' restaurantToEdit != []',  restaurantToEdit != [])
        restaurantToEdit.name = newRestaurantName
        session.add(restaurantToEdit)
        session.commit()