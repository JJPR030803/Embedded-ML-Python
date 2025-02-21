# Guía: Análisis de Temperatura con Suavizado Exponencial y Algoritmos Genéticos

## 1. Introducción
Esta guía describe cómo implementar un sistema de análisis de temperatura usando Arduino, aplicando suavizado exponencial y optimizando el parámetro alfa mediante algoritmos genéticos.

## 2. Componentes del Sistema
- Arduino (cualquier modelo)
- Sensor de temperatura (ej: DHT11, DS18B20)
- Conexión serial para transmisión de datos

## 3. Suavizado Exponencial Simple
El suavizado exponencial se usa para reducir el ruido en las mediciones y detectar tendencias.

### Fórmula básica:
```
St = α * Yt + (1 - α) * St-1

Donde:
- St: Valor suavizado en tiempo t
- Yt: Valor observado en tiempo t
- α: Parámetro de suavizado (0 < α < 1)
- St-1: Valor suavizado anterior
```

## 4. Métricas de Error
Para evaluar la calidad del suavizado:

### MAE (Error Medio Absoluto)
```
errorMAE = (1/n) * Σ|Yt - St|
```

### MSE (Error Cuadrático Medio)
```
errorMSE = (1/n) * Σ(Yt - St)²
```

### RMSE (Raíz del Error Cuadrático Medio)
```
errorRMSE = √(errorMSE)
```

### MADE (Error de Desviación Absoluta Media)
```
errorMADE = (1/n) * Σ|Yt - mediana(Y)|
```

## 5. Algoritmo Genético para Optimización de Alfa
El algoritmo genético ayudará a encontrar el mejor valor de α que minimice el error.

### Estructura del Cromosoma
- Un solo gen representando α (valor entre 0 y 1)

### Proceso del Algoritmo Genético
1. Inicialización:
   - Generar población inicial de valores α aleatorios

2. Evaluación:
   - Para cada α:
     - Aplicar suavizado exponencial
     - Calcular errores (MAE, MSE, RMSE, MADE)
     - Asignar fitness basado en el error seleccionado

3. Selección:
   - Seleccionar mejores individuos (valores de α)
   - Usar selección por torneo o ruleta

4. Cruce y Mutación:
   - Aplicar operadores genéticos para generar nuevos valores de α
   - Mantener valores dentro del rango [0,1]

5. Repetir hasta convergencia

## 6. Implementación en Arduino

### Código Base Arduino:
```cpp
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
float alpha = 0.2;  // Valor inicial
float smoothedTemp = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  // Primera lectura para inicializar
  smoothedTemp = dht.readTemperature();
}

void loop() {
  // Leer temperatura
  float currentTemp = dht.readTemperature();
  
  // Aplicar suavizado exponencial
  smoothedTemp = alpha * currentTemp + (1 - alpha) * smoothedTemp;
  
  // Enviar datos por serial
  Serial.print(currentTemp);
  Serial.print(",");
  Serial.println(smoothedTemp);
  
  delay(1000);
}
```

## 7. Procesamiento en Python
```python
import serial
import numpy as np

def calculate_errors(real_temps, smoothed_temps):
    n = len(real_temps)
    
    # MAE
    mae = np.mean(np.abs(real_temps - smoothed_temps))
    
    # MSE
    mse = np.mean((real_temps - smoothed_temps) ** 2)
    
    # RMSE
    rmse = np.sqrt(mse)
    
    # MADE
    made = np.mean(np.abs(real_temps - np.median(real_temps)))
    
    return mae, mse, rmse, made

# Implementación básica del algoritmo genético
def genetic_algorithm(data, population_size=50, generations=100):
    # Población inicial
    population = np.random.uniform(0, 1, population_size)
    
    for gen in range(generations):
        fitness_scores = []
        
        # Evaluar población
        for alpha in population:
            smoothed = np.zeros(len(data))
            smoothed[0] = data[0]
            
            for i in range(1, len(data)):
                smoothed[i] = alpha * data[i] + (1 - alpha) * smoothed[i-1]
            
            mae, _, _, _ = calculate_errors(data, smoothed)
            fitness_scores.append(1/mae)  # Menor MAE = mejor fitness
        
        # Selección y evolución
        # ... implementar selección, cruce y mutación
        
    return best_alpha
```

## 8. Recomendaciones
1. Recolectar suficientes datos antes de optimizar α
2. Experimentar con diferentes métricas de error
3. Ajustar parámetros del algoritmo genético según necesidades
4. Considerar implementar múltiples corridas para validar resultados

## 9. Consideraciones Adicionales
- El valor óptimo de α dependerá de:
  - Frecuencia de muestreo
  - Nivel de ruido en las mediciones
  - Velocidad de cambio en la temperatura
- Un α pequeño suaviza más pero responde más lento a cambios
- Un α grande responde rápido pero suaviza menos
