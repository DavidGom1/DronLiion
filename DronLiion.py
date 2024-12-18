import csv

def CargarCeldasCSV(file_path): # Carga de datos de las celdas desde el CSV
    celdas = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for datos_celdas in row:
                if ':' in datos_celdas:
                    capacidad, resistencia = map(int, datos_celdas.split(':'))
                    celdas.append({'capacidad': capacidad, 'resistencia': resistencia})
    return celdas

def OrdenCeldasPorCriterio(celdas, priorizar_capacidad=True): # Ordenar las celdas por capacidad o resistencia
    return sorted(celdas, key=lambda x: (-x['capacidad'], x['resistencia']) if priorizar_capacidad else (x['resistencia'], -x['capacidad']))

def ConstruccionBateria(celdas, cantidadSerie, cantidadParalelo): # Construcción de la batería
    celdasSeleccionadas = []
    for _ in range(cantidadSerie):
        parallel_group = celdas[:cantidadParalelo]
        celdas = celdas[cantidadParalelo:]
        if len(parallel_group) < cantidadParalelo:
            print("No hay suficientes celdas para completar la configuración.")
            break
        celdasSeleccionadas.append(parallel_group)
    return celdasSeleccionadas

def CalculoEspecificacionBateria(celdasSeleccionadas): # Cálculo de la capacidad total y resistencia media
    capacidadTotal = sum(min(group, key=lambda x: x['capacidad'])['capacidad'] for group in celdasSeleccionadas)/cantidadParalelo
    resistenciaMedia = sum(sum(cell['resistencia'] for cell in group) / len(group) for group in celdasSeleccionadas) / len(celdasSeleccionadas)
    return capacidadTotal, resistenciaMedia

if __name__ == "__main__": # Ejecución del programa
    file_path = input("Ingrese la ruta de su archivo CSV:")
    celdas = CargarCeldasCSV(file_path)
    if not celdas: # Verificación de la existencia de celdas en el archivo CSV
        print("No se encontraron celdas en el archivo CSV.")
        exit()
    cantidadSerie = int(input("Ingresa el número de celdas en serie: "))
    cantidadParalelo = int(input("Ingresa el número de celdas en paralelo: "))
    priorizar_capacidad = input("Priorizar capacidad sobre resistencia? (si/no): ").strip().lower() == 'si'
    sorted_celdas = OrdenCeldasPorCriterio(celdas, priorizar_capacidad)
    celdasSeleccionadas = ConstruccionBateria(sorted_celdas, cantidadSerie, cantidadParalelo)
    if not celdasSeleccionadas or len(celdasSeleccionadas) < cantidadSerie: # Verificación de la construcción de la batería
        print("No se puede construir la configuración de batería solicitada.")
    else:
        capacidadTotal, resistenciaMedia = CalculoEspecificacionBateria(celdasSeleccionadas)
        print(f"\nConfiguracion de la batería:")
        for idx, group in enumerate(celdasSeleccionadas, 1):
            print(f" Grupo en serie {idx}: {[f'{cell['capacidad']}mAh/{cell['resistencia']}m\u03a9' for cell in group]}")
        print(f"\nCapacidad total: {capacidadTotal}mAh")
        print(f"Resistencia interna media: {resistenciaMedia:.2f}m\u03a9")
