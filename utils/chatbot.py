from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def create_vectorstore(chunks):
    embeddings = OpenAIEmbeddings(openai_api_key="insert_key_here")
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return vectorstore


def create_conversation_chain(vectorstore=None):
    llm = ChatOpenAI(openai_api_key="insert_key_here")

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    return conversation_chain