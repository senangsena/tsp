#!/usr/bin/env 
# python3 solver_greedy.py ../input/input_0.csv > ../output/output_0.csv

import sys
import math

from common import print_tour, read_input


class Solve_greedy_2opt:

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

        # 最短距離と、移動先のcityのidを返す
        return min_distance, next_index
        
    
    # greedyな解き方で訪れる順番を求める。このとき、各移動の経路長も保存し、順番とともに返す
    def greedy(self):

        # city間の移動を表すmapping 3 -> 5 -> 1 なら、{3: 5, 5: 1}が入る
        self.next = {}

        # 訪れる順番を入れたリスト
        self.order = [0]

        # 【2optのための変更点】そのcityから次のcityまでの経路を保存するmapping
        self.distances = {}

        # cities[cirrent_index]を今見ているということ
        current_index = 0

        unvisitted_ids = [i for i in range(len(self.cities))]

        while len(unvisitted_ids) > 1:

            # 未訪問のcityリスト。自分自身にいくことはできないので取り除く
            unvisitted_ids.remove(current_index)
            
            min_distance, next_index = self.find_nearest_city(current_index, unvisitted_ids)
            
            # 最短経路の長さをdistaicesに保存、nextに入れ、current_indexを更新する
            self.distances[current_index] = min_distance
            self.next[current_index] = next_index
            current_index = next_index
            self.order.append(current_index)

    
    # a_start, a_goal, b_start, b_goalは座標
    # a_start -> a_goal の線と b_start -> b_goal の線が交差するか判定
    # 方針：a_start -> a_goalの線分を考え、b_start、b_goalがどっち側にあるかをeval_start, eval_doalの正負で評価
    def isCross(self, a_start, a_goal, b_start, b_goal) -> bool:

        if self.calc_distance(a_start, a_goal) + self.calc_distance(b_start, b_goal) > self.calc_distance(a_start, b_start) + self.calc_distance(a_goal, b_goal):
            return True
        else:
            return False
        

    def greedy_2opt(self):
        # ここがメイン
        # greedyの欠点は、残り少なくなってきた終盤で、大きくジャンプをしてしまい別の移動経路と交差すること。
        self.greedy()
        
        # 全ての経路について交差を判定し付け替えをするのは計算量が膨大(最悪計算量O(N^2))なので、最大10回のみにする
        # count = 0

        # 一回の更新で、変わったかどうか。何も変わらなかったらそこでループを抜ける
        change = True
        
        # while count < 10:
        while change:

            # 何も変わらなかった時のために最初はFalseにする
            change = False
            for i in range(len(self.cities) - 1):

                for j in range(i + 1, len(self.cities) - 1):

                    if self.isCross(self.cities[self.order[i]], self.cities[self.order[i + 1]],self.cities[self.order[j]], self.cities[self.order[j + 1]]):
                            self.order = self.order[:i + 1] + self.order[i+1: j+1][::-1] + self.order[j+1 :]
                            change = True

            # count += 1
        



    

if __name__ == '__main__':
    assert len(sys.argv) > 1
    s = Solve_greedy_2opt(read_input(sys.argv[1]))
    s.greedy_2opt()


    tour = s.order
    

    print_tour(tour)
