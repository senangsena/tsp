# TSP
## ヒューリスティクス
* ⭐️**solver_or_opt.py**  
    greedy + 2opt + or-opt  
    任意の2つのノードを、別のノードとノードの間に繋ぎかえることを考える、Orーoptを実装した
* **solver_greedy_2opt.py**  
    貪欲法+2opt  
    交差する経路を繋ぎかえることで経路長を短縮する  

ヒューリスティクスなし
* **solver_random.py** 
    入力の順番通りに進む
* **solver_greedy.py**  
    貪欲法の実装  
    常に、そこから最も近いcityに進む

## プログラム
* greedy
``` python
    def greedy(self):

        # 訪れる順番を入れたリスト
        self.order = [0]

        # cities[cirrent_index]を今見ているということ
        current_index = 0

        unvisited_ids = [i for i in range(len(self.cities))]

        while len(unvisited_ids) > 1:

            # 未訪問のcityリスト。自分自身にいくことはできないので取り除く
            unvisited_ids.remove(current_index)
            # find_nearest_cityは、まだ訪れていないcityの中で、city_idに最も近いcityのidを返す
            next_index = self.find_nearest_city(current_index, unvisited_ids)
            
            # current_indexを更新する
            current_index = next_index
            self.order.append(current_index)
```
* 2-opt
``` python 
def greedy_2opt(self):
        # greedyの欠点は、残り少なくなってきた終盤で、大きくジャンプをしてしまい別の移動経路と交差すること。
        self.greedy()

        # 一回の更新で、変わったかどうか。何も変わらなかったらそこでループを抜ける
        change = True
        
        while change:

            # 何も変わらなかった時のために最初はFalseにする
            change = False
            for i in range(len(self.cities) - 1):

                # order[i]と、order[j]を比較するイメージ。隣り合う辺は比較する必要ないのでi + 2から始める
                for j in range(i + 2, len(self.cities) - 1):

                    if self.isCross(self.cities[self.order[i]], self.cities[self.order[i + 1]],self.cities[self.order[j]], self.cities[self.order[j + 1]]):
                            self.order = self.order[:i + 1] + self.order[i+1: j+1][::-1] + self.order[j+1 :]
                            change = True

```
* or-opt
``` python
   def greedy_2opt_oropt(self):

        self.greedy_2opt()

        change = True

        while change:

            change = False

            # 4つのノードA,B,C,Dの、A-BとC-Dを切って、他と繋げたらもっと短くならないか確かめる
            for i in range(len(self.cities) - 3):

                distanceAB = self.calc_distance(self.cities[self.order[i]], self.cities[self.order[i + 1]])
                distanceCD = self.calc_distance(self.cities[self.order[i + 2]], self.cities[self.order[i + 3]])
                distanceAD = self.calc_distance(self.cities[self.order[i]], self.cities[self.order[i + 3]])

                # 付け替えた時に減る長さ
                minus_d = distanceAB + distanceCD - distanceAD

                # 付け替えた時に増える長さの最小値とその時のindex
                min_add_d = float('inf')
                min_add_i = i

                # 別の部分の、E,Fの間に入れた時と比較する
                for j in range(len(self.cities) - 1):

                    if i <= j and (j <= i + 2):
                        continue

                    distanceEF = self.calc_distance(self.cities[self.order[j]], self.cities[self.order[j + 1]])
                    distanceBF = self.calc_distance(self.cities[self.order[i + 1]], self.cities[self.order[j + 1]])
    
                    distanceCE = self.calc_distance(self.cities[self.order[i + 2]], self.cities[self.order[j]])

                    add_d = distanceCE + distanceBF - distanceEF

                    if add_d < minus_d and (add_d < min_add_d):
                        min_add_d = add_d
                        min_add_i = j
                
                # 更新されているなら
                if min_add_i != i:
                    change = True
                
                    nodes = self.order[i+1 : i+3] 
                    
                    if i < min_add_i:
                        # iの方が先: [最初〜A] + [D〜E] + [C, B] + [F〜最後]
                        self.order = self.order[:i+1] + self.order[i+3 : min_add_i+1] + nodes[::-1] + self.order[min_add_i+1:]
                    else:
                        # jの方が先: [最初〜E] + [C, B] + [F〜A] + [D〜最後]
                        self.order = self.order[:min_add_i+1] + nodes[::-1] + self.order[min_add_i+1 : i+1] + self.order[i+3:]
                    
                    # 一度のループで変更は一回のみ
                    break

```


## 結果
greedy + 2-opt + Or-optの結果  
sample/sa は焼きなまし法の結果 
* challenge 0 ~ 5では、 焼きなまし法の方が短い距離を見つけることができるが、challenge 6で逆転　
* or-optは都市が多いほど効果が出る
* 小〜中規模なら焼きなまし法が強い

