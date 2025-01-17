from walmart import *
import heapq
import random
import numpy as np

pop_size = 50
num_gen = 20
random_limit = 0.2
# Define mean and standard deviation
mean = 0.0
std_dev = 0.01  # Adjust this to control the spread
highest = None
high_score = 0

# Generate a random number within the range
def generate_random_number_in_range():
    while True:
        number = np.random.normal(loc=mean, scale=std_dev)
        if -random_limit <= number <= random_limit:
            return number
      
#plotter = LocationPlotter(min_lat, max_lat, min_lon, max_lon, n_warehouses, m_shops, map_image_file)
plotter_lst = []
for i in range(pop_size):
    plotter_lst.append(LocationPlotter(min_lat, max_lat, min_lon, max_lon, n_warehouses, m_shops, map_image_file))

for i in range(pop_size):
    plotter_lst[i].randomize_locations()
    #plotter_lst[i].plot_on_map(output_file)

no_parents = 20
parents = heapq.nlargest(no_parents, plotter_lst, key = lambda item : item.calculate_score_and_profit( population_density, 
    spending_amount, 
    labor_availability, 
    land_cost,
    max_stores_per_warehouse, 
    profit_weight, 
    land_cost_weight, 
    labor_availability_weight))
#print(parents)
for gen in range(num_gen):
    obj_lst = []
    for i in range(pop_size):
        obj_lst.append(LocationPlotter(min_lat, max_lat, min_lon, max_lon, n_warehouses, m_shops, map_image_file))
        A = random.choice(parents)
        B = random.choice(parents)
        for j in range(n_warehouses):
            point = random.choice([A.warehouses[j],B.warehouses[j]])
            obj_lst[-1].warehouses.append((point[0] + generate_random_number_in_range(), point[1] + generate_random_number_in_range()))
        for j in range(m_shops):
            obj_lst[-1].shops.append((point[0] + generate_random_number_in_range(), point[1] + generate_random_number_in_range()))

    #print(obj_lst)
    #obj_lst[1].plot_on_map(output_file)


    max_score = max(obj_lst, key = lambda item : item.calculate_score_and_profit( population_density, 
        spending_amount, 
        labor_availability, 
        land_cost,
        max_stores_per_warehouse, 
        profit_weight, 
        land_cost_weight, 
        labor_availability_weight))
    max_score_val = max_score.calculate_score_and_profit( population_density, 
        spending_amount, 
        labor_availability, 
        land_cost,
        max_stores_per_warehouse, 
        profit_weight, 
        land_cost_weight, 
        labor_availability_weight)[0]
    if max_score_val > high_score:
        high_score = max_score_val
        highest = max_score
    #print(max_score.warehouses, max_score.shops)

    print("Generation : ", gen,' -> ', max_score_val)
    
    plotter_lst = obj_lst

    #max_score.plot_on_map(output_file) 
highest.plot_on_map(output_file)