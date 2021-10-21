# LunarCrush

import requests

from pairs import PAIRS

API_KEY = '4i023iq6rqqnfnludrldui'


def req(params):
    r = requests.get('https://api.lunarcrush.com/v2', params=params)
    r.raise_for_status()
    res = r.json()

    # if res['data']:
    #     for c in res['data']:
    #         c['data']['cat_set'] = c['data']['categories'].split(',')

    print(res['usage'])
    return res['data']


def get_acr(l=100):
    p = {
        'key': API_KEY,
        'data': 'market',
        'type': 'fast',
        'sort': 'acr',
        'limit': l
    }
    return req(p)


def get_gs(l=100):
    p = {
        'key': API_KEY,
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
        pstr = ''
        if quote:
            p = f"{quote.upper()}_{c['s']}"
            avlbl = str(p in PAIRS[quote])
            pstr = f"{p:12s} {avlbl:8s}"

        print(f"{i:3d}   acr:{c['acr']:4d}   gs:{c['gs']:3.1f}   s:{c['s']:12s} {pstr} '{c['n']:25}' {c['categories']}")
        # print(f"{i:3d}   acr:{c['acr']:4d}   gs:{c['gs']:3.1f}   s:{c['s']:12s} {pstr} '{c['n']:25}' {c['cat_set']}")


def filter_by_quote(l, quote):
    quote = quote.upper()
    r = filter(lambda p: f"{quote}_{p['s']}" in PAIRS[quote], l)
    return r


def filter_by_gs(l, gs):
    return filter(lambda p: p['gs'] > gs, l)


if __name__ == '__main__':
    top_gscore = get_gs()
    print('==== GalaxyScore ====')
    print_coins(top_gscore)

    for q in PAIRS.keys():
        print(f'==== GalaxyScore {q} ====')
        print_coins(filter_by_quote(top_gscore, q), q)
        print("\n\n")

