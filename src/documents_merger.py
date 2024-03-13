import os
from PyPDF2 import PdfMerger

# Pasta de saída
output_folder = "output"

# Criar um objeto PdfFileMerger
pdf_merger = PdfMerger()

# Iterar sobre os arquivos na pasta de saída e adicionar cada PDF ao objeto de mesclagem
for filename in os.listdir(output_folder):
    if filename.endswith(".pdf"):
        filepath = os.path.join(output_folder, filename)
        pdf_merger.append(filepath)

# Salvar o arquivo mesclado
output_merged_path = "output/merged_output.pdf"
pdf_merger.write(output_merged_path)
pdf_merger.close()

print(f"Arquivos PDF mesclados com sucesso em {output_merged_path}")