import sys
from itertools import combinations
import csv
def readfile(file_name):
    try:
        transactions={}
        with open(file_name,'r') as file:
            for line in file:
                line_list=line.strip().split()
                print(line_list)
                dic={}
                for i in range(1,len(line_list),2):
                    time_stamp=int(line_list[i])
                    item=int(line_list[i+1])
                    if time_stamp not in dic:
                        dic[time_stamp]=set([item])
                    else:
                        dic[time_stamp].add(item)
                for key in dic:
                    dic[key]=frozenset(dic[key])
                TID=int(line_list[0])
                transactions[frozenset([TID])]=frozenset(list(dic.values()))
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
    # print(transactions)
    # for transaction in transactions:
    #     print(transaction)
    #     print(transactions[transaction])

if __name__ == "__main__":
    main()