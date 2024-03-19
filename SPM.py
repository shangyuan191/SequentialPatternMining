import sys
from itertools import combinations
import csv
def readfile(file_name):
    try:
        TDB={}
        one_item={}
        # count=0
        with open(file_name,'r') as file:
            for line in file:
                line_list=line.strip().split()
                # print(line_list)
                dic={}
                for i in range(1,len(line_list),2):
                    TID=int(line_list[i])
                    item=int(line_list[i+1])
                    if item not in one_item:
                        one_item[item]=0
                    if TID not in dic:
                        dic[TID]=set([item])
                    else:
                        dic[TID].add(item)
                for key in dic:
                    dic[key]=frozenset(dic[key])
                SID=int(line_list[0])
                TDB[frozenset([SID])]=frozenset(list(dic.values()))
                # count+=1
                # if count>=10:
                #     break
            return TDB,one_item
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
    TDB,one_item=readfile(file_name)
    for SID in TDB:
        tmp_set=set()
        transactions=TDB[SID]
        for transaction in transactions:
            for item in transaction:
                tmp_set.add(item)
        for item in tmp_set:
            one_item[item]+=1
    cnt=0
    for item in one_item:
        if one_item[item]<min_sup:
            cnt+=1
            one_item[item]=-1
    print(len(TDB))
    print(len(one_item)-cnt)

    TDB_after_one_item_prune={}
    for SID in TDB:
        transactions=TDB[SID]
        tmp_set=set()
        for transaction in transactions:
            tmp_tmp_set=set()
            for item in transaction:
                if one_item[item]!=-1:
                    tmp_tmp_set.add(item)
            if len(tmp_tmp_set)>0:
                tmp_set.add(frozenset(tmp_tmp_set))
        if len(tmp_set)>0:
            TDB_after_one_item_prune[SID]=tmp_set


 
    # for SID in TDB_after_one_item_prune:
    #     transactions=TDB_after_one_item_prune[SID]
    #     print(f"SID = {SID}")
    #     print(f"transactions = {transactions}")
    print(f"Before pruning: len is {len(TDB)}")
    print(f"After pruning: len is {len(TDB_after_one_item_prune)}")


if __name__ == "__main__":
    main()