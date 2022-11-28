from EditDistance import EditDistance

def main():
    str1 = input("Enter string 1: ")
    str2 = input("Enter string 2: ")

    ed = EditDistance(str1, str2, 1, 1, 2)
    cost_matrix = ed.CreateCostMatrix()
    print(cost_matrix)
    print(ed.FindDecisionSequence(len(str1), len(str2)))
    print(ed.sequences)
    print(ed.listAllSequence())

if __name__ == "__main__":
    main()
