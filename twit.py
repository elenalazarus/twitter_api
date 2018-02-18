import json
import ssl
import urllib.error
import urllib.parse
import urllib.request

import twurl


def take_information(acct, users):
    '''
    (str, str) -> dict

    This function takes a person's Twitter login and the number of
    users the information the user wants to know about. And then
    the function takes all information about friends of the user in Twitter
    and returns json file in the form of a dictionary
    '''
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print('')
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': users})
    print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    return js


def names(js):
    '''
    dict -> list
    This function takes the dictionary and helps to find out login of
    every friend. It returns a list with all screen names
    '''
    names = []
    for u in js['users']:
        # Looking for screen names in the cycle
        names.append("Screen name of {0} is {1}".format(u['name'],
                                                        u['screen_name']))
    return names


def id(js):
    '''
    dict -> list
    This function takes the dictionary and helps to find out id of
    every friend. It returns a list with all ids
    '''
    all_id = []
    for u in js['users']:
        # Looking for id in the cycle
        all_id.append("ID of {0} is {1}".format(u['name'], u['id']))
    return all_id


def location(js):
    '''
    dict -> list
    This function takes the dictionary and helps to find out location of
    every friend. It returns a list with all locations
    '''
    friend_location = []
    try:
        for u in js['users']:
            # If your friend didn't put the location
            if len(u['location']) < 1:
                print("Sorry, we couldn't find the location of {}".format(
                    u['name']))
            else:
                # Everything is OK
                friend_location.append([u['name'], u['location']])
                print(
                    "Location of {0} is {1}".format(u['name'], u['location']))
    except KeyError:
        print('This account has less friends than you input')
        return friend_location
    return friend_location


def friends(js):
    '''
    dict -> list
    This function takes the dictionary and helps to find out friends of
    every friend. It returns a list with the number of friends of each friend
    '''
    all_friends = []
    for u in js['users']:
        # Looking for friends in the cycle
        all_friends.append("{0} has {1} "
                           "friends".format(u['name'], u['friends_count']))
    return all_friends


def followers(js):
    '''
    dict -> list
    This function takes the dictionary and helps to find out followers of
    every friend. It returns a list with the number of followers of each friend
    '''
    all_followers = []
    for u in js['users']:
        all_followers.append(
            # Looking for followers in the cycle
            "{0} has {1} followers".format(u['name'], u['followers_count']))
    return all_followers


def likes(js):
    '''
    dict -> list
    This function takes the dictionary and helps to find out likes of
    every friend. It returns a list with the number of delivered likes
    of each friend
    '''
    all_likes = []
    for u in js['users']:
        # Looking for the number of likes in the cycle
        all_likes.append(
            "{0} liked {1} tweets".format(u['name'], u['favourites_count']))
    return all_likes


def create(js):
    '''
    dict -> list
    This function takes the dictionary and helps to find out the date of
    creation of the account of every friend. It returns a list with the
    dates
    '''
    all_dates = []
    for u in js['users']:
        # Looking for the date in the cycle
        all_dates.append(
            "{0} created the account {1}".format(u['name'], u['created_at']))
    return all_dates


def more_information(js):
    '''
    dict -> dict
    This function prints all information about users
    '''
    print(json.dumps(js, indent=2))


def status(js):
    '''
    dict -> None
    This function takes the dictionary and helps to find out the status
    every friend. It prints all statuses
    '''
    try:
        for u in js['users']:
            for inf in u['status']:
                if inf == 'text':
                    # Prints statuses in cycle
                    print(' ')
                    print("Status of {} is".format(u['name']))
                    print(u['status'][inf])
    except KeyError:
        # If the user posted nothing
        print('{0} has no status'.format(u['name']))


def input_output():
    '''
    () -> (str, int, str)
    This function explains to the user how to use the program, displays
    the necessary information for input and returns all data that the user
    entered
    '''
    # Short information about the program
    print("Hello. This is a programme which will help you to know more "
          "about people you follow in Twitter;)")
    # User inputs the login of a person in Twitter
    acct = input('Enter Twitter Account: ')
    # The number of users which user wants to see
    users = int(input("Please, input how many people I should look "
                      "for (no more than 20) \n"))
    # No more than 20 users
    assert (users <= 20)
    # Menu with all possible information
    print("Select the number that corresponds to the menu item "
          "of the information that you want to receive")
    print("1. Screen name")
    print("2. ID")
    print("3. Location")
    print("4. Friends")
    print("5. Followers")
    print("6. Likes")
    print("7. Date of creation")
    print("8. Status")
    print("9. You need all information")
    number = int(input())
    assert (number <= 9)
    users = str(users)
    return users, number, acct


def main():
    '''
    () -> ()
    This function controls calls of each function. This is a boss
    '''
    try:
        # Get all essential data
        data = input_output()
        users, number, acct = data[0], data[1], data[2]
        js = take_information(acct, users)
        # Conditions for calling functions, depending on what the user
        # entered when selecting it in the menu
        if number == 1:
            name = names(js)
            for every in name:
                print(every)
        elif number == 2:
            all_id = id(js)
            for every in all_id:
                print(every)
        elif number == 3:
            location(js)
        elif number == 4:
            all_friends = friends(js)
            for every in all_friends:
                print(every)
        elif number == 5:
            all_followers = followers(js)
            for every in all_followers:
                print(every)
        elif number == 6:
            all_likes = likes(js)
            for every in all_likes:
                print(every)
        elif number == 7:
            all_dates = create(js)
            for every in all_dates:
                print(every)
        elif number == 8:
            status(js)
        elif number == 9:
            more_information(js)
        return ' '
    except:
        # If user input is wrong
        return "Oops! Your data is not right!"

# print(main())
