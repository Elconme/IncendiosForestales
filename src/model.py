from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

from sklearn.preprocessing import LabelEncoder

from src.etl import load_data

df, df_model = load_data()

le = LabelEncoder()
df_model['lugar_cod'] = le.fit_transform(df_model['lugar'])
df_model['claseincendio_cod'] = le.fit_transform(df_model['claseincendio'])
df_model['combustible_cod'] = le.fit_transform(df_model['combustible'])
df_model['tipoataque_cod'] = le.fit_transform(df_model['tipodeataque'])
df_model['tipofuego_cod'] = le.fit_transform(df_model['tipodefuego'])
df_model['horadet_cod'] = le.fit_transform(df_model['horadeteccion'])
df_model['clasedia_cod'] = le.fit_transform(df_model['idclasedia'])

X = df_model[['idcomunidad', 'idprovincia', 'latitud', 'longitud', 'altitud',
              'lugar_cod', 'combustible_cod', 'horadet_cod', 'clasedia_cod',
              'humrelativa', 'velocidadviento', 'tempmaxima']]

# Entrenamiento modelo
def train_and_save_model(target_variable):
  y = df_model[target_variable]

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  model = RandomForestClassifier(n_estimators=100, random_state=42)
  model.fit(X_train, y_train)
  model_name = f"./assets/{target_variable}_model_rf.pkl"  # Changed extension to .pkl for pickle

  with open(model_name, 'wb') as f:
    pickle.dump(model, f)

  y_pred = model.predict(X_test)

  # Guardar métricas precisión
  accuracy = accuracy_score(y_test, y_pred)
  f1 = f1_score(y_test, y_pred, average='micro')

  try:
      with open(f"./assets/{target_variable}_metrics2.txt", "w") as metrics_file:
          metrics_file.write(f"Accuracy: {accuracy:.4f}\n")
          metrics_file.write(f"F1-score: {f1:.4f}\n")
      print(f"Metrics saved to: {metrics_file.name}")
  except OSError as e:
    print(f"Error writing metrics file: {e}")

  print(f"Accuracy:", accuracy)
  print(f"F1-score:", f1)

# Cargar modelo
def load_model(target_variable):
  model_name = f"./assets/{target_variable}_model_rf.pkl"
  try:
    with open(model_name, 'rb') as f:
      model = pickle.load(f)
    return model
  except OSError:
    print(f"Model for '{target_variable}' not found. Please train the model first.")
    train_and_save_model(target_variable)
    return load_model(model_name)

if __name__ == "__main__":
  load_model('idpeligro')