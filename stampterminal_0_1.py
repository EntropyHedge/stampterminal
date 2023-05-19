import streamlit as st 
import pandas as pd 
import json
import requests
import matplotlib.pyplot as plt


#data functions 


def get_address_data(address):

    site = "https://xchain.io/api/balances/" + address
    
    r = requests.get(site)
    a = r.json()
    a = json.dumps(a)
    
    return(pd.read_json(a))

def get_assets(dataframe):
    
    asset_list = []
    asset_quantity = []
    asset_value = []

    for index in dataframe.index:

        asset_list.append(dataframe.data[index]["asset"])
        asset_quantity.append(dataframe.data[index]["quantity"])  
        asset_value.append(dataframe.data[index]["estimated_value"]["usd"])
    
    user_dataframe = pd.DataFrame()

    user_dataframe["asset"] = asset_list
    user_dataframe["quantity"] = asset_quantity
    user_dataframe["value"] = asset_value
    
    return(user_dataframe)





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
tool = ""
if tool == "Wallet Checker":
    st.markdown(f'{user_address}')

st.divider()

#get brc20_token data 
df = brc20_token()
with st.sidebar:
    st.markdown('<h2 style="text-align: center; color:white">Select Tool</h2>', unsafe_allow_html=True)
    tool = st.radio('', ["SRC20 Progress","What if?","Wallet Checker"])
    #what if tool 
    if tool == "What if?":
        st.markdown('<h2 style="text-align: center; color:white">Settings</h2>', unsafe_allow_html=True)
        token1 = st.selectbox("Select SRC-20 Token", fd.token)
        token2 = st.selectbox("Select BRC-20 Token", df.token)
        custom_data = st.checkbox("Use your own data?")

        if custom_data:
            custum_marketcap = st.number_input("Marketcap in Million $", 10)
            custum_marketcap = custum_marketcap * 1000000
    #progress tool
    if tool == "SRC20 Progress":
       st.markdown("Enjoy")


    if tool == "Wallet Checker":

        user_address = st.text_input("Enter Address", value = "")

        
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

    market_cap_x = []
    price_per_coin_y = []
    for i in range(1, 1000):
        market_cap_x.append(i * 1000000)
        price_per_coin_y.append(round(i * 1000000 / fd.supply[index1[0]],8))

    chart_data = pd.DataFrame()
    chart_data.index = market_cap_x
    chart_data[f"Price per {token1} at x Market Cap"] = price_per_coin_y
    st.markdown("<br>", unsafe_allow_html=True)
    st.area_chart(chart_data)

if tool == "SRC20 Progress":
    st.markdown('<h2 style="text-align: center; color:white">SRC20 Progress Legend</h2>', unsafe_allow_html=True)

    data = pd.read_csv("mint_progress.csv")
    st.markdown("""<style> .st-cs { background-color: rgb(189 19 65);}</style>""", unsafe_allow_html=True )
    for i in data.index:
        
        if data.progress[i] > 100:
            st.progress(100, text=f"{data.token[i]} Progress: 100%")
        else:
            st.progress(float(data.progress[i])/100, text=f"{data.token[i]} Progress: {round(data.progress[i],4)}%")
            
        
if tool == "Wallet Checker":
    

    if user_address:
        try:
            user_data = get_address_data(user_address)
            user_data = get_assets(user_data)
            
            #calculate wallet worth 
            asset_value_total = 0
            for  t in user_data.index:
                asset_value_total = asset_value_total +  user_data["quantity"][i] * user_data["value"][i]
  

            for i in user_data.index:
                st.markdown(f'<img src="https://xchain.io/icon/{user_data["asset"][i]}.png"></img> Asset: {user_data["asset"][i]} | Amount: {user_data["quantity"][i]} | Value: {user_data["value"][i]}$', unsafe_allow_html=True)
            
            for i in range(0,5):
                st.markdown("<br><br>", unsafe_allow_html=True)
                
            st.markdown(f'Total asset value: {asset_value_total}$', unsafe_allow_html=True)
           
        except:

            st.markdown("Invalid Wallet")

    else:

        st.markdown("No address")





    


    


