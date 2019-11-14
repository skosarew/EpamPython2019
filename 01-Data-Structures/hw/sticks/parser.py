from collections import defaultdict

file_test = 'test.json'


def files_load(path):
    """Считывание файлов,  устранение дупликатов и сортировка объектов в низходящем порядке по цене
    в случае коллизий сортировка по сорту в лексикографическом порядке"""
    wines = set()
    wine_dict = {}
    parsed_wines = []

    # Считывание файлов, устранение дубликатов
    with open(path[0]) as f1, open(path[1]) as f2:
        for wine in f1.read()[2:-1].split('}, {'):
            # print(repr(wine))
            wine = wine.strip('}')
            wines.add(wine)
        for wine in f2.read()[2:-1].split('}, {'):
            # print(repr(wine))
            wine = wine.strip('}')
            wines.add(wine)

    # Формирование списка, содержащего вина в виде словарей
    for wine in wines:
        wine = wine.split(', "')
        for entity in wine:
            entity = entity.split(': ')
            if entity[0][0] != '"':
                entity[0] = '"' + entity[0]

            entity[0] = entity[0].replace('"', '')

            if entity[1] == 'null':
                entity[1] = None
            else:
                entity[1] = entity[1].replace('"', '')

            wine_dict[entity[0]] = entity[1]
        parsed_wines.append(wine_dict)
        wine_dict = {}

    # Сортировка
    parsed_wines = sorted(sorted(parsed_wines, key=lambda x: x['title'], reverse=False),
                          key=lambda x: int(x['price']) if x['price'] is not None else -1, reverse=True)
    return parsed_wines


def file_dump(path, parsed_wines):
    # Запись в общий файл
    with open(path, 'w') as out_f:
        out_f.write('[')
        for wine in parsed_wines:
            out_f.write('\n    {')
            len(wine)
            for key, val in wine.items():
                if val is None:
                    out_f.writelines(f'\n        "{key}": {"null"}, ')
                else:
                    out_f.writelines(f'\n        "{key}": "{val}", ')
            out_f.seek(out_f.tell() - 2)
            out_f.write('\n    }, ')
        out_f.seek(out_f.tell() - 2)
        out_f.write('\n]')


def stats_dump_json(path, interesting_wines, global_stat):
    """Merge 2 файлов в один winedata_full.json"""
    information = (
        "avarege_price", "min_price", "max_price", "most_common_region", "most_common_country", "avarage_score")

    with open(path, 'w') as out_f:
        out_f.write('{"statistics": {\n')
        out_f.write('               "wine": {\n')

        # Запись статистики по интересующим винам
        for wine, stats in interesting_wines.items():
            out_f.write(f'                      "{wine}": ')
            out_f.write('{')
            for i in information:
                if stats[i] is None:
                    out_f.write(f'"{i}": {"null"}, ')
                else:
                    out_f.write(f'"{i}": "{stats[i]}", ')
            out_f.seek(out_f.tell() - 2)
            out_f.write('},\n')
        out_f.seek(out_f.tell() - 2)
        out_f.write('\n               },')

        # Запись всей статистики
        for key, val in global_stat.items():
            out_f.write(f'\n               "{key}": ')
            out_f.write('{')
            for number, w in val.items():
                out_f.write(f'"{number}": [')
                for i in w:
                    out_f.write(f'"{i}", ')
                out_f.seek(out_f.tell() - 2)
                out_f.write(']')
            out_f.write('}, ')
        out_f.seek(out_f.tell() - 2)
        out_f.write('\n        }')
        out_f.write('\n}')


def stats_dump_markdown(interesting_wines, global_stat):
    """Оформление результатов из пункта 3 в виде красивого markdown файла"""
    information = (
        "avarege_price", "min_price", "max_price", "most_common_region", "most_common_country", "avarage_score")

    # Запись статистики по интересующим винам
    with open('stats.md', "w", encoding="utf-8") as out_f:
        out_f.write('## Статистика по интересующим винам: \n\n')
        for wine, stats in interesting_wines.items():
            out_f.write(f'{wine.encode("utf-8").decode("unicode-escape")}:\n\n')
            for i in information:
                if stats[i] is None:
                    out_f.write(f'* {i}: {"null"}')
                else:
                    out_f.write(f'* {i}: {stats[i]}')
                out_f.write('\n')
            out_f.write('\n')

        # Запись всей статистики
        out_f.write('## Общая статистика: \n\n')
        for entity, stat in global_stat.items():
            out_f.write(f'{entity}:\n')
            for key, val in stat.items():
                out_f.write(f'{key}:\n')
                for i in val:
                    out_f.write(f'* {i.encode("utf-8").decode("unicode-escape")}\n')
                out_f.write('\n\n')


