from numpy import *
import math 
import random




def new_matrix(matrix):
    for i in range(5):
        new_data = [[float(random.uniform(0,math.pi)), float(random.uniform(0,math.pi)), float(random.uniform(0,math.pi))]]
        new_matrix = append(matrix, new_data, 0)
        matrix = new_matrix
        

euler = array([[math.pi/2, math.pi/3, math.pi]])

print(new_matrix(euler))




