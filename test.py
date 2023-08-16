#Given a number n, print a nxn matrix with each square is the ith step of knight (originaly placed at [0,0]) that covers the whole matrix. 
#if the knight cannot cover the whole matrix return -1. 

def find():
    n = int(input("Enter n:"))
    matrix = [[0 for _ in range(n)]for _ in range(n)]

    moves = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
    visited = [[0 for _ in range(n)]for _ in range(n)]
    visited[0][0] = 1
    def helper(r, c, moveCount):
        if moveCount == n*n:
            return True
        for i in range(8):
            row = r + moves[i][0]
            col = c + moves[i][1]
            if 0<=row<n and 0<=col<n and visited[row][col] == 0:
                visited[row][col] = moveCount+1
                if helper(row, col, moveCount+1):
                    return True
                visited[row][col] = 0
        return False
        
    
    if not helper(0,0, 0):
        print(-1)
        return
    for row in visited:
        print(row)

find()
    # for i in range(n):
    #     for j in range(n):
    #         if (i != 0 or j != 0) and matrix[i][j] == 0:
    #             return -1
    #         print(matrix[i][j], " ")
    #         if j == n-1:
    #             print("\n")
        
    
    