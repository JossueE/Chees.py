""" Aquí se guarda la información de los movimientos, es la responsable de guardar los valores de movimiento """

class EstadoDelJuego():
    def __init__(self):
        #El tablero es de 8x8 graficamente r=8 c=16
        #La primera letra representa w = blanco y b = negro
        #La segunda representa el tipo
        # "--" es un espacio vacío
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.MovimientoFunctions = {"p": self.ObtenerMovimientosPeon, "R": self.ObtenerMovimientosTorre, "N": self.ObtenerMovimientosCaballero,
                              "B": self.ObtenerMovimientosAlfil, "Q": self.ObtenerMovimientosReyna, "K": self.ObtenerMovimientosRey}

        self.MovimientoBlanco = True
        self.MovimientoLog = []
        self.LugarReyBlanco = (7,4)
        self.LugarReyNegro = (0,4)

    def HacerMovimiento(self,Movimiento):
        self.board[Movimiento.startRow][Movimiento.startCol] = "--"
        self.board[Movimiento.endRow][Movimiento.endCol] = Movimiento.PiezaMovida
        self.MovimientoLog.append(Movimiento)
        self.MovimientoBlanco = not self.MovimientoBlanco

        if Movimiento.PiezaMovida == "wK":
            self.LugarReyBlanco = (Movimiento.endRow, Movimiento.endCol)

        elif Movimiento.PiezaMovida == "bK":
            self.LugarReyNegro = (Movimiento.endRow, Movimiento.endCol)

    def deshacerMovimiento(self):
        if len(self.MovimientoLog) != 0:
            Movimiento = self.MovimientoLog.pop()
            self.board[Movimiento.startRow][Movimiento.startCol] = Movimiento.PiezaMovida
            self.board[Movimiento.endRow][Movimiento.endCol] = Movimiento.PiezaCaptured
            self.MovimientoBlanco = not self.MovimientoBlanco

            if Movimiento.PiezaMovida == "wK":
                self.LugarReyBlanco = (Movimiento.startRow, Movimiento.startCol)

            elif Movimiento.PiezaMovida == "bK":
                self.LugarReyNegro = (Movimiento.startRow, Movimiento.startCol)

    def ObtenerMovimientosValidos(self):
        Movimientos = self.TodosLosMovimientosPosibles()
        for i in range(len(Movimientos)-1, -1, -1):
            self.HacerMovimiento(Movimientos[i])
            self.MovimientoBlanco = not self.MovimientoBlanco
            if self.enJake():
                Movimientos.remove(Movimientos[i])
            self.MovimientoBlanco = not self.MovimientoBlanco
            self.deshacerMovimiento()
        if len(Movimientos) == 0:
            if self.enJake():
                self.CheckMate = True
            else:
                self.staleMate = True

        else:
            self.CheckMate = False
            self.staleMate = False

        return Movimientos

    def enJake(self):
        if self.MovimientoBlanco:
            return self.CuadradoBajoAtaque(self.LugarReyBlanco[0], self.LugarReyBlanco[1])
        else:
            return self.CuadradoBajoAtaque(self.LugarReyNegro[0], self.LugarReyNegro[1])

    def CuadradoBajoAtaque(self, r, c):
        self.MovimientoBlanco = not self.MovimientoBlanco
        oppMovimientos = self.TodosLosMovimientosPosibles()
        for Movimiento in oppMovimientos:
            if Movimiento.endRow == r and Movimiento.endCol == c:
                return True
        return False


    def TodosLosMovimientosPosibles (self):
        Movimientos = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.MovimientoBlanco) or (turn == 'b' and not self.MovimientoBlanco):
                    Pieza = self.board[r][c][1]
                    self.MovimientoFunctions[Pieza](r, c, Movimientos)
        return Movimientos

    def ObtenerMovimientosPeon(self, r, c, Movimientos):
        if self.MovimientoBlanco:  # Blanco Peon Movimientos
            if self.board[r - 1][c] == "--":
                Movimientos.append(Movimiento((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    Movimientos.append(Movimiento((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    Movimientos.append(Movimiento((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    Movimientos.append(Movimiento((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r + 1][c] == "--":
                Movimientos.append(Movimiento((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    Movimientos.append(Movimiento((r, c), (r + 2, c), self.board))
            # Captures
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    Movimientos.append(Movimiento((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    Movimientos.append(Movimiento((r, c), (r + 1, c + 1), self.board))

    def ObtenerMovimientosTorre (self, r, c, Movimientos):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.MovimientoBlanco else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPieza = self.board[endRow][endCol]
                    if endPieza == "--":
                        Movimientos.append(Movimiento((r, c), (endRow, endCol), self.board))
                    elif endPieza[0] == enemyColor:
                        Movimientos.append(Movimiento((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break



    def ObtenerMovimientosCaballero (self, r, c, Movimientos):
        CaballeroMovimientos = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.MovimientoBlanco else "b"
        for m in CaballeroMovimientos:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPieza = self.board[endRow][endCol]
                if endPieza[0] != allyColor:
                    Movimientos.append(Movimiento((r, c), (endRow, endCol), self.board))

    def ObtenerMovimientosAlfil(self, r, c, Movimientos):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.MovimientoBlanco else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPieza = self.board[endRow][endCol]
                    if endPieza == "--":
                        Movimientos.append(Movimiento((r, c), (endRow, endCol), self.board))
                    elif endPieza[0] == enemyColor:
                        Movimientos.append(Movimiento((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def ObtenerMovimientosReyna(self, r, c, Movimientos):
        self.ObtenerMovimientosTorre(r, c, Movimientos)
        self.ObtenerMovimientosAlfil(r, c, Movimientos)

    def ObtenerMovimientosRey(self, r, c, Movimientos):
        ReyMovimientos = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.MovimientoBlanco else "b"
        for i in range(8):
            endRow = r + ReyMovimientos[i][0]
            endCol = c + ReyMovimientos[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPieza = self.board[endRow][endCol]
                if endPieza[0] != allyColor:
                    Movimientos.append(Movimiento((r, c), (endRow, endCol), self.board))

class Movimiento():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.PiezaMovida = board[self.startRow][self.startCol]
        self.PiezaCaptured = board[self.endRow][self.endCol]
        self.MovimientoID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):
        if isinstance(other,Movimiento):
            return self.MovimientoID == other.MovimientoID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]