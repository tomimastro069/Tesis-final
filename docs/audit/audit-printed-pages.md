import fitz

doc = fitz.open('docs/informe/informe-v17.pdf')

# Let's inspect page 6 (printed page 5), which has Índice de Figuras and Índice de Tablas
p6 = doc[5]
print("=== TEXT OF PDF PAGE 6 (Índices) ===")
print(p6.get_text())

print("\n=== VERIFYING FIGURES PRINTED PAGES ===")
fig_labels = {
    'Figura 1.': None,
    'Figura 2.': None,
    'Figura 3.': None,
    'Figura 4.': None,
    'Figura 1 (ampliada)': None,
    'Figura 2 (ampliada)': None,
    'Figura 3 (ampliada)': None,
    'Figura 4 (ampliada)': None,
}

for i, page in enumerate(doc):
    t = page.get_text()
    # Header page number is the first line or first number
    header_page = None
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    if lines and lines[0].isdigit():
        header_page = int(lines[0])
    
    for fig in fig_labels.keys():
        if fig_labels[fig] is None:
            for line in lines:
                if line.startswith(fig) and ('.' in line or '—' in line) and 'ampliada en el Anexo H' not in line:
                    fig_labels[fig] = header_page or (i)
                    print(f"Found {fig} at PDF page {i+1}, Printed Header Page: {header_page}")
                    break

print("\n=== VERIFYING TABLES PRINTED PAGES ===")
tabla_labels = {f'Tabla {k}.': None for k in range(1, 15)}

for i, page in enumerate(doc):
    t = page.get_text()
    header_page = None
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    if lines and lines[0].isdigit():
        header_page = int(lines[0])
    
    # skip index page itself (i == 5)
    if i == 5:
        continue
        
    for k in range(1, 15):
        prefix = f'Tabla {k}.'
        if tabla_labels[prefix] is None:
            for line in lines:
                if line.startswith(prefix):
                    tabla_labels[prefix] = header_page or (i)
                    print(f"Found {prefix} at PDF page {i+1}, Printed Header Page: {header_page}")
                    break
