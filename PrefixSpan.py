import sys
import csv
from tqdm import tqdm

def prune_low_sup(Ck,postfix_dic,min_sup):
    Lk=Ck
    cnt={}
    for item in Ck.copy():
        if len(postfix_dic[item]) not in cnt:
            cnt[len(postfix_dic[item])]=1
        else:
            cnt[len(postfix_dic[item])]+=1
        if len(postfix_dic[item])<min_sup:
            Lk.remove(item)
            postfix_dic.pop(item)
    return Lk,postfix_dic

def createC1(SDB,min_sup):
    C1=[]
    postfix_dic={}
    len_SDB=len(SDB)
    # Record each individual item's occurrences within sequences and the index of its first occurrence within these sequences.
    for i in tqdm(range(len_SDB), desc='Processing sequences'):
        for idx,item in enumerate(SDB[i]):
            tuple_item=tuple([item])
            if tuple_item not in C1:
                postfix_dic[tuple_item]={}
                C1.append(tuple_item)
            
            if i not in postfix_dic[tuple_item].keys():
                postfix_dic[tuple_item][i]=idx

    L1,postfix_dic=prune_low_sup(C1,postfix_dic,min_sup)
    return L1,postfix_dic
def readfile(file_name):
    try:
        SDB={}
        one_transaction_idx_mapping={}
        one_transaction_idx_reverse_mapping={}
        one_transaction_set_after_representation=set()
        cnt=0
        with open(file_name,'r') as file:
            for line in file:
                line_list=line.strip().split()
                dic={}
                for i in range(1,len(line_list),2):
                    TID=int(line_list[i])
                    item=int(line_list[i+1])
                    if TID not in dic:
                        dic[TID]=[item]
                    else:
                        dic[TID].append(item)
                for TID in dic:
                    dic[TID]=tuple(dic[TID])
                    transaction=dic[TID]
                    if dic[TID] not in one_transaction_idx_mapping:
                        one_transaction_idx_mapping[transaction]=cnt
                        one_transaction_idx_reverse_mapping[cnt]=dic[TID]
                        cnt+=1
                    one_transaction_set_after_representation.add(item)
                SID=int(line_list[0])
                SDB[SID]=list(dic.values())
            #return SDB,one_transaction_idx_mapping,one_transaction_idx_reverse_mapping,one_transaction_set_after_representation
            SDB_return=[]
            for SID in SDB:
                tmp=[]
                for transaction in SDB[SID]:
                    tmp.append(one_transaction_idx_mapping[transaction])
                SDB_return.append(tmp)
            return SDB_return,one_transaction_idx_mapping,one_transaction_idx_reverse_mapping,one_transaction_set_after_representation
    except FileNotFoundError:
        print(f"file {file_name} not found.")
    except Exception as e:
        print(f"A error occured: {e}")

def new_postfix_dic_gen(SDB,Lk,pre_post):
    postfix_dic={}
    for Ck in Lk:
        postfix_dic[Ck]={}
        end_of_now_sequence=Ck[-1]
        pre_post_list=pre_post[Ck[:-1]]
        for r_i in pre_post_list.keys():
            for c_i in range(pre_post_list[r_i]+1,len(SDB[r_i])):
                if SDB[r_i][c_i]==end_of_now_sequence:
                    postfix_dic[Ck][r_i]=c_i
                    break
    return postfix_dic

def candidate_gen(SDB,Lk,postfix_dic,min_sup):
    return_list=[]
    len_SDB=len(SDB)
    for Ck in Lk:
        item_count={}
        for i in postfix_dic[Ck].keys():
            item_exist={}
            for j in range(postfix_dic[Ck][i]+1,len(SDB[i])):
                if SDB[i][j] not in item_count.keys():
                    item_count[SDB[i][j]]=0
                if SDB[i][j] not in item_exist:
                    item_count[SDB[i][j]]+=1
                    item_exist[SDB[i][j]]=True
        C_items=[]

        for item in item_count.keys():
            if item_count[item]>=min_sup:
                C_items.append(item)

        for c_item in C_items:
            return_list.append(Ck+tuple([c_item]))

    return return_list
        



def main():
    if len(sys.argv) != 3:
        print("Usage: python PrefixSpan.py min_sup file_name")
        return
    min_sup = int(sys.argv[1])
    file_name = sys.argv[2]

    print("min_sup:", min_sup)
    print("file_name:", file_name)
    SDB,one_transaction_idx_mapping,one_transaction_idx_reverse_mapping,one_transaction_set_after_representation=readfile(file_name)
    
    
    
    L1,postfix_dic=createC1(SDB,min_sup)
    dic_L={}
    for x in L1:
        dic_L[x]=len(postfix_dic[x])
    #dic_L1=[{x:len(postfix_dic[x])} for x in L1]
    L=[L1]
    k=2
    while len(L[k-2])>0:
        Lk=candidate_gen(SDB,L[k-2],postfix_dic,min_sup)
        postfix_dic=new_postfix_dic_gen(SDB,Lk,postfix_dic)
        for x in Lk:
            dic_L[x]=len(postfix_dic[x])
        #dic_Lk=[{x:len(postfix_dic[x])} for x in Lk]

        L.append(Lk)
        # dic_L.append(dic_Lk)
        k+=1
    print(f"Num of sequential pattern is {len(dic_L)}")
    for sequential_pattern in dic_L:
        for item in sequential_pattern:
            print(f"{one_transaction_idx_reverse_mapping[item]} ",end="")
        print()
        print(f"Support is {dic_L[sequential_pattern]}\n")



if __name__ == "__main__":
    main()