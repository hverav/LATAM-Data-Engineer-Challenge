import jsonlines
from typing import List, Tuple
from collections import Counter

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Funcion que lee un archivo JSONL y encuentra los 10 usuarios con mayor numero de menciones, prioriza el tiempo de ejecucion.
    
    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets para analizar.
    
    Returns:
        List[Tuple[str, int]]: Lista de tuplas, donde el primer elemento corresponde al nombre de usuario y el segundo a la cantidad de menciones.
    """

    # Lista que almacena la informacion en memoria linea por linea
    data = []
    contador = Counter()
    # Lectura de archivo JSONL, se lee linea por linea
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            # Se rescata solo el campo mentionedUsers
            mentioned_users = obj.get('mentionedUsers', {})
            # Si se tienen mensiones en el tweet
            if mentioned_users:
                # Se extraen todos los usuarios mensionados
                data.extend([item['username'] for item in mentioned_users])
    # Se actualiza el contador
    contador.update(data)
    return contador.most_common(10)
