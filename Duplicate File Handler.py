import os
import sys
from collections import defaultdict
from pathlib import Path
from hashlib import md5
from itertools import count

base_dir = sys.argv
file_format = ''
if len(base_dir) == 1:
    print('Directory is not specified')
    exit()
else:
    base_dir = base_dir[1]
    print('Enter file format:')
    file_format = input()
    print('Size sorting options:\n'
          '1. Descending\n'
          '2. Ascending')

    while True:
        sort_mode = input('Enter a sorting option:\n')
        if sort_mode in ('1', '2'):
            rev_mod = {'1': True, '2': False}[sort_mode]
            break
        else:
            print('Wrong option')
size_dict = defaultdict(list)
for root, dirs, files in os.walk(base_dir):
    for name in files:
        if file_format == '' or name[-len(file_format):] == file_format:
            p = os.path.join(root, name)
            size_dict[Path(p).stat().st_size].append(p)

key_list = sorted(list(size_dict), reverse=rev_mod)
for key in key_list:
    print(key, 'bytes')
    for obj in size_dict[key]:
        print(obj)
    print()

while True:
    dup_chk = input('Check for duplicates?')
    if dup_chk == 'no':
        exit()
    elif dup_chk == 'yes':
        break
dup_size_hash_dict = {}
for key in key_list:
    if len(size_dict[key]) > 1:
        dup_size_hash_dict[key] = defaultdict(list)
        for obj in size_dict[key]:
            h = md5()
            with open(obj, 'rb') as f:
                for line in f:
                    h.update(line)
            dup_size_hash_dict[key][h.hexdigest()].append(obj)

n = count(1)
dup_list = [0]
for key, dups in dup_size_hash_dict.items():
    print(key, 'bytes')
    for hsh, objs in dups.items():
        if len(objs) > 1:
            print('Hash:', hsh)
            for obj in objs:
                print(f'{next(n)}. {obj}')
                dup_list.append((key, obj))
    print()

while True:
    dup_chk = input('Delete files?\n')
    if dup_chk == 'no':
        exit()
    elif dup_chk == 'yes':
        break
    print('Wrong option')

delete_list = []
while True:
    dup_chk = input('Enter file numbers to delete:\n')
    if not dup_chk.replace(' ', '').isdigit():
        print('Wrong option')
    else:
        delete_list = list(map(int, dup_chk.split()))
        if max(delete_list) >= len(dup_list):
            print('Wrong option')
        else:
            break

freebytes = 0
for cond in delete_list:
    freebytes += dup_list[cond][0]
    os.remove(dup_list[cond][1])

print(f'Total freed up space: {freebytes} bytes')

