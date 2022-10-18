# required for app
from cgi import print_arguments
from codecs import utf_16_le_decode
import streamlit as st

#
from gamedata import GameData


# misc
import pandas as pd
import time

# preform prediction
from recommender import tag_based_recommendation


# creating instances
game_features = GameData()


#
game_data = pd.read_csv('resources/data/clsutered_df.csv')
game_titles = game_data['title']

# test = game_data['hyperlink'][0]
# img = game_features.game_image(test)
# print(img)


# title
st.title('What play to next?')


# type of recommender
sys = st.radio('If game is\'nt in the list, switch to url and enter steam url for game page.',
               ('Game title', 'Game url'))

if sys == "Game title":

    # user game select
    # st.write("Game Title:")
    game_title = st.selectbox('Game titles:', game_titles)
    # print(game_title)

    if st.button("Recommend...."):

        try:
            with st.spinner('Looking for recommendation...'):
                recommendations = tag_based_recommendation(game_title)
                # print(recommendations)
                time.sleep(1)
            with st.spinner('Looking for banking details...'):
                time.sleep(1)
            with st.spinner('Found feet pictures!'):
                time.sleep(1)
            with st.spinner('uploading pictures...'):
                # progress bar
                prgress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    prgress_bar.progress(percent_complete + 1)
                time.sleep(.1)
                prgress_bar.empty()
                st.success("Upload complete!")
            st.title('Have you played... ?')
            # print list of recommendations
            for i, j in enumerate(recommendations['title']):
                st.subheader(str(i + 1) + '. ' + j)
                # st.write('test')
                url = recommendations[recommendations['title']
                                      == j]['hyperlink'].values[0]
                # image url
                img = game_features.game_image(url)
                price = game_features.get_price(url)
                st.image(img)
                if len(price) == 1:
                    st.write('Price: ' + price[0])
                else:
                    st.write('Original Price: ' + price[0])
                    st.write('Current Price: ' + price[1])
                    st.write('Discount: ' + price[2])

                # drop down for url and image
                expander = st.beta_expander('Page link')
                # game page url
                expander.write(url)
                # st.write('test')
        except:
            st.error('Insufficient funds...')

# if sys == 'Game url':

#     text_input_container = st.empty()
#     text_input_container.text_input("Enter something", key="text_input")

#     if st.session_state.text_input != "":
#         text_input_container.empty()
#         st.info(st.session_state.text_input)



# text_input_container = st.empty()
# t = text_input_container.text_input("Enter something")

# if t != "":
#     text_input_container.empty()
#     st.info(t)
