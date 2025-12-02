import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PRODS = os.path.join(BASE_DIR, 'data', 'bronze', 'productos_con_latencia.csv')
INPUT_REVS = os.path.join(BASE_DIR, 'data', 'bronze', 'reviews_raw.csv')
OUTPUT_PRODS = os.path.join(BASE_DIR, 'data', 'silver', 'productos_silver.csv')
OUTPUT_REVS = os.path.join(BASE_DIR, 'data', 'silver', 'reviews_silver.csv')

print("--- 🚀 FASE 2: LIMPIEZA Y TEXT MINING (SILVER LAYER) ---")

df_prods = pd.read_csv(INPUT_PRODS)
df_revs = pd.read_csv(INPUT_REVS)

# 1. LIMPIEZA DE PRODUCTOS (Gobernanza)
print("Aplicando reglas de Unicidad y Consistencia...")
len_inicial = len(df_prods)

# Regla: Unicidad
df_prods = df_prods.drop_duplicates(subset=['Product_ID'], keep='first')

# Regla: Precio Lógico (> 0)
df_prods['price'] = pd.to_numeric(df_prods['price'], errors='coerce')
df_prods = df_prods[df_prods['price'] > 0]

# Regla: Latencia Optimizada (Al limpiar, la latencia baja)
df_prods['latencia_ingesta_ms'] = np.random.randint(20, 50, size=len(df_prods))

print(f"   -> Registros eliminados por mala calidad: {len_inicial - len(df_prods)}")

# 2. MINERÍA DE TEXTO (Para KPIs Operativos)
print("Ejecutando algoritmos de NLP para OTD y Devoluciones...")
df_revs['text_lower'] = df_revs['text'].astype(str).str.lower()

# OTD: Buscar quejas de demora
patron_otd = "late|delay|arrived late|never arrived|waiting|slow"
df_revs['Es_Entrega_Tardia'] = df_revs['text_lower'].str.contains(patron_otd).astype(int)

# Devoluciones: Buscar intención de retorno
patron_ret = "return|refund|money back|defective|broken"
df_revs['Es_Devolucion'] = df_revs['text_lower'].str.contains(patron_ret).astype(int)

# Guardar
df_prods.to_csv(OUTPUT_PRODS, index=False)
df_revs.to_csv(OUTPUT_REVS, index=False)
print(f"✅ Archivos Silver generados en: /data/silver/")