from igdb.wrapper import IGDBWrapper
from config.config import IGDB_CLIENT_ID, IGDB_ACCESS_TOKEN
import json
from datetime import date

wrapper = IGDBWrapper(IGDB_CLIENT_ID, IGDB_ACCESS_TOKEN)

def get_igdb_game(game_id: int):
    game_array = wrapper.api_request('games', f'fields name,first_release_date,summary,cover.url,genres.name; where id={game_id};')
    game_json = json.loads(game_array)

    cover_url = game_json[0]['cover']['url'].replace("t_thumb", "t_1080p")
    name = game_json[0]['name']
    try:
        release_date = date.fromtimestamp(game_json[0]['first_release_date'])
    except KeyError as e:
        print(e)
        release_date = None
    description = game_json[0]['summary']

    genre_list = []
    for genre in game_json[0]['genres']:
        genre_list.append(genre['name'])

    game_dict = {'name': name, 
                 'release_date': release_date, 
                 'cover_url': cover_url, 
                 'genre_list': genre_list, 
                 'description': description
    }
    
    return game_dict

def get_screenshots_for_game(game_id: int) -> list:
    screenshots_array = wrapper.api_request('screenshots', f'fields url; where game={game_id};')
    screenshots_json = json.loads(screenshots_array)

    screenshot_list = []
    for screenshot in screenshots_json:
        screenshot_list.append(screenshot['url'].replace("t_thumb", "t_1080p"))

    return screenshot_list