def avarege_price(interesting_wines):
    for wines, values in interesting_wines.items():
        if len(values['price']) != 0:
            average_pr = sum(map(int, values['price'])) / len(values['price'])
            values['avarege_price'] = average_pr
        else:
            values['avarege_price'] = None
    return interesting_wines


def min_price(interesting_wines):
    for wines, values in interesting_wines.items():
        if values['price']:
            values['min_price'] = min(map(float, values['price']))
        else:
            values['min_price'] = None


def max_price(interesting_wines):
    for wines, values in interesting_wines.items():
        if values['price']:
            values['max_price'] = max(map(float, values['price']))
        else:
            values['max_price'] = None


def most_common_region(interesting_wines):
    for wines, values in interesting_wines.items():
        reg = values['region_1'] + values['region_2']
        if reg:
            values['most_common_region'] = max(set(reg), key=reg.count)
        else:
            values['most_common_region'] = None


def most_common_country(interesting_wines):
    for wines, values in interesting_wines.items():
        if values['country']:
            mcc = max(set(values['country']), key=values['country'].count)
            values['most_common_country'] = mcc
        else:
            values['most_common_country'] = None


def avarage_score(interesting_wines):
    for wines, values in interesting_wines.items():
        # print(wines, values)
        if len(values['points']) != 0:
            average_sc = sum(map(float, values['points'])) / len(values['points'])
            values['avarage_score'] = average_sc
        else:
            values['avarage_score'] = None
    return interesting_wines


def find_most_expensive_coutry(countries_stat):
    mec = -float("inf")
    mec_ans = defaultdict(list)
    for key, val in countries_stat.items():
        curr = sum(map(int, val)) / len(val)
        if curr > mec:
            mec = curr
            mec_ans = defaultdict(list)
            mec_ans[mec].append(key)
        elif curr == mec:
            mec_ans[mec].append(key)
    return mec_ans


def find_cheapest_coutry(countries_stat):
    cc = float("inf")
    cc_ans = defaultdict(list)
    for key, val in countries_stat.items():
        curr = sum(map(int, val)) / len(val)
        if curr < cc:
            cc = curr
            cc_ans = defaultdict(list)
            cc_ans[cc].append(key)
        elif curr == cc:
            cc_ans[cc].append(key)
    return cc_ans


def find_most_rated_country(countries_stat_point):
    mrc = -float("inf")
    mrc_ans = defaultdict(list)
    for key, val in countries_stat_point.items():
        curr = sum(map(int, val)) / len(val)
        if curr > mrc:
            mrc = curr
            mrc_ans = defaultdict(list)
            mrc_ans[mrc].append(key)
        elif curr == mrc:
            mrc_ans[mrc].append(key)
    return mrc_ans


def find_underrated_country(countries_stat_point):
    uc = float("inf")
    uc_ans = defaultdict(list)
    for key, val in countries_stat_point.items():
        curr = sum(map(int, val)) / len(val)
        if curr < uc:
            uc = curr
            uc_ans = defaultdict(list)
            uc_ans[uc].append(key)
        elif curr == uc:
            uc_ans[uc].append(key)
    return uc_ans


def find_most_active_commentator(commentators_stat):
    mac = 0
    mac_ans = defaultdict()
    for key, val in commentators_stat.items():
        curr = val
        if curr > mac:
            mac = curr
            mac_ans = defaultdict(list)
            mac_ans[mac].append(key)
        elif curr == mac:
            mac_ans[mac].append(key)
    return mac_ans


