"""
This is the main driver file.
It contains code to run all other modules and functions in this project.
"""
import pygame as p
import ChessEngine
import openai 

# openai.api_key = "API_KEY_ to add here"

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION #square size
MAX_FPS = 15
IMAGES = {}
#Loading images is expensive. I should load it only once and use them afterwards

#-------------------------GPT --------------------------------------
# def generate_gpt_response(context):
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=context,
#         max_tokens=50  # You can adjust the response length as needed
#     )
#     return response.choices[0].text.strip()
#----------------------------------------------------------------------
def loadImages():
    pieces = ['wP', 'wR', 'wB', 'wN', 'wQ', 'wK', 'bP', 'bR', 'bB', 'bN', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece +".png"), (SQ_SIZE, SQ_SIZE))

"""
The Followig is the Main driver. 
This will include:
    handling user input and updating the graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    #print(gs.board)
    validMoves = gs.getValidMoves()
    moveMade = False #a parameter to decide whether to generate new set of validMoves. if moveMade == True then generate new set of ValidMoves
    
    loadImages() 
    running = True
    selectedSquare = () #store the previously selected square
    
    playerMove = [] 
    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False
            #Upon clicking mouse - following happens
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # get the x, y coords of the mouse pointer
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                piece = gs.board[row][col]

                # print(gs.whoseTurn())

                if selectedSquare == (row , col):
                    selectedSquare = ()
                    playerMove = []
                else:
                    selectedSquare = (row, col)
                    playerMove.append(selectedSquare)
                if len(playerMove) == 2:
                    move = ChessEngine.Move(playerMove[0], playerMove[1], gs.board)
                    
                    print(move.getCoordinates())

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        coord1 = playerMove[0]
                        # coord2 = playerMove[1]
                        piece1 = gs.board[coord1[0]][coord1[1]]
                        if piece1 != "0":
                            gs.makeMove(move)
                        selectedSquare = ()
                        playerMove = []
                    else:
                        playerMove = [selectedSquare]
                        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u: # undo when 'u' key is pressed
                    gs.undo()
                    # validMoves = gs.getValidMoves()
                    moveMade =  True
                    
        if moveMade:
            validMoves = gs.getValidMoves()   
            moveMade = False
#------------------------------GPT stuff -------------------------------------------------------------
        # current_board_state = gs.generateCurrentBoardState()
        # previous_moves = gs.generatePreviousMoves()

        # Create a context for GPT
        # context = f"Player is about to make a move. Here's the current state of the game:\n\n{current_board_state}\n\nMoves played: {previous_moves}\n\nWhat move do you suggest?"

        # Generate GPT response based on the game state
        # gpt_response = generate_gpt_response(context)

        # Draw game state and GPT response
        # drawGameState(screen, gs)
        # drawGPTResponse(screen, gpt_response)
#--------------------------------------------------------------------------------------------
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
#--------------------------------GpT---------------------------------------
def drawGPTResponse(screen, response_text):
    font = p.font.Font(None, 18)
    text = font.render(response_text, True, (0, 0, 0))
    text_rect = text.get_rect(topleft=(10, HEIGHT + 10))
    screen.blit(text, text_rect)
#-------------------------------------------------------------------------
def drawGameState(screen, gs):
    """Draw/display graphics within the current game
    """
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    WHITE = (204, 255, 153)
    BLACK = (76, 153, 0)
    
    # screen = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    p.display.set_caption('Chessboard')
    FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    font = p.font.Font(None, 18)
    for row in range(8):
        for col in range(8):
            x = col * SQ_SIZE
            y = row * SQ_SIZE

            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK

            p.draw.rect(screen, color, p.Rect(x, y, SQ_SIZE, SQ_SIZE))

            if row == 7:  # Display file names along the bottom row
                file_label = FILES[col]
                text = font.render(file_label, True, (0, 0, 0))
                # text_rect = text.get_rect(topleft=(x + SQ_SIZE//2 + 2, y + SQ_SIZE//2 + 2))
                text_rect = text.get_rect(bottomright=(x + SQ_SIZE - 3, y + SQ_SIZE - 3))
                screen.blit(text, text_rect)
            if col == 0:  # Display rank names along the left column
                rank_label = str(8 - row)
                text = font.render(rank_label, True, (0, 0, 0))
                text_rect = text.get_rect(topleft=(x  + 5, y  + 5))
                # text_rect = text.get_rect(bottomright=(x + SQ_SIZE - 5, y + SQ_SIZE - 5))
                screen.blit(text, text_rect)
            
   

def drawPieces(screen, board): #stuff inside this function could also be done inside drawBoard function but it might not allow me add-in other cool features to the pieces
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece!= '0':
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()