from collections import Counter
from typing import List, Tuple

import jsonlines


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Funcion que lee un archivo JSONL y encuentra los 10 usuarios con mayor
    numero de menciones.
    
    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets 
        para analizar.
    
    Returns:
        List[Tuple[str, int]]: Lista de tuplas, donde el primer elemento 
        corresponde al nombre de usuario y el segundo a la cantidad de menciones.
    """
    # Contador para los usuarios
    contador = Counter()
    # Lectura de archivo JSONL, se lee linea por linea para para reducir
    # el uso de memoria
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            # Se rescata solo el campo mentionedUsers
            mentioned_users = obj.get('mentionedUsers', {})
            if mentioned_users:
                # Si existen usuarios mencionados rescato la lista de username
                mentioned_users = [item['username'] for item in mentioned_users]
                # Actualizo con contador de usuarios
                contador.update(mentioned_users)
    return contador.most_common(10)
