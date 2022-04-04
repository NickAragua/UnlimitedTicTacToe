class UTicTacToe:
    currentPlayer = 0
    currentBoard = { }
    minX = 0
    minY = 0
    maxX = 20
    maxY = 20

    def playSpace(self, coords):
        if (self.currentBoard.get(coords)):
            return
        
        self.currentBoard[coords] = self.currentPlayer

        #switch player
        if (self.currentPlayer == 1):
            self.currentPlayer = 0
        elif (self.currentPlayer == 0):
            self.currentPlayer = 1

        #expand coordinate boundaries
        if (coords[0] < self.minX):
            self.minX = coords[0] - 1
            return True;
        elif (coords[0] > self.maxX):
            self.maxX = coords[0] + 1
            return True;

        if (coords[1] < self.minY):
            self.minY = coords[1] - 1
            return True;
        elif (coords[1] > self.maxY):
            self.maxY = coords[1] + 1
            return True;

        return False;

    def getSpace(self, coords):
        return self.currentBoard[coords]
