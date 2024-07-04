import polars as pl
import jsonlines
from typing import List, Tuple
from datetime import datetime

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Funcion que lee un archivo JSONL y encuentra las 10 fechas con mayor cantidad de tweets, para cada una de estas fechas entrega el usuario con mayor cantidad de tweets, se prioriza el tiempo de ejecucion.
    Para esto se carga toda la informacion en memoria antes de procesarla.
    Args:
        file_path (str): Ruta del archivo JSONL que contiene los tweets para analizar.
    
    Returns:
        List[Tuple[datetime.date, str]]: Lista de tuplas, donde el primer elemento corresponde a la fecha y el segundo elemento al nombre del usuario.
    """
    # Lista que almacena la informacion en memoria linea por linea
    data = []
    # Lectura de archivo JSONL, se lee linea por linea
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            # Se rescata solo los campos que se analizaran
            filter_obj = {
                'date': obj.get('date'),
                'username': obj.get('user', {}).get('username')
            }
            data.append(filter_obj)
    # creacion de dataframe
    df = pl.DataFrame(data)
    # Transformacion de la columna date de str a date
    df = df.with_columns([pl.col('date').str.strptime(pl.Date, "%Y-%m-%dT%H:%M:%S%z").alias('date')])
    
    # Se retornan las 10 fechas con mayor cantidad de tweets
    top_fechas =( df
                    .group_by('date')
                    .len()
                    .sort('len',descending=True)
                    .head(10)['date']
                )
    # Se filtra el dataset por estas fechas
    df_filtrado = df.filter(pl.col('date').is_in(top_fechas))
    # Se elimina el dataset original
    del df
    # Se procesa el dataset filtrado
    result = (  df_filtrado.group_by(['date', 'username'])
            .len() # Se cuenta para cada usuario por fecha 
            .sort(by=['date', 'len'], descending=[False, True]) # Se ordena por fecha desendente false y largo true
            .group_by('date') # se agrupa por fechas
            .agg(
                    # Se agrega y se rescata le primer usuario por fecha
                    pl.col('username').first()
                )
     )
    # El resultado se joinea con las fechas para mantener el orden original
    # que consiste en las fechas con mas tweets
    result = top_fechas.to_frame().join(result, on='date',how="left")
    # Se formatea el output para que sea consistente con la descripcion de la funcion
    result = [tuple(row.values()) for row in result.to_dicts()]
    return result

