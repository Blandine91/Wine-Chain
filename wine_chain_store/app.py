from email import header
import os
import json
from turtle import width
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from st_clickable_images import clickable_images
import pandas as pd
from dataclasses import dataclass
from typing import Any, List
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json


load_dotenv()


w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))




@st.cache(allow_output_mutation=True)
def load_contract():

    
    with open(Path('./contracts/compiled/artregistry_abi.json')) as f:
        contract_abi = json.load(f)

    
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

   
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract



contract = load_contract()




def pin_artwork(artwork_name, artwork_file):
   
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

   
    token_json = {
        "name": artwork_name,
        "area_code": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

   
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash



image = Image.open('WINECHAIN.png')


st.image(image, caption='WineChain')
st.title("WINE-CHAIN")



video_file = open('winevid.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

clicked = clickable_images(
    [
        "https://aem.lcbo.com/content/dam/lcbo/products/2/2/2/8/222877.jpg.thumb.319.319.png",
        "https://aem.lcbo.com/content/dam/lcbo/products/7/1/0/4/710426.jpg.thumb.319.319.png",
        "https://aem.lcbo.com/content/dam/lcbo/products/7/0/8/9/708982.jpg.thumb.319.319.png",
        "https://aem.lcbo.com/content/dam/lcbo/products/6/4/6/1/646190.jpg.thumb.319.319.png",
        "https://aem.lcbo.com/content/dam/lcbo/products/6/2/8/5/628511.jpg.thumb.319.319.png",
        "https://aem.lcbo.com/content/dam/lcbo/products/6/5/6/5/656561.jpg.thumb.1280.1280.jpg",
    ],
    titles=[f"Image #{str(i)}" for i in range(6)],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "300px"},
)
st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "Clicked an Image")

from crypto_wallet import generate_account, get_balance, send_transaction 


wine_database = {
    "CAYMUS": [
        "CAYMUS",
        "0x47671F98549635cacf0bA7A396Cb11574AFd0aCf",
        "91",
        0.20,
    ],
    "CAKEBREAD": [
        "CAKEBREAD",
        "0x47671F98549635cacf0bA7A396Cb11574AFd0aCf",
        "93",
        0.33,
    ],
    "J.Lohr": [
        "J.Lohr",
        "0x47671F98549635cacf0bA7A396Cb11574AFd0aCf",
        "92",
        0.19,
    ],
    "Gott": [
        "Gott",
        "0x47671F98549635cacf0bA7A396Cb11574AFd0aCf",
        "91.5",
        0.20,
    ],
    "Artemis": [
        "Artemis",
        "0x47671F98549635cacf0bA7A396Cb11574AFd0aCf",
        "94",
        0.33,

    ]
  
}


wines = ["CAYMUS", "CAKEBREAD", "J.Lohr","Gott","Artemis"]


def get_wine():
    """Display the database of KryptoJobs2Go candidate information."""
    db_list = list(wine_database.values())

    for number in range(len(wines)):
        st.write("Wine: ", db_list[number][0])
        st.write("Ethereum Account Address: ", db_list[number][1])
        st.write("Wine Rating: ", db_list[number][2])
        st.write("Cost of Wine in Ether: ", db_list[number][3], "eth")
        st.text(" \n")




mnemonic = st.sidebar.text_input("Input mnemonic")
account = generate_account(mnemonic)


st.sidebar.write(account.address)


ether = get_balance(w3, account.address)

st.sidebar.markdown("## Purchase your wine here")







wine = st.sidebar.selectbox("Select a Wine", wines)

# Create a input field to record the number of hours the candidate worked
number_bottles = st.sidebar.number_input("Number of Bottle")

st.sidebar.header( " Wine Name, Price, and Ethereum Address")

# Identify the FinTech Hire candidate
wine_name = wine_database[wine][0]

# Write the KryptoJobs2Go candidate's name to the sidebar
st.sidebar.write(wine_name)

# Identify the KryptoJobs2Go candidate's hourly rate
cost_bottles = wine_database[wine][3]

# Write the inTech Finder candidate's hourly rate to the sidebar
st.sidebar.write(cost_bottles)

# Identify the KryptoJobs2Go candidate's Ethereum Address
wine_address = wine_database[wine][1]

# Write the inTech Finder candidate's Ethereum Address to the sidebar
st.sidebar.write(wine_address)

# Write the KryptoJobs2Go candidate's name to the sidebar

st.sidebar.markdown(" Total in Ether")


total = number_bottles * cost_bottles

# @TODO
# Write the `wage` calculation to the Streamlit sidebar
st.sidebar.write("Cost of Wine is", total)




if st.sidebar.button("Send Transaction"):

   
    transaction_hash = send_transaction(w3, account, wine_address, total)

    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()

# The function that starts the Streamlit application
# Writes KryptoJobs2Go candidates to the Streamlit page
get_wine()



################################################################################
# Client Register
################################################################################
st.markdown("## Client Register")
client_first_name = st.text_input("Enter Your First Name")
client_last_name = st.text_input("Enter Your Last Name")
client_address = st.text_input("Enter your Address")
client_area_code = st.text_input("Enter Your Area Code")

# Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.


if st.button("Register Address"):
   

  st.markdown("---")


