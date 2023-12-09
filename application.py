import chainlit as cl
from langchain.retrievers import AzureCognitiveSearchRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True, output_key="answer"
)

@cl.on_chat_start
def load_chain():
    prompt_template = """You are a helpful and friendly professor at Pennsylvania State University.
    You are an expert at understanding the course details for the Artificial Intelligence Program at
    Pennsylvania State University and your job is to assist students in
    answering any questions they may have about the courses within the program.
    If the answer can't be determined using only the information in the provided context simply output 'No Answer Available for Context'

    {context}

    Question: {question}
    Answer here:
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    retriever = AzureCognitiveSearchRetriever(content_key="content", top_k=10)

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name='gpt-4'),
        memory=memory,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": PROMPT},
    )
    return chain

chain = load_chain()

@cl.on_message
def chat(user_input):
    if user_input:
        output = chain.run(question=user_input)
        return output

