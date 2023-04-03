import copy
def kill():
    global graph, ans
    target = 0
    memo = []
    for i in range(n):
        for j in range(n):
            if graph[i][j] >0:
                tmp = [(i,j)]
                sub = graph[i][j]
                for go in [(1,1),(1,-1),(-1,1),(-1,-1)]:
                    for power in range(1,k+1):
                        c1 = go[0]*power
                        c2 = go[1]*power
                        if not(0<=i+c1<n and 0<=j+c2<n): break
                        elif graph[i+c1][j+c2] < 0: break
                        elif graph[i+c1][j+c2] ==0:
                            tmp.append((i+c1,j+c2))
                            break
                        else:
                            sub += graph[i+c1][j+c2]
                            tmp.append((i+c1,j+c2))
                if sub > target:
                    target = sub
                    memo = tmp
    ans += target
    for d in memo:
        x1, y1 = d
        graph[x1][y1] = 0
        herb[x1][y1] = c
def delete_herb():
    for i in range(n):
        for j in range(n): 
            if herb[i][j] > 0: 
                herb[i][j] -= 1
    kill()
                         
def grow():
    global graph
    temp = copy.deepcopy(graph)
    for i in range(n):
        for j in range(n):
            if graph[i][j] >0:
                cnt = 0
                t = []
                for c in move:
                    new_i = i+c[0]
                    new_j = j + c[1]
                    if not(0<=new_i<n and 0<=new_j<n):continue
                    elif graph[new_i][new_j] ==0 and herb[new_i][new_j]==0:
                        cnt += 1
                        t.append((new_i,new_j))
                    elif 0<=new_i<n and 0<=new_j<n and graph[new_i][new_j] > 0:
                        temp[i][j] += 1
                if cnt !=0:
                    plus = temp[i][j]//cnt
                for x, y in t:
                    temp[x][y] += plus
    graph = temp
    delete_herb()

if __name__=='__main__':
    n, m ,k, c = map(int, input().split()) # 격자의 크기, 박멸이 진행되는 년 수, 제초제의 확산 범위, 남아있는 년 수
    graph = [list(map(int,input().split())) for _ in range(n)]
    herb = [
    [0] * (n)
    for _ in range(n)
    ]
    move = [(-1,0), (0,1),(1,0), (0,-1)]
    ans = 0
    for _ in range(m):
        grow()
    print(ans)
