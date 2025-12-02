import pandas as pd
import os

# CONFIGURACIÓN
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_REVS = os.path.join(BASE_DIR, 'data', 'silver', 'reviews_silver.csv')

print("--- 🔍 AUDITORÍA DE RESULTADOS (CAPA SILVER) ---")

if os.path.exists(FILE_REVS):
    df = pd.read_csv(FILE_REVS)
    total = len(df)
    
    # 1. CONTEO DE ENTREGAS TARDÍAS (OTD)
    otd_count = df['Es_Entrega_Tardia'].sum()
    otd_pct = (otd_count / total) * 100
    
    print(f"\n🚚 [OTD] ENTREGAS TARDÍAS DETECTADAS:")
    print(f"   Total: {otd_count} de {total} registros ({otd_pct:.2f}%)")
    
    if otd_count > 0:
        print("   Ejemplos de texto detectado:")
        ejemplos = df[df['Es_Entrega_Tardia'] == 1]['text'].head(3).tolist()
        for i, txt in enumerate(ejemplos):
            print(f"     {i+1}. \"{txt[:100]}...\"")
    else:
        print("   ⚠️ ¡OJO! No se detectó ninguna. Revisa tus palabras clave en el script 2.")

    # 2. CONTEO DE DEVOLUCIONES
    dev_count = df['Es_Devolucion'].sum()
    dev_pct = (dev_count / total) * 100
    
    print(f"\n📦 [RET] DEVOLUCIONES DETECTADAS:")
    print(f"   Total: {dev_count} de {total} registros ({dev_pct:.2f}%)")
    
    if dev_count > 0:
        print("   Ejemplos de texto detectado:")
        ejemplos = df[df['Es_Devolucion'] == 1]['text'].head(3).tolist()
        for i, txt in enumerate(ejemplos):
            print(f"     {i+1}. \"{txt[:100]}...\"")
            
    print("\n------------------------------------------------")
    print("💡 CONSEJO: Si los números son muy bajos (< 1%), considera agregar")
    print("   más palabras clave en '2_limpieza_silver.py' (ej. 'slow', 'broken', 'damaged').")

else:
    print(f"❌ No encuentro el archivo: {FILE_REVS}")
    print("   Asegúrate de haber ejecutado primero el script '2_limpieza_silver.py'")