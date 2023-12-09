import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import pydeck as pdk 
st.set_page_config(layout="wide")

files = ['chefmozaccepts',
         'chefmozcuisine',
         'chefmozhours4',
         'chefmozparking',
         'usercuisine',
         'userpayment',
         'userprofile',
         'rating_final',
         'geoplaces2']
dfs = dict()

@st.cache_data ()    
def load_file(f):
    if f is not None:
        for file in files:
            fl= 'data/'+file+'.csv'
            dfs[file] = pd.read_csv(fl,encoding='ISO-8859-1')
    else:
        for file in files:
            fl= 'data/'+file+'.csv'
            dfs[file] = pd.read_csv(fl,encoding='ISO-8859-1')
    return(dfs)

dfs = load_file(files)
   
alt.data_transformers.disable_max_rows()

# #cleaning up the resturant hourly file
# #Trim white spaces
dfs['chefmozhours4']['hours'] = dfs['chefmozhours4']['hours'].str.strip()
dfs['chefmozhours4']['days'] = dfs['chefmozhours4']['days'].str.strip()


h1 = dfs['chefmozhours4']['hours'].str.split('-',expand = True)
h1[0] = h1[0].astype('datetime64[ns]')
h1[0] = pd.to_datetime(h1[0], format='%d/%m/%y %H:%M')
h2= h1[1].str.split(';',expand = True)
h1[1]= h2[0].astype('datetime64[ns]')
h1[1] = pd.to_datetime(h1[1], format='%d/%m/%y %H:%M')
h1['openhr'] = h1[0].dt.hour
h1['openmin'] = h1[0].dt.minute
h1['clshr'] = h1[1].dt.hour
h1['clsmin'] = h1[1].dt.minute

dfs['chefmozhours4']['opentime'] =h1[0].dt.time
dfs['chefmozhours4']['openhr'] = h1['openhr']
dfs['chefmozhours4']['openmin'] = h1['openmin']
dfs['chefmozhours4']['clstime'] =h1[1].dt.time
dfs['chefmozhours4']['clshr'] = h1['clshr']
dfs['chefmozhours4']['clsmin'] = h1['clsmin']

#converting days of operation into corresponding column

d1 =dfs['chefmozhours4']['days'].str.split(';',expand = True)
d1.drop([5],axis=1,inplace=True)
d1['Mon'] = d1[0] .apply(lambda x: (x=='Mon')==True )
d1['Tue'] = d1[1] .apply(lambda x: (x=='Tue')==True )
d1['Wed'] = d1[2] .apply(lambda x: (x=='Wed')==True )
d1['Thu'] = d1[3] .apply(lambda x: (x=='Thu')==True )
d1['Fri'] = d1[4] .apply(lambda x: (x=='Fri')==True )
d1['Sat'] = d1[0] .apply(lambda x: (x=='Sat')==True )
d1['Sun'] = d1[0] .apply(lambda x: (x=='Sun')==True )
d1.replace({False: 0, True: 1}, inplace=True)
d1['days_of_operation'] = d1['Mon']+d1['Tue']+d1['Wed']+d1['Thu']+d1['Fri']+d1['Sat']+d1['Sun']

dfs['chefmozhours4']['Mon'] = d1['Mon']
dfs['chefmozhours4']['Tue'] = d1['Tue']
dfs['chefmozhours4']['Wed'] = d1['Wed']
dfs['chefmozhours4']['Thu'] = d1['Thu']
dfs['chefmozhours4']['Fri'] = d1['Fri']
dfs['chefmozhours4']['Sat'] = d1['Sat']
dfs['chefmozhours4']['Sun'] = d1['Sun']
dfs['chefmozhours4']['days_of_operation'] =  d1['days_of_operation']


#drop res_df if exists

# for col in res_df:
#     res_df.drop(col,axis=1,inplace=True)
    
#Merge the files to get the rating file
res_df = dfs['chefmozaccepts'].merge(dfs['chefmozcuisine'],on ='placeID' )
res_df = res_df.merge(dfs['chefmozhours4'],on ='placeID' )
res_df = res_df.merge(dfs['chefmozparking'],on ='placeID' )
res_df = res_df.merge(dfs['geoplaces2'],on ='placeID' )
res_rating = res_df.merge(dfs['rating_final'],on ='placeID' )
usr_df = dfs['usercuisine'].merge(dfs['userpayment'],on ='userID' )
usr_df = usr_df.merge(dfs['userprofile'],on ='userID' )
usr_rating = usr_df.merge(dfs['rating_final'],on ='userID' )

