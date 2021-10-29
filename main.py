import time
from datetime import datetime

import lunarcrush as lc
import pairs
from accounts import ACCOUNTS
from p3commas import P3cClient, print_bot

BLACKLIST = {
    'USDT_BNBDOWN', 'USDT_SXPDOWN', 'BTC_JUV', 'USDT_JUV', 'USDT_ATM', 'BTC_ATM', 'USDT_ACM', 'BTC_ACM', 'BUSD_ACM',
    'USDT_ASR', 'BTC_ASR', 'BTC_OG', 'USDT_OG', 'USDT_PSG', 'BTC_PSG', 'BTC_BAR', 'BUSD_BAR', 'USDT_BAR', 'GBP_DOGE',
    'USD_DOGE', 'BUSD_USDC', 'USDT_PAX', 'USDT_PAXG', 'USDT_SUSD', 'BTC_SUSD', 'USDT_BUSD', 'USDT_EUR', 'BUSD_EUR',
    'USD_EUR', 'USDT_GBP', 'USD_GBP', 'USDT_AUD', 'BUSD_AUD', 'BTC_UNI', 'USDT_UNI', 'BTC_WBTC', 'ETH_WBTC',
    'USDT_WBTC', 'USD_WBTC', 'BTC_EZ', 'ETH_EZ', 'USDT_FTM', 'BTC_FTM', 'USDT_FTMUSDT', 'BUSD_FTM', 'BNB_FTM'
}

# for account_name, account_creds in ACCOUNTS.items():
#     print(f'====== {account_name}')
#     p3c = account_creds['p3c']
#     print_bot(p3c.get_bots())
#
# 1/0

#
# def filter_by_quote(l, quote):
#     quote = quote.upper()
#     r = filter(lambda p: f"{quote}_{p['s']}" in PAIRS[quote], l)
#     return r

while True:
    a = list(ACCOUNTS.values())[0]
    p3client = P3cClient(
        key=a['key'],
        secret=a['secret']
    )
    pairs = p3client.get_pairs('binance')

    lc_gs_top = lc.get_gs()
    lc_ar_top = lc.get_acr()

    print('============================  GalaxyScore  ============================')
    lc.print_coins(lc_gs_top)

    print('============================  AltRank  ============================')
    lc.print_coins(lc_ar_top)

    for account_name, account_creds in ACCOUNTS.items():
        print(f'\n\n====== {account_name}')
        p3c = P3cClient(
            key=account_creds['key'],
            secret=account_creds['secret']
        )
        # p3c = account_creds['p3c']

        bots = p3c.get_bots(mode='real') + p3c.get_bots(mode='paper')

        # for b in bots:
        for b in [bb for bb in bots if bb['is_enabled']]:
            for t in b['name'].upper().split():
                if t.startswith('LCF_'):
                    _, lc_type, num_pairs = t.split('_')
                    num_pairs = int(num_pairs)
                    print(lc_type, num_pairs)

                    # print_bot(b)
                    cur_pairs = b['pairs']
                    quote = b['pairs'][0].split('_')[0]

                    if lc_type == 'GALAXYSCORE':
                        lc_havequote = filter(lambda p: f"{quote}_{p['s']}" in pairs, lc_gs_top)
                        # lc_havequote = lc.filter_by_quote(lc_gs_top, quote=quote)
                        lc_havequote = lc.filter_by_gs(lc_havequote, 65)
                    elif lc_type == 'ALTRANK':
                        lc_havequote = filter(lambda p: f"{quote}_{p['s']}" in pairs, lc_ar_top)
                        # lc_havequote = lc.filter_by_quote(lc_ar_top, quote=quote)
                    else:
                        print('unknown lc_type', lc_type, 'for bot', b['id'], b['name'])
                        continue

                    new_pairs = [f"{quote}_{p['s']}" for p in lc_havequote]
                    new_pairs = new_pairs[:num_pairs]

                    # blacklist filter
                    new_pairs = list(filter(lambda p: p not in BLACKLIST, new_pairs))

                    b['pairs'] = new_pairs
                    p3c.update_bot(b['id'], b)
                    print(b['name'], 'updated')
                    print('current', sorted(cur_pairs))
                    print('new    ', sorted(new_pairs))

    print('\n\nlast update:', datetime.today().isoformat())
    time.sleep(2700)
