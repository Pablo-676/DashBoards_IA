import streamlit as st


import pyrebase

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth


firebaseConfig = {
    'apiKey': "AIzaSyDWiYwmedg6sAE0V6nCCl4yhqLaM1JYfXk",
    'authDomain': "ia-dash-b5671.firebaseapp.com",
    'databaseURL':'https://ia-dash-b5671-default-rtdb.firebaseio.com',
    'projectId': "ia-dash-b5671",
    'storageBucket': "ia-dash-b5671.appspot.com",
    'messagingSenderId': "172729420370",
    'appId': "1:172729420370:web:8bad132c95eccf58ef2d8b",
    'measurementId': "G-GM7MGEK8T2"
}

firebase= pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()


cred = credentials.Certificate("ia-dash-b5671-205db9162535.json") 
firebase_admin.initialize_app(cred)



st.set_page_config(page_title='Meu site Streamlit')

if 'email' not in st.session_state:
    st.session_state['email'] = None
    
if 'user' not in st.session_state:
    st.session_state['user'] = None

with st.container():
    
    choice=st.selectbox('Logn/Singup',['Login','Sing Up'])
    
    def f():
        try:
            login = auth.sign_in_with_email_and_password(email,password)
            print(login)
            st.success("Logado com sucesso")
            st.session_state['email'] = email
            st.session_state['user'] = login
            st.balloons()

        except:
            st.warning('Senha ou email invalidos')
    
    
    if choice == 'Login':
        email=st.text_input('Email')
        password = st.text_input('Password',type='password')
        st.button('Login', on_click=f)
        
    else:

        username=st.text_input('Seu nome completo')
        email=st.text_input('Email')
        password = st.text_input('Senha',type='password')
        conf_password = st.text_input('Confirme a sua senha',type='password')
        
        
        if st.button('Create my acoount'):
            if password == conf_password:
                try:
                    user = auth.create_user_with_email_and_password(email,password)
                    
                    st.success("Conta criada com sucesso!")
                    st.markdown('Por favor faça login ultilizando seu email e senha')
                    st.balloons()
                except:
                    st.warning('Esse e-mail já está cadastrado')
            else:
                st.warning('As senhas não conferem')
                
    
 