s1=["SLP","S.L.P.","s.l.p.","San Luis Potosi","slp","san luis potos","san luis potosi"]
s2 =["tamaulipas","Tamaulipas"]
s3=["morelos","Morelos"]
s4=["?","mexico"]
res_rating['state'] =  res_rating['state'].apply(lambda x: "San Luis Potosi" if x in s1 else x)
res_rating['state'] =  res_rating['state'].apply(lambda x: "Tamaulipas" if x in s2 else x)
res_rating['state'] =  res_rating['state'].apply(lambda x: "Morelos" if x in s3 else x)
res_rating['state'] =  res_rating['state'].apply(lambda x: "Not Determined" if x in s4 else x)

# creating Ranking dataframe for rating chart
filt_cols = ['placeID','name' ,'rating','food_rating','service_rating','state','price','parking_lot']
ranking = pd.DataFrame(res_rating,columns=filt_cols)
ranking['Avg_Rating'] = ranking[['rating','food_rating','service_rating']].mean(axis=1)
ranking = ranking[ranking['state'] != 'Not Determined' ]
ranking['parking_lot'] =  ranking['parking_lot'].apply(lambda x: "Not available" if x in 'none' else x)

APP_TITLE = "Let's discover a few dining options in the vicinity of Mexico"

st.title(APP_TITLE)

#get unique states

rs_st_list = (res_rating['state'].unique())
rs_st_list = rs_st_list.tolist()
rs_st_list.remove('Not Determined') 
sel_st = st.sidebar.selectbox('Select a state to explore your option:',rs_st_list )


rs_cus_list = (res_rating[(res_rating['rating'] > 0) & (res_rating['state'] == sel_st)]['Rcuisine'].unique())
sel_cuisine = st.sidebar.multiselect("Do you want to refine your search on your favorite cuisine", rs_cus_list)

## Display the filtered list
# st.dataframe(sel_cuisine)
APP_SUB_TITLE = "Restaurants of " + sel_st

st.subheader(APP_SUB_TITLE)

if bool(sel_cuisine):
    ranking = ranking[(ranking['state'] == sel_st) & (res_rating['Rcuisine'].isin(sel_cuisine))]
else:
    ranking = ranking[ranking['state'] == sel_st]

tab1,tab2 = st.tabs(['Location and rating','Parking and Price details'])


with tab1: 
    
    #Filter state attributes for map
    if bool(sel_cuisine):
        
        res_rat_filter  = res_rating[(res_rating['rating'] > 0) & (res_rating['state'] == sel_st)& (res_rating['Rcuisine'].isin(sel_cuisine) )]
    else:
        res_rat_filter  = res_rating[(res_rating['rating'] > 0) & (res_rating['state'] == sel_st)]
   
    st.write ('   Explore the map below to locate restaurants in Morelos. Utilize the sidebar to filter by cuisine for specific options. Adjust the zoom level for a more detailed view.')
    st.map(res_rat_filter,  
        latitude = 'latitude',	longitude ='longitude',color= "#396944",zoom = 11, use_container_width = True)
    
    ##
    ##
    
    res_rat_filter  = res_rating[(res_rating['rating'] > 0) & (res_rating['state'] == sel_st)& (res_rating['Rcuisine'] )]
        
    max_slider_len = 30
    ht_list_lmt = st.sidebar.slider("Slide to adjust restaurant list",min_value=5,max_value=max_slider_len,value=10, step=1)
    ranking_g= ranking.groupby(['name','price','parking_lot'], as_index=False).aggregate({'rating':'mean','food_rating':'mean','service_rating':'mean'}).sort_values(by=['rating','food_rating','service_rating'], ascending=False).head(ht_list_lmt)
    st.write ('Below chart displays the details of top '+ str(ht_list_lmt) + 
              ' Restaurants based on Average rating for the selected ' + str(sel_st) + ' and Cuisine.'             
              ' These charts are ranked based on the Top rated Restaurants. Use the slider on the side bar to expand the range of Restaurants')
    
    bars = alt.Chart(ranking_g, title = alt.Title("Top Restaurants based on Rating" )).mark_bar().encode(
    x=alt.X('mean(rating):Q', sort = '-x', title= "Rating"),
    y=alt.Y('name:N',sort=alt.EncodingSortField('rating', op='min', order='descending'), title = "Restaurant Name"),
    color=alt.Color('food_rating',title= "Food Rating",scale=alt.Scale(domain=(0.5, 2))),
    tooltip = ['food_rating','service_rating','price','parking_lot']
    ) 
    text = alt.Chart(ranking_g).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('mean(rating):Q', stack='zero', sort='-x'),
        y=alt.Y('name:N', sort='-x'),
        detail='rating:N',
        text=alt.Text('mean(rating):Q', format='.1f')
    )
    chart = bars + text
    st.altair_chart(chart,theme="streamlit", use_container_width=True)
    
   
    

