import asyncio
import genshin
import json

async def main():

    cookies = {"ltuid": 119480035, "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"} # uhm im lazy. this cookie is public anyways on the api thing
    client = genshin.Client(cookies)

    data = await client._request_genshin_record("gcg/basicInfo", uid=805613663)

    with open('DeckTracker/database.json', 'r') as f:
        replay_dict = json.load(f)

    lineup_1 = data['replays'][0]['self']['linups']
    lineup_2 = data['replays'][1]['self']['linups']

    opponent_lineup_1 = data['replays'][0]['opposite']['linups']
    opponent_lineup_2 = data['replays'][1]['opposite']['linups']

    #lineup_1 = list_of_links_converter(lineup_1)
    #lineup_2 = list_of_links_converter(lineup_2)
    #opponent_lineup_1 = list_of_links_converter(opponent_lineup_1)
    #opponent_lineup_2 = list_of_links_converter(opponent_lineup_2)

    if not 'last_played_games' in replay_dict.keys():
        replay_dict['last_played_games'] = ['blank', 'blank']
        replay_dict['total_games'] = 0
        replay_dict['total_wins'] = 0

    lineup_1 = str(lineup_1)
    lineup_2 = str(lineup_2)
    opponent_lineup_1 = str(opponent_lineup_1)  # delete later, once list_of_links_converter is finished. this is just so they can be hashed
    opponent_lineup_2 = str(opponent_lineup_2)

    if not lineup_1 in replay_dict.keys():
        replay_dict[lineup_1] = {'wins': 0, 'total_games': 0}
    if not str(data['replays'][0]['match_time']) in replay_dict['last_played_games']:
        if data['replays'][0]['is_win']:
            replay_dict[lineup_1]['wins'] += 1
            replay_dict['total_wins'] += 1
        replay_dict[lineup_1]['total_games'] += 1
        replay_dict['total_games'] += 1
        replay_dict['last_played_games'][0] = replay_dict['last_played_games'][1]
        replay_dict['last_played_games'][1] = str(data['replays'][0]['match_time'])

    if not lineup_2 in replay_dict.keys():
        replay_dict[lineup_2] = {'wins': 0, 'total_games': 0}
    if not str(data['replays'][1]['match_time']) in replay_dict['last_played_games']:
        if data['replays'][1]['is_win']:
            replay_dict[lineup_2]['wins'] += 1
            replay_dict['total_wins'] += 1
        replay_dict[lineup_2]['total_games'] += 1
        replay_dict['total_games'] += 1
        replay_dict['last_played_games'][0] = replay_dict['last_played_games'][1]
        replay_dict['last_played_games'][1] = str(data['replays'][1]['match_time'])

    with open('DeckTracker/database.json', 'w') as f:
        json.dump(replay_dict, f)

asyncio.run(main())