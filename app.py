import requests, os, base64, jsonify
import streamlit as st
from PIL import Image
from streamlit_card import card
from streamlit_javascript import st_javascript
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import sqlite3
from sqlite3 import Error
import yfinance as yf
import streamlit.components.v1 as components

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="xAgg", page_icon=":globe_with_meridians:", layout="wide", initial_sidebar_state="collapsed")

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to get headlines and URLs from the database
def get_headlines_and_urls(path='articles.db', timeout=5):
    data = []
    try:
        with sqlite3.connect(path, timeout=timeout) as conn:
            cur = conn.cursor()
            cur.execute("SELECT headline, url FROM articles ORDER BY published_date DESC LIMIT 10")
            data = cur.fetchall()
    except Error as e:
        st.error(f"Error connecting to or querying the database: {e}")
    return data

def get_sp500_ticker():
    # Fetch data for the S&P 500 index
    sp500 = yf.Ticker("^GSPC")
    sp500_data = sp500.history(period="1d")

    # Get the latest data point
    latest_data = sp500_data.iloc[-1]
    price = latest_data['Close']
    change = price - latest_data['Open']
    change_percent = (change / latest_data['Open']) * 100

    # Determine the sign of the change
    change_sign = 0
    if change_percent < 0:
        change_sign = -1
    elif change_percent > 0:
        change_sign = 1

    sp500_values = ['S & P 500', float(price), float(change_percent), change_sign]

    return sp500_values

