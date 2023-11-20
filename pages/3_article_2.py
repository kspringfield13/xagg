import requests, os, base64
import streamlit as st
from PIL import Image
from streamlit_extras.stoggle import stoggle
from streamlit_card import card
from streamlit_javascript import st_javascript
import streamlit.components.v1 as components

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="xAgg | Business", page_icon=":globe_with_meridians:", layout="wide", initial_sidebar_state="collapsed")

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" width="420" />
        </a>'''
    return html_code

tweet_html = get_img_with_href('images/1725569551490752556.png', 'https://twitter.com/SawyerMerritt/status/1725569551490752556')

# ---- LOAD ASSETS ----

st.title("SpaceX Launches Sleeker Starlink Terminal")
st.write("##")

left_column, right_column, pad_column = st.columns((10,4,2))

with left_column:

    st.write("##")
    st.markdown("""<div style="color: red;"><ul>
                <li style="font-size: 20px;">SpaceX Upgrades Starlink: The tweet announces SpaceX's introduction of a new, more portable design for their Starlink terminal.</li><br>
                <li style="font-size: 20px;">Enhanced Performance Features: The new terminal boasts a Gen 3 router with better range and speed, improved durability, and a simpler setup process.</li><br>
                <li style="font-size: 20px;">Significant User Engagement: The tweet has garnered significant attention, indicating high public interest in SpaceX's latest Starlink advancements.</li></ul></div>""", unsafe_allow_html=True)

    st.write("##")

    article = """
    SpaceX continues to push the boundaries of space technology and consumer hardware with the introduction of their next-generation Starlink terminal. Sawyer Merritt's recent tweet highlights the pivotal upgrades the aerospace manufacturer has implemented in this latest iteration. The advancements are not just a leap in technology but also showcase SpaceX's commitment to user-friendly design.

    The new Starlink terminal is described as slimmer and more portable, a significant improvement for users who prioritize mobility and space-saving technology. Furthermore, it incorporates a Gen 3 router with enhanced range and speeds, catering to the ever-increasing demand for fast and reliable internet connectivity, especially in remote areas previously underserved by traditional ISPs.

    One of the key features highlighted is the removal of motors from the design. This not only simplifies the physical setup with a "Simple kickstand" but likely contributes to increased durability and reduced maintenance needs. Additionally, the terminal now provides a 10% better field of view compared to the previous generation, which could translate to improved signal acquisition and stability.

    In terms of durability, the tweet notes an improved IP67 waterproof rating, ensuring the device's resilience in adverse weather conditions. This is complemented by the terminal's capability to operate in 60+ mph wind speeds, a step up from the previous threshold of 50+ mph.

    The engagement metrics of the tweet speak volumes about the public's interest. With 6.4 million views, over 20,000 likes, and more than 2,000 reposts, it's evident that the Starlink project continues to captivate the audience's imagination and interest. Such social media traction not only reflects the public's anticipation for new technology but also underscores the importance of internet connectivity as a utility.

    SpaceX's foray into satellite internet with Starlink has been closely watched by industry observers and consumers alike. While it's part of a broader vision to fund interplanetary travel, it also serves an immediate purpose: to provide high-speed internet across the globe, especially in areas where connectivity has been a challenge.

    In conclusion, the new Starlink terminal represents a synthesis of design and functionality that aligns with contemporary needs for portable and robust internet solutions. As SpaceX continues to innovate, the implications for global connectivity are profound, potentially transforming how we access and use the internet in our daily lives.
    """
    st.markdown(article, unsafe_allow_html=True)

with right_column:

    st.markdown(tweet_html, unsafe_allow_html=True)