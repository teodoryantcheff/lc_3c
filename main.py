import time
from datetime import datetime

import lunarcrush as lc
import pairs
from accounts import ACCOUNTS
from p3commas import P3cClient, print_bot

# for account_name, account_creds in ACCOUNTS.items():
#     print(f'====== {account_name}')
#     p3c = account_creds['p3c']
#     print_bot(p3c.get_bots())
#
# 1/0

while True:
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

        for b in bots:
            for t in b['name'].upper().split():
                if t.startswith('LCF_'):
                    _, lc_type, num_pairs = t.split('_')
                    num_pairs = int(num_pairs)
                    print(lc_type, num_pairs)

                    print_bot(b)
                    cur_pairs = b['pairs']
                    quote = b['pairs'][0].split('_')[0]

                    if lc_type == 'GALAXYSCORE':
                        lc_havequote = lc.filter_by_quote(lc_gs_top, quote=quote)
                        lc_havequote = lc.filter_by_gs(lc_havequote, 65)
                    if lc_type == 'ALTRANK':
                        lc_havequote = lc.filter_by_quote(lc_ar_top, quote=quote)

                    new_pairs = [f"{quote}_{p['s']}" for p in lc_havequote]
                    new_pairs = new_pairs[:num_pairs]

                    # blacklist filter
                    new_pairs = list(filter(lambda p: p not in pairs.blacklist, new_pairs))

                    b['pairs'] = new_pairs
                    p3c.update_bot(b['id'], b)
                    print(b['id'], 'updated', sorted(cur_pairs), ' => ', sorted(new_pairs))

    print('\n\nlast update:', datetime.today().isoformat())
    time.sleep(2700)
