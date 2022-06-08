'''
Autor: Martin Hric
UI Traveling Salesman Problem
2021/2022
'''

import random
import math
import csv
import time
from tkinter import *

CITIES_COUNT = 40
ITERATIONS = 10000
TABU_SIZE = 10
MAP_SIZE = 500
INITIAL_TEMP = 90
FINAL_TEMP = 0.1
ALPHA = 0.0005

def random_coordinates(count):
    array={}
    for x in range(count):
        array[x]=[random.randrange(50,MAP_SIZE - 50),random.randrange(100,MAP_SIZE - 50)]

    return array

def make_graph(cities,solution,time):
    top= Tk()
    top.geometry("500x500")
    c=Canvas(top,bg="white",height=MAP_SIZE,width=MAP_SIZE)
    c.create_line(5,5,5,MAP_SIZE)
    c.create_line(5,5,MAP_SIZE,5)
    c.create_text(10, 10, text="0")

    for a in range(100,MAP_SIZE,100):
        c.create_text(15,a,text=a)
        c.create_text(a,10,text=a)

    for x in range(CITIES_COUNT):
        c.create_oval(cities[x][0]-2,cities[x][1]-2,cities[x][0]+2,cities[x][1]+2,fill="black")

    c.create_line(cities[solution[0]][0],cities[solution[0]][1], cities[solution[CITIES_COUNT-1]][0],cities[solution[CITIES_COUNT-1]][1])

    for i in range(CITIES_COUNT - 1):
        c.create_line(cities[solution[i]][0], cities[solution[i]][1], cities[solution[i+1]][0],cities[solution[i+1]][1])

    c.create_text(150,MAP_SIZE -30,text = "celkova vzdialenost je : " + str(int(distance(cities, solution))))
    if time != 0:
        c.create_text(150,MAP_SIZE -10,text = "cas trvania: " + str(time) + 's')
    c.pack()
    top.mainloop()

def randomSolution(cities):
    solution=[]
    listofcities=list(range(len(cities)))
    for i in range(CITIES_COUNT):
        randomcity=listofcities[random.randint(0,len(listofcities)-1)]
        solution.append(randomcity)
        listofcities.remove(randomcity)
    return solution

def distance(cities, solution):
    total_distance = 0
    for i in range(CITIES_COUNT - 1):
        distance1 = math.sqrt((abs(cities[solution[i]][0] - cities[solution[i+1]][0]) ** 2) + (abs(cities[solution[i]][1] - cities[solution[i+1]][1]) ** 2))

        total_distance += distance1

    distance2 = math.sqrt((abs(cities[solution[0]][0] - cities[solution[CITIES_COUNT-1]][0]) ** 2) + (abs(cities[solution[0]][1] - cities[solution[CITIES_COUNT-1]][1]) ** 2))
    total_distance += distance2

    return total_distance

def permutacie(solution):
    neighbors = []
    randomIndex = random.randint(0,CITIES_COUNT-1)
    for i in range(CITIES_COUNT):
        if i == randomIndex:
            continue
        replace = solution.copy()
        replace[i] = solution[randomIndex]
        replace[randomIndex]= solution[i]
        neighbors.append(replace)
    return neighbors

def tabu_search(cities,solution):
    sBest = solution
    bestCandidate = solution
    tabuList = [solution]
    #distances = []
    #values = open("values_tabu.csv",'w', newline='')
    #writer = csv.writer(values)
    for i in range(ITERATIONS):
        sNeighborhood = permutacie(bestCandidate)
        bestCandidate = sNeighborhood[0]
        for sCandidate in sNeighborhood:
            if (sCandidate not in tabuList) and (distance(cities, sCandidate) < distance(cities,bestCandidate)):
                bestCandidate = sCandidate

        if distance(cities,bestCandidate) < distance(cities,sBest):
            sBest = bestCandidate

        #distances.append(int(distance(cities,bestCandidate)))
        tabuList.append(bestCandidate)
        if len(tabuList) > TABU_SIZE:
            tabuList.remove(tabuList[0])
    #writer.writerow(distances)
    #values.close()
    return sBest


def simulated_annealing(cities,initial_state):

    current_temp = INITIAL_TEMP

    current_state = initial_state.copy()
    solution = current_state
    values = open("values_annealing.csv", 'w', newline='')
    writer = csv.writer(values)
    distances = []

    while current_temp > FINAL_TEMP:

        bestneighbor = random.choice(permutacie(solution))
        cost_diff = distance(cities, bestneighbor) - distance(cities, solution)
        distances.append(int(distance(cities, solution)))

        if cost_diff < 0:
            solution = bestneighbor

        elif random.uniform(0, 1) < math.exp(-cost_diff / current_temp):
            solution = bestneighbor

        current_temp -= ALPHA
    writer.writerow(distances)
    values.close()
    return solution


def main():
    cities=random_coordinates(CITIES_COUNT)
    s0=randomSolution(cities)
    time.process_time_ns()

    '''start_time_tabu= time.time()
    solution_TABU = tabu_search(cities,s0)
    end_time_tabu = time.time()'''

    start_time_annealing = time.time()
    solution_SA = simulated_annealing(cities,s0)
    end_time_annealing =time.time()

    a= distance(cities,s0)
    #b= distance(cities,solution_TABU)
    c= distance(cities,solution_SA)

    print("vzdialenost nahodne vygenerovaneho riesenia: "+str(a))
    #print("vzdialenost riesenia tabu list: "+str(b))
    print("vzdialenost riesenia simulated annealing "+str(c))

    #print('\ncas trvania tabu: ' + str(end_time_tabu - start_time_tabu) + 's')
    print('\ncas trvania annealing: ' + str(end_time_annealing - start_time_annealing) + 's')

    make_graph(cities,s0,0)
    #make_graph(cities,solution_TABU,end_time_tabu - start_time_tabu)
    make_graph(cities,solution_SA, end_time_annealing - start_time_annealing)



main()