import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
# from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()
chat = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile",
                max_tokens=2000)


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("AI Website Development Assistant")


website_type = st.chat_input("Which type of website do you want to create?")


if website_type:

    st.session_state.chat_history.append(
        {"role": "human", "content": website_type})

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"If the user's query is not related to website structure or content, respond with the message:'Error: Out-of-domain query.'If the query contains the word 'website', respond by providing a detailed structure for a website. Include core pages that are essential for most websites, numbering each page and listing the necessary sections and subsections under them. Follow industry best practices and standards in your response, ensuring it is clear, logical, and easy to understand. Once the structure is provided, ask if the user would like content generated for each page, and wait for confirmation or requested changes before proceeding further. Do not respond to any other types of queries, and avoid providing any extra information unrelated to website structure."),
        ("human", f"Website type: {website_type}"),
        MessagesPlaceholder(variable_name="chat_history")
    ])

    # st.chat_message('user')
    context = {"chat_history": st.session_state.chat_history}

    chain = prompt_template | chat 
    response = chain.invoke(context)

    if hasattr(response, 'content'):

        st.session_state.chat_history.append(
            {"role": "ai", "content": response.content})

        if len(st.session_state.chat_history) > 0:

            for message in st.session_state.chat_history:

                if message['role'] == 'human':
                    user_query = st.chat_message('human')
                    user_query.write(f"{message['content']}")
                elif (message['role'] == 'ai'):
                    message_previous = st.chat_message('ai')
                    message_previous.write(f"{message['content']}")

    else:
        st.write("Error: Unable to retrieve response content")
