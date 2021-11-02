import time

import requests

from accounts import LC_API_KEY
from pairs import PAIRS, BINANCE_ALL


def req(params):
    cnt = 0
    while cnt < 100:
    # while True:
        p = {'key': LC_API_KEY, **params}
        r = requests.get('https://api.lunarcrush.com/v2', params=p)
        try:
            r.raise_for_status()
            res = r.json()
            if 'data' in res.keys():
                for i, c in enumerate(res['data'], start=1):
                    c['categories'] = list(c['categories'].split(',')) if c['categories'] else []
                    c['rank'] = i
                return res['data']
            else:
                return None
        except requests.exceptions.HTTPError as e:
            cnt += 1
            print(cnt, e)
            time.sleep(cnt * 1)
            # time.sleep(20)


def get_acr(l=150):
    p = {
        'data': 'market',
        'type': 'fast',
        'sort': 'acr',
        'limit': l
    }
    return req(p)


def get_gs(l=100):
    p = {
        'data': 'market',
        'type': 'fast',
        'sort': 'gs',
        'limit': l,
        'desc': True
    }
    return req(p)


def print_coins(l, quote=None):
    if quote:
        quote = quote.upper()

    for i, c in enumerate(l, start=1):

        avlbl = []
        if quote:
            quotes = [quote,]
        else:
            quotes = ['BUSD', 'USDT', 'USDC', 'TUSD']

        for q in quotes:
            p = f"{q.upper()}_{c['s']}"
            if p in BINANCE_ALL:
                avlbl.append(p)

        print(f"{i:3d} rank:{c['rank']:3d}  acr:{c['acr']:4d}   gs:{c['gs']:3.1f}   s:{c['s']:12s} '{c['n']:25}' pairs:{str(avlbl):30s}  categories:{c['categories']}")
        # print(f"{i:3d}   acr:{c['acr']:4d}   gs:{c['gs']:3.1f}   s:{c['s']:12s} {pstr} '{c['n']:25}' {c['cat_set']}")


def filter_by_gs(l, gs):
    return filter(lambda p: p['gs'] > gs, l)


if __name__ == '__main__':
    print('==== GalaxyScore ====')
    top_gscore = get_gs()
    print_coins(top_gscore)

    print('==== AltCoin Rank  ====')
    print_coins(get_acr())
    1/0
    for q in PAIRS.keys():
        print(f'==== GalaxyScore {q} ====')
        print_coins(filter_by_quote(top_gscore, q), q)
        print("\n\n")
