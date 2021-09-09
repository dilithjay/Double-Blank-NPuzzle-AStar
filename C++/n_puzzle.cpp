#include <iostream>
#include <queue>
#include <vector>
#include <tuple>
#include <string>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <ctime>


class Node{
    public:
        std::string** config;
        int **blank_pair;
        int cost;
        std::vector<std::string> path;

        friend bool operator<(const Node& n1, const Node& n2){
            // return n1.cost > n2.cost;
            return n1.path.size() > n2.path.size();
        }
};

enum HeuristicType{
    MISPLACED = 1,
    MANHATTAN
};

int get_heuristic_misplaced(std::string **mat1, std::string **mat2, const int n){
    int cost = 0;
    for (int r = 0; r < n; r++){
        for (int c = 0; c < n; c++){
            if (mat1[r][c] != mat2[r][c] && mat1[r][c] != "-" && mat2[r][c] != "-"){
                cost += 1;
            }
        }
    }
    return cost;
}

int get_heuristic_manhattan(std::string **mat1, std::string **mat2, const int n){
    int cost = 0;
    std::unordered_map<std::string, int[2]> umap;

    for (int r = 0; r < n; r++){
        for (int c = 0; c < n; c++){
            const std::string s = mat2[r][c];
            if (s != "-"){
                umap[s][0] = r;
                umap[s][1] = c;
            }
        }
    }

    for (int r = 0; r < n; r++){
        for (int c = 0; c < n; c++){
            const std::string s = mat1[r][c];
            if (s != "-"){
                cost += abs(r - umap[s][0]) + abs(c - umap[s][1]);
            }
        }
    }
    return cost;
}

int get_cost(std::string** mat1, std::string **mat2, const int n, const HeuristicType type){
    if (type == MISPLACED){
        return get_heuristic_misplaced(mat1, mat2, n);
    }
    return get_heuristic_manhattan(mat1, mat2, n);
}

void print_path(const std::vector<std::string> path){
    for (std::string s : path){
        std::cout << s << ", ";
    }
    std::cout << std::endl;
}

void print_matrix(std::string **mat, const int n){
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            std::cout << mat[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

void print_node_details(Node node_1, const int n){
    std::cout << "==========" << std::endl;
    std::cout << "Node Data:" << std::endl;
    print_matrix(node_1.config, n);
    std::cout << "blank: {{" << node_1.blank_pair[0][0] << "," << node_1.blank_pair[0][1] << "}, {" << node_1.blank_pair[1][0] << "," << node_1.blank_pair[1][1] << "}}" << std::endl;
    std::cout << "cost: " << node_1.cost << std::endl;
    std::cout << "path: ";
    print_path(node_1.path);
    std::cout << "==========" << std::endl;
}

void copy_matrix(std::string** mat1, std::string **mat2, const int n){
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            mat1[i][j] = mat2[i][j];
        }
    }
}

void swap(std::string **mat, const int r1, const int c1, const int r2, const int c2){
    std::string temp = mat[r1][c1];
    mat[r1][c1] = mat[r2][c2];
    mat[r2][c2] = temp;
}

std::string join_string_matrix (std::string **mat, const int n){
    std::string s = "";
    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            s += mat[i][j] + ",";
        }
    }
    s.pop_back();
    return s;
}

std::string number_to_string ( int number )
{
    std::ostringstream ss;
    ss << number;
    return ss.str();
}

