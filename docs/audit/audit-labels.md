import os, re

cap_dir = "docs/informe/capitulos"
files = [f for f in sorted(os.listdir(cap_dir)) if f.endswith('.typ')]
files.append("../informe-v17.typ")

labels_defined = set()
labels_referenced = set()

for f in files:
    path = os.path.join(cap_dir, f) if not f.startswith("..") else "docs/informe/informe-v17.typ"
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
        for m in re.finditer(r'<([a-zA-Z0-9_\-]+)>', content):
            labels_defined.add(m.group(1))
        for m in re.finditer(r'@([a-zA-Z0-9_\-]+)', content):
            labels_referenced.add(m.group(1))
        for m in re.finditer(r'pagina\(<([a-zA-Z0-9_\-]+)>\)', content):
            labels_referenced.add(m.group(1))

print(f"Total defined labels: {len(labels_defined)}")
print(f"Total referenced labels: {len(labels_referenced)}")

missing = labels_referenced - labels_defined
if missing:
    print("WARNING - Missing labels referenced:")
    for m in missing:
        print("  ", m)
else:
    print("All referenced labels are properly defined!")
