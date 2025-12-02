import pandas as pd
import numpy as np
import os

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_RAW_PRODS = os.path.join(BASE_DIR, 'data', 'bronze', 'productos_raw.csv')
PATH_RAW_REVS = os.path.join(BASE_DIR, 'data', 'bronze', 'reviews_raw.csv')
PATH_OUTPUT_BRONZE = os.path.join(BASE_DIR, 'data', 'bronze', 'productos_con_latencia.csv')

print("--- 🚀 FASE 1: INGESTA Y DIAGNÓSTICO (BRONZE LAYER) ---")

# 1. CARGA DE DATOS
print(f"Leyendo archivos desde: {PATH_RAW_PRODS}...")
try:
    df_prods = pd.read_csv(PATH_RAW_PRODS)
    df_revs = pd.read_csv(PATH_RAW_REVS)
except Exception as e:
    print(f"❌ Error leyendo archivos: {e}")
    exit()

# VERIFICACIÓN DE COLUMNAS (Para evitar errores)
print("Columnas encontradas en Productos:", df_prods.columns.tolist())

# Definimos el nombre correcto del ID (Si no es 'Product_ID', intenta 'parent_asin')
col_id = 'Product_ID' if 'Product_ID' in df_prods.columns else 'parent_asin'
print(f"   -> Usando columna de ID: '{col_id}'")

# 2. AUDITORÍA INICIAL (KPIs de Calidad BRONZE)
print("Calculando línea base de calidad...")

# KPI: Completitud (Features vacías)
def es_incompleto(x):
    s = str(x).strip()
    return s == '[]' or s == '' or s == 'nan' or pd.isna(x)

# Si la columna 'features' no existe, usamos 'title' como fallback
col_features = 'features' if 'features' in df_prods.columns else 'title'

incompletos = df_prods[col_features].apply(es_incompleto).sum()
tasa_incompletitud = (incompletos / len(df_prods)) * 100

# KPI: Unicidad (Duplicados)
duplicados = df_prods.duplicated(subset=[col_id]).sum()
tasa_duplicidad = (duplicados / len(df_prods)) * 100

print(f"   ⚠️ Tasa Incompletitud Inicial: {tasa_incompletitud:.2f}%")
print(f"   ⚠️ Tasa Duplicidad Inicial: {tasa_duplicidad:.2f}%")

# 3. SIMULACIÓN DE LATENCIA (KPI p95)
print("Simulando latencia de ingesta basada en suciedad del dato...")

def calcular_latencia(row):
    ms = np.random.randint(20, 50) # Latencia base normal
    
    # Penalización por Precio
    try:
        p = float(row['price'])
        if pd.isna(p) or p <= 0: ms += np.random.randint(200, 500)
    except:
        ms += np.random.randint(200, 500)
        
    # Penalización por Features
    f = str(row[col_features])
    if f == '[]' or f == 'nan': ms += np.random.randint(100, 300)
    
    return ms

df_prods['latencia_ingesta_ms'] = df_prods.apply(calcular_latencia, axis=1)

# Guardamos el archivo intermedio en Bronze
df_prods.to_csv(PATH_OUTPUT_BRONZE, index=False)
print(f"✅ Archivo generado con latencia: {PATH_OUTPUT_BRONZE}")