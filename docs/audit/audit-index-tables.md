import fitz

doc = fitz.open('docs/informe/informe-v17.pdf')

print("=== CHECKING INDEX OF FIGURES ===")
# Find page of index of figures (usually page 4 or 5)
for pno in range(1, 10):
    text = doc[pno].get_text()
    if 'Índice de Figuras' in text:
        print(f"Index of Figures on PDF page {pno+1}:")
        for line in text.split('\n'):
            if 'Figura' in line or 'fig-' in line:
                print("  ", line.strip())

print("\n=== ACTUAL LOCATION OF FIGURES ===")
for i, page in enumerate(doc):
    t = page.get_text()
    for line in t.split('\n'):
        line_s = line.strip()
        if line_s.startswith('Figura ') and ('.' in line_s or '—' in line_s):
            print(f"  PDF Page {i+1} (Printed p.{page.get_text().count('header') or i}): {line_s}")

print("\n=== CHECKING INDEX OF TABLES ===")
for pno in range(1, 10):
    text = doc[pno].get_text()
    if 'Índice de Tablas' in text:
        print(f"Index of Tables on PDF page {pno+1}:")
        for line in text.split('\n'):
            if 'Tabla' in line or 'tabla-' in line:
                print("  ", line.strip())

print("\n=== ACTUAL LOCATION OF TABLES ===")
for i, page in enumerate(doc):
    t = page.get_text()
    for line in t.split('\n'):
        line_s = line.strip()
        if line_s.startswith('Tabla ') and '.' in line_s:
            print(f"  PDF Page {i+1}: {line_s}")

print("\n=== PRINTED PAGE NUMBERS VS PDF PAGE NUMBERS ===")
# Inspect headers/footers for printed page numbers
for i in range(1, 15):
    t = doc[i].get_text()
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    first_few = lines[:3]
    last_few = lines[-3:]
    # look for page number in header
    print(f"PDF Page {i+1}: lines[:2]={first_few[:2]}, lines[-2:]={last_few[-2:]}")
