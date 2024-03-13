from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

def process_files(files):
    text = ""
    
    for file in files:
        if file.name.endswith(".pdf"):
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            text += file.read()
            
    return text

def create_chunks(text):
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks