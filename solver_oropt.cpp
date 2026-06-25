#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <algorithm>
#include <string>
#include <fstream>
#include <sstream>

// commonモジュールの代替（コンパイルを通すための仮定義）
struct Point {
    double x;
    double y;
};

// 入力ファイルを読み込む関数
std::vector<Point> read_input(const std::string& filename) {
    std::vector<Point> cities;
    std::ifstream ifs(filename);
    
    // ファイルが開けない場合のエラー処理
    if (!ifs) {
        std::cerr << "Error: Cannot open file " << filename << std::endl;
        exit(1);
    }
    
    std::string line;
    
    // Pythonの f.readlines()[1:] と同じように、最初の1行を読み飛ばす
    std::getline(ifs, line);
    
    while (std::getline(ifs, line)) {
        if (line.empty()) continue;
        
        std::stringstream ss(line);
        std::string x_str, y_str;
        
        // カンマ区切りでxとyを取得
        if (std::getline(ss, x_str, ',') && std::getline(ss, y_str, ',')) {
            double x = std::stod(x_str);
            double y = std::stod(y_str);
            cities.push_back({x, y});
        }
    }
    
    return cities;
}

// 経路をフォーマットする関数 (Pythonの format_tour に相当)
std::string format_tour(const std::vector<int>& tour) {
    std::ostringstream oss;
    oss << "index\n";
    for (size_t i = 0; i < tour.size(); ++i) {
        oss << tour[i];
        if (i != tour.size() - 1) {
            oss << "\n";
        }
    }
    return oss.str();
}

// 経路を出力する関数 (Pythonの print_tour に相当)
void print_tour(const std::vector<int>& tour) {
    std::cout << format_tour(tour) << std::endl;
}


class Solve_greedy_Oropt {
public:
    std::vector<Point> cities;
    std::vector<int> order;

    Solve_greedy_Oropt(const std::vector<Point>& cities) : cities(cities) {}
     
    // start, goalは(x, y)の座標
    double calc_distance(const Point& start, const Point& goal) {
        return std::sqrt(std::pow(start.x - goal.x, 2) + std::pow(start.y - goal.y, 2));
    }
    
    // まだ訪れていないcityの中で、city_idに最も近いcityのidを返す
    int find_nearest_city(int city_id, const std::vector<int>& unvisited_ids) {
        // 最短距離を入れるmin_distance
        double min_distance = std::numeric_limits<double>::infinity();
        int next_index = -1;

        for (int candidate_id : unvisited_ids) {
            // 2点間の距離を計算
            double d = calc_distance(cities[city_id], cities[candidate_id]);

            // 最短距離の更新
            if (min_distance > d) {
                min_distance = d;
                next_index = candidate_id; // ここに最後に入っているindexが次に進むcityのindex
            }
        }

        // 最も近いcityのidを返す
        return next_index;
    }
        
    
    // greedyな解き方で訪れる順番を求める。このとき、移動の順番を表すself.orderを作る
    void greedy() {
        // 訪れる順番を入れたリスト
        order.clear();
        order.push_back(0);

        // cities[current_index]を今見ているということ
        int current_index = 0;

        std::vector<int> unvisited_ids;
        for (size_t i = 0; i < cities.size(); ++i) {
            unvisited_ids.push_back(i);
        }

        while (unvisited_ids.size() > 1) {
            // 未訪問のcityリスト。自分自身にいくことはできないので取り除く
            unvisited_ids.erase(std::remove(unvisited_ids.begin(), unvisited_ids.end(), current_index), unvisited_ids.end());
            
            int next_index = find_nearest_city(current_index, unvisited_ids);
            
            // current_indexを更新する
            current_index = next_index;
            order.push_back(current_index);
        }
    }
    
    // a_start, a_goal, b_start, b_goalは座標
    // a_start -> a_goal の線と b_start -> b_goal の線が交差するか判定
    // 方針：交差するかを直接判定するのではなく、交差するとして繋ぎかえたときに距離が短くなるかどうかを考える
    bool isCross(const Point& a_start, const Point& a_goal, const Point& b_start, const Point& b_goal) {
        if (calc_distance(a_start, a_goal) + calc_distance(b_start, b_goal) > calc_distance(a_start, b_start) + calc_distance(a_goal, b_goal)) {
            return true;
        } else {
            return false;
        }
    }
        

