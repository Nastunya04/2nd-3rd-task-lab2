"""
Python-Spotify-Api
"""
import os
import base64
import json
import sys
from requests import post,get
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret  = os.getenv("CLIENT_SECRET")

def get_token():
    """
    Gets token
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic '+ auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers = headers, data = data, timeout = 10)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    """
    Gets auth header
    """
    return {'Authorization': 'Bearer ' + token}

def search_for_artist(token, artists_name):
    """
    Searches for artist
    """
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artists_name}&type=artist,track&limit=1'

    query_url = url + query
    result = get(query_url, headers = headers, timeout = 10)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print("""
Such artist does not exist
""")
        return  None
    return json_result[0]

def get_albums(token, artist_id):
    """
    Returns json with an information about albums
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = get_auth_header(token)
    res = get(url, headers=headers, timeout = 10)
    json_result = json.loads(res.content)['items']
    return json_result

def get_songs(token, artist_id, country):
    """
    Get top-10 songs by artist
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country}"
    headers = get_auth_header(token)
    result = get(url, headers=headers, timeout = 10)
    json_result = json.loads(result.content)['tracks']
    return json_result

def display_artist_id(artist_id):
    """
    Displays artist's id
    """
    print(f"""
The artist's id is '{artist_id}'
""")

def display_albums(albums):
    """
    Displays albums of an artist
    """
    print("""
Albums of an artist are given below:
""")
    for idx, album in enumerate(albums):
        print(f'{idx+1}.{album["name"]}')

def display_albums_with_dates(albums):
    """
    Displays albums of an artist with release dates
    """
    print("""
Albums of an artist and their release dates are given below:
""")
    for idx, album in enumerate(albums):
        print(f'{idx+1}. {album["release_date"]} - {album["name"]}')

def display_top_songs(songs):
    """
    Displays 10 top songs of an artist
    """
    print("""
Top-10 songs of an artist are given below:
""")
    for idx, song in enumerate(songs):
        print(f'{idx+1}. {song["name"]}')

def display_top10_songs_with_dates(songs):
    """
    Displays top-10 dongs with their release dates
    """
    print("""
Top-10 songs of an artist and their release dates are given below:
""")
    for idx, song in enumerate(songs):
        print(f'{idx+1}. {song["album"]["release_date"]} --- {song["name"]}')

def continue_func():
    """
    Function to continue search
    """
    print("""
    - - - - - - - - - - - - - - - - 
    Do you want to continue? Yes/No
    - - - - - - - - - - - - - - - -
        """)
    inputed = ''
    while inputed not in ('yes', 'no'):
        inputed = str(input(">>> "))
        if inputed.lower() == 'yes':
            main_function()
        elif inputed not in ('yes', 'no'):
            print("""
- - - - - - - - - - - - - 
Invalid input, try again:)
- - - - - - - - - - - - -
""")
        else:
            sys.exit()

def main_function():
    """
    Main function
    """
    artist_name = input("""
Enter a name of an artist below:
>>> """)
    try:
        token = get_token()
        result = search_for_artist(token, artist_name)
        artist_id = result['id']
    except TypeError:
        sys.exit()

    print("""
Such artist exists
    """)
    inp = ''
    while inp not in ('1', '2', '3', '4', '5'):
        print("Choose what to do you want to look for:")
        print("1. Artist's id")
        print('2. Albums of an artist')
        print('3. Albums of an artist and their release dates')
        print('4. Top-10 songs of an artist')
        print('5. Release dates of top-10 songs of an artist')
        print('6. Exit')
        inp = str(input('>>> '))
        if inp == '1':
            display_artist_id(artist_id)
        if inp == '2':
            albums = get_albums(token, artist_id)
            display_albums(albums)
        if inp == '3':
            albums = get_albums(token, artist_id)
            display_albums_with_dates(albums)
        if inp == '4':
            print('Enter a country where you want to find top-10 popular songs:')
            country = input(">>> ")
            songs = get_songs(token, artist_id, country)
            display_top_songs(songs)
        if inp == '5':
            print('Enter a country where you want to find top-10 popular songs')
            country = input(">>> ")
            songs = get_songs(token, artist_id, country)
            display_top10_songs_with_dates(songs)
        if inp == '6':
            sys.exit()
        elif inp not in ('1', '2', '3', '4', '5'):
            print("""
- - - - - - - - - - - - - 
Invalid input, try again:)
- - - - - - - - - - - - -
""")
    continue_func()

if __name__ == '__main__':
    main_function()
