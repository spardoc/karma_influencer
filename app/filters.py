from datetime import datetime
import pandas as pd

def filtrar_comentarios(df: pd.DataFrame, nombre_influencer=None, fecha_inicio=None, fecha_fin=None, red_social=None):
    """
    Aplica filtros sobre un DataFrame de comentarios.
    """
    if nombre_influencer:
        df = df[df['influencer'].str.lower() == nombre_influencer.lower()]
    
    if red_social:
        df = df[df['platform'].str.lower() == red_social.lower()]
    
    if fecha_inicio:
        try:
            fecha_inicio = pd.to_datetime(fecha_inicio)
            df = df[df['date'] >= fecha_inicio]
        except ValueError:
            pass

    if fecha_fin:
        try:
            fecha_fin = pd.to_datetime(fecha_fin)
            df = df[df['date'] <= fecha_fin]
        except ValueError:
            pass

    return df.reset_index(drop=True)
