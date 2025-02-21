# tournament.py
import numpy as np
from ML.selection import calculate_fitness_numpy


def binary_tournament(population: np.ndarray, num_parents: int) -> np.ndarray:
    """Perform binary tournament selection ensuring even number of parents."""
    if num_parents <= 0:
        raise ValueError("Number of parents must be positive")
        
    # Ensure even number of parents
    num_parents = num_parents - (num_parents % 2)
    if num_parents == 0:
        num_parents = 2  # Minimum number of parents
        
    if num_parents > len(population):
        num_parents = len(population) - (len(population) % 2)
        print(f"Warning: Adjusted number of parents to {num_parents} to match population size")
    
    population = np.array(population)
    pop_size = len(population)
    vector_length = len(population[0])
    
    result = np.zeros((num_parents, 2, max(1, vector_length)), dtype=float)
    
    for i in range(num_parents):
        x, y = np.random.choice(pop_size, size=2, replace=False)
        min_x = calculate_fitness_numpy(population[x])
        min_y = calculate_fitness_numpy(population[y])
        
        if min_x < min_y:
            result[i, 0, 0] = min_x
            result[i, 1, :] = population[x]
        else:
            result[i, 0, 0] = min_y
            result[i, 1, :] = population[y]
            
    return result