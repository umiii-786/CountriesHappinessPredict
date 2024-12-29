import streamlit as st 
import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 

df=pd.read_csv('./data/AllYearProcessed_data_1.csv')


st.markdown(
    """
    <style>
   #top-happiest-countries-in-overall-5-year{
   text-align:left
   }
   .st-emotion-cache-lpgk4i{
        background-color:green;
        color:white;

   }
#    .st-emotion-cache-1ssyx9w{
#    width:100%
#    }
     img{
    filter: invert(1);
     }
      h3{
    font-size:16px
    
    }
    p{
    color: #a0a0a0;
    }
    h2{
    
        text-align: center;
    border-bottom: 1px solid gray;
    margin-bottom: 30px;
    }
    </style>

   
    """,
    unsafe_allow_html=True,
)
# print(df.head(5))
def getQuerryField(df,column):
    col=df[column].value_counts().index
    return col


def GiveGroup(df,check,onbasis):
    if check=="Over All":
         return df
    else:
        return df.groupby(onbasis).get_group(check)
     
def getTopFiveCountry(df,check,ascending=True):
     
    if check=="Over All":
        df['Average Happiness']=df.groupby('Country')['Happiness Score'].transform(lambda x:x.mean())
        df=df.drop_duplicates(subset=['Country','Average Happiness'])
        df=df.sort_values(by="Average Happiness",ascending=ascending)
        if(df.shape[0]>5):
            df=df.head(5)
            df['Happiness Rank']=[1,2,3,4,5]
        df=df[['Country','Region','Happiness Rank','Average Happiness']]
    
    else:
        df=df.sort_values(by="Happiness Score",ascending=ascending)
        if(df.shape[0]>5):
            df=df.head(5)
            df['Happiness Rank']=[1,2,3,4,5]
        df=df[['Country','Region','Happiness Rank','Happiness Score']]
    df=df.set_index('Happiness Rank')
    return df


def HappinessAccording_Specific_Field(df,Column):
     
     counts=df.groupby(Column)['Happiness Score'].mean()

     data={f'{Column}':counts.index,
              'Happiness_Score':counts.values}
     data=pd.DataFrame(data)
     return data

def findTrend_Effected_Countries(df,ascending):
    newdf=df.drop_duplicates(subset=['Country','HappinessGrowth'])
    Countries=(newdf.sort_values(by="HappinessGrowth",ascending=ascending).head(5))['Country'].values
    # print(Countries)
    return Countries
    
def Return_Grouped_SpecifiedColumn_and_Year(countries,col):
    data=pd.DataFrame(columns=countries)
    for country in countries:
        newdf=df.groupby('Country').get_group(country)
        newdf=newdf.sort_values(by="year",ascending=True)
        # print(newdf)
        values=newdf[col].values
        if len(values)==4:
            values=np.insert(values,0,values[0])
        data[country]=values
    data['year']=[2015,2016,2017,2018,2019]
    data = data.set_index("year")
    return data


# def get_va rousFactor_according_to_group(df,onbasis,columns):
   




years=['Over All']+list(getQuerryField(df,'year'))
regions=['Over All']+list(getQuerryField(df,'Region'))
countries=['Over All']+list(getQuerryField(df,'Country'))



col1,col2,col3=st.columns(3)

filter_data=''



st.sidebar.title('Countries Happiness Level Analysis')
year=st.sidebar.selectbox('Choose the year',years,key="Years Option")
region=st.sidebar.selectbox('Choose the Region',regions,key="Regions Option")

if region=="Over All":
    country=st.sidebar.selectbox('Choose the Country',countries)

else:
    df=df.groupby('Region').get_group(region)
    countries=['Over All']+list(getQuerryField(df,'Country'))
    country=st.sidebar.selectbox('Choose the Country',countries)
    # country_list=country_list['Country'].value_counts().index
    # country_list=

