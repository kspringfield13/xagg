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

tweet_html = get_img_with_href('images/1725415906128310775.png', 'https://twitter.com/jessica_kirsh/status/1725415906128310775')

# ---- LOAD ASSETS ----

st.title("SpaceX Embraces Extensive Testing Culture")
st.write("##")

left_column, right_column, pad_column = st.columns((10,4,2))

with left_column:

    st.write("##")
    st.markdown('<div style="color: red;"><ul><li style="font-size: 20px;">SpaceX test flights, including the upcoming Starship ITF2, are crucial for gathering valuable empirical data, with each launch being a step towards refining their spacecraft.</li><br><li style="font-size: 20px;">The companys iterative design and testing approach have been fundamental in normalizing space travel, as evidenced by the routine success of Falcon 9 launches.</li><br><li style="font-size: 20px;">SpaceX commitment to pushing the boundaries of space exploration is exemplified by their embrace of risk and transparency, inspiring innovation within the aerospace industry.</li></ul></div>', unsafe_allow_html=True)

    st.write("##")

    article = """
    The social media landscape is abuzz with anticipation and opinions as SpaceX gears up for the Starship Integrated Test Flight 2 (ITF2). A recent tweet by Jessica Kirsh highlights the significance of this event and the pioneering strides SpaceX has achieved in the aerospace domain, particularly in South Texas. Kirsh underscores the innovative essence of SpaceX’s methodology, which often swims against the tide of public and media skepticism.

    The tweet emphasizes that the upcoming Starship flight is not just a demonstration of technological prowess but a testament to SpaceX's commitment to iterative design and testing. It is a prototype vessel—despite its polished appearance suggesting otherwise—and each launch is a step towards refining the final product. Such an approach is instrumental in the aerospace sector, where empirical data gathered from actual test flights are invaluable, and cannot be replicated by simulations alone.

    Kirsh also touches on the normalized marvel of Falcon 9 launches, signifying SpaceX’s successful track record in revolutionizing space travel with rapidly reusable rockets. It’s a nod to the company’s established precision, accuracy, and methodological rigor, achieved through relentless testing and reiteration. This iterative process, as Kirsh points out, is the backbone of the Starship Integrated Flight Test Campaign, and is what fuels SpaceX’s ability to turn what once seemed impossible into reality.

    The tweet concludes with a poignant reminder: the most precise and useful data are obtained not while Starship is stationary, but when it faces the elemental forces post-lift-off. This is when the real test begins, as these conditions cannot be fully replicated on the ground. Kirsh’s final words resonate with the spirit of innovation—'Not trying' would be the greatest failure.

    SpaceX’s journey has been characterized by pushing boundaries and embracing the risk inherent in space exploration. This tweet by Jessica Kirsh encapsulates the essence of SpaceX’s mission: to relentlessly pursue progress, even in the face of doubt and criticism. It is this ethos that continues to propel them towards unprecedented milestones in spaceflight.

    In the context of the broader aerospace industry, SpaceX’s Starship program stands out not just for its ambition but also for its transparency and public engagement. By sharing each step of the journey, SpaceX is not only refining its own technologies but also inspiring a culture of openness and learning in a sector that has traditionally been shrouded in secrecy.
    """
    st.markdown(article, unsafe_allow_html=True)

with right_column:

    st.markdown(tweet_html, unsafe_allow_html=True)