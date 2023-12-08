# Api keys : 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

import os
import random
import streamlit as st

def configure_openai_api_key():
    openai_api_key = st.sidebar.text_input(
        label = 'OpenAI API Key',
        type = 'password',
        value= st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else '',
        placeholder='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'
    )
    if openai_api_key:
        st.session_state['OPENAI_API_KEY'] = openai_api_key
        os.environ['OPENAI_API_KEY'] = openai_api_key
    else:
        st.error('Add OPENAI API KEY to Continue.')
        st.info('Open AI Generate Link : https://platform.openai.com/account/api-keys')
        st.stop()
    return openai_api_key

def enable_chat_history(func):
    if os.environ.get('OPENAI_API_KEY'):
        # to clear chat history after switching chatbot
        current_page = func.__qualname__
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = current_page
        if st.session_state['current_page'] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state['current_page']
                del st.session_state['messages']
            except:
                pass
        
        # Show chat history on User interface
        if 'messages' not in st.session_state:
            st.session_state['messages'] = [
                {'role':'assistant',
                'content': ' Can I Help You ?'}
                ]
        for msg in st.session_state['messages']:
            st.chat_message(msg['role']).write(msg['content'])
        
        def execute(*args, **kwargs):
            func(*args, **kwargs)
        return execute

def display_msg(msg, author):
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)
