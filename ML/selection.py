import numpy as np
from typing import Dict, List, Union

def calculate_fitness_numpy(vector: np.ndarray) -> float:
    """
    Calculate the fitness of a vector using sum of squares.
    
    Args:
        vector (np.ndarray): Input vector to evaluate
        
    Returns:
        float: Sum of squares of the vector elements
    """
    return np.sum(np.square(vector))

def environmental_selection(ratio: float, population: np.ndarray) -> Dict[float, np.ndarray]:
    """
    Select the best individuals from the population based on their fitness.
    
    Args:
        ratio (float): Selection ratio (0 to 1)
        population (np.ndarray): Population matrix
        
    Returns:
        Dict[float, np.ndarray]: Dictionary mapping fitness values to selected individuals
    
    Raises:
        ValueError: If ratio is not between 0 and 1
    """
    if not 0 <= ratio <= 1:
        raise ValueError("Selection ratio must be between 0 and 1")
        
    sorted_population = sorted(population, key=calculate_fitness_numpy)
    num_selected = round(len(sorted_population) * ratio)
    selected = {calculate_fitness_numpy(vec): vec for vec in sorted_population[:num_selected]}
    
    return selected