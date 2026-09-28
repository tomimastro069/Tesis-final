import fitz

doc = fitz.open('docs/informe/informe-v17.pdf')
print(f"Total pages: {len(doc)}")

print("\n--- ANEXO H PAGES AND DIMENSIONS ---")
for i in range(60, len(doc)):
    page = doc[i]
    t = page.get_text()
    if 'Anexo H' in t or 'ampliada' in t.lower() or 'anexo i' in t.lower():
        r = page.rect
        print(f"PDF Page {i+1}: size={r.width:.1f}x{r.height:.1f}, landscape={r.width > r.height}")
        for line in t.split('\n'):
            line = line.strip()
            if any(k in line.lower() for k in ['figura', 'anexo h', 'anexo i', 'diagrama']):
                print(f"   {line}")

print("\n--- V1 DETAILS ---")
# 12.6 flags
for i in range(30, 38):
    t = doc[i].get_text()
    if '12.6' in t:
        print(f"Found 12.6 on PDF page {i+1}:")
        for line in t.split('\n'):
            if any(k in line for k in ['batch', 'flush', 'forms', 'dbms', 'level', 'risk', 'threads', 'smart', 'technique']):
                print("  ", line.strip())

# 12.7 sqlmapapi
for i in range(32, 38):
    t = doc[i].get_text()
    if '12.7' in t:
        print(f"Found 12.7 on PDF page {i+1}:")
        for line in t.split('\n'):
            if any(k in line for k in ['sqlmap', 'api', 'json', 'format']):
                print("  ", line.strip())

# 13.4 technique and payload
for i in range(38, 43):
    t = doc[i].get_text()
    if '13.4' in t:
        print(f"Found 13.4 on PDF page {i+1}:")
        for line in t.split('\n'):
            if any(k in line for k in ['technique', 'SCVZ', 'RmAL', 'payload', 'Fqvd', 'Login']):
                print("  ", line.strip())

# 14.4 threads and smart
for i in range(43, 49):
    t = doc[i].get_text()
    if '14.4' in t:
        print(f"Found 14.4 on PDF page {i+1}:")
        for line in t.split('\n'):
            if any(k in line for k in ['threads', 'smart', 'bandera']):
                print("  ", line.strip())

# 15.2 allow_origins
for i in range(48, 54):
    t = doc[i].get_text()
    if '15.2' in t:
        print(f"Found 15.2 on PDF page {i+1}:")
        for line in t.split('\n'):
            if 'allow_origins' in line:
                print("  ", line.strip())
