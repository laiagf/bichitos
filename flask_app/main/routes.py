
from flask import render_template, Blueprint
#from  flask_app.main.forms import AEoutputsForm
from omegaconf import OmegaConf
import pandas as pd
from flask_app.main.utils import *

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def home():

	df = pd.read_excel('bichos2023.xlsx')
	df_filtered = df[[c for c in df.columns if not c[0:3].isupper()]]
	df_filtered.drop([0], inplace=True)
	players = [c for c in df_filtered.columns if c not in ['date', 'game', 'no_players', 'total_bichos', 'avg_morale',
       'time_of_day', 'laisdesk', 'gamelocation', 'comments', 'month']]
	df_filtered['winner'] = ''
	df_filtered.reset_index(drop=True, inplace=True)
	for i in df_filtered.index:
	    x = list(df_filtered[players].iloc[i])
	    x = [0 if r=='na' else r for r in x]
	    df_filtered.winner[i] = players[x.index(max(x))]


	games_played = []
	games_won = []
	for p in players:
	    games_played.append(len(df_filtered[df_filtered[p]!='na']))
	    games_won.append(len(df_filtered[df_filtered.winner==p]))
	    

	df_players = pd.DataFrame({'Player': players, 'games_played': games_played, 'games_won': games_won})

	df_players['win_ratio'] = 100*df_players['games_won']/df_players['games_played']
	df_players['win_ratio'] = df_players['win_ratio'].round(0)

	df_top_players = df_players[df_players['games_played']>2]

	pie_chart1 = create_pie_chart(df_filtered, 'avg_morale')
	pie_chart2 = create_pie_chart(df_filtered, 'time_of_day')
	pie_chart3 = create_pie_chart(df_filtered, 'laisdesk')
	pie_chart4 = create_pie_chart(df_filtered, 'gamelocation')

	games_month_chart = create_gamesxmonth_chart(df_filtered)


	morale_chart = create_morale_chart(df_filtered)


	return render_template('welcome.html', title="Welcome!", df_top_players = df_top_players, 
		pie_chart1=pie_chart1, pie_chart2=pie_chart2, pie_chart3=pie_chart3, pie_chart4=pie_chart4,
		games_month_chart=games_month_chart, morale_chart=morale_chart)

@main.route('/league')
def league():

	df = pd.read_excel('bichos2023.xlsx')
	df_filtered = df[[c for c in df.columns if not c[0:3].isupper()]]
	df_filtered.drop([0], inplace=True)
	players = [c for c in df_filtered.columns if c not in ['date', 'game', 'no_players', 'total_bichos', 'avg_morale',
       'time_of_day', 'laisdesk', 'gamelocation', 'comments', 'month']]
	df_filtered['winner'] = ''
	df_filtered.reset_index(drop=True, inplace=True)
	for i in df_filtered.index:
	    x = list(df_filtered[players].iloc[i])
	    x = [0 if r=='na' else r for r in x]
	    df_filtered.winner[i] = players[x.index(max(x))]


	games_played = []
	for p in players:
	    games_played.append(len(df_filtered[df_filtered[p]!='na']))
	    
	df_players = pd.DataFrame({'Player': players, 'games_played': games_played})


	df_top_players = df_players[df_players['games_played']>2]

	df_top_players.reset_index(drop=True, inplace=True)
	top_players = list(df_top_players.Player)
	df_top_players['people_played'] = ''

	matches = []
	for i in df_top_players.index:
	    p = df_top_players.Player[i]
	    df_player = df_filtered[df_filtered[p]!='na']
	    player_matches = []
	    for j in df_top_players.index:
	        p2 = df_top_players.Player[j]
	        s = [score for score in list(df_player[p2]) if score != 'na']
	        player_matches.append(len(s))
	    df_top_players.people_played[i] = len([player_matches[k] for k in range(len(player_matches)) if k!=i and player_matches[k]!=0])
	    matches.append(player_matches)


	df_top_players.sort_values('people_played', inplace=True, ascending=False)

	dropped_players = []
	for i in df_top_players.index:
	    if i not in dropped_players:
	        player_matches = matches[i]
	        dropped_players = dropped_players + [i for i, x in enumerate(player_matches) if x == 0]
	
	df_league_players = df_top_players[~df_top_players.index.isin(dropped_players)]