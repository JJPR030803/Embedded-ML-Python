import statistics

def lineal_interpolation(lista,missing_index):
    return lista[missing_index-1] + ((lista[missing_index+1] - lista[missing_index-1]) / 
                                     ((missing_index+1) - (missing_index-1)) * 
                                     (missing_index - (missing_index-1)))


def suavizamiento_exponencial_simple(valores,alfa):
    valores_suavizados = [valores[0]]
    for t in range(1,len(valores)):
        valor_suavizado = alfa * valores[t] + (1-alfa) * valores_suavizados[t-1]
        valores_suavizados.append(valor_suavizado)
    
    return valores_suavizados



def mediana(datos,intervalo_tiempo):
    lista_mediana = []
    for i in range(0,len(datos),intervalo_tiempo):
        segmento = datos[i:i+intervalo_tiempo]
        lista_mediana.append(statistics.median(segmento))
        
    return lista_mediana


