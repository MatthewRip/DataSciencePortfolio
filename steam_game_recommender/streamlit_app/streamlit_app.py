# app
import streamlit as st
# get info from steam
from fetch import FetchFromWeb

# plot graphs
import plotly.express as px

# misc
import pandas as pd
import time

# preform prediction
from recommender import title_recommendation
from recommender import url_recommendation
from recommender import determine_cluster
# for some reason it breaks with out this
from recommender import tokenizer


# class for getting information from steam
fetch_data = FetchFromWeb()

#
# game_data = pd.read_csv('resources/data/data.csv')
# game_data.dropna(inplace=True)
two_dim = pd.read_csv('resources/data/2d.csv')
three_dim = pd.read_csv('resources/data/3d.csv')
game_titles = game_data['title']


def main():

    # remove hamburger 'made with streamlit'
    # add #MainMenu {visibility: hidden;} to hide
    hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # side bar information
    with st.sidebar:
        # get recommendations or display data
        sidebar_selection = st.radio(
            'Select', ('Get recommendation', 'Visualize data', 'Info'))

        if sidebar_selection == 'Get recommendation':
            # with st.expander('Display type:'):
            #     display_type = st.radio(
            #         "Select:", ('Default', '2d', '3d'))

            # this will affect the results returned
            feature_max = st.slider(
                'Sensitivity', 0, 5, 0, 1)

            st.caption('This will effect how the comparisons are calculated.')
            # number of titles to return
            num_recommendations = st.slider(
                'Number of recommendations.', 10, 50, None, 10)


    if sidebar_selection == 'Get recommendation':

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
                # this is index position of list of recommendations
                try:
                    with st.spinner('Looking for recommendation...'):
                        game_recommendations = title_recommendation(
                            game=game_title, feature_sense=feature_max, top_n=num_recommendations)
                        # print(game_recommendations)
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

                    # """
                    # THIS IS WHERE WE CAN LOOK AT THE DISPLAY TYPE

                    # """

                    st.title('Have you played... ?')
                    # print list of recommendations
                    for i, j in enumerate(game_recommendations['title']):
                        st.subheader(str(i + 1) + '. ' + j)
                        # get game url
                        url = game_recommendations[game_recommendations['title']
                                                   == j]['hyperlink'].values[0]
                        # image url
                        img = fetch_data.game_image(url)
                        price = fetch_data.get_price(url)
                        st.image(img)
                        if 'erawrrr' in price:
                            st.write('Price:')
                            st.image(
                                "https://imgur.com/DuoAnjg.gif", width=150)
                        else:
                            if len(price) == 1:
                                st.write('Price: ' + price[0])
                            else:
                                st.write('Original Price: ' + price[0])
                                st.write('Current Price: ' + price[1])
                                st.write('Discount: ' + price[2])

                        # drop down for url and image
                        expander = st.expander('Page link')
                        # game page url
                        expander.write(url)

                except:
                    st.image("https://imgur.com/DuoAnjg.gif", width=300)
                    st.error('Insufficient funds... I mean something went wrong.')

        if sys == 'Game url':

            # add try block again

            # text bar
            text_input_container = st.empty()
            user_added_url = text_input_container.text_input("Paste url...")

            if user_added_url != "":
                # text_input_container.empty()
                st.info(user_added_url)

                try:
                    # scrap tags from steam webpage
                    title = fetch_data.get_name(user_added_url)
                    tags = fetch_data.get_tags(user_added_url)

                    # get cluster
                    cluster = determine_cluster(tags)
                    game_recommendations = url_recommendation(
                        title, tags, cluster, feature_sense=feature_max)
                    #

                    st.title('Have you played... ?')
                    # print list of recommendations
                    for i, j in enumerate(game_recommendations['title']):
                        st.subheader(str(i + 1) + '. ' + j)
                        url = game_recommendations[game_recommendations['title']
                                                   == j]['hyperlink'].values[0]
                        # image url
                        img = fetch_data.game_image(url)
                        price = fetch_data.get_price(url)
                        st.image(img)
                        if 'erawrrr' in price:
                            st.write('Price:')
                            st.image(
                                "https://imgur.com/DuoAnjg.gif", width=150)
                        else:
                            if len(price) == 1:
                                st.write('Price: ' + price[0])
                            else:
                                st.write('Original Price: ' + price[0])
                                st.write('Current Price: ' + price[1])
                                st.write('Discount: ' + price[2])

                        # drop down for url and image
                        expander = st.expander('Page link')
                        # game page url
                        expander.write(url)
                except:
                    st.image("https://imgur.com/DuoAnjg.gif", width=300)
                    st.error('Insufficient funds... I mean something went wrong.')

    if sidebar_selection == 'Visualize data':
        dim = st.radio('Dimensions', ('2d', '3d'))
        apply_filter = st.radio('Display similar games:', ('no', 'yes'))

        if dim == '2d':
            # st.write('Zoom in...')
            # plot
            num_k = two_dim['cluster'].max() + 1
            title = 'Games represented in 2d space: k {}'.format(num_k)

            if apply_filter == 'yes':
                opacity = st.number_input('Opacity', 0.0, 1.0, 1.0, 0.1)

                # select game title
                filter_games = st.selectbox('Filter:', game_titles)
                # get cluster value
                game_cluster = two_dim[two_dim['title']
                                       == filter_games]['cluster'].values[0]
                # filter clusters
                subsection = two_dim[two_dim['cluster'] == game_cluster]

                # get values for selected title
                d1 = two_dim[two_dim['title'] == filter_games]['D1']
                d2 = two_dim[two_dim['title'] == filter_games]['D2']

                # 2d scatter with cluster colors
                fig = px.scatter(subsection, x='D1', y='D2', color="cluster",
                                 hover_name='title', opacity=opacity, title='Games in the same space as {}.'.format(filter_games))

                # change color of selected title
                fig.add_traces(
                    px.scatter(x=d1, y=d2, hover_name=[
                        filter_games], color_discrete_sequence=['blue']).data
                )

                # Plot!
                st.write('Zoom in... Its in there some where.')
                st.plotly_chart(fig, use_container_width=True)

            else:
                fig = px.scatter(two_dim, x="D1", y="D2", color="cluster",
                                 hover_name='title', title=title)

                # Plot!
                st.plotly_chart(fig, use_container_width=True)

            # game_title = st.selectbox('Titles',game_title)

        if dim == '3d':

            num_k = two_dim['cluster'].max() + 1
            title = 'Games represented in 2d space: k {}'.format(num_k)

            if apply_filter == 'yes':
                opacity3d = st.number_input('Opacity', 0.0, 1.0, 1.0, 0.1)
                # 0.0 = 1 for some reason
                if opacity3d == 0.0:
                    opacity3d = 0.001

                # select game title
                filter_games = st.selectbox('Filter:', game_titles)
                # get cluster value
                game_cluster = three_dim[three_dim['title']
                                         == filter_games]['cluster'].values[0]
                # filter clusters
                subsection = three_dim[three_dim['cluster'] == game_cluster]

                # get values for selected title
                d1 = three_dim[three_dim['title'] == filter_games]['D1']
                d2 = three_dim[three_dim['title'] == filter_games]['D2']
                d3 = three_dim[three_dim['title'] == filter_games]['D3']

                # 2d scatter with cluster colors
                fig = px.scatter_3d(subsection, x='D1', y='D2', z='D3', color="cluster",
                                    hover_name='title', opacity=opacity3d, title='Games in the same space as {}.'.format(filter_games))

                # change color of selected title
                fig.add_traces(
                    px.scatter_3d(x=d1, y=d2, z=d3, hover_name=[
                        filter_games], color_discrete_sequence=['blue']).data
                )

                # Plot!
                st.write('Zoom in... Its in there some where.')
                st.plotly_chart(fig, use_container_width=True)

            else:

                st.write('Explore...')
                num_k = three_dim['cluster'].max() + 1
                title = 'Games represented in 3d space: k {}'.format(num_k)
                fig = px.scatter_3d(three_dim, x="D1", y="D2", z='D3', color="cluster",
                                    hover_name='title', title=title)

                # Plot!
                st.plotly_chart(fig, use_container_width=True)
    if sidebar_selection == 'Info':

        st.write('Hello there, a bit on how this app works.')
        """
        Recommendations take a bit to process as it looks up the current price and image used.


        This webapp is build using Streamlit.
        The data was scraped off of steam store. Dataset consists of around 52000 games
        This used t-nse to convert high dimensional space to low, to be able to create 2d and 3d graphs.
        This uses Natural Language Processing (NLP) to compare games using tags which describe them.
        To speed up the calculation of the similarity of given game and other games. And not use a cosine similarity pivot 
        table which would need around 60gigs of memory to run.

        I used unsupervised learning(Kmeans) to create logical groupings(clusters) of the games, 
        so when we want to get an recommendation we only look at all the titles which belong to the same cluster

        This also allows us to compare games that are not apart of the dataset. When a url is entered we look up the features we 
        need from the games steam page and then using the kmeans model we predict which cluster it would belong too and return the most similar games.
        """


if __name__ == '__main__':
    main()