with tab2:
    st.subheader("Feast on Flavor, Light on the Wallet:")
    st.write('Check this tab for food prices and parking info in '+sel_st + ' restaurants.Narrow your search by choosing your favorite cuisine. Charts rank places by customer-rated food and service. Use the sidebar slider to see more restaurants.')


    # st.write('Browse this tab for  the price of the food and Parking Facilities available for the restaurants from '+sel_st + ' and choose your favorite Cuisine to narrow your search. '
    #             ' The charts are ranked based on food and service rating provide by the customers. Use the slider on the side bar to expand the range of Restaurants')

    ranking_c= ranking.groupby(['name','price','parking_lot'], as_index=False).aggregate({'rating':'mean','food_rating':'mean','service_rating':'mean'}).sort_values(by=['rating','food_rating','service_rating'], ascending=False).head(ht_list_lmt)
    
    # Facet_chart = alt.Chart(ranking_g).mark_bar().encode(
    # x=  alt.X('name',title= None),
    # y= alt.Y('rating', title="Rating"), color = 'parking_lot'
    # ).properties( title="Restaurants categorized based on their Price", width = 200, height = 200).facet(
    #         row = alt.Row('price', sort =["low","medium","high"], header=alt.Header(title="Restaurants Name", titleOrient= 'bottom'))
    # ).resolve_scale(x='independent')
    # st.altair_chart(Facet_chart,theme="streamlit", use_container_width=True)                                                                                    
    # sel_cuisine = st.sidebar.multiselect("Do you want to refine your search on your favorite cuisine", rs_cus_list)
    
    st.subheader (" Discover Low-Cost Culinary Delights!")
    ranking_c1 = ranking_g[ranking_g['price'] == 'low']
    c1_bars = alt.Chart(ranking_c1, title = alt.Title("Top-Rated Restaurants with low Food Prices" )).mark_bar().encode(
        x=alt.X('mean(rating):Q', sort = '-x', title= "Rating"),
        y=alt.Y('name:N',sort=alt.EncodingSortField('rating', op='min', order='descending'), title = "Restaurant Name"),
        color=alt.Color('parking_lot',title= "Parking Availability", sort = 'descending'),

        tooltip = ['food_rating','service_rating','price','parking_lot']
        # order = alt.Order(# Sort the segments of the bars by this field
        #   'Avg_Rating',
        #   sort='descending')
    ) 
    
    c1_text = alt.Chart(ranking_c1).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('mean(rating):Q', stack='zero', sort='-x'),
        y=alt.Y('name:N', sort='-x'),
        detail='rating:N',
        text=alt.Text('mean(rating):Q', format='.1f')
    )
    c1_bars + c1_text
    st.subheader ("Savor the Middle Ground: Where Quality Meets Affordability in Every Bite!")
    ranking_c2 = ranking_g[ranking_g['price'] == 'medium']
    c2_bars = alt.Chart(ranking_c2, title = alt.Title("Medium-Cost Dining Delights!" )).mark_bar().encode(
        x=alt.X('mean(rating):Q', sort = '-x', title= "Rating"),
        y=alt.Y('name:N',sort=alt.EncodingSortField('rating', op='min', order='descending'), title = "Restaurant Name"),
        color=alt.Color('parking_lot',title= "Parking Availability", sort = 'descending'),

        tooltip = ['food_rating','service_rating','price','parking_lot']
        # order = alt.Order(# Sort the segments of the bars by this field
        #   'Avg_Rating',
        #   sort='descending')
    ) 
    c2_text = alt.Chart(ranking_c2).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('mean(rating):Q', stack='zero', sort='-x'),
        y=alt.Y('name:N', sort='-x'),
        detail='rating:N',
        text=alt.Text('mean(rating):Q', format='.1f')
    )
    c2_bars + c2_text
    
    st.subheader ("Moderate on Price, Rich in Flavor: Unveiling Culinary Excellence at the Right Cost!")
    ranking_c3 = ranking_g[ranking_g['price'] == 'high']
    c3_bars = alt.Chart(ranking_c3, title = alt.Title("Pinnacle Dining: High-End Indulgence!")).mark_bar().encode(
        x=alt.X('mean(rating):Q', sort = '-x', title= "Rating"),
        y=alt.Y('name:N',sort=alt.EncodingSortField('rating', op='min', order='descending'), title = "Restaurant Name"),
        color=alt.Color('parking_lot',title= "Parking Availability", sort = 'descending'),

        tooltip = ['food_rating','service_rating','price','parking_lot']
        # order = alt.Order(# Sort the segments of the bars by this field
        #   'Avg_Rating',
        #   sort='descending')
    ) 
    c3_text = alt.Chart(ranking_c3).mark_text(dx=-15, dy=3, color='white').encode(
        x=alt.X('mean(rating):Q', stack='zero', sort='-x'),
        y=alt.Y('name:N', sort='-x'),
        detail='rating:N',
        text=alt.Text('mean(rating):Q', format='.1f')
    )
    c3_bars + c3_text
    
st.header (" Buen Provecho !! ")