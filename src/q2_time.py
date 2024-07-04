import emoji
import jsonlines
import polars as pl
from typing import List, Tuple

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Funcion que lee un archivo JSONL y encuentra los 10 emojis mas usados, priorizando el uso de memoria.
    
    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets para analizar.
    
    Returns:
        List[Tuple[str, int]]: Lista de tuplas, donde el primer elemento corresponde al emoji y el segundo a la cantidad de veces que se utiliza.
    """
    # Contador para los emojis
    data = []
    # Lectura de archivo JSONL, se lee linea por linea para para reducir el uso de memoria
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            # Se obtiene el objeto content que es donde esta el cuerpo del tweet
            content = obj.get('content')
            # Se obtiene la lista de diccionarios de los emojis encontrados en el texto
            emojis = emoji.emoji_list(content)
            if(emojis):
                # Si se encontraron emojis en el texto se almacena solo los emojis
                emojis = [item['emoji'] for item in emojis]
                data.extend(emojis)
    # Se genera el dataframe
    df = pl.DataFrame(data)
    # Se retorna el top 10 de emojis
    result = df.group_by('column_0').len().sort('len',descending=True).head(10)
    # Se formatea el output para que sea consistente con la descripcion de la funcion
    result = [tuple(row.values()) for row in result.to_dicts()]
    return result
