#!/usr/bin/env 
# python3 solver_greedy.py ../input/input_0.csv > ../output/output_0.csv

import sys
import math

from common import print_tour, read_input



# cities: 座標のリスト
# 座標のindexで表した、訪れる順番リスト（[0, 4, 2, ...]なら、0番目の座標からスタート、４番目→２番目...と進むということ
def solve_greedy_2opt(cities):
     
    # start, goalは(x, y)の座標
    def calc_distance(start, goal):
        return math.sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2)
    
    # greedyな解き方で訪れる順番を求める。このとき、各移動の経路長も保存し、順番とともに返す
    def greedy(cities):

        # city間の移動を表すmapping 3 -> 5 -> 1 なら、{3: 5, 5: 1}が入る
        order = {}

        # 【2optのための変更点】そのcityから次のcityまでの経路を保存するmapping
        distances = {}

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
            
            # 最短経路の長さをdistaicesに保存、orderに入れ、current_indexを更新する
            distances[current_index] = min_distance
            order[current_index] = next_index
            current_index = next_index

        return order, distances
    
    # ここがメイン
    greedy_result, distances = greedy(cities)
    print(greedy_result, distances)
    sorted_distances = dict(sorted(distances.items(), key = lambda item:item[1], reverse = True))

    return [0,1,2,3,4]





if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve_greedy_2opt(read_input(sys.argv[1]))
    print_tour(tour)
