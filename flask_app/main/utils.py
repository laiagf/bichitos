import pandas as pd
import calendar
import plotly 
import plotly.express as px
import json
import plotly.graph_objects as go


def create_pie_chart(df, column):
	fig = px.pie(df[~df[column].isnull()], column)
	fig.update_traces(hoverinfo='label+percent',textposition='inside', textinfo='label+percent', showlegend=True, textfont_size=20)
	fig.update_layout(
	    hoverlabel=dict(
	        font_size=20,
	    )
	)
	
	fig.update_layout(

		annotations = [dict(
	    	x=0.5,
	    	y=-0.11,    #Trying a negative number makes the caption disappear - I'd like the caption to be below the map
	    	xref='paper',
	    	yref='paper',
	    	text=column +' for games played in 2023.',
		font=dict(size=16, family='Lato, sans-serif')

    	)])#,

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON

def create_gamesxmonth_chart(df):
	df['month'] = df.date.dt.month
	df_f_ms = df.groupby(['month']).month.agg('count').to_frame('Count')
	for i in range(1, 13):
	    if i not in list(df_f_ms.index):
	        df_f_ms.loc[i]= [0]

	df_f_ms = df_f_ms.reset_index()
	df_f_ms.sort_values('month', inplace=True)
	df_f_ms.month = df_f_ms['month'].apply(lambda x: calendar.month_abbr[x])
	df_f_ms
	fig = px.bar(df_f_ms, x='month', y='Count')
	fig.update_layout(

	annotations = [dict(
    	x=0.5,
    	y=-0.32,    #Trying a negative number makes the caption disappear - I'd like the caption to be below the map
    	xref='paper',
    	yref='paper',
    	text='Number of games played per month in 2023',
	font=dict(size=16, family='Lato, sans-serif')

	)])#,
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON

def create_morale_chart(df):
	df_filtered_m = df[~df.avg_morale.isnull()]
	morale_convertor = {'high':5, 'low':1, 'medium':3, 'medium-high':4, 'medium-low':2}
	m_values = []
	for i in df_filtered_m.index:
	    m_values.append(morale_convertor[df_filtered_m.avg_morale[i]])
	#df_filtered['morale_value'] = 0
	df_filtered_m['morale_value'] = m_values
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df_filtered_m.date, y=df_filtered_m.morale_value, name="morale",
	                    hoverinfo='text+name',
	                    line_shape='spline'))

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON