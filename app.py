import yaml
import streamlit as st
from pages import Home,Dataset,Caption

# st.markdown("# Pupvotes \U0001F436")
# st.sidebar.markdown("# Homepage \U0001F431")



# @st.cache
def load_translator():

    with open("translator.yml","r") as f:

        return yaml.load(f,Loader=yaml.FullLoader)

translator = load_translator()





def choose_language():
    return st.sidebar.selectbox("Choose a language / Sceglia una lingua", ["English","Italiano"])

language = choose_language()



pages = {
    "homepage": Home,
    "dataset": Dataset,
    "caption": Caption,
}


def grab_page(selected_page,translation,language):
    return selected_page(translation,language)



selected_page = st.sidebar.selectbox(translator[language]["navigator"], pages.keys(), format_func=lambda x:translator[language][x]["name"])


current_page = grab_page(pages[selected_page],translator,language)
current_page.render_frame()

