# principalProyecto1.py
from ML.genetic_optimizer import GeneticOptimizer
from Graficas.cuartiles import box_plot_datos,aplicar_interpolacion_lineal

VALOR_MAXIMO = 100
VALOR_MINIMO = 0
TAMANO_VECTORES = 100
TAMANO_MATRIZ = 100
TOTAL_PADRES = 20  
ITERACIONES = 10000

optimizer = GeneticOptimizer(
    pop_size=TAMANO_MATRIZ,
    vector_size=TAMANO_VECTORES,
    num_parents=TOTAL_PADRES,
    mutation_rate=0.5,
    selection_ratio=0.5,
    gene_min=VALOR_MINIMO,
    gene_max=VALOR_MAXIMO
)

fitness_history = optimizer.optimize(max_generations=ITERACIONES, target_fitness=0)

datos = box_plot_datos(fitness_history,printing=False)

print(aplicar_interpolacion_lineal(datos=datos,lower_limit=datos["Lower_Boundary"],upper_limit=datos["Upper_Boundary"]))