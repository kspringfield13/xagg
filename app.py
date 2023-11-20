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

def get_nasdaq_ticker():
    # Fetch data for the NASDAQ
    nasdaq = yf.Ticker("^IXIC")
    nasdaq_data = nasdaq.history(period="1d")

    # Get the latest data point
    latest_data = nasdaq_data.iloc[-1]
    price = latest_data['Close']
    change = price - latest_data['Open']
    change_percent = (change / latest_data['Open']) * 100

    # Determine the sign of the change
    change_sign = 0
    if change_percent < 0:
        change_sign = -1
    elif change_percent > 0:
        change_sign = 1

    nasdaq_values = ['NASDAQ', float(price), float(change_percent), change_sign]

    return nasdaq_values

def get_dow_ticker():
    # Fetch data for the Dow Jones
    dow = yf.Ticker("^DJI")
    dow_data = dow.history(period="1d")

    # Get the latest data point
    latest_data = dow_data.iloc[-1]
    price = latest_data['Close']
    change = price - latest_data['Open']
    change_percent = (change / latest_data['Open']) * 100

    # Determine the sign of the change
    change_sign = 0
    if change_percent < 0:
        change_sign = -1
    elif change_percent > 0:
        change_sign = 1

    dow_values = ['DJIA', float(price), float(change_percent), change_sign]

    return dow_values


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

with open("images/banner.png", "rb") as f:
    data = f.read()
    encoded = base64.b64encode(data)
banner = "data:image/png;base64," + encoded.decode("utf-8")

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

    # st.markdown('<h1 style="color: purple;">Suzieq</h1>',unsafe_allow_html=True)
    
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
            st.markdown(f'<div style="text-align: left; color: white; font-weight: bold; font-size: 16px;">{name}</div>', unsafe_allow_html=True)
            
        with trc:
            st.markdown(f'<div style="text-align: right; color: white; font-weight: bold; font-size: 16px;">{price:,.2f}</div>', unsafe_allow_html=True)

        tlc_2, trc_2 = st.columns((5,5),gap="small")
        with tlc_2:
            st.markdown(f'<div style="text-align: left; color: {color}; font-weight: bold; font-size: 16px;">{arrow}</div>', unsafe_allow_html=True)
            
        with trc_2:
            st.markdown(f'<div style="text-align: right; color: {color}; font-weight: bold; font-size: 16px;">{abs(change_percent):.2f}%</div>', unsafe_allow_html=True)

    st.markdown(
    """
    <style>
        div.st-emotion-cache-1l269bu:nth-child(2) > div:nth-child(1) > div:nth-child(1) {
            background: #1a1919; 
            border-radius: 10px 10px 10px 10px;
            padding: 5px 8px 5px 8px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

with t_column:
    
    # NASDAQ
    nasdaq_values = get_nasdaq_ticker()
    name, price, change_percent, sign = nasdaq_values

    # Define the arrow symbol based on the sign of the change
    arrow = "▲" if sign == 1 else "▼" if sign == -1 else ""

    # Define the color based on the sign of the change
    color = "#27ae60" if sign == 1 else "#c0392b" if sign == -1 else "#34495e"

    with st.container():

        tlc, trc = st.columns((5,5),gap="small")
        with tlc:
            st.markdown(f'<div style="text-align: left; color: white; font-weight: bold; font-size: 16px;">{name}</div>', unsafe_allow_html=True)
            
        with trc:
            st.markdown(f'<div style="text-align: right; color: white; font-weight: bold; font-size: 16px;">{price:,.2f}</div>', unsafe_allow_html=True)

        tlc_2, trc_2 = st.columns((5,5),gap="small")
        with tlc_2:
            st.markdown(f'<div style="text-align: left; color: {color}; font-weight: bold; font-size: 16px;">{arrow}</div>', unsafe_allow_html=True)
            
        with trc_2:
            st.markdown(f'<div style="text-align: right; color: {color}; font-weight: bold; font-size: 16px;">{abs(change_percent):.2f}%</div>', unsafe_allow_html=True)

    st.markdown(
    """
    <style>
        div.st-emotion-cache-1l269bu:nth-child(3) > div:nth-child(1) > div:nth-child(1) {
            background: #1a1919; 
            border-radius: 10px 10px 10px 10px;
            padding: 5px 8px 5px 8px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

with fr_column:
    
    # DOW
    dow_values = get_dow_ticker()
    name, price, change_percent, sign = dow_values

    # Define the arrow symbol based on the sign of the change
    arrow = "▲" if sign == 1 else "▼" if sign == -1 else ""

    # Define the color based on the sign of the change
    color = "#27ae60" if sign == 1 else "#c0392b" if sign == -1 else "#34495e"

    with st.container():

        tlc, trc = st.columns((5,5),gap="small")
        with tlc:
            st.markdown(f'<div style="text-align: left; color: white; font-weight: bold; font-size: 16px;">{name}</div>', unsafe_allow_html=True)
            
        with trc:
            st.markdown(f'<div style="text-align: right; color: white; font-weight: bold; font-size: 16px;">{price:,.2f}</div>', unsafe_allow_html=True)

        tlc_2, trc_2 = st.columns((5,5),gap="small")
        with tlc_2:
            st.markdown(f'<div style="text-align: left; color: {color}; font-weight: bold; font-size: 16px;">{arrow}</div>', unsafe_allow_html=True)
            
        with trc_2:
            st.markdown(f'<div style="text-align: right; color: {color}; font-weight: bold; font-size: 16px;">{abs(change_percent):.2f}%</div>', unsafe_allow_html=True)

    st.markdown(
    """
    <style>
        div.st-emotion-cache-1l269bu:nth-child(4) > div:nth-child(1) > div:nth-child(1) {
            background: #1a1919; 
            border-radius: 10px 10px 10px 10px;
            padding: 5px 8px 5px 8px;
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
business, finance, tech= st.tabs(["Business", "Finance", "Tech"])

with business:
   
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

with finance:

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

with tech:

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