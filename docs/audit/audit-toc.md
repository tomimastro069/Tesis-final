import fitz

doc = fitz.open('docs/informe/informe-v17.pdf')

# PDF pages 4 and 5 contain the main outline
outline_text = doc[3].get_text() + "\n" + doc[4].get_text()

# Extract lines with dot leaders and page numbers
toc_entries = []
for line in outline_text.split('\n'):
    line = line.strip()
    # Typst outline uses invisible characters or dots
    # Let's inspect each line
    if any(line.startswith(f"{k}.") for k in range(1, 20)) or 'Resumen' in line or 'Abstract' in line or 'Anexo' in line or 'Referencias' in line:
        toc_entries.append(line)

print(f"Total TOC sample lines found: {len(toc_entries)}")
for e in toc_entries[:25]:
    print(" ", e)

