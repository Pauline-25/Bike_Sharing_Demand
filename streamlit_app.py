import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import datetime

import plotly.express as px
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

st.set_page_config(layout="centered", page_icon="🚲", page_title="Bike Rental")
showWarningOnDirectExecution = False

st.write('# Bike Rental')

st.write('Our dataset is about bike sharing. For each hour of 2011 and 2012, we have the total number of bikes rent at one specific station, by registered and non-registered clients. We also have peripheric information about the type of day and the weather.') 
st.write('This dataset addresses a concrete issue of our daily lives, which makes it very interesting to visualize! Don\'t forget that bike is one of the most ecological mean of transport and is going to be more and more frequent in our cities in the future. Since it is time-based, you will understand the evolution of bike demand, peak and off hours, etc.')
st.write('Happy visualizing!')

st.write('## Average bike rental over two years')

st.write('First of all, let\'s have a global overview of, on average, how much bikes have been rent at the station at each month.')
st.write('You can already select the month we\'ll explore in part 2!')
# @st.cache decorator skip reloading the code when the apps rerun.

dico_indx_weekday = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
list_months = ['January','February','March','April','May','June','July','August','September','October','November','December']
dico_indx_month = {i:m for i,m in zip(list(range(1,13)),list_months)}
dico_month_indx = {m:i for i,m in zip(list(range(1,13)),list_months)}

dico_weather = {1:"☀️",2:"☁️",3:"🌧️",4:"⛈️"}
dico_weather_ = {"☀️":1,"☁️":2,"🌧️":3,"⛈️":4}
dico_working_day = {"Scholar period 🖊️":0, "Holiday 🏖️":1}
dico_weekend = {"Weekday 💼":0, "Weekend 🥳":1}

df = pd.read_csv('bike.csv')
df.datetime = pd.to_datetime(df.datetime)
df['month'] = df.datetime.dt.month
df['hour'] = df.datetime.dt.hour
df['year'] = df.datetime.dt.year
df['first_day_of_month'] = df.datetime.apply(lambda date : datetime.date(date.year, date.month, 1))
df['weekday'] = df.datetime.apply(lambda x : dico_indx_weekday[x.weekday()])


#######

col1, col2 = st.columns([4,1])

with col1:
    chosen_month = st.select_slider(
        'Select month to display average bike rental in part 2',
        options = list_months
        )

with col2:
    chosen_year = st.selectbox('Year', [2011,2012])

#########

# df_test = (pd.DataFrame(df.groupby(['first_day_of_month'])
#                         .agg({'casual':'mean','registered':'mean'})
#                         .astype('int')))

# st.area_chart(df_test)

def relative_number(row):
    if row.client_type == 'registered':
        return row.number
    else :
        return -row.number

df_monthly_mean = (pd.DataFrame(df.groupby(['first_day_of_month'])
        .agg({'casual':'mean','registered':'mean'})
        .astype('int').stack())
        .reset_index()
        .rename(columns={'level_1':'client_type',0:'number'})
        )

df_monthly_mean['relative_number'] = df_monthly_mean.apply(relative_number,axis=1)
df_monthly_mean['month_year'] = df_monthly_mean['first_day_of_month'].apply(lambda x: x.strftime('%B %Y')) 

# st.write(df_monthly_mean)

fig1 = px.area(df_monthly_mean, 
              x = "first_day_of_month", 
              y = "relative_number", 
              color = "client_type",
              custom_data = ['number','month_year'],
              # color_discrete_map = {"registered": "yellow", "casual": "blue"},
              title = 'Average number of bikes rent per hour'
              )

fig1.add_hline(y=0, line_color='white') 
fig1.add_vline(x=datetime.date(chosen_year, dico_month_indx[chosen_month], 1), 
              line_color='red')      

fig1.update_traces(hovertemplate = '%{customdata[1]} <br> Bikes rent: %{customdata[0]}')

fig1.update_layout(
    yaxis=dict(
        title_text = "Number of bikes rent",
        tickmode='array',
        tickvals=[-50, 0, 50, 100, 150, 200, 250],
        ticktext=[ 50, 0, 50, 100, 150, 200, 250]
    ),
    xaxis = dict(
        title_text = "Month and year"
    ),
    legend_title_text = 'Client type',
)


st.plotly_chart(fig1, use_container_width=True)

