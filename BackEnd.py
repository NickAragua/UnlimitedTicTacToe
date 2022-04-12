class ContiguousStructure:
    coords = set()
    vector = ( )
    owner = 0
    id = 0
    
    def __init__(self, myOwner, id):
        #interesting Python quirk: if you don't initialize local variables
        #they will retain their values for the previous such object initialized
        self.coords = set()
        self.vector = tuple()
        self.owner = myOwner
        self.id = id

    def canAddCoord(self, newCoords, myOwner):
        #print("add check for ", newCoords[0], ", ", newCoords[1], " for ", myOwner)
        
        if (self.owner != myOwner):
            #print (self.owner, " doesn't match", myOwner)
            return False

        if (len(self.coords) == 0):
            #print ("brand new contig")
            return True

        if (len(self.coords) == 1):
            #hack, but we know there's only one element in the set
            onlyCoord = next(iter(self.coords))
            #print ("length 1 is adjacent to ", onlyCoord, ": ", self.isAdjacent(onlyCoord, newCoords))
            return self.isAdjacent(onlyCoord, newCoords)

        for coord in self.coords:
            #print ("is adjacent to ", coord, ": ", self.isAdjacent(coord, newCoords))
            #print (self.vector, " vector match vs ", self.getVector(coord, newCoords))
            #print (self.vector, " vector match vs ", self.getVector(newCoords, coord))
            if (self.isAdjacent(coord, newCoords) and \
                (self.vector == None or \
                self.vector == self.getVector(coord, newCoords)) or \
                self.vector == self.getVector(newCoords, coord)):
                #print ("vector matches or is empty")
                return True

        return False

    def addCoord(self, newCoords):
        #print("adding coord ", newCoords, " to contig #", self.id)
        
        #degenerate case: no coordinates
        if(len(self.coords) == 0):
            #print("empty contig, adding coords ", newCoords)
            self.coords.add(newCoords)
            return
        
        for coord in self.getAdjacent(newCoords):
            if (coord in self.coords):
                self.vector = self.getVector(coord, newCoords)
                self.coords.add(newCoords)

    def getAdjacent(self, coord):
        adjacentCoords = []

        #apparently range is non-inclusive for the upper bound
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                #don't process the 0, 0 vector
                if (dx != 0 or dy != 0):
                    adjacentCoords.append((coord[0] + dx, coord[1] + dy))

        return adjacentCoords
                    

    def getVector(self, coords1, coords2):
        xDiff = coords1[0] - coords2[0]
        yDiff = coords1[1] - coords2[1]
        return (xDiff, yDiff)

    def isAdjacent(self, coords1, coords2):
        xDiff = abs(coords1[0] - coords2[0])
        yDiff = abs(coords1[1] - coords2[1])
        #print ("Diff ", xDiff, ", ", yDiff)
        notTheSame = xDiff <= 1 and yDiff <= 1 and (xDiff != 0 or yDiff != 0)
        return notTheSame

class UTicTacToe:
    currentPlayer = 0
    currentBoard = { }
    minX = 0
    minY = 0
    maxX = 2
    maxY = 2

    #data structure:
    #coordinates as key, list of contiguous straight lines as value
    # each contiguous straight line is a list of coordinates
    contiguousStructures = set()

    def updateContiguousStructures(self, newCoords):
        #algorithm: create a 'contiguous structure' with the new coordinates
        #as the only member.
        #loop through the other contiguous structures; if the two are neighbors
        #and have the same vector, join them together.

        joinedToExistingStructure = False

        for structure in self.contiguousStructures:
            if (structure.canAddCoord(newCoords, self.currentPlayer)):
                #print ("adding ", newCoords, " to ", structure)
                structure.addCoord(newCoords)
                joinedToExistingStructure = True

        if (joinedToExistingStructure == False):
            #print ("adding new structure")
            newStruct = ContiguousStructure(self.currentPlayer, len(self.contiguousStructures))
            newStruct.addCoord(newCoords)
            self.contiguousStructures.add(newStruct)

    def playSpace(self, coords):
        #can't play on top of existing pieces
        if(self.currentBoard.get(coords) != None):
            return
        
        self.currentBoard[coords] = self.currentPlayer
        self.updateContiguousStructures(coords)

        #switch player
        if (self.currentPlayer == 1):
            self.currentPlayer = 0
        elif (self.currentPlayer == 0):
            self.currentPlayer = 1

        #expand coordinate boundaries
        #print (coords[0], ", ", coords[1], "; min ", self.minX, ", ", self.minY, "; max", self.maxX, ", ", self.maxY)
        if (coords[0] <= self.minX):
            self.minX = coords[0] - 1

        if (coords[0] >= self.maxX):
            self.maxX = coords[0] + 1

        if (coords[1] <= self.minY):
            self.minY = coords[1] - 1

        if (coords[1] >= self.maxY):
            self.maxY = coords[1] + 1

        #for struct in self.contiguousStructures:
            #for coord in struct.coords:
                #print(struct.id, ": ", str(coord[0]), ", ", str(coord[1]))

    def detectVictory(self):
        for struct in self.contiguousStructures:
            if (len(struct.coords) >= 5):
                return struct

        return None

    #def checkForAdjacentStructures(self, coords):
        #neighborFound = False
#    
        #for dx in range(-1, 1):
            #for dy in range(-1, 1):
                #if (dx == 0 and dy == 0):
                    #continue
#
                #neighborCoords = ( coords[0] + dx, coords[1] + dy )
#
                #if (contiguousStructures[neighborCoords]):
        
    #    for x in range(newCoords[0] - 1, newCoords[0] + 1):
    #        for y in range(newCoords[1] - 1, newCoords[1] + 1):

    #def inStraightLine(coordList):
        #tbd, probably doesn't matter: length zero list
        #degenerate case: length one list is always in a straight line;
        #if (coordList.count() <= 1):
        #    return True

        #firstDelta = getDelta(coordList[0], coordList[1])

        #for (index in range(1, coordList.count() - 2)):
        #    currentDelta = getDelta(coordList[index], coordList[index + 1]
        #    if (currentDelta[0] != firstDelta[0] && currentDelta[1] != firstDelta[1]) :
         #       return False

        #return True
                                    

    """The delta between two coordinates"""
    def getDelta(coordOne, coordTwo):
        return (coordOne[0] - coordTwo[0], coordOne[1] - coordTwo[1])

    """Two coordinates are next to each other if their X and Y
        coordinates differ by 1 at most"""
    def nextToEachOther(coordOne, coordTwo):
        return abs(coordOne[0] - coordTwo[0]) <= 1 and abs(coordOne[1] - coordTwo[1]) <= 1
            
    def getSpace(self, coords):
        return self.currentBoard[coords]
