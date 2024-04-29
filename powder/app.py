import streamlit as st
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.llms import VertexAI
from langchain.memory import ConversationBufferMemory

from powder.tools import GetNearbySkiResorts, GetHotelsNearSkiResort


def initialize_llm():
    tools = [GetNearbySkiResorts(), GetHotelsNearSkiResort()]
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm_chain = initialize_agent(
        tools,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        llm=VertexAI(),
        memory=memory,
        verbose=True,
    )
    return llm_chain


st.set_page_config(page_title="🎿 Ski Travel Planner Assistant")
st.title('🎿 Ski Travel Planner Assistant')
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant",
         "content": "Hi I am a ski travel planner assistant. I can find you the nearest ski resort to you. And also help you find the best hotel deals. How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    llm = initialize_llm()
    new_message = llm(prompt)
    st.session_state.messages.append({"role": "assistant", "content": new_message["output"]})
    st.chat_message("assistant", avatar="🤖").write(new_message["output"])