# selected_points = plotly_events(fig1, click_event=True, hover_event=False, select_event=False)

# date = ''
# for element in selected_points:
#     date = element["x"]

# try :
#     year = int(date[:4])
#     month = int(date[5:7])
# except:
#     year = 2011
#     month = 1

# df_year_month = df[(df.year==year) & (df.month==month)]



# import plotly.graph_objects as go
  
# df_monthly_mean_casual = df_monthly_mean[df_monthly_mean.client_type=='casual']
# df_monthly_mean_registered = df_monthly_mean[df_monthly_mean.client_type=='registered']

# fig2 = go.Figure()

# fig2.add_trace(go.Scatter(
#      x= df_monthly_mean[df_monthly_mean.client_type=='casual']['first_day_of_month'], 
#      y = - df_monthly_mean[df_monthly_mean.client_type=='casual']['number'],
#      name = 'Casual',
#      mode = 'lines',
#      line=dict(width=0.5, color='orange'),
#      stackgroup = 'one'
#      )
# )

# fig2.add_trace(go.Scatter(
#      x= df_monthly_mean[df_monthly_mean.client_type=='registered']['first_day_of_month'], 
#      y = df_monthly_mean[df_monthly_mean.client_type=='registered']['number'],
#      name = 'Registered',
#      mode = 'lines',
#      line=dict(width=0.5,color='lightgreen'),
#      stackgroup = 'two'))

# fig2.update_layout(
#     yaxis=dict(
#         title_text = "Number of bikes rent",
#         tickmode='array',
#         tickvals=[-50, 0, 50, 100, 150, 200, 250],
#         ticktext=[50, 0, 50, 100, 150, 200, 250]
#     )
# )

# st.plotly_chart(fig2,use_container_width=True)




# base_1 = alt.Chart(df_monthly_mean)

# area_1 = base_1.mark_area(opacity=0.3).encode(
#             x=alt.X('first_day_of_month:T',title='Month'),
#             y=alt.Y("number:Q", title='Number of bikes rent', stack='center'),
#             tooltip=['number'],
#             color="client_type:N"
#         ).properties(width=800,
#                     height=300
#                     )


# xrule_1 = base_1.mark_rule(color="red", 
#                               strokeWidth=2, 
#                               fill='red', 
#                               stroke='red'
#                               ).encode(x=alt.datum(alt.DateTime(month=chosen_month,year=chosen_year)))

# st.altair_chart(area_1 + xrule_1, use_container_width=True)

#############################

st.write("## Average bike rental in the selected month")

st.write(f'Great, let\'s understand the bike rental in {chosen_month} {chosen_year}. First, you can eather see, on average, how much bikes have been rent in {chosen_month} {chosen_year} per hour. But you can also play with the day type and whether in order to understand their impact!')

def filter_dataset(month = None,
                   year = None,
                   holiday = True,
                   not_holiday = True,
                   weekend = True,
                   weekday = True,
                   weather = None,
                   temperature_up = None,
                   temperature_down = None,
                   humidity_up = None,
                   humidity_down = None,
                   windspeed_up = None,
                   windspeed_down = None,):

    df_result = df.copy()

    if month is not None :
        if isinstance(month,int):
            df_result = df_result[df_result.month == month]
        else :
            df_result = df_result[df_result.month == dico_month_indx[chosen_month]]
    if year is not None :
        df_result = df_result[df_result.year == year]    

    holiday_choice = []
    if holiday:
        holiday_choice.append(1)
    if not_holiday:
        holiday_choice.append(0)
    df_result = df_result[df_result.holiday.isin(holiday_choice)]

    weekdays_choice = []
    if weekday:
        weekdays_choice.append(1)
    if weekend:
        weekdays_choice.append(0)

    df_result = df_result[df_result.workingday.isin(weekdays_choice)]

    if weather is not None :
        df_result = df_result[df_result.weather == weather]
    if temperature_up is not None :
        df_result = df_result[(df_result.temp < temperature_up + 0.5) & (df_result.temp > temperature_down - 0.5) ] 
    if humidity_up is not None :
        df_result = df_result[(df_result.humidity < humidity_up + 0.5) & (df_result.humidity > humidity_down - 0.5) ]
    if windspeed_up is not None :
        df_result = df_result[(df_result.windspeed < windspeed_up + 0.5) & (df_result.windspeed > windspeed_down - 0.5) ]
    return df_result  

