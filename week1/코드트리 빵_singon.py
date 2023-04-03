import sys
input = sys.stdin.readline
INF = sys.maxsize
from collections import deque

def bfs(start):
    global step, visited
    que = deque()
    que.append((start[0],start[1]))
    visited = [[False for _ in range(n)] for _ in range(n)]
    step = [[0]*n for _ in range(n)]
    visited[start[0]][start[1]] = True
    
    while que:
        r, c= que.popleft()
        for go in move:
            new_r = r + go[0]
            new_c = c + go[1]
            if 0<=new_r<n and 0<=new_c<n and not visited[new_r][new_c] and graph[new_r][new_c] !=3:
                visited[new_r][new_c] = True
                step[new_r][new_c] = step[r][c] + 1
                que.append((new_r,new_c))


def main():
    global visited, step
    for i in range(m): # f home->convs onto 이므로 편의점은 다 집이랑 대응이 된다.
        if people[i] == (-1,-1) or people[i] == convs[i]: continue
        bfs(convs[i]) # 편의점에서 각 베이스캠프까지 거리를 보고 가장 짧은 곳으로 목적지를 정하기 위해
        px, py = people[i] # 현재 i번째 사람 위치
        min_dist = INF
        min_x, min_y = -1, -1
        for go in move:
            new_x, new_y = px+go[0], py+go[1]
            if 0<=new_x<n and 0<=new_y<n and visited[new_x][new_y] and min_dist>step[new_x][new_y]:
                min_dist = step[new_x][new_y]
                min_x, min_y = new_x, new_y
        people[i] = (min_x, min_y)

    for i in range(m):
        if people[i] == convs[i]:
            px, py = people[i]
            graph[px][py] = 3
    if time>m:
        return
    # 초기 세팅
    bfs(convs[time-1])
    min_dist = INF
    min_x, min_y = -1, -1
    for i in range(n):
        for j in range(n):
            if visited[i][j] and graph[i][j] == 1 and min_dist>step[i][j]: # convs[time-1]에서 가장 가까운 곳
                min_dist= step[i][j]
                min_x, min_y = i, j
    people[time-1] = (min_x, min_y) # people[i]를 conv[i]로 가는 것으로 목적지 매칭
    graph[min_x][min_y] = 3 # 사용 불가

def check():
    for i in range(m):
        if people[i] != convs[i]:
            return False
    return True

if __name__=='__main__':
    n, m = map(int, input().split()) # 격자 길이, 사람의 수
    graph = [list(map(int, input().split())) for _ in range(n)]
    convs = []
    for _ in range(m): # 편의점이 m개 만큼 있다고 합니다...
        r, c = map(int,input().split()) # 편의점 좌표
        convs.append((r-1,c-1))
    move = [(-1,0),(0,-1),(0,1),(1,0)] # 우선순서
    people = [[-1,-1] for _ in range(m)]
    time = 0
    visited = [[False for _ in range(n)] for _ in range(n)]
    step = [[0 for _ in range(n)] for _ in range(n)]
    while True:
        time += 1
        main()
        if check():
            break
    print(time)


