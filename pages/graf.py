import streamlit as st
import pandas as pd
import plotly.express as px
import os
import pyrebase

import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import auth
import json
import requests

firebaseConfig = {
    'apiKey': "AIzaSyDWiYwmedg6sAE0V6nCCl4yhqLaM1JYfXk",
    'authDomain': "ia-dash-b5671.firebaseapp.com",
    'databaseURL':'https://ia-dash-b5671-default-rtdb.firebaseio.com/',
    'projectId': "ia-dash-b5671",
    'storageBucket': "ia-dash-b5671.appspot.com",
    'messagingSenderId': "172729420370",
    'appId': "1:172729420370:web:8bad132c95eccf58ef2d8b",
    'measurementId': "G-GM7MGEK8T2"
}

firebase= pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()


cred = credentials.Certificate("ia-dash-b5671-205db9162535.json") 

#firebase_admin.initialize_app(cred)

storage_client = storage

bucket2 = storage_client.bucket('ia-dash-b5671.appspot.com')

bucket = storage.bucket('ia-dash-b5671.appspot.com')
storage = firebase.storage()

diretorio_atual = os.getcwd()

st.set_page_config(page_title='Meu site Streamlit')


user=st.session_state['user']


caminho_diretorio = f'{diretorio_atual}\{user['email']}'  # replace with your directory path

file_names = [f for f in os.listdir(caminho_diretorio) if os.path.isfile(os.path.join(caminho_diretorio, f))]


print(user['email'])
try:
    if st.session_state['email']:
        email=st.session_state['email']
        st.title(f"DashBoard do {email[:5].upper()}")
        #st.write(f"Gráficos pertencentes á {user}")
        

except:
    st.write("Por favor, faça o login para visualizar a informação.")
    
st.write("Quer acompanhar a jornada de 30 dias com python? siga o meu perfil no link [Clique Aqui](https://www.linkedin.com/in/pablo-almeida-160b21223)")

@st.cache_data
def carregar_dados():  
    df_original = pd.read_csv('C:/Users/Pablo Vítor/Desktop/Scripts/30daysOfPython/day18/pablovitorrocha017@gmail.com/netflix_titles.csv', encoding='ISO-8859-1')
    df_tratado = df_original.iloc[:, 1:12]
    df_tratado = df_tratado.dropna()
    df_tratado['release_year'] = df_tratado['release_year'].astype(int)
    df_tratado=df_tratado.sort_values(by='release_year')
    return df_tratado

def download_arquivos():
    storage.download(f'{email}',f'{email}_storage.txt')
    if not os.path.exists(email):
        os.makedirs(email)
        
    list_itens=[]
    with open(f'{email}_storage.txt', 'r') as file:
        content = file.read()
        content = json.loads(content)
        for item in content['items']:
            if email in item['name']:
                list_itens.append(item['name'])
            
    for itens in list_itens:
  
        blob = bucket2.blob(itens)
        blob.download_to_filename(f'{email}/{itens.split("/")[-1]}')

    os.remove(f"{email}_storage.txt")
    file_names = [f for f in os.listdir(caminho_diretorio) if os.path.isfile(os.path.join(caminho_diretorio, f))]
    

def carregar_df(data_frame):
    caminho=f'C:/Users/Pablo Vítor/Desktop/Scripts/30daysOfPython/day18/pablovitorrocha017@gmail.com/{data_frame}'
    if '.csv' in data_frame:
        df= pd.read_csv(caminho, encoding='ISO-8859-1')
        st.dataframe(df)
    elif '.xlsx' in data_frame:
        df= pd.read_excel(caminho)
        st.dataframe(df)
    
dataframes = st.selectbox('Selecione o df',file_names) 
carregar_df(dataframes) 
    
with st.container():
    st.write("---")
    if email == 'pablovitorrocha017@gmail.com':
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt", "xlsx"])
        if uploaded_file is not None:
            file_name, file_extension = os.path.splitext(uploaded_file.name)
            local_file_path = os.path.join(os.getcwd(), file_name + file_extension)
            with open(local_file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            storage_path=f'{email}/{uploaded_file.name}'
            storage.child(storage_path).put(local_file_path)
            os.remove(local_file_path)
            
        st.button('Download', on_click=download_arquivos)
        try:
            dados = carregar_dados()
            list_type=list(dados['type'].unique())
            list_type.append('Movie e TV Show')
            type = st.selectbox('Selecione o tipo',list_type)
            if type not in list(dados['type'].unique()):
                dados = carregar_dados()
            else:
                dados=dados[dados['type']==type]
            
            df_fig1 = pd.pivot_table(dados, index=['release_year','type'], columns=[], aggfunc='count')
            fig1 = px.bar(df_fig1, x=df_fig1.index.get_level_values(0), color=df_fig1.index.get_level_values(1), y='cast', 
                        title='Quantidade de filmes e séries lançadas por ano', barmode="group")
            
            fig1.update_layout(
                paper_bgcolor="#0E1117",
                plot_bgcolor="#0E1117",
                autosize=True,
                title_font=dict(color='white'),
                xaxis=dict(color='white'),
                yaxis=dict(color='white'),
                legend=dict(bgcolor='#0E1117', bordercolor='#0E1117', font=dict(color='white')),
                margin=dict(l=10, r=10, b=10, t=40)) 
            st.plotly_chart(fig1, use_container_width=True)
        except:
            st.write("Pasta não encontrada")
            