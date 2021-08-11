import requests

base_fiat = input().lower()
url = f'http://www.floatrates.com/daily/{base_fiat}.json'
r = requests.get(url)
if r:
    json_dict = r.json()
rate = 0
cache = {'eur', 'usd'}
while True:
    order_fiat = input().lower()
    if not order_fiat:
        break
    amount = int(input())
    print('Checking the cache...')
    try:
        if order_fiat in cache:
            print('Oh! It is in the cache!')
        else:
            cache.add(order_fiat)
            print('Sorry, but it is not in the cache!')
        rate = json_dict[order_fiat]['rate']
    except KeyError:
        url = f'http://www.floatrates.com/daily/{base_fiat}.json'
        r = requests.get(url)
        if r:
            json_dict = r.json()
            rate = json_dict[order_fiat]['rate']
        else:
            print('try again')
            continue
    finally:
        changed_amount = round(amount * rate, 2)
        print(f'You received {changed_amount} {order_fiat}.')
