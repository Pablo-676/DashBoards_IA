import streamlit as st
import pandas as pd
import plotly.express as px

import pyrebase

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests


#firebase_admin.initialize_app(cred)

st.set_page_config(page_title='Meu site Streamlit')


with st.container():
    st.subheader("Meu primeiro site com o Streamlit")
    st.title("DashBoard Com streamlit e plotly.express")
    st.write("Graficos criados no dia 6")
    st.write("Quer acompanhar a jornada de 30 dias com python? siga o meu perfil no link [Clique Aqui](https://www.linkedin.com/in/pablo-almeida-160b21223)")


 