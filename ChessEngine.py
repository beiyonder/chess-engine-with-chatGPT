"""
This file will store all the information about the current state of the game.
It'll calculate the valid moves at the current state.
It'll keep a log of all moves
"""

class GameState():
    #constructor here
    #Two dimenstional list will be used. Numpy array could also be used for more effciency (TO be checked afterwords)
    def __init__(self):
        #"0" is black space. b is black, w is white, 
        self.board = [
            ["bR","bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "bN", "0", "0", "wN", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR","wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True

        self.moveLog = [] #stores the moves 
    def whoseTurn(self):
        '''prints white or black depending on who's turn it is currently'''
        return "w" if self.whiteToMove else "b"

    def makeMove(self, move):
        """This won't work for complex moves like casting, en-passant and pawn promotion"""

        self.board[move.startRow][move.startCol] = "0"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove #switch turns

    def undo(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        """Get all moves considering checks"""

        return self.getAllPossibleMoves()
    
    def getAllPossibleMoves(self):
        """Calculates all possible moves without considering checks"""
        # moves = [Move((1,1), (2,2), self.board)] # just to check
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0] #e.g., board[r][c] = "wR" then board[r][c][0] = "w"
                
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    pieceType = self.board[r][c][1]

                    if pieceType == 'P':
                        self.generatePawnMoves( r, c, moves)
                        # print("hi")
                    if pieceType == 'R':
                        self.generateRookMoves( r, c, moves)
                        # print("Rook moves calculated")
                    if pieceType == 'N':
                        self.generateKnightMoves( r, c, moves)
                    if pieceType == 'B':
                        self.generateBishopMoves( r, c, moves)
                    if pieceType == 'Q':
                        self.generateQueenMoves( r, c, moves)
                    if pieceType == 'K':
                        self.generateKingMoves( r, c, moves)
        return moves

    def generatePawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn valid moves

            if self.board[r-1][c] == "0":
                moves.append( Move((r, c), (r-1,c), self.board) )
                if r==6 and self.board[r-2][c]:
                    moves.append( Move((r, c), (r-2,c), self.board) )

            if c+1 < 8 and self.board[r-1][c+1][0] == 'b':
                moves.append( Move((r, c), (r-1,c+1), self.board) )

            if c-1 >= 0 and self.board[r-1][c-1][0] == 'b':
                moves.append( Move((r, c), (r-1,c-1), self.board) )

            #PAWN PROMTION BELOW:   

        else: #black pawn valid moves
            if self.board[r+1][c] == "0":
                moves.append( Move((r, c), (r+1,c), self.board) )
                if r==1 and self.board[r+2][c]:
                    moves.append( Move((r, c), (r+2,c), self.board) )
                    # print(moves)

            if c+1 < 8 and self.board[r+1][c+1][0] == 'w':
                moves.append( Move((r, c), (r+1,c+1), self.board) )

            if c-1 >= 0 and self.board[r+1][c-1][0] == 'w':
                moves.append( Move((r, c), (r+1,c-1), self.board) )
            
            #PAWN PROMTION BELOW:

    def generateRookMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1, 0), ((0, 1))) 
        # player = self.whoseTurn()
        # enemy = "b" if player == "w" else "w"
        enemy  = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "0":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r,c),(endRow, endCol ), self.board))
                        print('enemy piece capture bis')
                        break
                    else:
                        break
                else:
                    break
    
                # if 0 <= endRow < 8 and 0 <= endCol < 8:  # piece on board
                #     row_range = range(r + 1, endRow) if d[0] != 0 else [r] * (abs(endCol - c) - 1)
                #     col_range = range(c + 1, endCol) if d[1] != 0 else [c] * (abs(endRow - r) - 1)

                #     for row, col in zip(row_range, col_range):
                #         if self.board[row][col][0] == enemy:
                #             moves.append(Move((r, c), (row, col), self.board))
                #             break
                #         elif self.board[row][col] == "0":
                #             moves.append(Move((r, c), (row, col), self.board))
                #         else:
                #             break
        
                                    
    def generateKnightMoves(self, r, c, moves):
        teamPiece = "w" if self.whiteToMove else "b"
        directions = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        for d in directions:
            endRow = r+d[0]
            endCol = c+d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if self.board[endRow][endCol][0] != teamPiece: # count it valid if the (endRow, endCol) position has anything expect team's piece
                    moves.append(Move((r, c),(endRow, endCol ), self.board))
                
                
    def generateBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1),(1, 1)]
        enemy = "b" if self.whiteToMove else "w"
        for dir in directions:
            for i in range(1, 8):
                endRow = r + dir[0]*i
                endCol = c + dir[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "0":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r,c),(endRow, endCol ), self.board))
                        break
                    else:
                        break
                else:
                    break 
    def generateQueenMoves(self, r, c, moves):
        self.generateBishopMoves(r,c, moves)
        self.generateRookMoves(r,c,moves)

    def generateKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        teamPiece = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != teamPiece:
                    moves.append(Move((r,c), (endRow, endCol), self.board))

class Move():
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, start, end, board):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow *1000 + self.startCol*100 + self.endRow*10 + self.endCol
        print("Move ID", self.moveID)
    
    def __eq__(self, other):
        """The move made by the user and the valid move cannot be compared in python
        because they two are different objects - hence the existance of this function"""
        """This is called overidding the equals method"""
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getCoordinates(self):
        return self.getRankFiles(self.startRow, self . startCol) + self .getRankFiles(self .endRow, self .endCol)

    def getRankFiles(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
        