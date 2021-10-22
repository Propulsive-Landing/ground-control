import collections 
import matplotlib.pyplot as plt
import random

random_deque = collections.deque([0, 0])


def random_generator(): 
    random_deque.popleft()
    random_deque.append(random.randint(1, 11)) 
        




random_generator()

print('Hello', random_deque[-1])