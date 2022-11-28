import copy

class EditDistance:
    def __init__(self, str1: str, str2: str, cDel: int, cIns: int, cRep: int) -> None:
        self.str1 = str1
        self.str2 = str2
        self.d = cDel
        self.i = cIns
        self.r = cRep
        self.sequences = []

    def CreateCostMatrix(self) -> list:
        self.CostMatrix = [[0 for _ in range(len(self.str2) + 1)] for _ in range(len(self.str1) + 1)]

        # intialize the first column
        for i in range(len(self.str1) + 1):
            self.CostMatrix[i][0] = i
        
        # initialize the first row
        for i in range(len(self.str2) + 1):
            self.CostMatrix[0][i] = i

        # calculate cost for each substring
        for c1 in range(1, len(self.str1) + 1):
            for c2 in range(1, len(self.str2) + 1):
                # condition 1: characters are equivalent
                if (self.str1[c1-1] == self.str2[c2-1]):
                    self.CostMatrix[c1][c2] = self.CostMatrix[c1-1][c2-1]
                # condition 2: characters are not equivalent, find minimum cost of the adjacent top-left corner cells
                else:
                    self.CostMatrix[c1][c2] = min(self.CostMatrix[c1-1][c2-1]+self.r,self.CostMatrix[c1-1][c2]+self.d,self.CostMatrix[c1][c2-1]+self.i)

        return self.CostMatrix

    def FindDecisionSequence(self, row: int, col: int, sequence: list = None) -> list:
        if sequence is None:
            sequence = []
        sequence = sequence + [self.CostMatrix[row][col]]
        if row == 0 and col == 0:
            self.sequences.append(sequence)
        for path in self.FindNextPath(row, col):
            self.FindDecisionSequence(path[0], path[1], sequence)

    def FindNextPath(self, row: int, col: int):
        next = []

        # check for equivalent character
        if self.str1[row-1] == self.str2[col-1]:
            # check for top cell
            if self.CostMatrix[row-1][col] == self.CostMatrix[row][col]:
                next.append([row-1,col])
            # check for top left cell
            if self.CostMatrix[row-1][col-1] == self.CostMatrix[row][col]:
                next.append([row-1,col-1])
            # check for left cell
            if self.CostMatrix[row][col-1] == self.CostMatrix[row][col]:
                next.append([row,col-1])
        
        # check for non-equivalent character
        # string to be converted is shorter 
        if len(self.str1) < len(self.str2) and row == 0 and col > 0:
            # check for left cell
            if (self.CostMatrix[row][col-1] + self.d) == self.CostMatrix[row][col-1] and [row,col-1] not in next:
                next.append([row,col-1])
        # string to be converted is longer
        elif len(self.str1) > len(self.str2) and row > 0 and col == 0:
            # check for top cell
            if (self.CostMatrix[row-1][col] + self.i) == self.CostMatrix[row][col] and [row-1,col] not in next:
                next.append([row-1,col])
        else:
            # check for top cell
            if (self.CostMatrix[row-1][col] + self.i) == self.CostMatrix[row][col] and [row-1,col] not in next:
                next.append([row-1,col])
            # check for top left cell
            if (self.CostMatrix[row-1][col-1] + self.r) == self.CostMatrix[row][col] and [row-1,col-1] not in next:
                next.append([row-1,col-1])
            # check for left cell
            if (self.CostMatrix[row][col-1] + self.d) == self.CostMatrix[row][col] and [row,col-1] not in next:
                next.append([row,col-1])
        return next

    def backtrackSequence(self, i=None, j=None):
        matrix = self.CostMatrix
        StringA = self.str1
        StringB = self.str2
        if(i==None):
            i = len(StringA)
        if(j==None):
            j = len(StringB)
        if(i==0 and j==0):
            return [[[],StringA,0]]
        if(StringA[i-1] == StringB[j-1]):
            paths = self.backtrackSequence(i-1,j-1)
            return paths
        else:
            paths = []
            if(matrix[i-1][j] + 1 == matrix[i][j] and i-1 >= 0):
                allPaths = self.backtrackSequence(i-1,j)
                for path in allPaths:
                    cS = path[1]
                    deviation = path[2]
                    path[1] = cS[0:i+deviation-1] + cS[i+deviation:len(cS)]
                    path[2] = deviation - 1
                    #print(cS + " delete " + StringA[i-1] + " " + path[1] + " " + "("+str(i)+","+str(j)+")")
                    path[0].append(cS + " delete " + StringA[i-1] + "("+str(i-1+deviation)+")")
                paths.extend(allPaths)
                #print('Paths',paths)
            if(matrix[i][j-1] + 1 == matrix[i][j] and j-1 >= 0):
                allPaths = self.backtrackSequence(i,j-1)
                for path in allPaths:
                    cS = path[1]
                    deviation = path[2]
                    path[1] = cS[0:i+deviation] + StringB[j-1] + cS[i+deviation:len(cS)]
                    path[2] = deviation + 1
                    path[0].append(cS + " insert " + StringB[j-1] +  "("+str(i-1+deviation)+")")
                paths.extend(allPaths)
                #print('Paths',paths)
            if(matrix[i-1][j-1] + 1 == matrix[i][j] and i-1 >= 0 and j-1 >= 0):
                allPaths = self.backtrackSequence(i-1,j-1)
                for path in allPaths:
                    cS = path[1]
                    deviation = path[2]
                    path[1] = cS[0:i+deviation-1] + StringB[j-1] + cS[i+deviation:len(cS)]
                    path[0].append(cS + " replace " + StringA[i-1]  + " with " + StringB[j-1] +  "("+str(i-1+deviation)+")")
                paths.extend(allPaths)
                #print('Paths',paths)
            return paths

    def listAllSequence(self):
        allSequence = self.backtrackSequence()
        for path in allSequence:
            if(len(path[0])>0):
                print(" -> ".join(path[0])," -> ",path[1])
            else:
                print(self.str1," -> ",self.str2)
