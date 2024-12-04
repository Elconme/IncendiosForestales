import pandas as pd

def load_data(data_path="./Datos/incendios.csv", sep=';'):
  df = pd.read_csv(data_path, sep=sep)
  df.isna().sum()
  df_model = df.drop(['puntosinicioincendio','idnivelgravedadmaximo','probabilidadignicion' ,'idgradoresponsabilidad','idautorizacionactividad','direccionviento','idinvestigacioncausa','diastormenta','huso','idmotivacion','diasultimalluvia','iddatum','x','y'], axis=1) #,'humrelativa','velocidadviento','tempmaxima' 
  df_model = df_model.dropna()
  df = df.drop(['puntosinicioincendio','idnivelgravedadmaximo','probabilidadignicion' ,'idgradoresponsabilidad','idautorizacionactividad','humrelativa','velocidadviento','direccionviento','idinvestigacioncausa','diastormenta','huso','idmotivacion','diasultimalluvia','tempmaxima' ,'iddatum','x','y'], axis=1)
  df = df.dropna()
  
  #Mapeo de meses para poder generar fechas
  month_map = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
  df['mes_numerico'] = df['mesdeteccion'].map(month_map)
  df['fecha'] = pd.to_datetime(df['anio'].astype(str) + '-' + df['mes_numerico'].astype(str), format='%Y-%m')
  return df, df_model

if __name__ == "__main__":
  df, df_model = load_data()
  print(df.head())
  print(df_model.head())  
