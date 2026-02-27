import os

path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Noul cod curat, folosind un dicționar pentru a ocoli eroarea constructorului Protobuf
# chr(10) este comanda internă Python pentru "Enter" (\n), ca să fentăm bash-ul definitiv.
new_rag = [
    "def search_rag(query):\n",
    "    try:\n",
    "        client = clients.get('search')\n",
    "        if not client: return 'Eroare: Client RAG offline.'\n",
    "        req_dict = {'serving_config': 'projects/axon-core-os/locations/global/collections/default_collection/dataStores/axon-knowledge-base_1771593704304/servingConfigs/default_serving_config', 'query': query, 'page_size': 3}\n",
    "        response = client.search(request=req_dict)\n",
    "        res_list = [str(r.document.derived_struct_data) for r in response.results]\n",
    "        sep = chr(10) + '---' + chr(10)\n",
    "        return sep.join(res_list) if res_list else 'Fără rezultate în RAG.'\n",
    "    except Exception as e:\n",
    "        return f'Eroare RAG: {str(e)}'\n",
    "\n"
]

# Tăiem exact și matematic: păstrăm până la 197 (inclusiv), inserăm noul cod, lipim de la 222 încolo
# (În Python, indexarea începe de la 0, deci linia 198 este indexul 197, linia 222 este indexul 221)
final_lines = lines[:197] + new_rag + lines[221:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("✅ [OPERAȚIE REUȘITĂ]: Liniile 198-221 au fost excizate și înlocuite precis.")
