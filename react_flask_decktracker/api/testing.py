import asyncio
import genshin
import json
from flask import *
from flask_cors import CORS
import time

app = Flask(__name__)

CORS(app) 

uids = ['809458646', '859401792', '812310683', '878964522', '622963441', '860236862', '606415530', '646346491', '624516438', '612358049', '649486104', '626398278', '704822600', '819042492', '603200036']

open('db.json', 'a')
with open('db.json', 'r') as f:
    replay_dict = json.load(f)

@app.route('/')
async def main():
    while True:
        for uid in uids:
            await testing(uid)

@app.route('/append_uid')
def append_uid(uid):
    uids.append(uid)

@app.route('/remove_uid')
def remove_uid(uid):
    uids.remove(uid)

@app.route('/get_db')
def get_db():
    with open('db.json', 'r') as f:
        replay_dict = json.load(f)
    return replay_dict

@app.route('/testing/<uid>', methods=['GET'])
async def testing(uid):
    client = genshin.Client()
    client.set_cookies({'cookie_token_v2': 'v2_CAQSDGM5b3FhcTNzM2d1OCDKsOOoBii9hLyzAzDctN6tAUILYmJzX292ZXJzZWE=', 'account_mid_v2': '12ekf22ko5_hy', 'account_id_v2': '364354140', 'ltoken_v2': 'v2_CAISDGM5b3FhcTNzM2d1OCDKsOOoBiiIqZTqAzDctN6tAUILYmJzX292ZXJzZWE=', 'ltmid_v2': '12ekf22ko5_hy', 'ltuid_v2': '364354140'})
    data = await client._request_genshin_record("gcg/basicInfo", uid=uid)
    with open('db.json', 'r') as f:
        replay_dict = json.load(f)

    lineup_1 = data['replays'][0]['self']['linups']
    lineup_2 = data['replays'][1]['self']['linups']

    opponent_lineup_1 = data['replays'][0]['opposite']['linups']
    opponent_lineup_2 = data['replays'][1]['opposite']['linups']

    lineup_1 = list_of_links_converter(lineup_1)
    lineup_2 = list_of_links_converter(lineup_2)
    opponent_lineup_1 = list_of_links_converter(opponent_lineup_1)
    opponent_lineup_2 = list_of_links_converter(opponent_lineup_2)

    if not 'last_played_games' + str(uid) in replay_dict.keys():
        replay_dict['last_played_games' + str(uid)] = ['blank', 'blank']
    
    if not 'total_games' in replay_dict.keys(): #only is called if replay_dict was never made before. 
        replay_dict['total_games'] = 0
        replay_dict['total_wins'] = 0
        replay_dict['opponents'] = {}
        replay_dict['opponents']['opp_total_wins'] = 0
        replay_dict['opponents']['opp_total_games'] = 0

    if not uid in replay_dict.keys():
        replay_dict[uid] = {}

    lineup_1 = str(lineup_1)
    lineup_2 = str(lineup_2)
    opponent_lineup_1 = str(opponent_lineup_1)  # delete later, once list_of_links_converter is finished. this is just so they can be hashed
    opponent_lineup_2 = str(opponent_lineup_2)

    if (not str(data['replays'][1]['match_time']) in replay_dict['last_played_games' + str(uid)]) and (data['replays'][1]['match_type'] == 'Co-Op Mode' or data['replays'][1]['match_type'] == 'Matching Mode' or data['replays'][1]['match_type'] == 'Teammate Invitation'):
        if not lineup_2 in replay_dict.keys():
            replay_dict[lineup_2] = {'wins': 0, 'total_games': 0}
        if not opponent_lineup_2 in replay_dict['opponents'].keys():
            replay_dict['opponents'][opponent_lineup_2] = {'wins': 0, 'total_games': 0}
        if data['replays'][1]['is_win']:
            replay_dict[lineup_2]['wins'] += 1
            replay_dict['total_wins'] += 1
        else:
            replay_dict['opponents'][opponent_lineup_2]['wins'] += 1
            replay_dict['opponents']['opp_total_wins'] += 1
        replay_dict[lineup_2]['total_games'] += 1
        replay_dict['opponents'][opponent_lineup_2]['total_games'] += 1
        replay_dict['total_games'] += 1
        replay_dict['opponents']['opp_total_games'] += 1
        replay_dict['last_played_games' + str(uid)][0] = replay_dict['last_played_games' + str(uid)][1]
        replay_dict['last_played_games' + str(uid)][1] = str(data['replays'][1]['match_time'])

    if not str(data['replays'][0]['match_time']) in replay_dict['last_played_games' + str(uid)]  and (data['replays'][1]['match_type'] == 'Co-Op Mode' or data['replays'][1]['match_type'] == 'Matching Mode'):
        if not lineup_1 in replay_dict.keys():
            replay_dict[lineup_1] = {'wins': 0, 'total_games': 0}
        if not opponent_lineup_1 in replay_dict['opponents'].keys():
            replay_dict['opponents'][opponent_lineup_1] = {'wins': 0, 'total_games': 0}
        if data['replays'][0]['is_win']:
            replay_dict[lineup_1]['wins'] += 1
            replay_dict['total_wins'] += 1
        else:
            replay_dict['opponents'][opponent_lineup_1]['wins'] += 1
            replay_dict['opponents']['opp_total_wins'] += 1
        replay_dict[lineup_1]['total_games'] += 1
        replay_dict['opponents'][opponent_lineup_1]['total_games'] += 1
        replay_dict['total_games'] += 1
        replay_dict['opponents']['opp_total_games'] += 1
        replay_dict['last_played_games' + str(uid)][0] = replay_dict['last_played_games' + str(uid)][1]
        replay_dict['last_played_games' + str(uid)][1] = str(data['replays'][0]['match_time'])

    with open('db.json', 'w') as f:
        json.dump(replay_dict, f)
    return replay_dict

