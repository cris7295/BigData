import pandas as pd
import ast
import os

print("--- INICIANDO AUDITORÍA DE DATOS (VS CODE) ---")

# Nombres de tus archivos (Deben estar en la misma carpeta que este script)
FILE_PRODS = 'Amazon_Productos_Clean.csv'
FILE_REVS = 'Amazon_Reviews_Clean.csv'

# Verificamos que existan antes de cargar
if not os.path.exists(FILE_PRODS) or not os.path.exists(FILE_REVS):
    print(f"❌ ERROR: No encuentro los archivos en la carpeta.")
    print(f"Asegúrate de que '{FILE_PRODS}' y '{FILE_REVS}' estén junto a este script.")
else:
    try:
        print("1. Cargando datos... (esto puede tardar unos segundos)")
        df_prods = pd.read_csv(FILE_PRODS)
        df_revs = pd.read_csv(FILE_REVS)
        
        print(f"   -> Productos cargados: {len(df_prods)}")
        print(f"   -> Reviews cargadas: {len(df_revs)}")

        # --- CÁLCULO 1: COMPLETITUD (Productos incompletos) ---
        print("\n2. Calculando Completitud...")
        
        # Función para detectar si la lista de características está vacía "[]"
        def es_lista_vacia(x):
            if pd.isna(x): return True # Si es null/nan
            s = str(x).strip()
            if s == '[]' or s == '': return True
            return False

        # Contamos cuántos fallan en 'features' (o 'brand' si prefieres)
        # Ajusta 'features' si tu columna se llama diferente (ej. 'description')
        if 'features' in df_prods.columns:
            col_target = 'features'
        else:
            col_target = 'title' # Fallback por si acaso

        prods_sin_data = df_prods[col_target].apply(es_lista_vacia).sum()
        pct_incompletos = (prods_sin_data / len(df_prods)) * 100
        
        # --- CÁLCULO 2: VERACIDAD (Duplicados) ---
        print("3. Calculando Duplicados (Inconsistencias)...")
        # Buscamos duplicados en reviews (mismo producto, mismo texto)
        duplicados = df_revs.duplicated(subset=['Product_ID', 'text']).sum()
        pct_duplicados = (duplicados / len(df_revs)) * 100

        # --- RESULTADOS FINALES PARA TU WORD ---
        print("\n" + "="*40)
        print("📊 RESULTADOS PARA TU CAPÍTULO 1")
        print("="*40)
        print(f"A) Porcentaje de Incompletitud: {pct_incompletos:.2f}%")
        print(f"B) Porcentaje de Inconsistencias: {pct_duplicados:.2f}%")
        print("="*40)
        print("Copia estos números exactos en tu párrafo de 'Realidad Problemática'.")

    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")