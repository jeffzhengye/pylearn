import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
# data = load_data(10000)
# # Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

st.subheader('Number of pickups by hour')
# hist_values = np.histogram(
#     data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

# st.bar_chart(hist_values)

# hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)

import time

# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')

# with st.status("Downloading data..."):
#     st.write("Searching for data...")
#     time.sleep(2)
#     st.write("Found URL.")
#     time.sleep(1)
#     st.write("Downloading data...")
#     time.sleep(1)

st.button('Rerun')
st.toast('Your edited image was saved!', icon='😍')

st.balloons()

from pathlib import Path
base_dir_path = Path("D:/wps/剪印/auto_generate/amateur/b61a76ffb1836e232beef111d03a4f0d-每日美女推荐工之大波浪美女")
imgs = list(base_dir_path.rglob("*.JPEG"))

imgs_pil = [Image.open(img) for img in imgs]
st.info(f"imgs={len(imgs_pil[:4])}")
# st.image(imgs_pil)
st.image(imgs_pil, width=200, caption=["some generic text"] * len(imgs_pil))


from streamlit_image_select import image_select

img = image_select(
    label="Select a cat",
    images=imgs_pil[:4],
    captions=["A cat", "Another cat", "Oh look, a cat!", "Guess what, a cat..."],
)

from streamlit_text_rating.st_text_rater import st_text_rater
import streamlit as st
st.title("Awesome App")
for text in ["Is this text helpful?", "Do you like this text?"]:
    response = st_text_rater(text=text)
    st.write(f"response --> {response}")

from streamlit_extras.badges import badge 
from streamlit_extras.echo_expander import echo_expander 


def example_pypi():
    badge(type="pypi", name="plost")
    badge(type="pypi", name="streamlit")

# example_pypi()

def example1():
    with echo_expander():
        import streamlit as st

        st.markdown(
            """
            This component is a combination of `st.echo` and `st.expander`.
            The code inside the `with echo_expander()` block will be executed,
            and the code can be shown/hidden behind an expander
            """
        )

example1()


# import pandas as pd
# from st_aggrid import AgGrid, JsCode
# from st_aggrid.grid_options_builder import GridOptionsBuilder
# # Dummy data
# data = {'name': ['The Shawshank Redemption', 'The Godfather', 'The Godfather: Part II', 'The Dark Knight'],
#         'year': [1994, 1972, 1974, 2008],
#         'description': ['Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
#                         'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
#                         'The early life and career of Vito Corleone in 1920s New York is portrayed while his son, Michael, expands and tightens his grip on the family crime syndicate.',
#                         'When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham, the Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.'],
#         'rating': [9.2, 9.2, 9.0, 9.0],
#         'image_url': [
#             "https://pics0.baidu.com/feed/9825bc315c6034a86a25a752866cb8580b2376ad.jpeg@f_auto?token=d2df21428b4c2ac65b7f7c981fa5e883",
#             "https://pics7.baidu.com/feed/f603918fa0ec08fa017f84561491cc6154fbda54.jpeg@f_auto?token=937c75d14451d2921383c945d2a5446c",
#             "https://pics6.baidu.com/feed/5882b2b7d0a20cf483714a573b76ba3aaeaf99e5.jpeg@f_auto?token=386cf0a99a585104305d5b74233a2e6b",
#             "https://pics1.baidu.com/feed/37d3d539b6003af3ac1761c7785537501138b670.jpeg@f_auto?token=5c89a7838ff069b7c38c82b53a45ce1f"
#         ]
#         }

# df = pd.DataFrame(data)
# # st.dataframe(df)


# render_image = JsCode('''
                      
#     function renderImage(params) {
#     // Create a new image element
#     var img = new Image();

#     // Set the src property to the value of the cell (should be a URL pointing to an image)
#     img.src = params.value;

#     // Set the width and height of the image to 50 pixels
#     img.width = 50;
#     img.height = 50;

#     // Return the image element
#     return img;
#     }
# '''
# )

# # Build GridOptions object
# options_builder = GridOptionsBuilder.from_dataframe(df)
# options_builder.configure_column('image_url', cellRenderer = None)
# options_builder.configure_selection(selection_mode="single", use_checkbox=True)
# grid_options = options_builder.build()

# # Create AgGrid component
# grid = AgGrid(df, 
#                 gridOptions = grid_options,
#                 allow_unsafe_jscode=True,
#                 height=200, width=500, theme='streamlit')

# sel_row = grid["selected_rows"]
# if sel_row:
#   with st.expander("Selections", expanded=True):
#     col1,col2 = st.columns(2)
#     st.info(sel_row[0]['description'])              
#     col1.image(sel_row[0]['image_url'],caption=sel_row[0]['name'])