def list_of_links_converter(lst_of_links):
    toReturn = []
    for i in lst_of_links:
        if i in link_translator.keys():
            toReturn.append(link_translator[i])
        else:
            toReturn.append(i)
    toReturn = sorted(toReturn)
    return toReturn

link_translator = {
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/aee9819994c7d8238f8775561c66f529.png' : 'Ganyu',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/9ac8286f673db13561d4c2f7087bade1.png' : 'Kaeya',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/34f48373ff107eb3c3f3bfa71d0200ff.png' : 'Chongyun',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/5810ee90e7d788093e706d80fff40eee.png' : 'Kamisato Ayaka',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/f412096f6862a58147d2698473017d8d.png' : 'Xingqiu',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/e45acf89c0378556c011c8b3df796c06.png' : 'Mona',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/b23f6237eac50f198c5285b9d85c26b6.png' : 'Diluc',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/0abbf351a613f0d2097f213d621f1685.png' : 'Xiangling',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/fa1944e88cad933aab66415a358ced8f.png' : 'Bennett',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/c76f65c5ee7e5bdd2128f98e5908bd37.png' : 'Amber',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/e4d63f6bfa32b911e9a3e7c7b4045183.png' : 'Yoimiya',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/7854c64188dc2ff35b79089d8f929127.png' : 'Fischl',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/4589831be30106ce1505bae5f7dda5c8.png' : 'Razor',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/af13951c793ebf4cfb0fcf9dfe40e7c4.png' : 'Keqing',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/d4decc3250e0a4e3048a1a3d381133c8.png' : 'Sucrose',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/bc845920b83e5ef1f99aac74d5b0407e.png' : 'Jean',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/05c59650977c5dd2d7f4b125020e3f01.png' : 'Ningguang',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/3ca2155f3b3fb43bf87c436686643542.png' : 'Noelle',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/5b7f607b35e5ec7a86106be0d7b97f5f.png' : 'Collei',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/05fa71ab111fbc8ad7aaff6ac2674b23.png' : 'Rhodeia of Loch',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/1ad2d13af02e1aba0a2ebc19f411e490.png' : 'Fatui Pyro Agent',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/1f77fd5d1c4c8d534a24541319085354.png' : 'Maguu Kenki',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/764a1a4ea89c2eb8e6d467f0404b3b8f.png' : 'Stonehide Lawachurl',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/5428245cffccd4b0891cf545ced41bd8.png' : 'Diona',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/ceee8b9a0f82c76cbc1bab0d4457d4e2.png' : 'Cyno',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/c05a01da8f23e3b73f22ca70dd97887a.png' : 'Barbara',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/db4cf8b675a53c29c74b0a5bbce120d6.png' : 'Mirror Maiden',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/a6747d250580a1f08ec704e11a80cbcd.png' : 'Jadeplume Terrorshroom',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/8182cb6d87ef0d1329fb59370b0a99d1.png' : 'Eula',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/5aa5a53d52ce7252382d2329510b650d.png' : 'Tartaglia',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/f61fedf51c721e47fddebfb62dee0947.png' : 'Sangonomiya Kokomi',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/2b7def0f8c6ba608a5b0651c9f03bc05.png': 'Kamisato Ayato',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/ce73f0d061946e019f8514eb31e362a2.png' : 'Klee',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/0e17cb2ab066832c8124b18731272730.png' : 'Hu Tao',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/6e021e0edb413f3cbb6ddabcf2c7fb17.png' : 'Beidou',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/647c26f41e25a29f8967df945071b511.png' : 'Kujou Sara',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/d59cc7b9af785258032a01274cbcfaaa.png': 'Raiden Shogun',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/3b56222eca26de466323aa6fdc266dbd.png' : 'Yae Miko',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/1ef1cf4d7dee217eae0fdd916faac164.png' : 'Venti',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/dc9706f936d8522735f62d4966a045a4.png' : 'Xiao',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/d7ddb56e23a65d6d95514eb442efa8d3.png' : 'Zhongli',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/1bb80ee2da3ad046cb1d1abbe352879e.png' : 'Albedo',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/f307c59dfd90ecfea57ec80ff05d1655.png' : 'Arataki Itto',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/91cd62a2ab77909ef0e7a923f8a769e6.png' : 'Tighnari',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/c3ff9a66a59d4ee30bb9e6231027bfc0.png' : 'Nahida',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/f984801392bf1236d281492b6bd06e90.png' : 'Fatui Cryo Cicin Mage',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/ca2c7aa66caa1b441416fe29c0cce081.png' : 'Abyss Lector: Fathomless Flames',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/595c8190c48ca319eaec4bf518dd2a20.png' : 'Electro Hypostasis',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/44a09d79d90563d2b267b0b6ff47db8d.png' : 'Shenhe',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/d4733ba2bd0d7cf0568325465551dbf4.png' : 'Candace',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/85dcadf0f6f23640c2b24d754488320d.png' : 'Yanfei',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/a0c5a75e35005f5731edbbe88d78b431.png' : 'Kaedehara Kazuha',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/71eee9b8a47df9047dba0218203a1001.png' : 'Qiqi',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/ccce121050d68be1cd995ebd5ca50416.png' : 'Lisa',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/cff8b343edafbdcaf95742dc0a4cda7b.png' : 'Wanderer',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/e97234cb2eaab032b0eb2d1041739d7c.png' : 'Dehya',
    'https://act.hoyoverse.com/hk4e/e20200928calculate/item_char_icon_u38a6e/20bf81d83529af1bea25043e2ece8ba2.png' : 'Yaoyao'
}