    void greedy_2opt() {
        // greedyの欠点は、残り少なくなってきた終盤で、大きくジャンプをしてしまい別の移動経路と交差すること。
        greedy();

        // C++の size_t アンダーフローを防ぐためのガード
        if (cities.size() < 2) return; 

        // 一回の更新で、変わったかどうか。何も変わらなかったらそこでループを抜ける
        bool change = true;
        
        while (change) {
            // 何も変わらなかった時のために最初はFalseにする
            change = false;
            for (size_t i = 0; i < cities.size() - 1; ++i) {

                // order[i]と、order[j]を比較するイメージ。隣り合う辺は比較する必要ないのでi + 2から始める
                for (size_t j = i + 2; j < cities.size() - 1; ++j) {

                    if (isCross(cities[order[i]], cities[order[i + 1]], cities[order[j]], cities[order[j + 1]])) {
                            // Pythonの self.order = self.order[:i + 1] + self.order[i+1: j+1][::-1] + self.order[j+1 :] は、C++のstd::reverseと等価
                            std::reverse(order.begin() + i + 1, order.begin() + j + 1);
                            change = true;
                    }
                }
            }
        }
    }

    void greedy_2opt_oropt() {

        greedy_2opt();

        bool change = true;

        while (change) {

            change = false;

            // 4つのノードA,B,C,Dの、A-BとC-Dを切って、他と繋げたらもっと短くならないか確かめる
            // vectorのサイズによるアンダーフローを防ぐため、十分な要素数があるか事前にチェック
            if (cities.size() < 4) break; 

            for (size_t i = 0; i < cities.size() - 3; ++i) {

                double distanceAB = calc_distance(cities[order[i]], cities[order[i + 1]]);
                double distanceCD = calc_distance(cities[order[i + 2]], cities[order[i + 3]]);
                double distanceAD = calc_distance(cities[order[i]], cities[order[i + 3]]);

                // 付け替えた時に減る長さ
                double minus_d = distanceAB + distanceCD - distanceAD;

                // 付け替えた時に増える長さの最小値とその時のindex
                double min_add_d = std::numeric_limits<double>::infinity();
                size_t min_add_i = i;

                // 別の部分の、E,Fの間に入れた時と比較する
                for (size_t j = 0; j < cities.size() - 1; ++j) {

                    if (i <= j && j <= i + 2) {
                        continue;
                    }

                    double distanceEF = calc_distance(cities[order[j]], cities[order[j + 1]]);
                    double distanceBF = calc_distance(cities[order[i + 1]], cities[order[j + 1]]);
    
                    double distanceCE = calc_distance(cities[order[i + 2]], cities[order[j]]);

                    double add_d = distanceCE + distanceBF - distanceEF;

                    if (add_d < minus_d && add_d < min_add_d) {
                        min_add_d = add_d;
                        min_add_i = j;
                    }
                }
                
                // 更新されているなら
                if (min_add_i != i) {
                    change = true;
                
                    // nodes = self.order[i+1 : i+3] 
                    std::vector<int> nodes = {order[i + 1], order[i + 2]};
                    std::reverse(nodes.begin(), nodes.end()); // [::-1] 相当

                    std::vector<int> new_order;
                    new_order.reserve(cities.size());
                    
                    if (i < min_add_i) {
                        // iの方が先: [最初〜A] + [D〜E] + [C, B] + [F〜最後]
                        new_order.insert(new_order.end(), order.begin(), order.begin() + i + 1);
                        new_order.insert(new_order.end(), order.begin() + i + 3, order.begin() + min_add_i + 1);
                        new_order.insert(new_order.end(), nodes.begin(), nodes.end());
                        new_order.insert(new_order.end(), order.begin() + min_add_i + 1, order.end());
                    } else {
                        // jの方が先: [最初〜E] + [C, B] + [F〜A] + [D〜最後]
                        new_order.insert(new_order.end(), order.begin(), order.begin() + min_add_i + 1);
                        new_order.insert(new_order.end(), nodes.begin(), nodes.end());
                        new_order.insert(new_order.end(), order.begin() + min_add_i + 1, order.begin() + i + 1);
                        new_order.insert(new_order.end(), order.begin() + i + 3, order.end());
                    }
                    
                    order = new_order;
                    
                    // 一度のループで変更は一回のみ
                    break;
                }
            }
        }
    }
};

int main(int argc, char* argv[]) {
    if (argc <= 1) {
        std::cerr << "Usage: " << argv[0] << " <input_file>" << std::endl;
        return 1;
    }

    std::vector<Point> cities = read_input(argv[1]);
    Solve_greedy_Oropt s(cities);
    s.greedy_2opt_oropt();

    std::vector<int> tour = s.order;

    print_tour(tour);

    return 0;
}