int main(){
    int size;
    std::cout << "Enter n: ";
    std::cin >> size;
    const int n = size;
    const HeuristicType type = MANHATTAN;

    int dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    std::string opposite_dirs[4] = {"down", "up", "right", "left"};

    int **blank0 = new int*[2];
    int blank_i = 0;
    for(int i = 0; i < 2; i++){
        blank0[i] = new int[2];
    }
    
    std::string** start = new std::string*[n];
    for(int i = 0; i < n; i++){
        start[i] = new std::string[n];
        for (int j = 0; j < n; j++){
            std::cin >> start[i][j];
            if (start[i][j] == "-"){
                blank0[blank_i][0] = i;
                blank0[blank_i][1] = j;
                blank_i++;
            }
        }
    }

    std::string** goal = new std::string*[n];
    for(int i = 0; i < n; i++){
        goal[i] = new std::string[n];
        for (int j = 0; j < n; j++){
            std::cin >> goal[i][j];
        }
    }

    std::time_t start_time = std::time(NULL);

    std::priority_queue<Node> pq{};
    Node node1{start, blank0, get_cost(start, goal, n, type), std::vector<std::string>()};
    pq.push(node1);

    std::unordered_set<std::string> open_set{};

    while (!pq.empty()){
        Node node = pq.top();
        pq.pop();
        // std::cout << "a" << std::endl;
        // print_node_details(node, n);
        // print_path(node.path);

        std::string config_s = join_string_matrix(node.config, n);

        if (open_set.find(config_s) == open_set.end()){
            open_set.insert(config_s);
        }
        else{
            continue;
        }

        if (node.cost == node.path.size()){
            print_path(node.path);
            break;
        }
        
        for (int j = 0; j < 4; j++){
            // std::cout << "------------ i: " << i << std::endl;
            // std::cout << "b0: " << blank1[0] << "," << blank1[1] << std::endl;

            for (int i = 0; i < 2; i++){
                int blank1[2];
                blank1[0] = node.blank_pair[i][0];
                blank1[1] = node.blank_pair[i][1];
                // std::cout << "------------- j: " << j << std::endl;
                const int r = blank1[0] + dirs[j][0];
                const int c = blank1[1] + dirs[j][1];
                // std::cout << "c: " << r << "," << c << std::endl;

                if (0 <= r && r < n && 0 <= c && c < n && node.config[r][c] != "-"){
                    std::string **mat = new std::string*[n];
                    for(int k = 0; k < n; k++)
                        mat[k] = new std::string[n];
                    
                    copy_matrix(mat, node.config, n);
                    // print_matrix(mat, n);
                    swap(mat, blank1[0], blank1[1], r, c);
                    const int cost = get_cost(mat, goal, n, type);


                    // std::cout << "\ne: " + number_to_string(mat[r][c]) << std::endl;
                    std::vector<std::string> path_new = node.path;
                    path_new.push_back("(" + mat[blank1[0]][blank1[1]] + "," + opposite_dirs[j] + ")");
                    // print_path(path_new);

                    int **blank2 = new int*[2];
                    for(int i = 0; i < 2; i++){
                        blank2[i] = new int[2];
                    }
                    blank2[0][0] = node.blank_pair[(i + 1)%2][0];
                    blank2[0][1] = node.blank_pair[(i + 1)%2][1];
                    blank2[1][0] = r;
                    blank2[1][1] = c;

                    Node node_new{mat, blank2, cost + (int)path_new.size(), path_new};
                    pq.push(node_new);
                }
            }
        }
        delete(node.config);
        delete(node.blank_pair);
    }

    delete(goal);

    std::cout << std::time(NULL) - start_time << " seconds" << std::endl;
}

/*
1	4	-	7
9	2	3	5
6	-	10	13
8	11	14	12
1	4	7	5
9	2	3	-
-	11	10	13
6	8	14	12

1 4 - 7
9 2 3 5
6 - 10 13
8 11 14 12
1 4 7 5
9 2 3 -
- 11 10 13
6 8 14 12
*/

/*
[['-', '1', '6', '14'], ['7', '4', '5', '2'], ['3', '11', '8', '9'], ['12', '-', '13', '10']]
[['12', '10', '2', '1'], ['5', '4', '7', '9'], ['-', '11', '8', '13'], ['6', '-', '3', '14']]

-   1   6   14
7   4   5   2
3   11  8   9
12  -   13  10
12  10  2   1
5   4   7   9
-   11  8   13
6   -   3   14

-   1   6   14
7   4   5   2
3   11  8   9
12  -   13  10
1   4   -   6
7   -   2   14
3   5  10   8
12  11  13  9
*/