→ 現在の、or-optに、焼きなまし法を追加すればより良さそう

```
sena@SenanoMacBook-Air google-step-tsp % python3 output_verifier.py               
Challenge 0
output          :    3418.10
sample/random   :    3862.20
sample/sa       :    3291.62

Challenge 1
output          :    3832.29
sample/random   :    6101.57
sample/sa       :    3778.72

Challenge 2
output          :    5232.96
sample/random   :   13479.25
sample/sa       :    4494.42

Challenge 3
output          :    9261.01
sample/random   :   47521.08
sample/sa       :    8150.91

Challenge 4
output          :   11434.32
sample/random   :   92719.14
sample/sa       :   10675.29

Challenge 5
output          :   22314.05
sample/random   :  347392.97
sample/sa       :   21119.55

Challenge 6
output          :   43175.38
sample/random   : 1374393.14
sample/sa       :   44393.89

Challenge 7
output          :   83165.58
```

```
(tsp) sena@SenanoMacBook-Air google-step-tsp % python3 output_verifier.py 
Challenge 0
output          :    3418.10
sample/random   :    3862.20
sample/sa       :    3291.62

Challenge 1
output          :    3832.29
sample/random   :    6101.57
sample/sa       :    3778.72

Challenge 2
output          :    5232.96
sample/random   :   13479.25
sample/sa       :    4494.42

Challenge 3
output          :    9261.01
sample/random   :   47521.08
sample/sa       :    8150.91

Challenge 4
output          :   11591.84
sample/random   :   92719.14
sample/sa       :   10675.29

Challenge 5
output          :   22314.05
sample/random   :  347392.97
sample/sa       :   21119.55

Challenge 6
output          :   43825.39
sample/random   : 1374393.14
sample/sa       :   44393.89
```

## 2opt の実装
``` python
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
    
    # まだ訪れていないcityの中で、city_idに最も近いcityのidを返す
    def find_nearest_city(self, city_id: int, unvisited_ids: list[int]) -> int:
        # 最短距離を入れるmin_distance
        min_distance = float('inf')

        for candidate_id in unvisited_ids: 

            # 2点間の距離を計算
            d = self.calc_distance(self.cities[city_id], self.cities[candidate_id])

            # 最短距離の更新
            if min_distance > d:
                min_distance = d
                next_index = candidate_id # ここに最後に入っているindexが次に進むcityのindex

        # 最も近いcityのidを返す
        return next_index
        
    
    # greedyな解き方で訪れる順番を求める。このとき、移動の順番を表すself.orderを作る
    def greedy(self):

        # 訪れる順番を入れたリスト
        self.order = [0]

        # cities[cirrent_index]を今見ているということ
        current_index = 0

        unvisited_ids = [i for i in range(len(self.cities))]

        while len(unvisited_ids) > 1:

            # 未訪問のcityリスト。自分自身にいくことはできないので取り除く
            unvisited_ids.remove(current_index)
            
            next_index = self.find_nearest_city(current_index, unvisited_ids)
            
            # current_indexを更新する
            current_index = next_index
            self.order.append(current_index)

    
    # a_start, a_goal, b_start, b_goalは座標
    # a_start -> a_goal の線と b_start -> b_goal の線が交差するか判定
    # 方針：交差するかを直接判定するのではなく、交差するとして繋ぎかえたときに距離が短くなるかどうかを考える
    def isCross(self, a_start, a_goal, b_start, b_goal) -> bool:

        if self.calc_distance(a_start, a_goal) + self.calc_distance(b_start, b_goal) > self.calc_distance(a_start, b_start) + self.calc_distance(a_goal, b_goal):
            return True
        else:
            return False
        

    def greedy_2opt(self):
        # ここがメイン
        # greedyの欠点は、残り少なくなってきた終盤で、大きくジャンプをしてしまい別の移動経路と交差すること。
        self.greedy()

        # 一回の更新で、変わったかどうか。何も変わらなかったらそこでループを抜ける
        change = True
        
        while change:

            # 何も変わらなかった時のために最初はFalseにする
            change = False
            for i in range(len(self.cities) - 1):

                # order[i]と、order[j]を比較するイメージ。隣り合う辺は比較する必要ないのでi + 2から始める
                for j in range(i + 2, len(self.cities) - 1):

                    if self.isCross(self.cities[self.order[i]], self.cities[self.order[i + 1]],self.cities[self.order[j]], self.cities[self.order[j + 1]]):
                            self.order = self.order[:i + 1] + self.order[i+1: j+1][::-1] + self.order[j+1 :]
                            change = True
  

if __name__ == '__main__':
    assert len(sys.argv) > 1
    s = Solve_greedy_2opt(read_input(sys.argv[1]))
    s.greedy_2opt()

    tour = s.order

    print_tour(tour)

```
