import emot
import jsonlines
from collections import Counter
from typing import List, Tuple

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Funcion que lee un archivo JSONL y encuentra los 10 emojis mas usados, priorizando el uso de memoria.
    
    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets para analizar.
    
    Returns:
        List[Tuple[str, int]]: Lista de tuplas, donde el primer elemento corresponde al emoji y el segundo a la cantidad de veces que se utiliza.
    """
    # Contador para los emojis
    contador = Counter()
    # Se genera un objeto emot.core.emot
    emot_obj = emot.core.emot()
    # Lectura de archivo JSONL, se lee linea por linea para para reducir el uso de memoria
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            # Se obtiene el objeto content que es donde esta el cuerpo del tweet
            content = obj.get('content')
            # Se obtiene la lista de diccionarios de los emojis encontrados en el texto
            emojis = emot_obj.emoji(content)
            if(emojis['value']):
                # Si se encontraron emojis en el texto se almacena solo los emojis
                emojis = [item for item in emojis['value']]
                # Se actualiza el contador con la lista de emojis
                contador.update(emojis)
    # Se retorna el top 10 de emojis
    return contador.most_common(10)