if year==region==country=='Over All':
    st.header('Descriptive Analysis')
    r1_col1,r2_col2=st.columns(2)
    with r1_col1:
         st.write('Top 5 Happiest Countries in OverAll 5 Year')
         st.dataframe(getTopFiveCountry(df,'Over All',ascending=False))
    with r2_col2:
        st.write('Top 5 Un-Happiest Countries in OverAll 5 Year')
        st.dataframe(getTopFiveCountry(df,'Over All',ascending=True))

    r2_col1,r2_col2=st.columns(2)
    with r2_col1:
        st.write('Average Happiness in Each Region')
        data=HappinessAccording_Specific_Field(df,'Region')
        st.bar_chart(x="Region",y="Happiness_Score",data=data)
    with r2_col2:
        st.write('Average Happiness in Each Year')
        data=HappinessAccording_Specific_Field(df,'year')
        st.bar_chart(x="year",y="Happiness_Score",data=data)

        plt.style.use('fivethirtyeight')
    
    fig, ax = plt.subplots()
    table=pd.pivot_table(index="Region",columns="year",values="Happiness Score",aggfunc="mean",data=df)
    sns.heatmap(table,annot=True, ax=ax)
    st.pyplot(fig)

    st.header('Trend Analysis')
    col5,col6=st.columns(2)


    st.write('Countries Having High Improvemet over Time')
    countries=findTrend_Effected_Countries(df,False)
    data=Return_Grouped_SpecifiedColumn_and_Year(countries=countries,col='Happiness Score')
    st.line_chart(data=data)



    st.write('Countries Having High Declined over Time')
    countries=findTrend_Effected_Countries(df,True)
    data=Return_Grouped_SpecifiedColumn_and_Year(countries=countries,col='Happiness Score')
    st.line_chart(data=data)


    r3_col1,r3_col2=st.columns(2)
    r4_col1,r4_col2=st.columns(2)
   
    top_countries=getTopFiveCountry(df,'Over All',ascending=False)
    top_countries=top_countries['Country'].values
    with r3_col1:
        st.write('GDP Trend in Top Happiest Country')
        data=Return_Grouped_SpecifiedColumn_and_Year(top_countries,'Economy (GDP per Capita)')
        st.line_chart(data=data)
 
    
    with r3_col2:
       st.write('Health (Life Expectancy) Trend in Top Happiest Country')
       data=Return_Grouped_SpecifiedColumn_and_Year(top_countries,'Health (Life Expectancy)')
       st.line_chart(data=data)

    st.write('Generosity Trend in Top Happiest Country')
    data=Return_Grouped_SpecifiedColumn_and_Year(top_countries,'Generosity')
    st.bar_chart(data=data)

    with r4_col1:
        st.write('Freedom Trend in Top Happiest Country')
        data=Return_Grouped_SpecifiedColumn_and_Year(top_countries,'Freedom')
        st.line_chart(data=data)

    with r4_col2:
       st.write('Social support Trend in Top Happiest Country')
       data=Return_Grouped_SpecifiedColumn_and_Year(top_countries,'Social support')
       st.line_chart(data=data)
    
    

    st.header('Correlation Analysis')
    st.write('Happiness Relation with GDP and Health')
   
    r5_col1,r5_col2=st.columns(2)
    with r5_col1:
        st.scatter_chart(x="Economy (GDP per Capita)",y='Happiness Score',data=df[['Happiness Score','Economy (GDP per Capita)']])
    with r5_col2:
        st.scatter_chart(x="Health (Life Expectancy)",y='Happiness Score',data=df[['Happiness Score','Health (Life Expectancy)']])


    st.write('Relation between Various Factor ')
    r6_col1,r6_col2=st.columns(2)
    with r6_col1:
            st.scatter_chart(x="Economy (GDP per Capita)",y='Health (Life Expectancy)',data=df[['Health (Life Expectancy)','Economy (GDP per Capita)']])
    with r6_col2:
              st.scatter_chart(x="Freedom",y='Social support',data=df[['Freedom','Social support']])
       
        
 
elif country=='Over All':
    region_head='' if region=="Over All" else region
    year_head='' if year=="Over All" else year
    st.header(f'Analysis of {region_head} in OverAll {year_head} Year')
    filter_data=GiveGroup(df,year,'year')
    filter_data=GiveGroup(filter_data,region,'Region')  
    print(filter_data)  

    if region=="Over All" or year=='Over All':
        result='Region' if region=="Over All" else "year"
         
        happyCountry=getTopFiveCountry(filter_data,'other',ascending=False)
        UnhappyCountry=getTopFiveCountry(filter_data,'other',ascending=True)
        r1_col1,r2_col2=st.columns(2)
        with r1_col1:
            st.write(f'Happiest Countries')
            st.dataframe(happyCountry)
        with r2_col2:
            st.write(f'Un-Happiest Countries')
            st.dataframe(UnhappyCountry)

        
    
        st.write(f'Happiness Level in Different {result}')
        data=HappinessAccording_Specific_Field(filter_data,result)
        st.bar_chart(x=f"{result}",y="Happiness_Score",data=data)
        data1=df.groupby(result)[['Economy (GDP per Capita)','Health (Life Expectancy)']].mean()
        data2=df.groupby(result)[['Freedom', 'Social support']].mean()
        data3=df.groupby(result)['Generosity'].mean()
        st.write('GDP And Health Trend')
        st.line_chart(
        data=data1)
        st.write('Freedom And Social Support Trend')
        st.line_chart(
        data=data2)

        st.write('Generosity Trend ')
        # data=Return_Grouped_SpecifiedColumn_and_Year(happyCountry,'Generosity')
        st.area_chart(data=data3)

    else:
        r1_col1,r1_col2,r1_col3=st.columns(3)
        r2_col1,r2_col2,r2_col3=st.columns(3)
        with r1_col1:
            st.subheader('Countries')
            st.write(f'{filter_data['Country'].count()}')
        
        with r1_col2:
            st.subheader('Higgest Happiness Score')
            st.write(f'{filter_data['Happiness Score'].sort_values(ascending=False).values[0]}')

        with r1_col3:
            st.subheader('Higgest (GDP per Capita)')
            st.write(f'{filter_data['Economy (GDP per Capita)'].sort_values(ascending=False).values[0]}')


        with r1_col1:
            st.subheader('Average Health Expectancy')
            st.write(f'{filter_data['Health (Life Expectancy)'].mean()}')
        
        with r1_col2:
            st.subheader('Average Freedom')
            st.write(f'{filter_data['Freedom'].sort_values(ascending=False).values[0]}%')

        with r1_col3:
            st.subheader('Average Government Corruption')
            st.write(f'{filter_data['Trust (Government Corruption)'].sort_values(ascending=False).values[0]}%')

        data1=filter_data[['Country','Happiness Score']]
        data1.set_index('Country',inplace=True)
        st.write('Countriess and Threir Happiness Score')
        st.bar_chart(
        data=data1)

        st.write('Health and GDP Trend in Varous Country')
        data1=filter_data[['Country','Economy (GDP per Capita)','Health (Life Expectancy)']]
        data1.set_index('Country',inplace=True)
        st.area_chart(
        data=data1)


        st.write('Fundamental Rights in Various Country')
        data1=filter_data[['Country','Freedom','Social support']]
        data1.set_index('Country',inplace=True)
        st.line_chart(
        data=data1)