df_month_year = filter_dataset(month=chosen_month, year = chosen_year)

def frequent_weather(df):

    mode_weather = df.weather.mode().iloc[0]
    q1_temperature = int(df.temp.quantile(0.25))
    q3_temperature = int(df.temp.quantile(0.75))+1
    q1_humidity = int(df.humidity.quantile(0.25))
    q3_humidity = int(df.humidity.quantile(0.75))+1
    q1_windspeed = int(df.windspeed.quantile(0.25))
    q3_windspeed = int(df.windspeed.quantile(0.75))+1

    return (mode_weather, 
            q1_temperature, 
            q3_temperature, 
            q1_humidity, 
            q3_humidity,
            q1_windspeed,
            q3_windspeed)

mode_weather, q1_temperature, q3_temperature, q1_humidity, q3_humidity, q1_windspeed, q3_windspeed = frequent_weather(df_month_year) 

chosen_display = st.radio('Do you want to play with weather and working days ?', 
                          ["Yes I want to change the parameters!",
                           "No, show me the mean bike rental in "+chosen_month+' '+str(chosen_year)],
                          index = 1)

if chosen_display[0] == 'Y' :

    st.write('### Select the day type')
    col1, col2 = st.columns(2)

    with col1 :
        st.write('Day of week')
        weekday = st.checkbox("Weekday 💼",True)
        weekend = st.checkbox("Weekend 🥳",True)

    with col2 :
        st.write('Vacation')
        not_holiday = st.checkbox("Scholar period 🖊️",True)
        holiday = st.checkbox("Holiday 🏖️",True)
    
    st.text("")

    st.write('### Select the weather')
    st.write(f'The default range values of the slider are the first and third quantile of the weather in {chosen_month} {chosen_year}.')
    col1, col2, col3, col4 = st.columns(4)
    with col1 :
        chosen_weather = dico_weather_[st.select_slider('Weather',
                                          options = ["☀️","☁️","🌧️","⛈️"],
                                          value = dico_weather[mode_weather]
                                         )]

    with col2 :
        temperature_down, temperature_up = st.slider(label='Temperature (°C)',
                                    min_value=int(df.temp.min()),
                                    max_value=int(df.temp.max()),
                                    step=1,
                                    value = (q1_temperature, q3_temperature),
                                    )
                   

    with col3 : 
        humidity_down, humidity_up = st.slider(label='Humidity',
                                    min_value=df.humidity.min(),
                                    max_value=df.humidity.max(),
                                    value = (q1_humidity, q3_humidity)
                                    )

    with col4 : 
        windspeed_down, windspeed_up = st.slider(label='Windspeed',
                                    min_value=int(df.windspeed.min()),
                                    max_value=int(df.windspeed.max()),
                                    value=(q1_windspeed, q3_windspeed),
                                    step = 1,
                                    )                                   

else :
    chosen_weather = None
    temperature_up = None
    temperature_down = None 
    humidity_up = None
    humidity_down = None
    windspeed_up = None
    windspeed_down = None
    holiday = True
    not_holiday = True
    weekend = True
    weekday = True

def df_preprocessed(dataframe):
    return (pd.DataFrame(dataframe.groupby('hour')
                                  .agg({'casual':'mean','registered':'mean'})
                                  .stack()
                                  ).reset_index()
                                   .rename(columns={'level_1':'client_type',0:'number'}))

df_filtered= filter_dataset(month=chosen_month,
                            year=chosen_year,
                            holiday = holiday,
                            not_holiday = not_holiday,
                            weekend = weekend,
                            weekday = weekday,
                            weather = chosen_weather,
                            temperature_up = temperature_up,
                            temperature_down = temperature_down,
                            humidity_up = humidity_up,
                            humidity_down = humidity_down,
                            windspeed_up = windspeed_up,
                            windspeed_down = windspeed_down)


if len(df_filtered) == 0:
    st.error('Such conditions don\'t coexist! Please change either the date, the weather of the day type.')

# st.write(total_bikes)
# st.write(f'Only {len(df_filtered)//24} days and {len(df_filtered)%24} hours are taken into account')

complementary_information = ' with set weather and day type' if chosen_display[0] == 'Y' else ''

