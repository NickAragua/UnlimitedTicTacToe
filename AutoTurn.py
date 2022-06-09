import BackEnd
import copy

class AutoTurn:
    # given a back-end object, perform a move
    def makeMove(self, backend):
        #generate possible moves
        #evaluate state of game copy with move applied, for each possible move
        #pick move with highest score

        bestValue = -9000
        bestCoord = []
        for coord in self.generatePossibleMoves(backend.contiguousStructures):
            newMove = BackEnd.UTicTacToe()
            newMove.currentPlayer = backend.currentPlayer
            newMove.currentBoard = copy.deepcopy(backend.currentBoard)
            newMove.minX = backend.minX
            newMove.minY = backend.minY
            newMove.maxX = backend.maxX
            newMove.maxY = backend.maxY
            newMove.contiguousStructures = copy.deepcopy(backend.contiguousStructures)
            newMove.structuresForCoords = copy.deepcopy(backend.structuresForCoords)
            
            newMove.playSpace(coord)
            newMoveValue = self.evaluateState(newMove.contiguousStructures, backend.currentBoard, backend.currentPlayer)
            if (newMoveValue > bestValue):
                bestValue = newMoveValue
                bestCoord = coord

        backend.playSpace(bestCoord)
        

    def generatePossibleMoves(self, contiguousStructures):
        #given a list of contiguous structures, we generate a list of coordinates representing possible moves
        #if no contiguous structures at all - 0,0
        possibleMoves = set()
    
        for structure in contiguousStructures:
            for adjacent in structure.getAllAdjacentCoords():
                possibleMoves.add(adjacent)

        if (len(possibleMoves) == 0):
            possibleMoves.add((0, 0))

        return possibleMoves
        

    def evaluateState(self, contiguousStructures, board, mover):
        totalValue = 0
        
        #for each contiguous structure, give it a score
        #formula: length ^ 2 * (1 - # blocked ends * .5) * (-1 if opponent owned)
        #exception: five-long segments are victory, so just return max int
        for structure in contiguousStructures:
            value = len(structure.coords) ** 2

            tipValue = 0
            for tip in structure.getTipCoords():
                # trick - if there's something in the tip, it's not ours
                # since otherwise it would be in the structure
                if (board.get(tip) != None):
                    tipValue += .5

            value *= (1 - tipValue)

            #if the structure belongs to the other guy, its value is opposite
            if (structure.owner != mover):
                value = -value
                    
            totalValue += value

        return totalValue
