import sys
from itertools import combinations
import csv
def readfile(file_name):
    try:
        transactions=[]
        with open(file_name,'r') as file:
            for line in file:
                line_list=line.strip().split()
                print(line_list)
                # for i in range(len(line_list)):
                #     line_list[i]=int(line_list[i])
                # sorted(line_list)
                # transactions.append(line_list)
            return transactions
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"A error occurred: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python association_rule.py min_sup file_name")
        return

    min_sup = int(sys.argv[1])
    file_name = sys.argv[2]

    print("min_sup:", min_sup)
    print("file_name:", file_name)
    transactions=readfile(file_name)

if __name__ == "__main__":
    main()