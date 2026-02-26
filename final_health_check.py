import sys

file_path = "/home/admin/AXON_CORE/axon_core_os.py"

try:
    with open(file_path, "r") as f:
        source = f.read()
    
    # 1. Verificare sintaxă (Indentare)
    compile(source, file_path, 'exec')
    print("✅ SINTAXĂ: OK (Nicio eroare de indentare găsită)")
    
    # 2. Verificarea logicii în Tab Gestiune
    if "Progres Real" in source and "Cantitate_Validata" in source:
        print("✅ LOGICĂ: OK (Regula de Aur și Procentele sunt prezente)")
    else:
        print("⚠️ ATENȚIE: Verifică dacă logica de progres este completă.")

except IndentationError as e:
    print(f"❌ EROARE INDENTARE: Linia {e.lineno}")
    print(f"   Cod: {e.text.strip()}")
except Exception as e:
    print(f"❌ EROARE: {e}")

