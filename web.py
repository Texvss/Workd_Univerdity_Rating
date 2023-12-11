import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import requests
from bs4 import BeautifulSoup


def top(aspect):
    plot = plt.figure(figsize=(10, 5))
    sns.barplot(x=aspect, y='institution', data=df.sort_values(by=aspect)[:10], palette='magma')
    plt.title(f'Top 5 universities by: {aspect}')
    plt.xlabel(aspect)
    plt.ylabel('Universities')
    st.write("""
        # Remark:
        The shorter the column in this bar chart, the better the university is doing.
        """)
    return st.pyplot(plot.get_figure())


st.set_page_config(page_title='World University rating', page_icon='</3')

tab1, tab2, tab3, tab4 = st.tabs(['Full Information', 'Tops!)', 'Comparison of 3 countries', 'Search!'])

with tab1:
    st.title('World University Rating')
    image = Image.open('Universities.png')
    st.image(image, use_column_width=True)
    st.write("""
    Dataframe provides information about best universities in the world.
    """, font='')
    st.write('There are null values in dataframe.'
             ' if you want to check full dataframe click Nan!:')
    df = pd.read_csv(r"C:\Users\Asus\Desktop\proekt\ratings\cwurData.csv")
    nan = st.checkbox('NaN!')
    if nan:
        st.dataframe(df)
    else:
        df_cleaned = df.dropna(how='any')
        st.dataframe(df_cleaned)
    st.write("""
    # Information about Dataframe
    """)
    st.write('Dataset has 2200 rows anf 14 columns: 2 object columns, 2 float columns and 10 integer columns.'
             ' In broad_impact column i have 200 null values, this only 10% of my dataset, so i decided to delete rows which contain null values.')

    # dataset cleaning
    st.write("""
    # Hypothesis:
    """)
    st.write('My hypothesis is: quality of education has the most influense on overall score.')

    # Make a corelation heatmap
    fig = plt.figure(figsize=(10, 8))
    columns = ['quality_of_education', 'alumni_employment', 'publications', 'influence', 'citations', 'broad_impact',
               'patents', 'score']
    sns.heatmap(df[columns].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    st.pyplot(fig.get_figure())
    st.write(
        'As we can see all compelations are negative. This is becase dataframe is a rating, that mean lower the value, the result is better. '
        'Absolute value of "quality_of_education" is the biggest one that means, quallity of education has the biggest impact on overall score.')

    # 10 big countries

    pivot_table = df_cleaned.groupby(by=['year', 'country']).size().reset_index(name='university_count')
    pivot_table = pivot_table.sort_values(by='university_count', ascending=False)[:10]
    st.write("""
    # Amount of universities in each country in 2014 and 2015.
    """)
    st.dataframe(pivot_table)
    fig1 = px.bar(pivot_table, x='university_count', y='country', orientation='h',
                  title='Amount of Universities in each country',
                  color='year',
                  labels={'university_count': 'amount of universities'})
    st.plotly_chart(fig1, theme='streamlit', use_container_width=True)

    # sunburst
    big_countries = ['USA', 'China', 'Japan', 'United Kingdom', 'Germany', 'France', 'Russia', 'Canada', 'Italy',
                     'Netherlands']
    poi = df_cleaned[df_cleaned['country'].isin(big_countries)]
    poi = poi.loc[(poi['national_rank'] < 5) & (poi['world_rank'] < 100)]
    sb = px.sunburst(poi, color='country', path=['country', 'institution', 'world_rank', 'national_rank', 'year'],
                     hover_name='country')
    st.title('Sunburst with some countries and universities in these countries:')
    st.plotly_chart(sb, theme='streamlit', use_container_width=True)

with tab2:
    # Top university rating be some aspects
    st.title("""
    Top universities by some aspects
    """)
    aspects = ['quality_of_education', 'publications', 'alumni_employment', 'patents', 'world_rank']
    chose = st.radio('', aspects)
    if chose == 'quality_of_education':
        top('quality_of_education')
    elif chose == 'alumni_employment':
        top('alumni_employment')
    elif chose == 'publications':
        top('publications')
    elif chose == 'patents':
        top('patents')
    elif chose == 'world_rank':
        top('world_rank')

    best_uni = df_cleaned.loc[(df['national_rank'] == 1)]
    uni_2014 = best_uni.loc[df['year'] == 2014]
    uni_2014 = uni_2014.sort_values(by=['world_rank'])[:10]  # 10 best unis in 2014

    uni_2015 = best_uni.loc[df['year'] == 2015]
    uni_2015 = uni_2015.sort_values(by=['world_rank'])[:10]  # 10 best unis in 2015
    options = [2014, 2015]
    option = st.radio('', options)
    if option == 2014:
        top_10 = px.bar(uni_2014, x='institution', y='score', color='country', title='10 best univesity in 2014')
        st.plotly_chart(top_10, theme='streamlit', use_container_width=True)
    else:
        top_10 = px.bar(uni_2015, x='institution', y='score', color='country', title='10 best univesity in 2015')
        st.plotly_chart(top_10, theme='streamlit', use_container_width=True)
    # Top 10 universities in some countries in 2014
    st.write("""
    # Top 10 University in selected country!
    """)

    country = st.text_input('Enter the name of the country!')
    df_2014 = df_cleaned.loc[df['year'] == 2014]
    df_2014 = df_2014.loc[df_2014['country'] == country][:10]
    df_2015 = df_cleaned.loc[df['year'] == 2015]
    df_2015 = df_2015.loc[df_2015['country'] == country][:10]
    years = [2015, 2014]
    year = st.radio('', years)
    if year == 2014:
        st.dataframe(df_2014['institution'])
    else:
        st.dataframe(df_2015['institution'])

with tab3:
    st.title("""
     Compsrison of three countries
    """)
    st.write('I decided to compare three countre: USA, United Kingdom and China. There all from different continents.'
             'Ultimately, I want to conclude by continent!')
    st.write("Let's take a look at the top 10 universities in these countries ")
    usa_2014 = df_cleaned.loc[(df_cleaned['country'] == 'USA') & (df_cleaned['year'] == 2014)].drop(
        ['year', 'national_rank'],
        axis=1)[:10]
    uk_2014 = df_cleaned.loc[(df_cleaned['country'] == 'United Kingdom') & (df_cleaned['year'] == 2014)].drop(
        ['year', 'national_rank'],
        axis=1)[:10]
    china_2014 = df_cleaned.loc[(df_cleaned['country'] == 'China') & (df_cleaned['year'] == 2014)].drop(
        ['year', 'national_rank'], axis=1)[:10]

    usa_2015 = df_cleaned.loc[(df_cleaned['country'] == 'USA') & (df_cleaned['year'] == 2015)].drop(
        ['year', 'national_rank'],
        axis=1)[:10]
    uk_2015 = df_cleaned.loc[(df_cleaned['country'] == 'United Kingdom') & (df_cleaned['year'] == 2014)].drop(
        ['year', 'national_rank'],
        axis=1)[:10]
    china_2015 = df_cleaned.loc[(df_cleaned['country'] == 'China') & (df_cleaned['year'] == 2014)].drop(
        ['year', 'national_rank'], axis=1)[:10]
    year = st.selectbox('Select year:', df_cleaned['year'].unique())
    countries = ['USA', 'United Kingdom', 'China']
    countri = st.radio('', countries)
    if year == 2014:
        if countri == 'USA':
            st.dataframe(usa_2014)
        elif countri == 'China':
            st.dataframe(china_2014)
        else:
            st.dataframe(uk_2014)
        st.write("""
           # Let's compare 10 best universities in these countries in 2014:
           """)
        data_2014 = pd.concat([usa_2014, uk_2014, china_2014], keys=['USA', 'UK', 'China'])

        figura = plt.figure(figsize=(12, 6))
        sns.boxplot(data=data_2014, x=data_2014.index.get_level_values(0), y='quality_of_education')
        plt.title('Comparing 10 best universities in 3 counties by quality of education in 2014.')
        plt.xlabel('Country')
        plt.ylabel('Quality of Education')
        plt.gca().invert_yaxis()  # for comfortability
        st.pyplot(figura.get_figure())

        average_usa_2014 = usa_2014.mean(numeric_only=True)
        average_uk_2014 = uk_2014.mean(numeric_only=True)
        average_china_2014 = china_2014.mean(numeric_only=True)

        data_2014 = pd.concat([average_usa_2014, average_uk_2014, average_china_2014], axis=1)
        data_2014.columns = ['USA', 'UK', 'China']

        data_2014 = -data_2014  # for comfortable vision

        fig_2014_t3 = px.line(data_2014, x=data_2014.index, y=['USA', 'UK', 'China'],
                              labels={'value': 'Value', 'variable': 'Country'},
                              title='Comparing 3 countries by mean values in 2014')
        st.plotly_chart(fig_2014_t3, theme='streamlit', use_container_width=True)

        st.title('Conclusion:')
        st.write('As we can see, in 2014 best universities were in USA, second place was United Kingdom, then China.')
    else:
        if countri == 'USA':
            st.dataframe(usa_2015)
        elif countri == 'China':
            st.dataframe(china_2015)
        else:
            st.dataframe(uk_2015)
        st.write("""
           # Let's compare 10 best universities in these countries in 2015:
           """)
        data_2015 = pd.concat([usa_2015, uk_2015, china_2015], keys=['USA', 'UK', 'China'])

        figura = plt.figure(figsize=(12, 6))
        sns.boxplot(data=data_2015, x=data_2015.index.get_level_values(0), y='quality_of_education')
        plt.title('Comparing 10 best universities in 3 counties by quality of education in 2015.')
        plt.xlabel('Country')
        plt.ylabel('Quality of Education')
        plt.gca().invert_yaxis()  # for comfortability
        st.pyplot(figura.get_figure())

        average_usa_2015 = usa_2015.mean(numeric_only=True)
        average_uk_2015 = uk_2015.mean(numeric_only=True)
        average_china_2015 = china_2015.mean(numeric_only=True)

        data_2015 = pd.concat([average_usa_2015, average_uk_2015, average_china_2015], axis=1)
        data_2015.columns = ['USA', 'UK', 'China']

        data_2015 = -data_2015  # for comfortable vision

        fig_2015_t3 = px.line(data_2015, x=data_2015.index, y=['USA', 'UK', 'China'],
                              labels={'value': 'Value', 'variable': 'Country'},
                              title='Comparing 3 countries by mean values in 2015')
        st.plotly_chart(fig_2015_t3, theme='streamlit', use_container_width=True)

        st.title('Conclusion:')
        st.write('As we can see, in 2015 best universities were in USA, second place was United Kingdom, then China.')
    st.title('Overall conclusion:')
    st.write('Virtually nothing has changed in a year.')

with tab4:
    try:
        st.title('Full information!')
        university_name = st.text_input('Write name of the university as in dataframe:')
        if university_name == '':
            st.write('')
        elif university_name not in df['institution'].unique():
            st.title('No such university in dataframe!')
        else:
            row = df[df['institution'] == university_name].index.values
            strana = df['country'][row[0]]
            university_name_url = "-".join([i.lower() for i in university_name.split()])
            if strana == 'USA':
                strana = 'united-states'
            else:
                strana = "-".join([i.lower() for i in strana.split()])
            url = f'https://www.alluniversity.info/{strana}/{university_name_url}/'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            description = soup.find("div", class_="slide-text").find("p").text
            st.write(f"""
            ## Information about {university_name}:
            """, description)
            st.write('##')
            st.title('If you want to check another information, you should go to this link:')
            st.write(url)
    except AttributeError:
        st.title('No information about this university :(')







