'''
roate 부분은 해설 참고했습니다.
https://www.acmicpc.net/problem/17406 도 회전인것 같은데 연습해야겠습니다...
'''
def rotate_square(sx, sy, square_n):
    # 정사각형을 시계방향으로 90' 회전합니다.
    for x in range(sx, sx + square_n):
        for y in range(sy, sy + square_n):
            # Step 1. (sx, sy)를 (0, 0)으로 옮겨주는 변환을 진행합니다. 
            ox, oy = x - sx, y - sy
            # Step 2. 변환된 상태에서는 회전 이후의 좌표가 (x, y) -> (y, square_n - x - 1)가 됩니다.
            rx, ry = oy, square_n - ox - 1
            # Step 3. 다시 (sx, sy)를 더해줍니다.
            next_graph[rx + sx][ry + sy] = graph[x][y]

def rotate():
    # Step 1. next graph값을 초기화해줍니다.
    for i in range(n):
        for j in range(n):
            next_graph[i][j] = 0
    
    # Step 2. 회전을 진행합니다.
    # Step 2 - 1. 십자 모양에 대한 반시계 회전을 진행합니다.
    for i in range(n):
        for j in range(n):
            # Case 2 - 1. 세로줄에 대해서는 (i, j) -> (j, i)가 됩니다.
            if j == n // 2:
                next_graph[j][i] = graph[i][j]
            # Case 2 - 2. 가로줄에 대해서는 (i, j) -> (n - j - 1, i)가 됩니다.
            elif i == n // 2:
                next_graph[n-j-1][i] = graph[i][j]
    # Step 2 - 2. 4개의 정사각형에 대해 시계 방향 회전을 진행합니다.
    sqaure_n = n // 2
    rotate_square(0, 0, sqaure_n)
    rotate_square(0, sqaure_n + 1, sqaure_n)
    rotate_square(sqaure_n + 1, 0, sqaure_n)
    rotate_square(sqaure_n + 1, sqaure_n + 1, sqaure_n)
    
    # Step 3. next graph값을 다시 옮겨줍니다.
    for i in range(n):
        for j in range(n):
            graph[i][j] = next_graph[i][j]

def get_score():
    global group_n
    group_n = 0
    # visited 값을 초기화 해줍니다.
    for i in range(n):
        for j in range(n):
            visited[i][j] = False
    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                group_n += 1
                visited[i][j] = True
                group[i][j] = group_n
                group_cnt[group_n] = 1
                dfs(i, j)
    return get_art_score()

# (x, y) 위치에서 DFS를 진행합니다.
def dfs(x, y):
    for dx, dy in zip(dxs, dys):
        nx, ny = x + dx, y + dy
        # 인접한 칸 중 숫자가 동일하면서 방문한 적이 없는 칸으로만 이동이 가능합니다.
        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and graph[nx][ny] == graph[x][y]:
            visited[nx][ny] = True
            group[nx][ny] = group_n
            group_cnt[group_n] += 1
            dfs(nx, ny)
def get_art_score():
    art_score = 0
    # 특정 변을 사이에 두고 두 칸의 그룹이 다른 경우라면
    # (그룹 a에 속한 칸의 수 + 그룹 b에 속한 칸의 수) x 그룹 a를 이루고 있는 숫자 값 x 그룹 b를 이루고 있는 숫자 값
    # 만큼 예술 점수가 더해집니다.
    for i in range(n):
        for j in range(n):
            for dx, dy in zip(dxs, dys):
                nx, ny = i + dx, j + dy
                if 0 <= nx < n and 0 <= ny < n and graph[i][j] != graph[nx][ny]:
                    g1, g2 = group[i][j], group[nx][ny]
                    num1, num2 = graph[i][j], graph[nx][ny] # g1, g2의 숫자값
                    cnt1, cnt2 = group_cnt[g1], group_cnt[g2] #g1, g2에 속한 칸의 수
                    art_score += (cnt1 + cnt2) * num1 * num2
    # 중복 계산을 제외해줍니다.
    return art_score // 2

if __name__=='__main__':
    n = int(input())
    graph = [list(map(int, input().split())) for _ in range(n)]
    next_graph = [[0 for _ in range(n)] for _ in range(n)] # 회전 한 후의 그래프
    # 그룹의 개수를 관리합니다.
    group_n = 0
    # 각 칸에 그룹 번호를 적어줍니다.
    group = [[0 for _ in range(n)] for _ in range(n)]
    group_cnt = [0] * (n**2+1) # 각 그룹마다 칸의 수를 세줍니다.
    visited = [[False] * n for _ in range(n)]
    dxs, dys = [1, -1, 0, 0], [0, 0, 1, -1]
    # 3회전까지의 예술 점수를 더해줍니다.
    ans = 0
    for _ in range(4):
        # 현재 예술 점수를 더해줍니다.
        ans += get_score()
        # 회전을 진행합니다.
        rotate()
    print(ans)
