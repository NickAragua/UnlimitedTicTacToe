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
        
        for coord in ContiguousStructure.getAdjacent(newCoords):
            if (coord in self.coords):
                self.vector = self.getVector(coord, newCoords)
                self.coords.add(newCoords)

    @staticmethod
    def getAdjacent(coord):
        adjacentCoords = []

        #apparently range is non-inclusive for the upper bound
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                #don't process the 0, 0 vector
                if (dx != 0 or dy != 0):
                    adjacentCoords.append((coord[0] + dx, coord[1] + dy))

        return adjacentCoords

    def canJoin(self, otherStructure):
        return self.id != otherStructure.id and \
               ((abs(self.vector[0]) == abs(otherStructure.vector[0]) and \
               abs(self.vector[1]) == abs(otherStructure.vector[1])) or \
               self.vector == None or otherStructure.vector == None)

    def join(self, otherStructure):
        self.coords.union(otherStructure.coords)

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
    structuresForCoords = { }

    def addStructureForCoords(self, newCoords, structure):
        if (newCoords not in self.structuresForCoords):
            self.structuresForCoords[newCoords] = set()
        self.structuresForCoords[newCoords].add(structure)

    def updateContiguousStructures(self, newCoords):
        #algorithm: create a 'contiguous structure' with the new coordinates
        #as the only member.
        #loop through the other contiguous structures; if the two are neighbors
        #and have the same vector, join them together.

        createSingleton = True
        joinedStructures = set()

        for structure in self.contiguousStructures:
            if (structure.canAddCoord(newCoords, self.currentPlayer)):
                #print ("adding ", newCoords, " to ", structure)
                structure.addCoord(newCoords)
                createSingleton = False
                self.addStructureForCoords(newCoords, structure)
                joinedStructures.add(structure)

        # if we are here, that means we have exhausted all adjacent contiguous structures
        # that we can join. Now we need to create a new contiguous structure with each
        # adjacent "friendly" square. We do not have to worry about joining multi-square
        # existing structures here as we would already have done so
        
        for adjacentCoords in ContiguousStructure.getAdjacent(newCoords):
            # the adjacent coordinate contains a 'friendly' square
            friendlySquare = self.currentBoard.get(adjacentCoords) == self.currentPlayer

            # the adjacent coordinate does not contain a structure of which we are already a part
            alreadyJoined = adjacentCoords in self.structuresForCoords and \
                len(self.structuresForCoords[adjacentCoords].intersection(joinedStructures)) > 0
            
            if (friendlySquare and not alreadyJoined):
                newStruct = ContiguousStructure(self.currentPlayer, len(self.contiguousStructures))
                newStruct.addCoord(newCoords)
                newStruct.addCoord(adjacentCoords)
                self.contiguousStructures.add(newStruct)
                createSingleton = False
                self.addStructureForCoords(newCoords, newStruct)

        # this is a special case of a new square all by itself
        if (createSingleton == True):
            print ("adding new structure")
            newStruct = ContiguousStructure(self.currentPlayer, len(self.contiguousStructures))
            newStruct.addCoord(newCoords)
            self.contiguousStructures.add(newStruct)
            self.addStructureForCoords(newCoords, newStruct)

        # now we loop through all contiguous structures for these coordinates, and join together
        # the ones that have the same vector (i.e. we closed a gap)
        structuresToRemove = set()
        
        for structure in self.structuresForCoords[newCoords]:
            for otherStructure in self.structuresForCoords[newCoords]:
                if structure.canJoin(otherStructure):
                    structure.join(otherStructure)
                    self.contiguousStructures.remove(otherStructure)
                    structuresToRemove.add(otherStructure)

        #cleanup
        for structure in structuresToRemove:
            self.structuresForCoords[newCoords].remove(structure)
                    
                    

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
        structs = list()
        
        for struct in self.contiguousStructures:
            if (len(struct.coords) >= 5):
                structs.append(struct)

        return structs                                    

    """The delta between two coordinates"""
    def getDelta(coordOne, coordTwo):
        return (coordOne[0] - coordTwo[0], coordOne[1] - coordTwo[1])

    """Two coordinates are next to each other if their X and Y
        coordinates differ by 1 at most"""
    def nextToEachOther(coordOne, coordTwo):
        return abs(coordOne[0] - coordTwo[0]) <= 1 and abs(coordOne[1] - coordTwo[1]) <= 1
            
    def getSpace(self, coords):
        return self.currentBoard[coords]
