import sys
from itertools import permutations
import csv


def readfile(file_name):
    try:
        TDB={}
        one_item={}
        with open(file_name,'r') as file:
            for line in file:
                line_list=line.strip().split()
                dic={}
                for i in range(1,len(line_list),2):
                    TID=line_list[i]
                    item=line_list[i+1]
                    if item not in one_item:
                        one_item[item]=0
                    if TID not in dic:
                        dic[TID]=[item]
                    else:
                        dic[TID].append(item)
                # for key in dic:
                #     dic[key]=frozenset(dic[key])
                SID=int(line_list[0])
                TDB[SID]=list(dic.values())
            return TDB,one_item
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"A error occurred: {e}")

def get_one_item_frequency(one_item,TDB):
    for SID in TDB.keys():
        sequence=TDB[SID]
        tmp_set=set()
        for transaction in sequence:
            for item in transaction:
                tmp_set.add(item)
        for item in tmp_set:
            one_item[item]+=1
    return one_item



def main():
    if len(sys.argv) != 3:
        print("Usage: python my_SPM.py min_sup file_name")
        return
    min_sup = int(sys.argv[1])
    file_name = sys.argv[2]

    print("min_sup:", min_sup)
    print("file_name:", file_name)
    TDB,one_item=readfile(file_name)
    one_item=get_one_item_frequency(one_item,TDB)
    # for SID in TDB:
    #     print(SID)
    #     print(TDB[SID])
    # print(one_item)
    one_item_after_prune={}
    for item in one_item:
        if one_item[item]>=min_sup:
            one_item_after_prune[item]=one_item[item]
    frequent_sequential_pattern={}
    for item in one_item_after_prune:
        frequent_sequential_pattern[item]=one_item_after_prune[item]
    ## gen L2
    L2={}
    for perm in list(permutations(one_item_after_prune.keys(),2)):
        SID_set=set()
        perm=list(perm)
        for SID in TDB:
            sequence=TDB[SID]
            idx=0
            # print(SID)
            for transaction in sequence:
                if perm[idx] in transaction:
                    idx+=1
                if idx==2:
                    break
            if idx==2:
                SID_set.add(SID)
        if len(SID_set)>=min_sup:
            key_string=""
            for item in perm:
                key_string+=f"{item} "
            L2[key_string[:-1]]=frozenset(SID_set)
    # for key in L2.keys():
    #     print(key)
    #     print(L2[key])
    # print(len(L2))
    for pattern in L2:
        frequent_sequential_pattern[pattern]=len(L2[pattern])
    # for pattern in frequent_sequential_pattern:
    #     print(pattern)
    #     print(frequent_sequential_pattern[pattern])
    #     print()
    # L2_list=list(L2.keys())
    # print(L2_list)
    Lk=L2
    Lk_list=list(Lk.keys())
    old_len=len(frequent_sequential_pattern)
    new_len=0
    k=3
    while old_len!=new_len:
        tmp_dic={}
        old_len=len(frequent_sequential_pattern)
        # print(Lk_list)
        # print(Lk)
        for perm in list(permutations(Lk_list,2)):
            overlap_range=k-2
            LHS=perm[0].split()
            RHS=perm[1].split()
            if LHS[-overlap_range:]==RHS[:overlap_range]:
                new_SID_intersection=Lk[perm[0]]&Lk[perm[1]]
                if len(new_SID_intersection)>=min_sup:
                    new_key=""
                    new_list=LHS+RHS[overlap_range:]
                    for item in new_list:
                        new_key+=f"{item} "
                    tmp_dic[new_key[:-1]]=frozenset(new_SID_intersection)
                    frequent_sequential_pattern[new_key[:-1]]=len(tmp_dic[new_key[:-1]])
            
        new_len=len(frequent_sequential_pattern)
        # print(old_len,new_len)
        k+=1
        Lk=tmp_dic
        Lk_list=list(Lk.keys())
    print(frequent_sequential_pattern)
    for fsp in frequent_sequential_pattern.keys():
        print(f"Frequency sequential pattern = \"{fsp}\"")
        print(f"support = {frequent_sequential_pattern[fsp]}")
        print() 
    



            
    


        


if __name__ == "__main__":
    main()