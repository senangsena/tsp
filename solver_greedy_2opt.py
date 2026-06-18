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
        self.order = {}

        # 【2optのための変更点】そのcityから次のcityまでの経路を保存するmapping
        self.distances = {}

        # cities[cirrent_index]を今見ているということ
        current_index = 0

        unvisitted_ids = [i for i in range(len(cities))]

        while len(unvisitted_ids) > 1:

            # 未訪問のcityリスト。自分自身にいくことはできないので取り除く
            unvisitted_ids.remove(current_index)
            
            min_distance, next_index = self.find_nearest_city(current_index, unvisitted_ids)
            
            # 最短経路の長さをdistaicesに保存、orderに入れ、current_indexを更新する
            self.distances[current_index] = min_distance
            self.order[current_index] = next_index
            current_index = next_index

    
    # a_start, a_goal, b_start, b_goalは座標
    # a_start -> a_goal の線と b_start -> b_goal の線が交差するか判定
    # 方針：a_start -> a_goalの線分を考え、b_start、b_goalがどっち側にあるかをeval_start, eval_doalの正負で評価
    def isCross(self, a_start, a_goal, b_start, b_goal) -> bool:

        # a_start -> a_goalの線文が満たす、方程式 y = ax + bの係数a, bを求める
        # a_startのx座標 == a_goalのx座標　の時、傾き存在しないので別枠で考える
        if a_start[0] == a_goal[0]:
            eval_start = b_start[0] - a_start[0]
            eval_goal = b_goal[0] - a_start[0]

        else:
            a = (a_start[1] - a_goal[1]) / (a_start[0] - a_goal[0])
            b = (a_start[0]*a_goal[1] - a_start[1]*a_goal[0]) / (a_start[0] - a_goal[0])

            # y - ax - bの正負で評価
            eval_start = b_start[1] - a * b_start[0] - b
            eval_goal = b_goal[1] - a * b_goal[0] - b

        if eval_start * eval_goal <= 0:
            return True
        else:
            return False
        
    def hasCross(self, city_id):
        
        # クロスする候補
        candidate = [i for i in range(len(self.cities))]
        candidate.remove(city_id)

        for id in candidate:
            if self.isCross(self.cities[city_id], self.cities[self.order[city_id]], self.cities[id], self.cities[self.order[id]]):
                return True
        
        return False

    def greedy_2opt(self):
        # ここがメイン
        # greedyの欠点は、残り少なくなってきた終盤で、大きくジャンプをしてしまい別の移動経路と交差すること。
        greedy_result, distances = self.greedy(self.cities)
        print(greedy_result, distances)
        sorted_distances = dict(sorted(distances.items(), key = lambda item:item[1], reverse = True))

        # 全ての経路について交差を判定し付け替えをするのは計算量が膨大(最悪計算量O(N^2)?)
        # そこで上位から見ていき、交差しない経路を見つけたらそこで交差探索を終了する(これも計算量自体はO(N^2)?)
        
        for id in sorted_distances[:5]:

            # id から出る線が、他とクロスするかどうかを判定
            # クロスするなら、id と、order[id](idの次に訪れることになってるcity)を、それぞれ一番近くのcityに結びつける
            # idから最も近いcity をcityAとして、現在cityA -> cityBに移動してるとすると、その間にidを入れてcityA -> id -> cityBにするということ
            if self.hasCross(id):

                old_nextID = self.order[id]

                # まずはid側を繋ぎかえる
                cityA = self.find_nearest_city(id)
                cityB = self.order[cityA]

                self.order[cityA] = id
                self.order[id] = cityB

                # 次にold_nextID側を繋ぎかえる
                cityA = self.find_nearest_city(old_nextID)
                cityB = self.order[cityA]

                self.order[cityA] = old_nextID
                self.order[id] = cityB
    






if __name__ == '__main__':
    assert len(sys.argv) > 1
    s = Solve_greedy_2opt(read_input(sys.argv[1]))
    s.greedy_2opt()


    tour = [0]
    index = 0

    while True:
        if s.order[index] != None:
            tour.append(s.order[index])
            index = s.order[index]
        else:
            break
        
    print_tour(tour)
