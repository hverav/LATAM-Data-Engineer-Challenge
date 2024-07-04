import jsonlines
from collections import Counter
from typing import List, Tuple
from datetime import datetime

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Funcion que lee un archivo JSONL y encuentra las 10 fechas con mayor cantidad de tweets, para cada una de estas fechas entrega el usuario con mayor cantidad de tweets.
    
    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets para analisar.
    
    Returns:
        List[Tuple[datetime.date, str]]: Lista de tuplas, donde el primer elemento corresponde a la fecha y el segundo elemento al nombre del usuario.
    """
    result = []
    # Contador para las fechas
    fecha_counter = Counter()
    # Lectura de archivo JSONL, se lee linea por linea para para reducir el uso de memoria
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            # Se obtiene la fecha de cada uno de los registros
            fecha_str = obj.get('date')[:10]
            # Se castea de string a datetime.date
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            # Se actualiza el contador de fechas
            fecha_counter[fecha] += 1
    
    # El top 10 de elementos mas comunes del contador
    top_fechas = fecha_counter.most_common(10)
    print(top_fechas)
    return result

q1_memory('../data/farmers-protest-tweets-2021-2-4.json')