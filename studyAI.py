import streamlit as st
import time
from ppx_helper import get_content
from mode_prompt import mode_prompts

st.title("StudyAI - igcse made easy")

mode = "General assistance"

def get_memory(messages):
    conversation_format = "The following is a friendly conversation between a human student who is an igcse student and an AI assistant. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.\n\nCurrent conversation:\n"
    for message in messages:
        conversation_format += f'{message["role"]}: {message["content"]}\n'
    return conversation_format


# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Teaching modes dropdown menu
mode = st.selectbox(
    "What sort of question would you like me to give feedback on?",
    ("General assistance", "History - 2 effects", "History - 16 marker", "Geography - explain 2"),  
)

# Display chat messages in history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Say something"):
    if prompt in ["clear", "quit", "exit"]:
        st.session_state.messages = []
    else:    
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
            
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Get previous messages
            memory = get_memory(st.session_state.messages)
            
            # Determine mode for answering prompt
            if mode != "General assistance":
                prefix = f"Unless I have asked a question, based on the instructions above along \
                with this marking guide, give extensive feedback on this answer, then rewriting it, giving me a level as explained in the guide. \
                Also, tell me how I could improve (e.g. could I have used more facts). Use this marking guide, along with research on model answers for the \
                igcse edexcel exam board: {mode_prompts[mode]}"
                response = get_content(f"{memory} AI:\n{prefix}")
            else:
                response = get_content(f"{memory} AI:")
            
            # Display response
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                # Blinking cursor
                time.sleep(0.02)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