else:
    
    filter_data=GiveGroup(df,year,'year')
    filter_data=GiveGroup(filter_data,region,'Region')
    filter_data=GiveGroup(filter_data,country,'Country')
    r1_col1,r1_col2,r1_col3=st.columns(3)
    r2_col1,r2_col2,r2_col3=st.columns(3)
    

    labels=["Higgest Happiness Score",
            'Higgest (GDP per Capita)',
            'Average Health Expectancy',
            'Average Freedom %',
            'Average Government Corruption %',
            'Average Generosity'
            ]
    
    columnsName=['Happiness Score',
                 'Economy (GDP per Capita)',
                 'Health (Life Expectancy)',
                 'Freedom',
                 'Trust (Government Corruption)',
                  'Generosity'
      
              ]
    
    if year!="Over All":
        st.header(f'{country} Analysis of {year}')
        for i in range(len(labels)):
           labels[i]=labels[i].replace('Higgest','')
           labels[i]=labels[i].replace('Average','') 
    else:
        st.header(f'{country} Over-All 5 Year Analysis')
    
    count=0
    for row in range(2): 
        rows=st.columns(3)
        for col in range(3):
            with rows[col]:
                   st.subheader(labels[count])
                   if "Higgest" in labels[count]:
                        st.write(f'{filter_data[columnsName[col]].sort_values(ascending=False).values[0]}')
                   else:
                      st.write(f'{filter_data[columnsName[col]].mean()}')
            count=count+1

    if year=="Over All":
        data=filter_data[['year','Happiness Score']]
        data=data.set_index('year')
        st.bar_chart(data=data)

        st.write('Economy (GDP) and Health Expectancy')
        data=filter_data[['year','Economy (GDP per Capita)','Health (Life Expectancy)']]
        data=data.set_index('year')
        st.area_chart(data=data)

        st.write('Fundamental Rights')
        data=filter_data[['year','Freedom','Social support']]
        data=data.set_index('year')
        st.area_chart(data=data)
       
        st.write('Corruption and Generosity')
        data=filter_data[['year','Trust (Government Corruption)','Generosity']]
        data=data.set_index('year')
        st.area_chart(data=data)
        # print(filter_data)

    

                        

                 
             
    # with r1_col1:
    #         st.subheader('Countries')
    #         st.write(f'{filter_data['Country'].count()}')
        
    # with r1_col2:
    #         st.subheader('Higgest Happiness Score')
    #         st.write(f'{}')

    # with r1_col3:
    #         st.subheader('Higgest (GDP per Capita)')
    #         st.write(f'{filter_data['Economy (GDP per Capita)'].sort_values(ascending=False).values[0]}')


    # with r1_col1:
    #         st.subheader('Average Health Expectancy')
    #         st.write(f'{filter_data['Health (Life Expectancy)'].mean()}')
        
    # with r1_col2:
    #         st.subheader('Average Freedom')
    #         st.write(f'{filter_data['Freedom'].sort_values(ascending=False).values[0]}%')

    # with r1_col3:
    #         st.subheader('Average Government Corruption')
    #         st.write(f'{filter_data['Trust (Government Corruption)'].sort_values(ascending=False).values[0]}%')
    # if region=="Over All":

    #     pass

    # if year=="Over All":
    #     pass

    # print(filter_data)


getQuerryField(df,'year')
