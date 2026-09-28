import fitz

doc = fitz.open('docs/informe/informe-v17.pdf')

# Let's check PDF pages 74 and 75 (printed 73 and 74)
print("=== TEXT OF PDF PAGES 74 AND 75 (ANEXO I) ===")
print("--- PAGE 74 ---")
print(doc[73].get_text())
print("--- PAGE 75 ---")
print(doc[74].get_text())
