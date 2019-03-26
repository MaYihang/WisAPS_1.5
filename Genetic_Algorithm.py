#!/usr/bin/env python
# coding: utf-8
#基于deap框架的遗传算法优化排产顺序，以实现优化目标
from deap import base,creator,tools
from Calculate_DateTime import date_timechrchuo
import Main,random,json,time

def evaluate(individual):
    #上升排序
    newindividual=sorted(individual)
    #确定索引
    p=[]
    for i in range(len(newindividual)):
        p.append(individual.index(newindividual[i]))
    #调用排产
    for i in range(len(Sales_Order['saleOrder'])):
        Sales_Order['saleOrder'][i]['priority']=p[i]
    OUTPUT=Main.Scheduling_Plan(Production_Calendar, BOM, Sales_Order, Materials)
    #统计交期
    PlanTdict=OUTPUT['jiaohuoT']
    #计算优化值
    TargetValue=0 #目标优化值
    OptimizationStyle=Sales_Order['optimizationtarget']
    if OptimizationStyle==1:
        for key in PlanTdict:
            PlanTdict[key]=date_timechrchuo(PlanTdict[key])
            if key in SalesTdict:
                if SalesTdict[key]<PlanTdict[key]:
                    TargetValue+=1

    elif OptimizationStyle==2:
        for key in PlanTdict:
            PlanTdict[key]=datetochuo(PlanTdict[key])
            if key in SalesTdict:
                if SalesTdict[key]<PlanTdict[key]:
                    TargetValue+=PlanTdict[key]-SalesTdict[key]

    elif OptimizationStyle==3:
        PostponeTMax=0
        for key in PlanTdict:
            PlanTdict[key]=datetochuo(PlanTdict[key])
            if key in SalesTdict:
                k_=PlanTdict[key]-SalesTdict[key]
                if k_>PostponeTMax:
                    PostponeTMax=k_
        TargetValue=PostponeTMax

    return TargetValue,


# Algorithms
def main():
    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=4)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 1
    '''
    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    #
    # NGEN  is the number of generations for which the
    #       evolution runs
    '''
    OUTPUT=Main.Scheduling_Plan(Production_Calendar, BOM, Sales_Order, Materials)
    if 'error' in OUTPUT or OUTPUT=={'productionOrder':[]}:
        bestvalue='error'
        pop=0
        return OUTPUT, bestvalue,pop
    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))  # 这时候，pop的长度还是300呢
    print("-- Iterative %i times --" % NGEN)

    for g in range(NGEN):
        if g % 10 == 0:
            print("-- Generation %i --" % g)
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Change map to list,The documentation on the official website is wrong

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring
    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print(best_ind)
    print(best_ind.fitness.values)
    return best_ind, best_ind.fitness.values,pop  # return the result:Last individual,The Return of Evaluate function


def AlgorithmOptimization(Production_Calendar,BOM,Sales_Order,Materials,NowTime,OUTPUT,urlpath,L):

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    # weights 1.0, 求最大值,-1.0 求最小值
    # (1.0,-1.0,)求第一个参数的最大值,求第二个参数的最小值
    creator.create("Individual", list, fitness=creator.FitnessMin)

    # Initialization

    IND_SIZE=len(Sales_Order['saleOrder'])  # 种群数

    toolbox = base.Toolbox()
    toolbox.register("attribute", random.random)
    # 调用randon.random为每一个基因编码编码创建 随机初始值 也就是范围[0,1]
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attribute, n=IND_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    #统计订单交货期
    SalesTdict={}
    for i in range(len(Sales_Order['saleOrder'])):
        if 'deliveryDate' in Sales_Order['saleOrder'][i]:
            SalesTdict[str(Sales_Order['saleOrder'][i]['saleOrderId'])+'-'+str(Sales_Order['saleOrder'][i]['saleOrderLineId'])]=Sales_Order['saleOrder'][i]['deliveryDate']
    # Operators
    # difine evaluate function
    # Note that a comma is a must

    # use tools in deap to creat our application
    toolbox.register("mate", tools.cxTwoPoint) # mate:交叉
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1) # mutate : 变异
    toolbox.register("select", tools.selTournament, tournsize=3) # select : 选择保留的最佳个体
    toolbox.register("evaluate", evaluate)  # commit our evaluate

    best_ind, fitness,pop=main()

    return fitness
# if __name__ == "__main__":
#     t1 = time.clock()
#     best_ind, bestvalue,pop=main()
#     print(pop, best_ind, best_ind.fitness.values)
#     print("pop",pop)
#     print("best_ind",best_ind)
#     print("best_ind.fitness.values",bestvalue)
#
#     t2 = time.clock()
#
#     print(t2-t1)
    



# In[ ]:




