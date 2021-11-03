import time
from datetime import datetime

import lunarcrush as lc
from accounts import USERS
from p3commas import P3cClient

BLACKLIST = {
    'USDT_BNBDOWN', 'USDT_SXPDOWN', 'BTC_JUV', 'USDT_JUV', 'USDT_ATM', 'BTC_ATM', 'USDT_ACM', 'BTC_ACM', 'BUSD_ACM',
    'USDT_ASR', 'BTC_ASR', 'BTC_OG', 'USDT_OG', 'USDT_PSG', 'BTC_PSG', 'BTC_BAR', 'BUSD_BAR', 'USDT_BAR', 'GBP_DOGE',
    'USD_DOGE', 'BUSD_USDC', 'USDT_PAX', 'USDT_PAXG', 'USDT_SUSD', 'BTC_SUSD', 'USDT_BUSD', 'USDT_EUR', 'BUSD_EUR',
    'USD_EUR', 'USDT_GBP', 'USD_GBP', 'USDT_AUD', 'BUSD_AUD', 'BTC_UNI', 'USDT_UNI', 'BTC_WBTC', 'ETH_WBTC',
    'USDT_WBTC', 'USD_WBTC', 'BTC_EZ', 'ETH_EZ', 'USDT_FTM', 'BTC_FTM', 'USDT_FTMUSDT', 'BUSD_FTM', 'BNB_FTM'
}


def filter_by_quote(lst, pairs, quote):
    return list(filter(lambda p: f"{quote.upper()}_{p['s']}" in pairs, lst))


accounts_cache = dict()
pairs_cache = dict()

while True:
    lc_galaxyscore = lc.get_gs()
    lc_altrank = lc.get_acr()

    print('============================  GalaxyScore  ============================')
    lc.print_coins(lc_galaxyscore)

    print('============================  AltRank  ============================')
    lc.print_coins(lc_altrank)

    for user_name, creds in USERS.items():
        print(f'\n\n====== {user_name}')
        p3c = P3cClient(
            key=creds['key'],
            secret=creds['secret']
        )

        bots = p3c.get_bots(mode='real') + p3c.get_bots(mode='paper')

        # for b in bots:
        for b in [bb for bb in bots if bb['is_enabled']]:
            num_pairs, lc_type = None, None

            if b['account_id'] not in accounts_cache:
                print('calling get account')
                accounts_cache[b['account_id']] = p3c.get_account(b['account_id'])
            account = accounts_cache[b['account_id']]

            if account['market_code'] not in pairs_cache:
                print('calling get pairs')
                pairs_cache[account['market_code']] = p3c.get_pairs(account['market_code'])
            pairs = pairs_cache[account['market_code']]

            for t in b['name'].upper().split():
                if t.startswith('LCF_'):
                    _, lc_type, num_pairs = t.split('_')
                    num_pairs = int(num_pairs)
                    # print('\n', lc_type, num_pairs)

            if num_pairs and lc_type:
                # print_bot(b)
                cur_pairs = b['pairs'].copy()
                quote = b['pairs'][0].split('_')[0]

                if lc_type == 'GALAXYSCORE':
                    lc_havequote = filter_by_quote(lc_galaxyscore, pairs, quote)
                    lc_havequote = lc.filter_by_gs(lc_havequote, 65)
                elif lc_type == 'ALTRANK':
                    lc_havequote = filter_by_quote(lc_altrank, pairs, quote)
                else:
                    print('unknown lc_type', lc_type, 'for bot', b['id'], b['name'])
                    continue

                new_pairs = [f"{quote}_{p['s']}" for p in lc_havequote]

                new_str = ' '.join([f"{c:5s}" for c in sorted([c['s'] for c in lc_havequote[:num_pairs]])])
                old_str = ' '.join([f"{p.split('_')[1]:5s}" for p in sorted(cur_pairs)])
                # blacklist filter
                new_pairs = list(set(new_pairs) - BLACKLIST)

                new_pairs = new_pairs[:num_pairs]

                if len(new_pairs) > 0:
                    b['pairs'] = new_pairs
                    u = p3c.update_bot(b['id'], b)
                    # print(sorted(u['pairs']))
                    print(f"\nUpdated '{b['name']}' {lc_type} {num_pairs}")
                    print(f' current {len(cur_pairs)} {old_str}')
                    # print(f' current {len(cur_pairs)}', sorted(cur_pairs))
                    print(f' new     {len(new_pairs)} {new_str}')
                    # print(f' new     {len(new_pairs)}', sorted(new_pairs))

    print('\n\nlast update:', datetime.today().isoformat())
    time.sleep(3600)
