#!/usr/bin/env 
# python3 solver_greedy.py ../input/input_0.csv > ../output/output_0.csv

import sys
import math

from common import print_tour, read_input



# cities: 座標のリスト
# 座標のindexで表した、訪れる順番リスト（[0, 4, 2, ...]なら、0番目の座標からスタート、４番目→２番目...と進むということ
def solve_greedy(cities):

     
    # start, goalは(x, y)の座標
    def calc_distance(start, goal):
        return math.sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2)

    # 訪れる順番を保存するorder
    order = [0]

    # cities[cirrent_index]を今見ているということ
    current_index = 0

    unvisitted_ids = [i for i in range(len(cities))]

    while len(unvisitted_ids) > 1:

        # 最短距離を入れるmin_distance
        min_distance = float('inf')

        # 未訪問のcityリスト。自分自身にいくことはできないので取り除く
        unvisitted_ids.remove(current_index)
        

        for candidate_id in unvisitted_ids: # city は座標

            # 2点間の距離を計算
            d = calc_distance(cities[current_index], cities[candidate_id])

            # 最短距離の更新
            if min_distance > d:
                min_distance = d
                next_index = candidate_id # ここに最後に入っているindexが次に進むcityのindex
        
        order.append(next_index)
        current_index = next_index

    return order


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve_greedy(read_input(sys.argv[1]))
    print_tour(tour)
