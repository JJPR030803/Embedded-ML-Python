# genetic_optimizer.py
import numpy as np
from typing import List, Optional
from ML.crossover_mutation import crossover, mutation
from ML.selection import environmental_selection
from ML.tournament import binary_tournament

class GeneticOptimizer:
    def __init__(self, 
                 pop_size: int = 100,
                 vector_size: int = 100,
                 num_parents: int = 20,
                 mutation_rate: float = 0.5,
                 selection_ratio: float = 0.5,
                 gene_min: float = 0,
                 gene_max: float = 100):
        """
        Initialize the genetic optimizer with parameter validation and adjustments.
        """
        # Validate parameters
        if pop_size <= 0:
            raise ValueError("Population size must be positive")
        if vector_size <= 0:
            raise ValueError("Vector size must be positive")
        if num_parents <= 0:
            raise ValueError("Number of parents must be positive")
            
        # Ensure population size is sufficient and even
        self.pop_size = max(4, pop_size)  # Minimum population size of 4
        
        # Ensure number of parents is even and not larger than population
        if num_parents > self.pop_size:
            num_parents = self.pop_size - (self.pop_size % 2)  # Make it even
            print(f"Warning: Adjusted number of parents to {num_parents} to match population size")
        elif num_parents % 2 != 0:
            num_parents = num_parents - 1  # Make it even
            print(f"Warning: Adjusted number of parents to {num_parents} to ensure even number")
            
        self.vector_size = vector_size
        self.num_parents = num_parents
        self.mutation_rate = np.clip(mutation_rate, 0, 1)
        self.selection_ratio = np.clip(selection_ratio, 0.1, 1)  # Minimum 10% selection
        self.gene_min = min(gene_min, gene_max)
        self.gene_max = max(gene_min, gene_max)
        
        # Initialize population
        self.population = np.random.uniform(
            self.gene_min, self.gene_max, 
            size=(self.pop_size, self.vector_size)
        )
    
    def maintain_population_size(self):
        """Ensure population size remains constant"""
        current_size = len(self.population)
        if current_size < self.pop_size:
            additional_needed = self.pop_size - current_size
            new_individuals = np.random.uniform(
                self.gene_min, self.gene_max,
                size=(additional_needed, self.vector_size)
            )
            self.population = np.vstack((self.population, new_individuals))
        elif current_size > self.pop_size:
            self.population = self.population[:self.pop_size]
    
    def step(self) -> float:
        """Perform one generation of evolution."""
        # Ensure population size is correct
        self.maintain_population_size()
        
        # Parent selection
        parents = binary_tournament(self.population, self.num_parents)
        
        # Crossover
        offspring = crossover(parents, num_crosspoints=2)
        
        # Mutation
        mutated = mutation(self.mutation_rate, self.gene_min, self.gene_max, offspring)
        
        # Environmental selection
        selected = environmental_selection(self.selection_ratio, mutated)
        
        # Update population with selected individuals
        self.population = np.array(list(selected.values()))
        
        # Maintain population size
        self.maintain_population_size()
        
        return min(selected.keys()) if selected else float('inf')
    
    def optimize(self, max_generations: int, 
                target_fitness: Optional[float] = None) -> List[float]:
        """Run the genetic algorithm optimization."""
        fitness_history = []
        
        for gen in range(max_generations):
            best_fitness = self.step()
            fitness_history.append(best_fitness)
            
            if target_fitness is not None and best_fitness <= target_fitness:
                print(f"Target fitness reached at generation {gen}")
                break
                
        return fitness_history
