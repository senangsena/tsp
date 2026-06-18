#!/usr/bin/env 
# python3 solver_greedy.py ../input/input_0.csv > ../output/output_0.csv

import sys
import math

from common import print_tour, read_input


class Solve_greedy:

    def __init__(self, cities):
        self.cities = cities
     
    # start, goalは(x, y)の座標
    def calc_distance(self, start, goal):
        return math.sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2)
    
    # inthisAreaの中で、city_idに最も近いcityのidを返す
    def find_nearest_city(self, city_id: int, unvisitted_ids: list[int]) -> int:
        # 最短距離を入れるmin_distance
        min_distance = float('inf')

        for candidate_id in unvisitted_ids: 

            # 2点間の距離を計算
            d = self.calc_distance(self.cities[city_id], self.cities[candidate_id])

            # 最短距離の更新
            if min_distance > d:
                min_distance = d
                next_index = candidate_id # ここに最後に入っているindexが次に進むcityのindex

        # 移動先のcityのidを返す
        return next_index
        
    
    # greedyな解き方で訪れる順番を求める。このとき、各移動の経路長も保存し、順番とともに返す
    def greedy(self):

        # city間の移動の順番のリスト 3 -> 5 -> 1 なら、[3, 5, 1]
        self.order = [0]

        # cities[cirrent_index]を今見ているということ
        current_index = 0

        unvisitted_ids = [i for i in range(len(self.cities))]

        while len(unvisitted_ids) > 1:

            # 未訪問のcityリスト。自分自身にいくことはできないので取り除く
            unvisitted_ids.remove(current_index)
            
            next_index = self.find_nearest_city(current_index, unvisitted_ids)
            
            self.order.append(next_index)
            current_index = next_index



if __name__ == '__main__':
    assert len(sys.argv) > 1
    s = Solve_greedy(read_input(sys.argv[1]))
    s.greedy()
    tour = s.order
    print_tour(tour)
