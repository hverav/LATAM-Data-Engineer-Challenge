import jsonlines
from collections import Counter
from typing import List, Tuple

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Funcion que lee un archivo JSONL y encuentra los 10 usuarios con mayor numero de menciones.
    
    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets para analizar.
    
    Returns:
        List[Tuple[str, int]]: Lista de tuplas, donde el primer elemento corresponde al nombre de usuario y el segundo a la cantidad de menciones.
    """
    contador = Counter()
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            mentioned_users = obj.get('mentionedUsers', {})
            if mentioned_users:
                mentioned_users = [item['username'] for item in mentioned_users]
                contador.update(mentioned_users)
    return contador.most_common(10)

f = q3_memory('../data/farmers-protest-tweets-2021-2-4.json')
print(f)