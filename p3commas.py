import time

from py3cw.request import Py3CW

# p3cw = Py3CW(
#     key='c28d0197b53740d8b91216f0031996b84fa39d7deae344a3a396831ae6d4dbd2',
#     secret='1b247aebf604a5db02eade2a80fb7417ec0e54fcb40bc56c055944761d3bba8867f972f3e01aedb73f20512f3ab0b82250bfedfa65c6bc4a7da779a3f38206c2ce12175242fe453a64e1fc9a7501f3764989e03c012afa7d1bb24b96315e5efa515d0d9f')
from accounts import ACCOUNTS


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

    def get_bots(self):
        return self.req(entity='bots', action='')

    def get_bot(self, bot_id: str):
        return self.req(entity='bots', action='show', action_id=bot_id)

    def update_bot(self, bot_id: str, bot_data: dict):
        self.req(entity='bots', action='update', action_id=str(bot_id), payload=bot_data)


def print_bot(data):
    if isinstance(data, dict):
        data = [data, ]

    for b in data:
        print(", ".join([f"{k}: {b[k]}" for k in ['id', 'is_enabled', 'name', 'pairs']]), f"pairs: {len(b['pairs'])}")


if __name__ == '__main__':
    a = list(ACCOUNTS.values())[0]
    p3client = P3cClient(
        key=a['key'],
        secret=a['secret']
    )

    print_bot(p3client.get_bots())

    print_bot(p3client.get_bot('6316317'))
