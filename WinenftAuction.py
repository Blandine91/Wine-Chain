# Imports
import os
import json
import requests
from eth_account import account
from eth_typing import abi
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from dataclasses import dataclass
from typing import Any, List


load_dotenv("s.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper functions:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path("compiled_contract.json")) as f:
        auction_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=auction_abi
    )

    return contract

# Load the contract

contract = load_contract()

################################################################################
# Helper functions to pin files and json to Pinata
################################################################################

def pin_wine(wine_name, wine_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfswine_file.getvalue()
    
    # Build a token metadata file for the wine NFT
    token_json = {
        "name": wine_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata

    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, token_json


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash

################################################################################
# View the NFT
################################################################################

wine_database = {
    "CAYMUS": [
        "CAYMUS",
        "0x656D5887c3BBafdee31B2FA6AB95B6653A51e091",
        "91",
        0.20,
    ],
    "CAKEBREAD": [
        "CAKEBREAD",
        "0x656D5887c3BBafdee31B2FA6AB95B6653A51e091",
        "93",
        0.33,
    ],
    "JAYLORE": [
        "JAYLORE",
        "0x656D5887c3BBafdee31B2FA6AB95B6653A51e091",
        "92",
        0.19,
    ],
  
}

wines = ["CAYMUS", "CAKEBREAD", "JAYLORE"]

def get_wine():
    """Display the database of KryptoJobs2Go candidate information."""
    db_list = list(wine_database.values())

    for number in range(len(wines)):
        st.write("Wine: ", db_list[number][0])
        st.write("Ethereum Account Address: ", db_list[number][1])
        st.write("Wine Rating: ", db_list[number][2])
        st.write("Cost of Wine in Ether: ", db_list[number][3], "eth")
        st.text(" \n")


################################################################################
# Streamlit code
################################################################################

# Streamlit application headings
st.markdown("# Wine NFT Auction House!")
st.markdown("## Bid For Your Favourite Wine NFT!")
st.text(" \n")

# Streamlit Sidebar Code - Start
get_wine()

st.sidebar.markdown("## Client Account Address and Ethernet Balance in Ether")

accounts = w3.eth.accounts
address = st.sidebar.selectbox("Select Account", options=accounts)


# Write the client's Ethereum account address to the sidebar
st.sidebar.write()

# Create a select box to chose a wine to bid on
wine = st.sidebar.selectbox('Select Wine NFT', wines)

# Create a input field to record the initial bid
starting_bid = st.sidebar.number_input("Bid")

# Identify the wine for auction
wine = wine_database[wine][0]

# Write the wine's name to the sidebar
st.sidebar.markdown("## Wine NFT Name")
st.sidebar.write(wine)

# Identify the the starting bid for the wine being auctioned
st.sidebar.markdown("## Minimum Bid")
starting_bid = wine_database[wine][3]

# Write the wines starting bid
st.sidebar.write(starting_bid)

# Identify the auction owner's Ethereum Address
st.sidebar.markdown("## Account Address")
wine_address = wine_database[wine][1]

# Write the auction owner's Ethereum Address to the sidebar
st.sidebar.write(wine_address)

if st.sidebar.button("Place Bid"):
    
    #st.write(accounts)
    
    tx_hash = contract.functions.bid().transact({'from': accounts[1], 'gas': 300000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
 
if st.sidebar.button("Withdraw"):
    tx_hash = contract.functions.withdraw()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

if st.sidebar.button("End Auction"):
    tx_hash = contract.functions.auctionend()
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

st.sidebar.markdown("## Highest Bid in Ether")

## Additional code apart from BID, to showcase proof of transaction
purchase_price = starting_bid

# Write the `total purchase` calculation to the Streamlit sidebar
st.sidebar.write(purchase_price)


if st.sidebar.button("Send Transaction"):

    # Call the `send_transaction` function and pass it 3 parameters:
    # Your `account`, the `wine_address`, and the `purchase_price` as parameters
    # Save the returned transaction hash as a variable named `transaction_hash`
    transaction_hash = send_transaction(w3, accounts, wine_address, purchase_price)

    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()