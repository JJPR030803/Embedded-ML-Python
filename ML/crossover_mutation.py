# crossover_mutation.py
import numpy as np
from typing import List

def crossover(parents: np.ndarray, num_crosspoints: int) -> np.ndarray:
    """
    Perform multi-point crossover between pairs of parents.
    
    Args:
        parents (np.ndarray): Parent population matrix
        num_crosspoints (int): Number of crossover points
        
    Returns:
        np.ndarray: Offspring population
        
    Raises:
        ValueError: If number of parents is not even
    """
    parents = parents[:, 1, :]  # Extract actual parent vectors
    num_parents = len(parents)
    
    if num_parents % 2 != 0:
        raise ValueError("Number of parents must be even")
    
    vector_length = len(parents[0])
    offspring = np.zeros((num_parents, vector_length))
    
    for i in range(0, num_parents, 2):
        parent1 = parents[i].copy()
        parent2 = parents[i + 1].copy()
        
        crosspoints = sorted(np.random.choice(range(1, vector_length), 
                                            num_crosspoints, replace=False))
        
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        for j in range(len(crosspoints)):
            if j % 2 == 0:
                start = crosspoints[j]
                end = crosspoints[j + 1] if j + 1 < len(crosspoints) else vector_length
                child1[start:end], child2[start:end] = (
                    child2[start:end].copy(),
                    child1[start:end].copy()
                )
                
        offspring[i] = child1
        offspring[i + 1] = child2
        
    return offspring

def mutation(mutation_rate: float, gene_min: float, gene_max: float, 
            offspring: np.ndarray) -> np.ndarray:
    """
    Perform mutation on offspring population.
    
    Args:
        mutation_rate (float): Probability of mutation (0 to 1)
        gene_min (float): Minimum value for genes
        gene_max (float): Maximum value for genes
        offspring (np.ndarray): Offspring population to mutate
        
    Returns:
        np.ndarray: Mutated offspring
        
    Raises:
        ValueError: If mutation_rate is not between 0 and 1
    """
    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1")
        
    mutated = offspring.copy()
    
    # Vectorized mutation
    mutation_mask = np.random.random(mutated.shape) < mutation_rate
    new_values = np.random.uniform(gene_min, gene_max, size=mutated.shape)
    mutated[mutation_mask] = new_values[mutation_mask]
    
    return mutated