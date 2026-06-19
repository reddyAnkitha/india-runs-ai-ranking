from docx import Document

doc = Document(r"E:\india-runs-ai-ranking\data\job_description.docx")

job_description = ""

for para in doc.paragraphs:
    job_description += para.text + "\n"

print(job_description)