import asyncio
import genshin
import json

async def main():

    cookies = {"ltuid": 119480035, "ltoken": "cnF7TiZqHAAvYqgCBoSPx5EjwezOh1ZHoqSHf7dT"} # uhm im lazy
    client = genshin.Client(cookies)

    data = await client._request_genshin_record("gcg/basicInfo", uid=603200036)

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




    lineup_1 = str(lineup_1)
    lineup_2 = str(lineup_2)
    opponent_lineup_1 = str(opponent_lineup_1)  # delete later, once list_of_links_converter is finished. this is just so they can be hashed
    opponent_lineup_2 = str(opponent_lineup_2)

    if lineup_1 in replay_dict.keys():
        editing = replay_dict[lineup_1]
        print(editing)






    with open('DeckTracker/database.json', 'w') as f:
        json.dump(data, f)

asyncio.run(main())