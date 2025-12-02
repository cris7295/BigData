import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PRODS = os.path.join(BASE_DIR, 'data', 'silver', 'productos_silver.csv')
INPUT_REVS = os.path.join(BASE_DIR, 'data', 'silver', 'reviews_silver.csv')
OUTPUT_GOLD = os.path.join(BASE_DIR, 'data', 'gold', 'kpis_powerbi.csv')

print("--- 🚀 FASE 3: MODELADO Y AGREGACIÓN (GOLD LAYER) ---")

try:
    df_prods = pd.read_csv(INPUT_PRODS)
    df_revs = pd.read_csv(INPUT_REVS)
except Exception as e:
    print(f"❌ Error leyendo archivos Silver: {e}")
    exit()

# 1. CRUCE DE DATOS (JOIN)
# Usamos Product_ID que es el nombre correcto ahora
print("1. Uniendo tablas (Merge)...")
df_gold = pd.merge(df_revs, df_prods, on='Product_ID', how='inner')

# 2. VALIDACIÓN DE KPIs EN CONSOLA
total = len(df_gold)
if total > 0:
    otd_rate = (1 - df_gold['Es_Entrega_Tardia'].mean()) * 100
    return_rate = df_gold['Es_Devolucion'].mean() * 100
    csat = (len(df_gold[df_gold['rating'] >= 4]) / total) * 100

    print(f"\n📊 RESULTADOS FINALES PARA TESIS:")
    print(f"   - OTD Estimado: {otd_rate:.2f}%")
    print(f"   - Tasa Devolución: {return_rate:.2f}%")
    print(f"   - CSAT (Satisfacción): {csat:.2f}%")
else:
    print("⚠️ ADVERTENCIA: El cruce de tablas quedó vacío. Verifica los IDs.")

# 3. EXPORTAR PARA POWER BI
# CORRECCIÓN: Usamos 'Product_ID' en lugar de 'parent_asin'
# Nota: 'title_x' es el título del review, 'title_y' es del producto. Usamos title_y para el reporte.
cols = ['Product_ID', 'rating', 'timestamp', 'main_category', 'price', 
        'Es_Entrega_Tardia', 'Es_Devolucion', 'latencia_ingesta_ms']

# Verificamos si las columnas existen antes de guardar para evitar otro error
existing_cols = [c for c in cols if c in df_gold.columns]

df_gold[existing_cols].to_csv(OUTPUT_GOLD, index=False)

print(f"\n✅ DATA MART GENERADO: {OUTPUT_GOLD}")
print("   -> Carga este archivo en Power BI.")