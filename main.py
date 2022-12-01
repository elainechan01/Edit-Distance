from EditDistance import EditDistance
import numpy as np
import os
import sys

def main():
    ## interactive mode
    # while True:
    #     str1 = input("Enter string 1: ")
    #     str2 = input("Enter string 2: ")
    #     if str1 == str2:
    #         print("Invalid input: strings are equivalent.")
    #         continue
    #     elif len(str1) == 0 or len(str2) == 0:
    #         print("Invalid input: strings are empty")
    #         continue
    #     break
    # cDel = float(input("Enter the deletion cost: "))
    # cIns = float(input("Enter the insertion cost: "))
    # cRep = float(input("Enter the replacement/change cost: "))

    ## input file mode
    cDel = 0.4
    cIns = 0.5
    cRep = 1.2
    directory = 'datasets'
    for file in os.listdir(directory):
        try:
            filePath = os.path.join(directory, file)
            print()
            print(filePath)
            if os.path.isfile(filePath):
                f = open(filePath, 'r')
                str1 = f.readline().rstrip()
                str2 = f.readline().rstrip()

                if len(str1) <= 10 and len(str2) <= 10:
                    print("String 1: " + str1)
                    print("String 2: " + str2)

                # instantiate edit distance object
                ed = EditDistance(str1, str2, cDel, cIns, cRep)

                # calculate cost matrix
                cost_matrix = ed.CreateCostMatrix()
                if len(str1) <= 10 and len(str2) <= 10:
                    print("=======  Cost Matrix  =======")
                    print(np.matrix(cost_matrix))
                    print()

                # find decision sequences
                sequences = ed.backtrackSequence()
                i = 1
                if len(str1) <= 10 and len(str2) <= 10:
                    for path in sequences:
                        print("=======  Sequence %s  ======="%i)
                        sequence_matrix = [[' - ' if [row,col] in path[3] else '%.1f'%cost_matrix[row][col] for col in range(len(cost_matrix[0]))] for row in range(len(cost_matrix))]
                        if len(str1) <= 10 and len(str2) <= 10:
                            print(np.matrix(sequence_matrix))
                        if len(path[0]) > 0:
                            for op in range(len(path[0])-1):
                                print(path[0][op] + " => " + path[0][op+1].split(' ')[0])
                            print(path[0][-1] + " => " + path[1])
                            print()
                            i += 1
                print("Final cost: %.1f"%cost_matrix[-1][-1])
        except RecursionError:
            continue
        

if __name__ == "__main__":
    sys.setrecursionlimit(500)
    main()
