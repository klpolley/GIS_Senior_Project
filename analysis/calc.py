from typing import List

import psycopg2
import psycopg2.extras
from analysis.config import config
import sys

from statistics import mean
import numpy as np


# districts = [
#     '001', '002', '003', '004', '005', '006', '007', '008', '009', '010',
#     '011', '012', '013', '014', '015', '016', '017', '018', '019', '020',
#     '021', '022', '023', '024', '025', '026', '027', '028', '029', '030',
#     '031', '032', '033', '034', '035', '036', '037', '038', '039', '040',
#     '041', '042', '043', '044', '045', '046', '047', '048', '049', '050',
#     '051', '052', '053', '054', '055', '056', '057', '058', '059', '060',
#     '061', '062', '063', '064', '065', '066', '067', '068', '069', '070',
#     '071', '072', '073', '074', '075', '076', '077', '078', '079', '080',
#     '081', '082', '083', '084', '085', '086', '087', '088', '089', '090',
#     '091', '092', '093', '094', '095', '096', '097', '098', '099', '100',
#     '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
#     '111', '112', '113', '114'
# ]

districts = [

    '091', '092', '093', '094', '095', '096', '097', '098', '099', '100',
    '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
    '111', '112', '113', '114'
]

def calc_sums(cursor):
    for dis in districts:
        table = 'congress.districts'+dis
        select = "select avg(perimeter_to_area) from "+table
        cursor.execute(select)
        value = cursor.fetchone()[0]
        insert = "insert into congress.aggregation values("+dis+","+str(value)+");"
        cursor.execute(insert)


def calc_ratios(cursor):
    for dis in districts:
        alter = "alter table congress.districts"+dis+" add column perimeter_to_area double precision;"
        cursor.execute(alter)
        update = "update congress.districts"+dis+" set perimeter_to_area = ST_perimeter(geom) / ST_area(geom);"
        cursor.execute(update)
        print(dis)


def area_perim(cursor):
    for dis in districts:
        alter = "alter table congress.districts"+dis+" add column perimeter double precision;"
        cursor.execute(alter)
        update = "update congress.districts" + dis + " set perimeter = ST_perimeter(geom);"
        cursor.execute(update)

        alter = "alter table congress.districts" + dis + " add column area double precision;"
        cursor.execute(alter)
        update = "update congress.districts"+dis+" set area = ST_area(geom);"
        cursor.execute(update)


def define_names(cursor):
    for dis in districts:
        table = 'congress.districts' + dis

        alter = "alter table " + table + " add column name varchar"
        cursor.execute(alter)

        select = "select statename, district from " + table
        cursor.execute(select)
        info = cursor.fetchall()

        for i in info:
            state = i[0]
            district = i[1]
            name = state + " " + district

            update = "update " + table + " set name = '" + name + \
                     "' where statename = '" + state + "' and district = '" + district + "'"
            cursor.execute(update)

            print(name)

def calc_compact(cursor):
    for dis in districts:
        # alter = "alter table congress.districts" + dis + " add column compactness double precision;"
        # cursor.execute(alter)
        #
        # update = "update congress.districts" + dis + " set compactness = area / (perimeter*perimeter / 4 * 3.14159);"
        # cursor.execute(update)

        alter = "alter table congress.districts" + dis + " add column index double precision;"
        cursor.execute(alter)

        update = "update congress.districts" + dis + " set index = 100 - (100*compactness);"
        cursor.execute(update)


def best_fit(name, xs, ys, cursor):

    num = ((mean(xs) * mean(ys)) - mean(xs * ys))
    denom = ((mean(xs) ** 2) - mean(xs ** 2))

    if denom == 0: return

    m = num / denom

    update = "update congress.districts114 set m = " + str(m) + " where name = '" + name + "'"
    cursor.execute(update)


def lets_go(cursor):
    data = {}

    names114 = set()
    #alter = "alter table congress.districts114 add column m double precision;"
    #cursor.execute(alter)

    update = "update congress.districts114 set m = 0"
    cursor.execute(update)

    for dis in districts:
        table = 'congress.districts' + dis
        select = "select name, index from " + table
        cursor.execute(select)
        info = cursor.fetchall()

        for i in info:
            name = i[0]
            comp = i[1]
            dis_num = int(dis)
            if name not in data.keys():
                data[name] = [(dis_num, comp)]
            else:
                data[name].append((dis_num, comp))
            if dis_num == 114: names114.add(name)

    for name in data.keys():
        nums = []
        comps = []
        for y in data[name]:
            nums.append(y[0])
            comps.append(y[1])

        #print(len(nums))

        if len(nums) < 20: continue
        if None in comps: continue

        xs = np.array(nums)
        ys = np.array(comps)



        best_fit(name, xs, ys, cursor)





def connect():
    try:
        params = config()
        con = psycopg2.connect(**params)
        cur = con.cursor()

        #calc_ratios(cur)
        #calc_sums(cur)

        #area_perim(cur)

        #define_names(cur)

        #calc_compact(cur)

        lets_go(cur)

        con.commit()

    except psycopg2.DatabaseError as e:
        print(f'Error {e}')
        sys.exit(1)

    finally:
        if con:
            con.close()


if __name__ == '__main__':
    connect()