import BackEnd

class AutoTurn
    def __init__(self)

    # given a back-end object, perform a move
    def makeMove(backend)
        #generate possible moves
        #evaluate state of game copy with move applied, for each possible move
        #pick move with highest score

    def generatePossibleMoves(contiguousStructures, mover)
        #given a list of contiguous structures, we generate a list of coordinates representing possible moves
        #if no contiguous structures at all - 0,0
        

    def evaluateState(contiguousStructures, mover)
        totalValue = 0
        
        #for each contiguous structure, give it a score
        #formula: length ^ 2 * (1 - # blocked ends * .5) * (-1 if opponent owned)
        #exception: five-long segments are victory, so just return max int
        for structure in contiguousStructures
            value = len(structure.coords) ** 2

            #create function in back end to return "next off the end"

        return totalValue
