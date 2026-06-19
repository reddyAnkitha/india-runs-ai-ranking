from docx import Document

doc = Document(r"E:\india-runs-ai-ranking\data\job_description.docx")

text = ""

for para in doc.paragraphs:
    text += para.text + "\n"

with open(
    r"E:\india-runs-ai-ranking\data\job_description.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(text)

print("job_description.txt created successfully!")