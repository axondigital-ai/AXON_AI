import os

path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Căutăm linia unde își ia contextul RAG
target = "k_context = search_rag(p)"

# Îi adăugăm o injecție care citește fișierul direct de pe disc dacă există
injection = """k_context = search_rag(p)
                    # CITIRE DIRECTĂ LOCALĂ (Bypass Cloud RAG)
                    if os.path.exists('programator_activ.txt'):
                        with open('programator_activ.txt', 'r', encoding='utf-8') as fs:
                            k_context += "\\n--- SNAPSHOT LOCAL DIRECT ---\\n" + fs.read()"""

if target in content and "SNAPSHOT LOCAL DIRECT" not in content:
    content = content.replace(target, injection)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ [NEURAL LINK ACTIVAT]: Programatorul citește acum fișierele de pe disc instantaneu!")
else:
    print("ℹ️ Legătura locală există deja sau ținta nu a fost găsită.")