df_filtered_and_preprocessed = df_preprocessed(df_filtered)
df_filtered_and_preprocessed['round_number'] = df_filtered_and_preprocessed.number.astype(int)

fig2 = px.line(df_filtered_and_preprocessed, 
              x="hour", 
              y="number", 
              color='client_type',
              custom_data = ['round_number'],
              title = "Average number of bikes rent hourly in "+chosen_month+' '+str(chosen_year)+complementary_information,
              height=600)

fig2.update_traces(hovertemplate = 'At %{x}h, %{customdata[0]} bikes rent')

fig2.update_layout(
    yaxis=dict(
        title_text = "Number of bikes rent",
    ),
    xaxis = dict(
        title_text = "Hour of day"
    ),
    legend_title_text = 'Client type',
)

fig2.update_yaxes(range=[-200, 650])
# st.plotly_chart(fig2, use_container_width=True)

selected_points = plotly_events(fig2, click_event=True, hover_event=False, select_event=False)


# base_2 = alt.Chart(df_preprocessed(df_filtered)
#                     .assign(round_number = lambda x : x['number'].astype(int))
#                     .drop(columns=['number']))

# graph_2 = base_2.mark_line(point = False).encode(
#                 x = alt.X("hour:O", title="Hour of day"),
#                 y = alt.Y("round_number:Q", title="Number of bikes rent", scale = alt.Scale(domain=[0,650])),
#                 color = alt.Color("client_type:N",title='Client Type'),
#                 tooltip = alt.Tooltip("round_number:Q", title="Number of bikes rent")
#             ).properties(
#                 title="Average number of bikes rent hourly in "+chosen_month+' '+str(chosen_year)+complementary_information,
#                 width=700,
#                 height=600,
#             )

# hover = alt.selection_single(
#         fields=["round_number"],
#         nearest=True,
#         on="mouseover",
#         empty="none",
#     )

# tooltips = (base_2
#             .mark_rule()
#             .encode(
#                 x = alt.X("hour:O", title="Hour of day"),
#                 y = alt.Y("round_number:Q",title="Number of bikes rent"),
#                 opacity=alt.condition(hover, alt.value(0.1), alt.value(0)),
#                 tooltip=[
#                     alt.Tooltip("round_number:Q", title="Number of bikes rent"),
#                     alt.Tooltip("client_type:N",title='Client Type'),
#                 ],
#             )
#             .add_selection(hover))

# st.altair_chart(graph_2+tooltips,use_container_width=True)



#################

import base64

file = open("biker.gif", "rb")
contents = file.read()
data_url = base64.b64encode(contents).decode("utf-8")
file.close()

conditions = ' and under those conditions!' if chosen_display[0] == 'Y' else '.'
total_bikes_per_hour = int(df_filtered['count'].sum() / len(df_filtered))
st.write(f'There is an average of {total_bikes_per_hour} bikes rent at this station per hour in {chosen_month} {chosen_year}'+conditions)
nb_bikes_to_display = min(total_bikes_per_hour // 70 + 1 , 4)

st.write('The more people rent bikes, the more bikers are displayed!')

col1, col2, col3, col4 = st.columns(4)

with col1:
    
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )

with col2:
    if nb_bikes_to_display > 1 :
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
        )

with col3:
    if nb_bikes_to_display > 2 :
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
        )

with col4:
    if nb_bikes_to_display > 3 :
        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
        )

####################################

st.write('## Repartition of the bike rental on the selected hour')

if selected_points == []:
    st.write('You haven\'t selected any hour. Please click on the preceding graph to select an hour!')
else :
    for element in selected_points :
        hour = int(element["x"])
        break
    st.write(f'Let\'s see the repartiton of the bike rentals at {hour}h on the different days of the week.')

    df_hour = df[df.hour==hour][['weekday','casual','registered']]
    
    fig3 = go.Figure()

    fig3.add_trace(go.Violin(x=df_hour['weekday'],
                            y=df_hour['registered'],
                            legendgroup='Registered', 
                            scalegroup='Registered', 
                            name='Registered',
                            side='positive',
                            line_color='orange')
                )

    fig3.add_trace(go.Violin(x=df_hour['weekday'],
                            y=df_hour['casual'],
                            legendgroup='Casual', 
                            scalegroup='Casual', 
                            name='Casual',
                            side='negative',
                            line_color='blue')
                )


    fig3.update_traces(meanline_visible=True)
    fig3.update_layout(title=f"Repartition of bike rental at {hour}h",
                        xaxis_title="Days of week",
                        yaxis_title="Number of bikes rents",
                            violingap=0, 
                      violinmode='overlay')
    
    st.plotly_chart(fig3,use_container_width=True)