def info_for_wines(wines_processed, interesting_wines, information, global_stat):
    """Сбор статистики для задания 3"""
    highest_sc = -float("inf")
    lowest_sc = float("inf")
    mew = wines_processed[0]['price']
    cw = int(wines_processed[0]['price'])

    global_stat['most_expensive_wine'][mew] = []
    global_stat['cheapest_wine'][cw] = []
    global_stat['highest_score'][highest_sc] = []
    global_stat['lowest_score'][lowest_sc] = []

    countries_stat_price = defaultdict(list)
    countries_stat_point = defaultdict(list)
    commentators_stat = defaultdict(int)

    for wine_processed in wines_processed:
        if wine_processed['price'] == mew:
            global_stat['most_expensive_wine'][mew].append(wine_processed['title'])

        # find cheapest_wine
        if wine_processed['price'] is not None and int(wine_processed['price']) < int(cw):
            cw = wine_processed['price']
            global_stat['cheapest_wine'] = defaultdict(list)
            global_stat['cheapest_wine'][cw].append(wine_processed['title'])
        elif wine_processed['price'] == cw:
            global_stat['cheapest_wine'][cw].append(wine_processed['title'])

        # find highest_score
        curr_score = int(wine_processed['points'])
        if curr_score > highest_sc:
            global_stat['highest_score'] = defaultdict(list)
            highest_sc = curr_score
            global_stat['highest_score'][highest_sc].append(wine_processed['title'])
        elif curr_score == highest_sc:
            global_stat['highest_score'][highest_sc].append(wine_processed['title'])

        # find lowest_score
        if curr_score < lowest_sc:
            global_stat['lowest_score'] = defaultdict(list)
            lowest_sc = curr_score
            global_stat['lowest_score'][lowest_sc].append(wine_processed['title'])
        elif curr_score == lowest_sc:
            global_stat['lowest_score'][lowest_sc].append(wine_processed['title'])

        # information gathering for finding countries prices
        if wine_processed['price'] is not None:
            countries_stat_price[wine_processed['country']].append(wine_processed['price'])

        # information gathering for finding countries points
        if wine_processed['points'] is not None:
            countries_stat_point[wine_processed['country']].append(wine_processed['points'])

        # information gathering for finding most active commentator
        if wine_processed['taster_name'] is not None:
            commentators_stat[wine_processed['taster_name']] += 1

        # Обратка интересующих вин (задание 3.1)
        for wine in interesting_wines:
            if wine_processed['variety'] == wine:
                for info in information:
                    if wine_processed[info] is not None:
                        interesting_wines[wine][info].append(wine_processed[info])

    # find most_expensive_coutry
    mec = find_most_expensive_coutry(countries_stat_price)
    global_stat['most_expensive_coutry'] = mec

    # find cheapest_coutry
    cc = find_cheapest_coutry(countries_stat_price)
    global_stat['cheapest_coutry'] = cc

    # find most_rated_country
    mrc = find_most_rated_country(countries_stat_point)
    global_stat['most_rated_country'] = mrc

    # find underrated_country
    uc = find_underrated_country(countries_stat_point)
    global_stat['underrated_country'] = uc

    # find most_active_commentator
    mac = find_most_active_commentator(commentators_stat)
    global_stat['most_active_commentator'] = mac

    return interesting_wines


def main():
    file1 = 'winedata_1.json'
    file2 = 'winedata_2.json'
    files = (file1, file2)
    file_full = 'winedata_full.json'
    file_stat = 'stats.json'
    wines_list = ('Gew\\u00fcrztraminer',
                  'Riesling',
                  'Merlot',
                  'Madera',
                  'Tempranillo',
                  'Red Blend'
                  )

    global_stat = {'most_expensive_wine': defaultdict(list), 'cheapest_wine': defaultdict(list),
                   'highest_score': defaultdict(list), 'lowest_score': defaultdict(list),
                   'most_expensive_coutry': defaultdict(list), 'cheapest_coutry': defaultdict(list),
                   'most_rated_country': defaultdict(list),
                   'underrated_country': defaultdict(list), 'most_active_commentator': defaultdict(list)}

    information = ('price', 'region_1', 'region_2', 'country', 'points')
    interesting_wines = {i: {j: [] for j in information} for i in wines_list}

    wines_processed = files_load(files)
    interesting_wines = info_for_wines(wines_processed, interesting_wines, information, global_stat)

    avarege_price(interesting_wines)
    avarage_score(interesting_wines)
    min_price(interesting_wines)
    max_price(interesting_wines)
    most_common_country(interesting_wines)
    most_common_region(interesting_wines)

    file_dump(file_full, wines_processed)
    stats_dump_json(file_stat, interesting_wines, global_stat)
    stats_dump_markdown(interesting_wines, global_stat)


if __name__ == '__main__':
    main()
