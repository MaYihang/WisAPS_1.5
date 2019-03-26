#!/usr/bin/env python
# coding: utf-8
#根据物料损耗率、废品率计算各工序的加工数量，返回净数量和估计数量
def calculatenum(T,N,num,scraprate,consumptionrate):
    materialsnum = {N:round(num*(1+scraprate[0]/100),6)}
    netmaterialsnum={N:num}
    netnum=[]
    for i in range(len(T)):
        T_={}
        netnumlist={}
        if '=' in T[i]:
            t1=T[i][:T[i].index('=')]
            if '&' in t1:
                t2=t1[:t1.index('&')]
            NUM=materialsnum[t2]
            NETNUM=netmaterialsnum[t2]
            t1=T[i][T[i].index('=')+1:]
            j=0
            while '+' in t1:
                t2=t1[:t1.index('+')]
                if '*' in t2:
                    P=float(t2[:t2.index('*')])
                    name=t2[t2.index('*')+1:]
                else:
                    P=1.0
                    name=t2
                if name not in materialsnum:
                    if i!=len(T)-1:
                        materialsnum[name]=round(NUM*P*(1+consumptionrate[i][j]/100)*(1+scraprate[i+1]/100),6)
                        T_[name]=round(NETNUM*P,6)
                        netmaterialsnum[name]=round(NETNUM*P,6)
                        if name not in netnumlist:
                            netnumlist[name]=netmaterialsnum[name]
                        else:
                            netnumlist[name]+=netmaterialsnum[name]
                    else:
                        materialsnum[name]=round(NUM*P*(1+consumptionrate[i][j]/100),6)
                        T_[name]=round(NETNUM*P,6)
                        netmaterialsnum[name]=round(NETNUM*P,6)
                        if name not in netnumlist:
                            netnumlist[name]=netmaterialsnum[name]
                        else:
                            netnumlist[name]+=netmaterialsnum[name]
                else:
                    if i!=len(T)-1:
                        materialsnum[name]=round((materialsnum[name]+NUM*(1+scraprate[i+1]/100)*P*(1+consumptionrate[i][j]/100)),6)
                        T_[name]=round((netmaterialsnum[name]+NETNUM*P),6)
                        netmaterialsnum[name]=round((netmaterialsnum[name]+NETNUM*P),6)
                        if name not in netnumlist:
                            netnumlist[name]=netmaterialsnum[name]
                        else:
                            netnumlist[name]+=netmaterialsnum[name]
                    else:
                        materialsnum[name]=round((materialsnum[name]+NUM*P*(1+consumptionrate[i][j]/100)),6)
                        T_[name]=round((netmaterialsnum[name]+NETNUM*P),6)
                        netmaterialsnum[name]=round((netmaterialsnum[name]+NETNUM*P),6)
                        if name not in netnumlist:
                            netnumlist[name]=netmaterialsnum[name]
                        else:
                            netnumlist[name]+=netmaterialsnum[name]
                j+=1
                t1=t1[t1.index('+')+1:]
            t2=t1
            if '*' in t2:
                P=float(t2[:t2.index('*')])
                name=t2[t2.index('*')+1:]
            else:
                P=1.0
                name=t2
            if name not in materialsnum:
                if i!=len(T)-1:
                    materialsnum[name]=round(NUM*P*(1+consumptionrate[i][j]/100)*(1+scraprate[i+1]/100),6)
                    T_[name]=round(NETNUM*P,6)
                    netmaterialsnum[name]=round(NETNUM*P,6)
                    if name not in netnumlist:
                        netnumlist[name]=netmaterialsnum[name]
                    else:
                        netnumlist[name]+=netmaterialsnum[name]
                else:
                    materialsnum[name]=round(NUM*P*(1+consumptionrate[i][j]/100),6)
                    T_[name]=round(NETNUM*P,6)
                    netmaterialsnum[name]=round(NETNUM*P,6)
                    if name not in netnumlist:
                        netnumlist[name]=netmaterialsnum[name]
                    else:
                        netnumlist[name]+=netmaterialsnum[name]
            else:
                if i!=len(T)-1:
                    materialsnum[name]=round((materialsnum[name]+NUM*(1+scraprate[i+1]/100)*P*(1+consumptionrate[i][j]/100)),6)
                    T_[name]=round((netmaterialsnum[name]+NETNUM*P),6)
                    netmaterialsnum[name]=round((netmaterialsnum[name]+NETNUM*P),6)
                    if name not in netnumlist:
                        netnumlist[name]=netmaterialsnum[name]
                    else:
                        netnumlist[name]+=netmaterialsnum[name]
                else:
                    materialsnum[name]=round((materialsnum[name]+NUM*P*(1+consumptionrate[i][j]/100)),6)
                    T_[name]=round((netmaterialsnum[name]+NETNUM*P),6)
                    netmaterialsnum[name]=round((netmaterialsnum[name]+NETNUM*P),6)
                    if name not in netnumlist:
                        netnumlist[name]=netmaterialsnum[name]
                    else:
                        netnumlist[name]+=netmaterialsnum[name]
        netnum.append(netnumlist)
    num=[]
    for i in range(len(T)):
        t1=T[i][:T[i].index('=')]
        if '&' in t1:
            t2=t1[:t1.index('&')]
        else:
            t2=t1
        num.append(materialsnum[t2])
    NUM=[]
    NUM=[num,netnum]
    return NUM
