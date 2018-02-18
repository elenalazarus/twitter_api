from twit import location
from twit import take_information
import folium
from geopy.geocoders import ArcGIS
import html


def user_input():
    '''
    () -> (str, int)
    This function controls user's input
    '''
    try:
        # The goal of a program
        print("Hello. This is a programme which will help you to know "
              "where live people you follow in Twitter;)")
        # User inputs
        acct = input('Enter Twitter Account: ')
        users = int(input('Input the number of users you need'
                          '(no more than 20): '))
        return acct, users
    except:
        # Input is not good
        print("It seems you input some wrong data")
        user_input()


def search(acct, users):
    '''
    (str, int) -> list
    This function searches location of friends
    '''
    # Dictionary with all information
    js = take_information(acct, users)
    # List with all locations
    where = location(js)
    return where


def do_coordinates(friends):
    '''
    list -> list
    This function turns location of friends into coordinates and returns
    a list with them
    '''
    all_locations = []
    for friend in friends:
        location = ArcGIS(timeout=10)
        place = location.geocode(friend[-1])
        # Coordinates of every friend
        lat = place.latitude
        lon = place.longitude
        # Add coordinates to the list
        all_locations.append([friend[0], (lat, lon)])
    return all_locations


def do_map(coordinates):
    '''
    (list) -> None
    This function creates a map and add to it location of friends
    '''
    # Creating of the map
    maps = folium.Map()
    fg = folium.FeatureGroup(name="Friends_map")
    # Layer with friends
    for coor in coordinates:
        # Every coordinate
        lat = coor[1][0]
        lon = coor[1][1]
        friend = html.escape(coor[0])
        # Adding markers of friends
        fg.add_child(folium.Marker(location=[lat, lon], popup=friend,
                                   icon=folium.Icon(color='red')))
    # Adding all stuff at the map
    maps.add_child(fg)
    maps.add_child(folium.LayerControl())
    # Save a map
    maps.save("templates/Map_1.html")


def main():
    '''
    () -> None
    Manage work of all functions in program
    '''
    try:
        data = user_input()
        acct, users = data[0:2]
        # Take all information
        friends = search(acct, users)
        # Location of all friends
        coordinates = do_coordinates(friends)
        # All coordinates
        do_map(coordinates)
        # Map
    except:
        return "Your data is not right"

# print(main())
