import json
import re
from collections import Counter, defaultdict
from itertools import product, combinations

data_structure = (("bus_id", int, True, ''),
                  ("stop_id", int, True, ''),
                  ("stop_name", str, True, re.compile(r'^([A-Z][a-z]+ )+(Street|Avenue|Boulevard|Road)$').match),
                  ("next_stop", int, True, ''),
                  ("stop_type", str, False, re.compile(r'[SOF]$').match),
                  ("a_time", str, True, re.compile(r'^([01][0-9]|^2[0-4]):[0-5][0-9]$').match))


def input_checker(df, structure=data_structure):
    errors = Counter()
    for line in df:
        for field, field_type, field_req, field_format in structure:
            if field_format and line[field] and field_format(line[field]) is None:
                errors[field] += 1
                errors['all'] += 1

    print(f'Format validation: {errors["all"]} errors')
    for title in ['stop_name', 'stop_type', 'a_time']:
        print(f'{title}: {errors[title]}')


def line_stop_counter(df):
    stops = Counter()
    for line in df:
        stops[line["bus_id"]] += 1

    for code, num in stops.items():
        print(f'bus_id: {code}, stops: {num}')


def stations_structure(df):
    line_stations = defaultdict(list)
    type_stations = {"S": set(),
                     "F": set(),
                     "O": set()}
    lines_stops = defaultdict(set)

    iters = ((line['stop_type'], line['bus_id'], line['stop_name']) for line in df)
    for stop_type, bus_id, name in iters:
        if stop_type in list('SF'):
            if stop_type in lines_stops[bus_id]:
                mod = {'S': 'start', 'F': 'end'}[stop_type]
                print(f'There is 2 {mod} stop for the line: {bus_id}.')
                return
            else:
                lines_stops[bus_id].add(stop_type)
            type_stations[stop_type].add(name)
        line_stations[bus_id].append(name)

    for id in lines_stops:
        if not lines_stops[id] >= {'F', 'S'}:
            print(f'There is no start or end stop for the line: {id}.')
            return

    for a, b in combinations(line_stations, 2):
        for stop_a, stop_b in product(line_stations[a], line_stations[b]):
            if stop_a == stop_b:
                type_stations['O'].add(stop_b)

    for typ, i in zip(['Start', 'Transfer', 'Finish'], 'SOF'):
        print(f'{typ} stops: {len(type_stations[i])} {sorted(type_stations[i])}')


def travel_time_checker(df):
    iters = ((line['bus_id'], line['stop_name'], line['a_time']) for line in df)
    id_last = None
    last_time = '23:59'
    block_ids = set()
    print('Arrival time test:')
    for bus_id, name, time in iters:
        if bus_id not in block_ids:
            if bus_id == id_last and time <= last_time:
                block_ids.add(bus_id)
                print(f'bus_id line {bus_id}: wrong time on station {name}')
            id_last, last_time = bus_id, time
    if not block_ids:
        print('OK')


def demand_checker(df):
    stations = defaultdict(list)
    wrong_stations = set()
    for line in df:
        stations[line['stop_name']].append(line['stop_type'])

    for name, stops in stations.items():
        stops_s = set(stops)
        if len(stops) > 1 and len(stops_s) > 1 and {'O'} <= stops_s:
            wrong_stations.add(name)

    print('On demand stops test:')
    print(sorted(wrong_stations) or 'OK')


if __name__ == '__main__':
    json_data = json.loads(input())
    demand_checker(json_data)
