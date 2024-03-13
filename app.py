import streamlit as st
from streamlit_message import message
from utils import text_processor, chatbot



def main():

    st.set_page_config(page_title='ChatPDF Dataway', page_icon=':books:')

    st.header('Converse com seus arquivos :robot_face:')
    user_question = st.text_input("Faça uma pergunta para mim!")

    if('conversation' not in st.session_state):
        st.session_state.conversation = None

    if(user_question):
        
        try:
        
            response = st.session_state.conversation(user_question)['chat_history']

            for i, text_message in enumerate(response):

                if(i % 2 == 0):
                    message(text_message.content, is_user=True, key=str(i) + '_user')

                else:
                    message(text_message.content, is_user=False, key=str(i) + '_bot')
        
        except:
            
            st.session_state.conversation = chatbot.create_conversation_chain()
            
            response = st.session_state.conversation(user_question)['chat_history']
            
            for i, text_message in enumerate(response):

                if(i % 2 == 0):
                    message(text_message.content, is_user=True, key=str(i) + '_user')

                else:
                    message(text_message.content, is_user=False, key=str(i) + '_bot')



    with st.sidebar:

        st.subheader('Seus arquivos')
        pdf_docs = st.file_uploader("Carregue os seus arquivos em formato PDF", accept_multiple_files=True)

        if st.button('Processar'):
            raw_text = text_processor.process_files(pdf_docs)

            chunks = text_processor.create_chunks(raw_text)

            vectorstore = chatbot.create_vectorstore(chunks)

            st.session_state.conversation = chatbot.create_conversation_chain(vectorstore)

            

if __name__ == '__main__':

    main()
