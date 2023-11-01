""" Este es el programa principal, recibe el input del usuario :D """
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGENES = {}

"""Se llaman las imágenes una vez en el main."""

def CargarImagen():
    piezas = ["wp", "wR", "wN", "wB","wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for pieza in piezas:
        IMAGENES[pieza] = p.transform.scale(p.image.load("IMAGES/" + pieza + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((HEIGHT,WIDTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white "))
    gs = ChessEngine.EstadoDelJuego()
    validMoves = gs.ObtenerMovimientosValidos()
    moveMade = False

    CargarImagen()
    running = True
    sqSelected = ()#ninguna casilla ha sido selecionada
    playerClicks = []#Guarda los inputs del usuario


    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #Esto determina el input() del usario en X y Y
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    Movimiento = ChessEngine.Movimiento(playerClicks[0], playerClicks[1], gs.board)
                    print(Movimiento.getChessNotation())
                    if Movimiento in validMoves:
                        gs.HacerMovimiento(Movimiento)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.deshacerMovimiento()
                    moveMade = True
        if moveMade:
            validMoves = gs.ObtenerMovimientosValidos()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

""" Responsable de los gráficos """

def drawGameState(screen,gs):
    drawBoard(screen) #Dibuja Cuadrados
    drawpieces(screen, gs.board) #Dibuja las piezas encima de los tableros

"""Dibuja los cuadraditos"""
#Nota el cuadro de arriba a la iquierda siempre será blanco

def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range (DIMENSION):
        for c in range (DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
"""Dibuja las piezas usando GameState.board"""

def drawpieces(screen, board):
    for r in range (DIMENSION):
        for c in range(DIMENSION):
            pieza = board[r][c]
            if pieza != "--":
                screen.blit(IMAGENES[pieza], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    main()