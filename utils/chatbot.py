from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub

def create_vectorstore(chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    new_vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)    
    
    #vectorstore.save_local('faiss_default')

    vectorstore = FAISS.load_local('faiss_default', embeddings=embeddings, allow_dangerous_deserialization=True)
    vectorstore.merge_from(new_vectorstore)
    
    return vectorstore

def create_conversation_chain(vectorstore=None):
    
    if(not vectorstore):
        embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        vectorstore = FAISS.load_local('faiss_default', embeddings=embeddings, allow_dangerous_deserialization=True)
    
    llm = HuggingFaceHub(repo_id="maritaca-ai/sabia-7b", model_kwargs={"temperature":0.5, "max_length":512})
    
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, 
                                                            retriever=vectorstore.as_retriever(), 
                                                            memory=memory)
    
    return conversation_chain