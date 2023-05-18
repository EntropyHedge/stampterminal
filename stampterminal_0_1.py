import streamlit as st 
import pandas as pd 
import json
import requests
import matplotlib.pyplot as plt


#data functions 

def brc20_token():
    site = "https://brc-20.io/api_prices"
    r = requests.get(site)
    a = r.json()
    a = json.dumps(a)
    return(pd.read_json(a))

fd = pd.DataFrame()

fd["token"] = ["Kevin","STAMP","BOBO","pepe","A","wagmi","PIZZA","$VIVA"]
fd["supply"] = [690000000,1000000000,69420000,21000000,100000000000,1000000,11100000,42000000]
fd["mint"] = [420000,100000,100000,1000,10000000000,1000000,11111,420000]
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


#Main Page 

st.markdown("<style> span.tilealpha {color:rgb(189, 19, 65)} span.important {color:rgb(189, 19, 65); font-size:20px; font-weight:bold} span.donation {font-style: italic; font-weight:bold} </style>", unsafe_allow_html=True)

##Title
st.markdown('<h1 style="text-align: center; color: white;">Stamps Terminal <span class = "tilealpha">α</span></h1>', unsafe_allow_html=True)
st.divider()

#get brc20_token data 
df = brc20_token()
with st.sidebar:
    st.markdown('<h2 style="text-align: center; color:white">Select Tool</h2>', unsafe_allow_html=True)
    tool = st.radio('', ["SRC20 Progress","What if?"])
    #what if tool 
    if tool == "What if?":
        st.markdown('<h2 style="text-align: center; color:white">Settings</h2>', unsafe_allow_html=True)
        token1 = st.selectbox("Select SRC-20 Token", fd.token)
        token2 = st.selectbox("Select BRC-20 Token", df.token)
        custom_data = st.checkbox("Use your own data?")

        if custom_data:
            custum_marketcap = st.number_input("Marketcap in Million", 10)
            custum_marketcap = custum_marketcap * 1000000

    #progress tool
    else:
       st.markdown("Enjoy")



        
    st.image("https://i.ibb.co/6nnb854/qr-code.png")

    st.markdown(f'<span class="donation">If you want support further development please consider supporting to this wallet:</span> 1PorJqv3K4amxs7cMCFEUH9cCA7DZk5Jgr', unsafe_allow_html=True)


if tool == "What if?":

    index1 = fd[fd['token'] == token1].index.values
    index2 = df[df['token'] == token2].index.values


    if custom_data:

        price_per_token = custum_marketcap / fd.supply[index1[0]]
        price_per_token = round(price_per_token,8)


        mint_value = price_per_token * fd.mint[index1]

        mint_value = int(mint_value)

    else:
        price_per_token = df.marketCap[index2[0]] / fd.supply[index1[0]]
        price_per_token = round(price_per_token,8)


        mint_value = price_per_token * fd.mint[index1]

        mint_value = int(mint_value)

    #st.markdown(f'{price_per_token}')


    st.markdown(f'<p style="text-align: center">Worth of a single "{token1}" mint at "{token2}" marketcap: <span class="important">{str(mint_value)}</span>$</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center">That is <span class="important">{price_per_token}$</span> per "{token1}"</p>', unsafe_allow_html=True)

    #st.table(fd)

else:
    st.markdown('<h2 style="text-align: center; color:white">SRC20 Progress Legend</h2>', unsafe_allow_html=True)

    data = pd.read_csv("mint_progress.csv")

    for i in data.index:
        if float(data.progress[i]) > 100:
            st.progress(100, text=f"{data.token[i]} Progress: 100%")
        else:
            st.progress(float(data.progress[i]/100), text=f"{data.token[i]} Progress: {round(data.progress[i],3)}%")
    

    st.markdown("""<style> .st-cs { background-color: rgb(189 19 65);}</style>""", unsafe_allow_html=True )
    st.markdown("""<style> .st-h7 { background-color:  rgb(189 19 65);}</style>""", unsafe_allow_html=True )
   

