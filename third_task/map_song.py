"""
An application to generate map
"""
import os
import base64
import json
from requests import post,get
from dotenv import load_dotenv
import pycountry
from geopy.geocoders import Nominatim
import folium

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
    res = post(url, headers = headers, data = data, timeout = 10)
    json_result = json.loads(res.content)
    token_access = json_result['access_token']
    return token_access

def get_auth_header(tokens):
    """
    Gets auth header
    """
    return {'Authorization': 'Bearer ' + tokens}

def search_for_artist(tkn, artists_name):
    """
    Searches for artist
    """
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(tkn)
    query = f'?q={artists_name}&type=artist,track&limit=1'

    query_url = url + query
    result = get(query_url, headers = headers, timeout = 10)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        map_is_here = folium.Map(location = [0, 0])
        map_is_here.save("templates/songs_map.html")
        print("""
Such artist does not exist
""")
        return  None
    return json_result[0]

def get_top_song(tkns, artists_id):
    """
    Get top-10 songs by artist
    """
    url = f"https://api.spotify.com/v1/artists/{artists_id}/top-tracks?country=US"
    headers = get_auth_header(tkns)
    resulties = get(url, headers=headers, timeout = 10)
    json_result = json.loads(resulties.content)['tracks']
    lst = [song['name'] for song in json_result]
    return lst[0]

def get_songs_markets(tkns, song_name):
    """
    Get 1st top song by an artist
    """
    url = f"https://api.spotify.com/v1/search?q={song_name}&type=track&limit=1"
    headers = get_auth_header(tkns)
    reslt = get(url, headers=headers, timeout = 10)
    json_result = json.loads(reslt.content)['tracks']['items'][0]['available_markets']
    return json_result

def map_func(market, frstsong):
    """
    Function that creates map
    """
    map_is = folium.Map(location = [0, 0])
    for i in market:
        geolocator = Nominatim(user_agent="Anastasiya")
        country = pycountry.countries.get(alpha_2 = i)
        if country is None:
            continue
        name = country.name
        if ',' in name:
            name = name.split(',')[0]
        location = geolocator.geocode(name, timeout=10, country_codes = i)
        if location is None:
            continue
        map_is.add_child(folium.Marker(location=[location.latitude, \
        location.longitude], popup = f'Song:{frstsong} - Country:{name}',
                                icon=folium.Icon(color = 'darkred', icon = 'circle')))
    map_is.save("templates/songs_map.html")

def main_function(artist):
    """
    Main function
    """
    try:
        token = get_token()
        result = search_for_artist(token, artist)
        artist_id = result['id']
    except TypeError:
        return None
    songs = get_top_song(token, artist_id)
    markets = get_songs_markets(token, songs)
    map_func(markets, songs)
