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

tweet_html = get_img_with_href('images/1725598245404197360.png', 'https://twitter.com/imPenny2x/status/1725598245404197360')

# ---- LOAD ASSETS ----

st.title("Elon Musk: Asset or Liability?")
st.write("##")

left_column, right_column, pad_column = st.columns((10,4,2))

with left_column:

    st.write("##")
    st.markdown("""<div style="color: red;"><ul>
                <li style="font-size: 20px;">Tweet defends Elon Musk's value as a national security asset.</li><br>
                <li style="font-size: 20px;">Criticism of the White House's stance on Musk's alleged remarks.</li><br>
                <li style="font-size: 20px;">Highlights tension between government and tech leaders.</li></ul></div>""", unsafe_allow_html=True)

    st.write("##")

    article = """
    In a digital age where social media becomes the battleground for public opinion, a recent tweet by user @imPenny2x has surfaced, stirring a significant conversation around Elon Musk's role in national security and his relationship with the government. The tweet comes in response to an article by The New York Times, detailing the White House's condemnation of Elon Musk for alleged 'Antisemitic and Racist Hate.'

    The user comes to Musk's defense, asserting his irreplaceability and value as a national security asset, referring to SpaceX's contributions to space exploration and Tesla's advancements in manufacturing. The tweet suggests that Musk's enterprises are integral to the nation's technological and security capabilities, and thus, alienating him could have adverse effects on the country's global standing.

    The tweet goes further to criticize the current administration, accusing it of self-destructive behavior by creating an antagonist out of a potential ally in Musk. It implies a disconnect between the government's actions and the best interests of the nation, pointing to a power struggle that overlooks the larger picture of national security and progress.

    However, the engagement stats on the tweet reveal a divided audience. With a relatively modest number of likes and shares, it suggests that while the sentiment has resonance, it may not be the majority view. The use of terms like "morons" to describe government officials may undermine the user's argument, indicating a more emotional response rather than a constructive critique.

    In the context of recent history, Elon Musk has been a polarizing figure, known for his significant contributions to technology and space travel, as well as his controversial statements and actions. The White House's response to Musk's behavior, as reported, reflects an ongoing debate about the extent to which private individuals' statements, particularly those in positions of considerable influence, impact public sentiment and policy.

    The article in question, not directly accessible from the tweet, could provide more context to the White House's stance. Without it, the tweet's audience is left with a one-sided argument. This underscores the importance of full context in public discourse, especially when involving influential figures and national policy.

    In conclusion, the tweet from @imPenny2x opens a window into the complex interplay between government and private sector leaders in the realm of national security and public policy. While it defends Elon Musk's importance to national interests, it also challenges the government's approach to managing relationships with such entities. The debate is likely to continue as the boundaries between private innovation and public interest become increasingly intertwined.
    """
    st.markdown(article, unsafe_allow_html=True)

with right_column:

    st.markdown(tweet_html, unsafe_allow_html=True)