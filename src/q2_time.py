from typing import List, Tuple
from itertools import chain
from collections import Counter

import emot
import pandas as pd


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Funcion que lee un archivo JSONL y encuentra los 10 emojis mas usados, 
    priorizando el uso de memoria.

    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets 
        para analizar.

    Returns:
        List[Tuple[str, int]]: Lista de tuplas, donde el primer elemento 
        corresponde al emoji y el segundo a la cantidad de veces que se utiliza.
    """
    # Contador para los emojis
    contador = Counter()
    # Lectura de archivo JSONL, se carga todo en memoria con pandas
    df = pd.read_json(file_path, lines=True)
    # Se genera un objeto emot.core.emot
    emot_obj = emot.core.emot()
    # Se genera una lista con todos los elementos del dataframe de la
    # columna content.
    # Esta columna es la que tiene la informacion del texto del tweet
    data = df['content'].tolist()
    # Se utiliza el metodo bulk_emoji ya que utiliza multi procesamiento
    emojis = emot_obj.bulk_emoji(data)
    # Se deja la lista aplana la lista de listas solamente cuando existen emojis
    emojis = list(chain.from_iterable(item['value']
                  for item in emojis if item['value']))
    # Actualizo el contador
    contador.update(emojis)
    return contador.most_common(10)
