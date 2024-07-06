from collections import Counter, defaultdict
from typing import List, Tuple
from datetime import datetime

import jsonlines


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Funcion que lee un archivo JSONL y encuentra las 10 fechas con mayor 
    cantidad de tweets, para cada una de estas fechas entrega el usuario 
    con mayor cantidad de tweets.

    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets para 
        analizar.

    Returns:
        List[Tuple[datetime.date, str]]: Lista de tuplas, donde el primer 
        elemento corresponde a la fecha y el segundo elemento al nombre del 
        usuario.
    """
    result = []
    # Contador para las fechas
    fecha_counter = Counter()
    fecha_usuario_counter = defaultdict(Counter)
    # Lectura de archivo JSONL, se lee linea por linea para para reducir el uso
    # de memoria
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            # Se obtiene la fecha de cada uno de los registros
            fecha_str = obj.get('date')[:10]
            # Se castea de string a datetime.date
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            # Se actualiza el contador de fechas
            fecha_counter[fecha] += 1
            # Se actualiza el contador de usuarios por fechas
            fecha_usuario_counter[fecha][obj.get(
                'user', {}).get('username')] += 1

    # El top 10 de elementos mas comunes del contador
    top_fechas = fecha_counter.most_common(10)
    # Se itera por cada una de las fechas con mayor cantidad de tweets
    for fecha in top_fechas:
        usuarios = fecha_usuario_counter[fecha[0]]
        usuario_mas_repetido = usuarios.most_common(1)[0][0]
        result.append((fecha[0], usuario_mas_repetido))

    return result