def get_bitcoin_data(api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    parameters = {
        'start': '1',
        'limit': '1',
        'convert': 'USD'
    }
    
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    # Assuming Bitcoin is the first in the list
    bitcoin_data = data['data'][0]
    price = float(bitcoin_data['quote']['USD']['price'])
    change_percent = float(bitcoin_data['quote']['USD']['percent_change_24h'])
    
    # Determine the sign of the change
    change_sign = 0
    if change_percent > 0:
        change_sign = 1
    elif change_percent < 0:
        change_sign = -1
    
    return ['Bitcoin', float(price), float(change_percent), change_sign]

def get_ethereum_data(api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    parameters = {
        'start': '1',
        'limit': '2',
        'convert': 'USD'
    }
    
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    # Assuming Bitcoin is the first in the list
    bitcoin_data = data['data'][1]
    price = float(bitcoin_data['quote']['USD']['price'])
    change_percent = float(bitcoin_data['quote']['USD']['percent_change_24h'])
    
    # Determine the sign of the change
    change_sign = 0
    if change_percent > 0:
        change_sign = 1
    elif change_percent < 0:
        change_sign = -1
    
    return ['Ethereum', float(price), float(change_percent), change_sign]

key = 'cd2698aa-18bc-4c59-bb6d-73bfdc540887'

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

local_css("style/style.css")

# ---- LOAD ASSETS ----
with open("images/spacexrocket.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
a_1 = "data:image/png;base64," + encoded.decode("utf-8")

with open("images/sat.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
a_2 = "data:image/png;base64," + encoded.decode("utf-8")

with open("images/elon.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
a_3 = "data:image/png;base64," + encoded.decode("utf-8")

with open("images/logo.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
logo = "data:image/png;base64," + encoded.decode("utf-8")

cur_url = st_javascript("await fetch('').then(r => window.parent.location.href)")

# ---- HEADER SECTION ----
st.markdown(
    """
        <style>
            .appview-container .main .block-container {{
                padding-top: {padding_top}rem;
                padding-bottom: {padding_bottom}rem;
                gap: 0rem;
                }}

        </style>""".format(
        padding_top=0, padding_bottom=0
    ),
    unsafe_allow_html=True,
)

st.markdown(
    """
        <style>
            .element-container.st-emotion-cache-gc25js.e1f1d6gn3 {{
                padding-top: {padding_top}rem;
                padding-bottom: {padding_bottom}rem;
                gap: 0rem;
                height: 0px;
                }}

        </style>""".format(
        padding_top=0, padding_bottom=0
    ),
    unsafe_allow_html=True,
)

f_column, s_column, t_column, fr_column = st.columns((4.5,1.5,1.5,1.5))

with f_column:

    st.image(logo, width=120)
    st.markdown(
    """
    
    <style>
        @media screen and (max-width:640px) {
            div.st-emotion-cache-1kyxreq.e115fcil2 {
                width: 150px !important;
            }
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

with s_column:

    #S & P 500
    sp500_values = get_sp500_ticker()
    name, price, change_percent, sign = sp500_values

    # Define the arrow symbol based on the sign of the change
    arrow = "▲" if sign == 1 else "▼" if sign == -1 else ""

    # Define the color based on the sign of the change
    color = "#27ae60" if sign == 1 else "#c0392b" if sign == -1 else "#34495e"

    with st.container():

        tlc, trc = st.columns((5,5),gap="small")
        with tlc:
            render_svg("""<svg xmlns="http://www.w3.org/2000/svg" height="32" width="32"><path d="M16 32C7.163 32 0 24.837 0 16S7.163 0 16 0s16 7.163 16 16-7.163 16-16 16zm6.5-12.846c0-2.523-1.576-3.948-5.263-4.836v-4.44c1.14.234 2.231.725 3.298 1.496l1.359-2.196a9.49 9.49 0 00-4.56-1.776V6h-2.11v1.355c-3.032.234-5.093 1.963-5.093 4.486 0 2.64 1.649 3.925 5.19 4.813v4.58c-1.577-.234-2.886-.935-4.269-2.01L9.5 21.35a11.495 11.495 0 005.724 2.314V26h2.11v-2.313c3.08-.257 5.166-1.963 5.166-4.533zm-7.18-5.327c-1.867-.537-2.327-1.168-2.327-2.15 0-1.027.8-1.845 2.328-1.962zm4.318 5.49c0 1.122-.873 1.893-2.401 2.01v-4.229c1.892.538 2.401 1.168 2.401 2.22z" fill="#fff" fill-rule="evenodd"/></svg>""")
            
        with trc:
            st.markdown(f'<div style="text-align: right; color: white; font-size: 16px;">{name}</div>', unsafe_allow_html=True)

        tlc_2, trc_2 = st.columns((5,5),gap="small")
        with tlc_2:
            st.markdown(f'<div style="text-align: left; color: white; font-weight: bold; font-size: 16px;">${price:,.2f}</div>', unsafe_allow_html=True)
            
        with trc_2:
            st.markdown(f'<div style="text-align: right; color: {color}; font-weight: bold; font-size: 16px;">{abs(change_percent):.2f}%  {arrow}</div>', unsafe_allow_html=True)

    st.markdown(
    """
    <style>
        div.st-emotion-cache-1l269bu:nth-child(2) > div:nth-child(1) > div:nth-child(1) {
            background: #1a1919; 
            border-radius: 10px 10px 10px 10px;
            padding: 8px 10px 5px 10px;
        }

        @media screen and (max-width:640px) {
            div.st-emotion-cache-1l269bu:nth-child(2) > div:nth-child(1) > div:nth-child(1) {
                width: 100%;
                line-height: 0px;
            }
        }

        @media screen and (max-width:640px) {
            div.st-emotion-cache-nahz7x.e1nzilvr5:nth-child(1) {
                float: inherit;
            }
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

with t_column:
    
    # Bitcoin
    bitcoin_values = get_bitcoin_data(key)
    name, price, change_percent, sign = bitcoin_values

    # Define the arrow symbol based on the sign of the change
    arrow = "▲" if sign == 1 else "▼" if sign == -1 else ""

    # Define the color based on the sign of the change
    color = "#27ae60" if sign == 1 else "#c0392b" if sign == -1 else "#34495e"

    with st.container():

        tlc, trc = st.columns((5,5),gap="small")
        with tlc:
            render_svg("""<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"><g fill="none" fill-rule="evenodd"><circle cx="16" cy="16" r="16" fill="#F7931A"/><path fill="#FFF" fill-rule="nonzero" d="M23.189 14.02c.314-2.096-1.283-3.223-3.465-3.975l.708-2.84-1.728-.43-.69 2.765c-.454-.114-.92-.22-1.385-.326l.695-2.783L15.596 6l-.708 2.839c-.376-.086-.746-.17-1.104-.26l.002-.009-2.384-.595-.46 1.846s1.283.294 1.256.312c.7.175.826.638.805 1.006l-.806 3.235c.048.012.11.03.18.057l-.183-.045-1.13 4.532c-.086.212-.303.531-.793.41.018.025-1.256-.313-1.256-.313l-.858 1.978 2.25.561c.418.105.828.215 1.231.318l-.715 2.872 1.727.43.708-2.84c.472.127.93.245 1.378.357l-.706 2.828 1.728.43.715-2.866c2.948.558 5.164.333 6.097-2.333.752-2.146-.037-3.385-1.588-4.192 1.13-.26 1.98-1.003 2.207-2.538zm-3.95 5.538c-.533 2.147-4.148.986-5.32.695l.95-3.805c1.172.293 4.929.872 4.37 3.11zm.535-5.569c-.487 1.953-3.495.96-4.47.717l.86-3.45c.975.243 4.118.696 3.61 2.733z"/></g></svg>""")

        with trc:
            st.markdown(f'<div style="text-align: right; color: white; font-size: 16px;">{name}</div>', unsafe_allow_html=True)

        tlc_2, trc_2 = st.columns((5,5),gap="small")
        with tlc_2:
            st.markdown(f'<div style="text-align: left; color: white; font-weight: bold; font-size: 16px;">${price:,.2f}</div>', unsafe_allow_html=True)
            
        with trc_2:
            st.markdown(f'<div style="text-align: right; color: {color}; font-weight: bold; font-size: 16px;">{abs(change_percent):.2f}%  {arrow}</div>', unsafe_allow_html=True)

    st.markdown(
    """
    <style>
        div.st-emotion-cache-1l269bu:nth-child(3) > div:nth-child(1) > div:nth-child(1) {
            background: #1a1919; 
            border-radius: 10px 10px 10px 10px;
            padding: 8px 10px 5px 10px;
        }

        @media screen and (max-width:640px) {
            div.st-emotion-cache-1l269bu:nth-child(3) > div:nth-child(1) > div:nth-child(1) {
                width: 100%;
                line-height: 0px;
            }
        }

        @media screen and (max-width:640px) {
            div.st-emotion-cache-1wmy9hl.e1f1d6gn0:nth-child(3) {
            }
        }

    </style>
    """,
        unsafe_allow_html=True,
    )

with fr_column:
    
    # Ethereum
    ethereum_values = get_ethereum_data(key)
    name, price, change_percent, sign = ethereum_values

    # Define the arrow symbol based on the sign of the change
    arrow = "▲" if sign == 1 else "▼" if sign == -1 else ""

    # Define the color based on the sign of the change
    color = "#27ae60" if sign == 1 else "#c0392b" if sign == -1 else "#34495e"

    with st.container():

        tlc, trc = st.columns((5,5),gap="small")
        with tlc:
            render_svg("""<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"><g fill="none" fill-rule="evenodd"><circle cx="16" cy="16" r="16" fill="#627EEA"/><g fill="#FFF" fill-rule="nonzero"><path fill-opacity=".602" d="M16.498 4v8.87l7.497 3.35z"/><path d="M16.498 4L9 16.22l7.498-3.35z"/><path fill-opacity=".602" d="M16.498 21.968v6.027L24 17.616z"/><path d="M16.498 27.995v-6.028L9 17.616z"/><path fill-opacity=".2" d="M16.498 20.573l7.497-4.353-7.497-3.348z"/><path fill-opacity=".602" d="M9 16.22l7.498 4.353v-7.701z"/></g></g></svg>""")
            
        with trc:
            st.markdown(f'<div style="text-align: right; color: white; font-size: 16px;">{name}</div>', unsafe_allow_html=True)

        tlc_2, trc_2 = st.columns((5,5),gap="small")
        with tlc_2:
            st.markdown(f'<div style="text-align: left; color: white; font-weight: bold; font-size: 16px;">${price:,.2f}</div>', unsafe_allow_html=True)
            
        with trc_2:
            st.markdown(f'<div style="text-align: right; color: {color}; font-weight: bold; font-size: 16px;">{abs(change_percent):.2f}%  {arrow}</div>', unsafe_allow_html=True)

    st.markdown(
    """
    <style>
        div.st-emotion-cache-1l269bu:nth-child(4) > div:nth-child(1) > div:nth-child(1) {
            background: #1a1919; 
            border-radius: 10px 10px 10px 10px;
            padding: 8px 10px 5px 10px;
        }

        @media screen and (max-width:640px) {
            div.st-emotion-cache-1l269bu:nth-child(4) > div:nth-child(1) > div:nth-child(1) {
                width: 100%;
                line-height: 0px;
            }
        }

        @media screen and (max-width:640px) {
            div.st-emotion-cache-1wmy9hl.e1f1d6gn0:nth-child(4) {
            }
        }

    </style>
    """,
        unsafe_allow_html=True,
    )

st.write("##")
st.write("##")

# FEATURED STORIES

left_column, middle_column, right_column = st.columns(3, gap="small")
with left_column:
    
    with st.container():
        lc, rc = st.columns((5,5),gap="small")
        with lc:

            card(
                title="",
                text="",
                image=a_1,
                styles={
                    "card": {
                        "width": "188px",
                        "height": "188px",
                        "border-radius": "20px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                        "margin": "2px 2px",
                        "padding-bottom": "0px",
                    }
                },
                url=f'{cur_url}article_1',
                on_click=lambda: print("Clicked!")
                )
            
        with rc:
            
            st.markdown(f'<div style="color: #ed4b28; font-size: 12px;">Tech</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 18px;"><a href="{cur_url}article_1" style="color:#ffffff;">SpaceX Embraces Extensive Testing Culture</a></div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; color: #b4b5b8; font-size: 14px;">SpaceX continues to push the boundaries of space technology and consumer hardware with the introduction of their next-generation Starlink terminal.</div>', unsafe_allow_html=True)

    with st.container():

        lc_2, rc_2 = st.columns((5,5),gap="small")
        with lc_2:

            card(
                title="",
                text="",
                image=a_2,
                styles={
                    "card": {
                        "width": "188px",
                        "height": "188px",
                        "border-radius": "20px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                        "margin": "2px 2px",
                        "padding-bottom": "0px",
                    }
                },
                url=f'{cur_url}article_4',
                on_click=lambda: print("Clicked!")
                )
            
        with rc_2:
            
            st.markdown(f'<div style="color: #ed4b28; font-size: 12px;">Finance</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 18px;"><a href="{cur_url}article_4" style="color:#ffffff;">Rohan Enterprises Capitulates Their Short Hedge Funds</a></div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; color: #b4b5b8; font-size: 14px;">SpaceX continues to push the boundaries of space technology and consumer hardware with the introduction of their next-generation Starlink terminal.</div>', unsafe_allow_html=True)            

with middle_column:
    
    with st.container():
        mlc, mrc = st.columns((5,5),gap="small")
        with mlc:

            card(
                title="",
                text="",
                image=a_2,
                styles={
                    "card": {
                        "width": "188px",
                        "height": "188px",
                        "border-radius": "20px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                        "margin": "2px 2px",
                        "padding-bottom": "0px",
                    }
                },
                url=f'{cur_url}article_2',
                on_click=lambda: print("Clicked!")
                )
            
        with mrc:
            
            st.markdown(f'<div style="color: #ed4b28; font-size: 12px;">Tech</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 18px;"><a href="{cur_url}article_2" style="color:#ffffff;">SpaceX Launches Sleeker Starlink Terminal</a></div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; color: #b4b5b8; font-size: 14px;">SpaceX continues to push the boundaries of space technology and consumer hardware with the introduction of their next-generation Starlink terminal.</div>', unsafe_allow_html=True)

    with st.container():

        mlc_2, mrc_2 = st.columns((5,5),gap="small")
        with mlc_2:

            card(
                title="",
                text="",
                image=a_1,
                styles={
                    "card": {
                        "width": "188px",
                        "height": "188px",
                        "border-radius": "20px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                        "margin": "2px 2px",
                        "padding-bottom": "0px",
                    }
                },
                url=f'{cur_url}article_5',
                on_click=lambda: print("Clicked!")
                )
            
        with mrc_2:
            
            st.markdown(f'<div style="color: #ed4b28; font-size: 12px;">Tech</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 18px;"><a href="{cur_url}article_5" style="color:#ffffff;">Gang Violence! Wins in Spectabular Come From Behind Fantasy Battle</a></div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; color: #b4b5b8; font-size: 14px;">SpaceX continues to push the boundaries of space technology and consumer hardware with the introduction of their next-generation Starlink terminal.</div>', unsafe_allow_html=True)


with right_column:
    
    with st.container():

        rlc, rrc = st.columns((5,5),gap="small")
        with rlc:

            card(
                title="",
                text="",
                image=a_3,
                styles={
                    "card": {
                        "width": "188px",
                        "height": "188px",
                        "border-radius": "20px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                        "margin": "2px 2px",
                        "padding-bottom": "0px",
                    }
                },
                url=f'{cur_url}article_3',
                on_click=lambda: print("Clicked!")
                )
            
        with rrc:
            
            st.markdown(f'<div style="color: #ed4b28; font-size: 12px;">Business</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 18px;"><a href="{cur_url}article_3" style="color:#ffffff;">Elon Musk: Asset or Liability?</a></div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; color: #b4b5b8; font-size: 14px;">In a digital age where social media becomes the battleground for public opinion, a recent tweet by user @imPenny2x has surfaced...</div>', unsafe_allow_html=True)

    with st.container():

        rlc_2, rrc_2 = st.columns((5,5),gap="small")
        with rlc_2:

            card(
                title="",
                text="",
                image=a_2,
                styles={
                    "card": {
                        "width": "188px",
                        "height": "188px",
                        "border-radius": "20px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.5)",
                        "margin": "2px 2px",
                        "padding-bottom": "0px",
                    }
                },
                url=f'{cur_url}article_6',
                on_click=lambda: print("Clicked!")
                )
            
        with rrc_2:
            
            st.markdown(f'<div style="color: #ed4b28; font-size: 12px;">Finance</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; font-weight: bold; font-size: 18px;"><a href="{cur_url}article_6" style="color:#ffffff;">Stock Market Rally Seems to Never End</a></div>', unsafe_allow_html=True)

            st.markdown(f'<div style="text-align: left; color: #b4b5b8; font-size: 14px;">In a digital age where social media becomes the battleground for public opinion, a recent tweet by user @imPenny2x has surfaced...</div>', unsafe_allow_html=True)


st.write("##")

# TABS
headlines, memes, financials = st.tabs(["Headlines", "Memes", "Financials"])

with headlines:
   
    with st.container():

        st.markdown(
            """
            <style>
                div[data-testid="column"]:nth-of-type(1)
                {
                    text-align: justify,
                } 

                div[data-testid="column"]:nth-of-type(2)
                {
                    text-align: justify;
                } 

                div[data-testid="column"]:nth-of-type(3)
                {
                    text-align: justify;
                } 
            </style>
            """,unsafe_allow_html=True
        )

        left_column, middle_column, right_column = st.columns(3, gap="medium")
        with left_column:

            # Get headlines and URLs from the database
            business_left_headlines = get_headlines_and_urls()

            if business_left_headlines:
                for business_left_headline, business_left_url in business_left_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{business_left_headline}]({business_left_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline

        with middle_column:
            
            # Get headlines and URLs from the database
            business_middle_headlines = get_headlines_and_urls()

            if business_middle_headlines:
                for business_middle_headline, business_middle_url in business_middle_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{business_middle_headline}]({business_middle_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline

        with right_column:

            # Get headlines and URLs from the database
            business_right_headlines = get_headlines_and_urls()

            if business_right_headlines:
                for business_right_headline, business_right_url in business_right_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{business_right_headline}]({business_right_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline

with memes:

    with st.container():

        st.markdown(
            """
            <style>
                div[data-testid="column"]:nth-of-type(1)
                {
                    text-align: justify,
                } 

                div[data-testid="column"]:nth-of-type(2)
                {
                    text-align: justify;
                } 

                div[data-testid="column"]:nth-of-type(3)
                {
                    text-align: justify;
                } 
            </style>
            """,unsafe_allow_html=True
        )

        left_column, middle_column, right_column = st.columns(3, gap="medium")
        with left_column:
            
            # Get headlines and URLs from the database
            finance_left_headlines = get_headlines_and_urls()

            if finance_left_headlines:
                for finance_left_headline, finance_left_url in finance_left_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{finance_left_headline}]({finance_left_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline

        with middle_column:
            
            # Get headlines and URLs from the database
            finance_middle_headlines = get_headlines_and_urls()

            if finance_middle_headlines:
                for finance_middle_headline, finance_middle_url in finance_middle_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{finance_middle_headline}]({finance_middle_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline

        with right_column:

            # Get headlines and URLs from the database
            finance_right_headlines = get_headlines_and_urls()

            if finance_right_headlines:
                for finance_right_headline, finance_right_url in finance_right_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{finance_right_headline}]({finance_right_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline

with financials:

    with st.container():

        st.markdown(
            """
            <style>
                div[data-testid="column"]:nth-of-type(1)
                {
                    text-align: justify,
                } 

                div[data-testid="column"]:nth-of-type(2)
                {
                    text-align: justify;
                } 

                div[data-testid="column"]:nth-of-type(3)
                {
                    text-align: justify;
                } 
            </style>
            """,unsafe_allow_html=True
        )

        left_column, middle_column, right_column = st.columns(3, gap="medium")
        with left_column:
            
            # Get headlines and URLs from the database
            tech_left_headlines = get_headlines_and_urls()

            if tech_left_headlines:
                for tech_left_headline, tech_left_url in tech_left_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{tech_left_headline}]({tech_left_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline

        with middle_column:
            
            # Get headlines and URLs from the database
            tech_middle_headlines = get_headlines_and_urls()

            if tech_middle_headlines:
                for tech_middle_headline, tech_middle_url in tech_middle_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{tech_middle_headline}]({tech_middle_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline

        with right_column:

            # Get headlines and URLs from the database
            tech_right_headlines = get_headlines_and_urls()

            if tech_right_headlines:
                for tech_right_headline, tech_right_url in tech_right_headlines:
                    # The line below creates a hyperlink with the headline text pointing to the URL
                    st.markdown(f"[{tech_right_headline}]({tech_right_url})", unsafe_allow_html=True)
                    st.text("")  # Adds a line break after each headline