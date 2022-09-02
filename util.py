import streamlit as st



def translate():

    if st.session_state.new_language:
        st.session_state["lang"] = st.session_state.new_language


def flip_page():

    if st.session_state.new_page:
        st.session_state["page"] = st.session_state.new_page



def apply_filter1():

    if st.session_state.new_filter1:
        st.session_state["filter1"] = st.session_state.new_filter1



def apply_filter2():

    if st.session_state.new_filter2:
        st.session_state["filter2"] = st.session_state.new_filter2