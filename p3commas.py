import time
from pprint import pprint

from py3cw.request import Py3CW

# p3cw = Py3CW(
#     key='c28d0197b53740d8b91216f0031996b84fa39d7deae344a3a396831ae6d4dbd2',
#     secret='1b247aebf604a5db02eade2a80fb7417ec0e54fcb40bc56c055944761d3bba8867f972f3e01aedb73f20512f3ab0b82250bfedfa65c6bc4a7da779a3f38206c2ce12175242fe453a64e1fc9a7501f3764989e03c012afa7d1bb24b96315e5efa515d0d9f')
from accounts import USERS


class P3cClient:
    def __init__(self, key, secret):
        self.p3cw = Py3CW(
            request_options={'retry_status_codes': [500, 502, 503, 504]},
            key=key,
            secret=secret,
        )

    def req(self, *args, **kwargs):
        cnt = 0
        while cnt < 10:
            error, data = self.p3cw.request(**kwargs)
            if error:
                print(error)
                cnt += 1
                time.sleep(cnt * 1.1)
            else:
                return data

    def get_bots(self, mode='real'):
        """ mode is one of 'real'|'paper' """
        return self.req(entity='bots', action='', additional_headers={'Forced-Mode': mode})

    def get_bot(self, bot_id: str, mode='real'):
        return self.req(entity='bots', action='show', action_id=bot_id, additional_headers={'Forced-Mode': mode})

    def update_bot(self, bot_id: str, bot_data: dict, mode='real'):
        return self.req(entity='bots', action='update', action_id=str(bot_id), payload=bot_data,
                        additional_headers={'Forced-Mode': mode})

    def get_accounts(self, mode='real'):
        return self.req(entity='accounts', action='', additional_headers={'Forced-Mode': mode})

    def get_account(self, account_id, mode='real'):
        return self.req(entity='accounts', action='account_info', action_id=str(account_id), additional_headers={'Forced-Mode': mode})

    def get_markets(self):
        return self.req(entity='accounts', action='market_list')

    def get_pairs(self, market_code=''):
        return self.req(entity='accounts', action='market_pairs', payload={'market_code': market_code})


def print_bot(bots):
    if isinstance(bots, dict):
        data = [bots, ]

    for b in bots:
        b['pairs'] = sorted(b['pairs'])
        print(", ".join([f"{k}: {b[k]}" for k in ['name', 'id', 'is_enabled', 'pairs']]), f"pairs: {len(b['pairs'])}")


if __name__ == '__main__':
    a = list(USERS.values())[0]
    p3client = P3cClient(
        key=a['key'],
        secret=a['secret']
    )

    # print_bot(p3client.get_bots('paper'))
    # print_bot(p3client.get_bots('real'))

    # b = p3client.get_bot('6208906')
    # pprint(sorted(b.items()))
    # 1/0
    # a = p3client.get_account(b['account_id'])
    # print(a['id'], a['name'], a['market_code'])
    # print(len(p3client.get_pairs(a['market_code'])))

    #print_bot(b)
    # b['pairs'] = ['USDT_1INCH', "USDC_BNB"]
    # print(p3client.update_bot(b['id'], b, mode='paper'))

    # a = p3client.get_accounts(mode='real')
    # a = a[1]
    # pprint(a)
    # print(a['id'], a['market_code'], a['name'])

    # pprint(p3client.get_markets())
    pprint(sorted(p3client.get_pairs('binance')))

    # print_bot(p3client.get_bot('6316317', mode='real'))
