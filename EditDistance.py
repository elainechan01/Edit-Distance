import copy

class EditDistance:
    def __init__(self, str1: str, str2: str, cDel: float, cIns: float, cRep: float) -> None:
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

    def backtrackSequence(self, row:int=None, col:int=None):
        # print(row,col)
        if(row==None):
            row = len(self.str1)
        if(col==None):
            col = len(self.str2)
        """base case: return an array with these values
           index 0: operation sequence
           index 1: current edited string
           index 2: position of edit
           index 3: decision sequence"""
        sequences = []
        # base case
        if(row==0 and col==0):
            return [[[],self.str1,0,[[row,col]]]]
        # elif((row-1==0 or row==0) and (col-1==0 or col==0)):
        #     return [[[],self.str1,0,[[row,col]]]]
        # condition 1: characters match
        if(self.str1[row-1] == self.str2[col-1]):
            allPaths = self.backtrackSequence(row-1,col-1)
            # print(allPaths)
            try:
                for path in allPaths:
                    path[3].append([row,col])
                sequences.extend(allPaths)
            except TypeError:
                pass
        # condition 2: characters don't match -> check for operation
        # check for deletion operation (upward)
        if(self.CostMatrix[row-1][col] + self.d == self.CostMatrix[row][col] and row >= 1):
            allPaths = self.backtrackSequence(row-1,col)
            # print(allPaths)
            try:
                for path in allPaths:
                    currStr = path[1]
                    editIndex = path[2]
                    path[1] = currStr[0:row+editIndex-1] + currStr[row+editIndex:len(currStr)]
                    path[2] = editIndex - 1
                    path[0].append(currStr + " delete " + self.str1[row-1] + " at " + str(row+editIndex-1))
                    path[3].append([row,col])
                sequences.extend(allPaths)
            except TypeError:
                pass
        elif(row == 1 and col == 0):
            allPaths = self.backtrackSequence(row-1,col)
            # print(allPaths)
            try:
                for path in allPaths:
                    currStr = path[1]
                    editIndex = path[2]
                    path[1] = currStr[0:row+editIndex-1] + currStr[row+editIndex:len(currStr)]
                    path[2] = editIndex - 1
                    path[0].append(currStr + " delete " + self.str1[row-1] + " at " + str(row+editIndex-1))
                    path[3].append([row,col])
                sequences.extend(allPaths)
            except TypeError:
                pass
        # check for insertion operation (leftward)
        if(self.CostMatrix[row][col-1] + self.i == self.CostMatrix[row][col] and col >= 1):
            allPaths = self.backtrackSequence(row,col-1)
            # print(allPaths)
            try:
                for path in allPaths:
                    currStr = path[1]
                    editIndex = path[2]
                    path[1] = currStr[0:row+editIndex] + self.str2[col-1] + currStr[row+editIndex:len(currStr)]
                    path[2] = editIndex + 1
                    path[0].append(currStr + " insert " + self.str2[col-1] +  " at " + str(row-1))
                    path[3].append([row,col])
                sequences.extend(allPaths)
            except TypeError:
                pass
        elif(row == 0 and col == 1):
            allPaths = self.backtrackSequence(row,col-1)
            # print(allPaths)
            try:
                for path in allPaths:
                    currStr = path[1]
                    editIndex = path[2]
                    path[1] = currStr[0:row+editIndex] + self.str2[col-1] + currStr[row+editIndex:len(currStr)]
                    path[2] = editIndex + 1
                    path[0].append(currStr + " insert " + self.str2[col-1] +  " at " + str(row-1))
                    path[3].append([row,col])
                sequences.extend(allPaths)
            except TypeError:
                pass
        # check for replacement/change operation (diagonal)
        if(self.CostMatrix[row-1][col-1] + self.r == self.CostMatrix[row][col] and row >= 1 and col >= 1):
            allPaths = self.backtrackSequence(row-1,col-1)
            # print(allPaths)
            try:
                for path in allPaths:
                    currStr = path[1]
                    editIndex = path[2]
                    path[1] = currStr[0:row+editIndex-1] + self.str2[col-1] + currStr[row+editIndex:len(currStr)]
                    path[0].append(currStr + " replace " + self.str1[row-1]  + " with " + self.str2[col-1] +  " at " + str(row+editIndex-1))
                    path[3].append([row,col])
                sequences.extend(allPaths)
            except TypeError:
                pass
        return sequences