# import altair as alt
# from vega_datasets import data

# source = data.seattle_weather.url

# step = 20
# overlap = 1

# chart = alt.Chart(source, height=step).transform_timeunit(
#     Month='month(date)'
# ).transform_joinaggregate(
#     mean_temp='mean(temp_max)', groupby=['Month']
# ).transform_bin(
#     ['bin_max', 'bin_min'], 'temp_max'
# ).transform_aggregate(
#     value='count()', groupby=['Month', 'mean_temp', 'bin_min', 'bin_max']
# ).transform_impute(
#     impute='value', groupby=['Month', 'mean_temp'], key='bin_min', value=0
# ).mark_area(
#     interpolate='monotone',
#     fillOpacity=0.8,
#     stroke='lightgray',
#     strokeWidth=0.5
# ).encode(
#     alt.X('bin_min:Q', bin='binned', title='Maximum Daily Temperature (C)'),
#     alt.Y(
#         'value:Q',
#         scale=alt.Scale(range=[step, -step * overlap]),
#         axis=None
#     ),
#     alt.Fill(
#         'mean_temp:Q',
#         legend=None,
#         scale=alt.Scale(domain=[30, 5], scheme='redyellowblue')
#     )
# ).facet(
#     row=alt.Row(
#         'Month:T',
#         title=None,
#         header=alt.Header(labelAngle=0, labelAlign='right', format='%B')
#     )
# ).properties(
#     title='Seattle Weather',
#     bounds='flush'
# ).configure_facet(
#     spacing=0
# ).configure_view(
#     stroke=None
# ).configure_title(
#     anchor='end'
# )

# st.altair_chart(chart,use_container_width=True)

# import altair as alt
# import pandas as pd
# import streamlit as st
# from vega_datasets import data

# @st.experimental_memo
# def get_data():
#     source = data.stocks()
#     source = source[source.date.gt("2004-01-01")]
#     return source

# source = get_data()

# def get_chart(data):
#     hover = alt.selection_single(
#         fields=["date"],
#         nearest=True,
#         on="mouseover",
#         empty="none",
#     )

#     lines = (
#         alt.Chart(data, title="Evolution of stock prices")
#         .mark_line()
#         .encode(
#             x="date",
#             y="price",
#             color="symbol",
#         )
#     )

#     # Draw points on the line, and highlight based on selection
#     points = lines.transform_filter(hover).mark_circle(size=65)

#     # Draw a rule at the location of the selection
#     tooltips = (
#         alt.Chart(data)
#         .mark_rule()
#         .encode(
#             x="yearmonthdate(date)",
#             y="price",
#             opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
#             tooltip=[
#                 alt.Tooltip("date", title="Date"),
#                 alt.Tooltip("price", title="Price (USD)"),
#             ],
#         )
#         .add_selection(hover)
#     )
#     return (lines + points + tooltips).interactive()



# chart = get_chart(source)

# # Input annotations
# ANNOTATIONS = [
#     ("Mar 01, 2008", "Pretty good day for GOOG"),
#     ("Dec 01, 2007", "Something's going wrong for GOOG & AAPL"),
#     ("Nov 01, 2008", "Market starts again thanks to..."),
#     ("Dec 01, 2009", "Small crash for GOOG after..."),
# ]

# # Create a chart with annotations
# annotations_df = pd.DataFrame(ANNOTATIONS, columns=["date", "event"])
# annotations_df.date = pd.to_datetime(annotations_df.date)
# annotations_df["y"] = 0
# annotation_layer = (
#     alt.Chart(annotations_df)
#     .mark_text(size=15, text="⬇", dx=0, dy=0, align="center")
#     .encode(
#         x="date:T",
#         y=alt.Y("y:Q"),
#         tooltip=["event"],
#     )
#     .interactive()
# )

# # Display both charts together
# st.altair_chart((chart + annotation_layer).interactive(), use_container_width=True)