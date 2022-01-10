# Core Pkgs
import streamlit as st
import streamlit.components.v1 as stc 
import SessionState
from module_wareneingang import *
from crud_operations import *
from math import ceil
#import SessionState 
import altair as alt
import pymysql
from PIL import Image
img = Image.open("/Users/danielbluemlein/Library/Mobile Documents/com~apple~CloudDocs/KI Beratung & Entwicklung/00_Gründung/Logo/Standard Logo Files/Original on Transparent.png")

# Load EDA Pkg
import pandas as pd 
import numpy as np 

# Load Data Vis Pkg
import plotly.express as px

# DB connection
conn = pymysql.connect(database = 'data', user = 'root', password = '')
cursor = conn.cursor()
query = "SELECT * FROM wareneingang LIMIT 100"
df = pd.read_sql(query, conn)


label_dict = {"No":0,"Yes":1}
gender_map = {"Female":0,"Male":1}
target_label_map = {"Negative":0,"Positive":1}

html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Early Stage DM Risk Data App </h1>
		<h4 style="color:white;text-align:center;">Diabetes </h4>
		</div>
		"""

def get_fvalue(val):
	feature_dict = {"No":0,"Yes":1}
	for key,value in feature_dict.items():
		if val == key:
			return value 

def get_value(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return value 

def main():
        st.set_page_config(page_title="WE", layout="wide",
                initial_sidebar_state="auto")
        st.sidebar.image(img)
        rad = st.sidebar.selectbox("Menü", ["Übersicht", "Prognose"])

        if rad == "Übersicht":
        
                #st.sidebar.write("Übersicht")
                #st.sidebar.write("Prognose")
                st.sidebar.button("Einstellungen")

                

                
                st.title("Wareneingang - Eigenfertigung")

                #search inputs
                col1, col2 = st.columns(2)
                with col1:
                        art_nr = st.text_input("Artikelnummer einscanen")
                        st.write(art_nr)
                with col2:
                        lieferanten_nr = st.text_input("Lieferantennummer einscanen")
                        st.write(lieferanten_nr)

                message = st.text_area("Volltextsuche",height=50)
                st.write(message)

                # Date Input
                col01, col02, col03 = st.columns(3)

                with col01:
                        myappointment = st.date_input("Suche nach exaktem Datum")
                        #df = pd.read_csv("/Users/danielbluemlein/Documents/Dokumente - Daniels MacBook Pro/Data Science/Tutorials/Projekte/Wareneingang/data/archive/archive/.wareneingang_preprocessed.csv.icloud")

                with col02:
                        slider = st.date_input("Suche nach Zeitraum", [])
                        st.write(slider)
                        
                # DataFrame mehr anzeigen
                N = 20 # Number of entries per screen
                prev, _ ,next = st.columns([0.1, 0.8, 0.1])
                last_page = len(df) // N
                session_state = SessionState.get(page_number = 0)

                if next.button("Next"):

                    if session_state.page_number + 1 > last_page:
                        session_state.page_number = 0
                    else:
                        session_state.page_number += 1

                with _:
                        st.write("")

                if prev.button("Previous"):

                    if session_state.page_number - 1 < 0:
                        session_state.page_number = last_page
                    else:
                        session_state.page_number -= 1

                # Get start and end indices of the next page of the dataframe
                start_idx = session_state.page_number * N 
                end_idx = (1 + session_state.page_number) * N
                
                # Index into the sub dataframe
                sub_df = df.iloc[start_idx:end_idx]
                st.write(sub_df)             
                
                

                st.header("")

                col1, col2, col3 = st.columns(3)
                col1.metric(label="Wareneingänge heute insgesamt", value = len(df), delta="-28 seit gestern")
                col2.metric(label="davon mit Fehlern", value = "1", delta="100 %")
                col3.metric(label="Teile insgesamt", value = int(df['liefer_menge'].sum()), delta="100 %")

                st.header("")

                col3, col4, col5 = st.columns([0.33,0.33,0.33])

                with col3:
                        fig = px.pie(df,color_discrete_sequence=px.colors.sequential.dense,width=400, height=400, values='bauraumkenner',names='bauraumkenner',title='Bauraumkenner')
                        st.plotly_chart(fig)


                with col4:
                        fig1 = px.pie(df,color_discrete_sequence=px.colors.sequential.dense,width=400, height=400, names='fehler_klein',title='Anzahl kleiner Fehler')
                        st.plotly_chart(fig1)

                with col5:
                        fig2 = px.pie(df,color_discrete_sequence=px.colors.sequential.dense,width=400, height=400, names='fehler_gros',title='Anzahl großer Fehler')
                        st.plotly_chart(fig2)

        
                
                #LineChart
                #chart=pd.DataFrame(np.random.randn(20,3),columns=['a','b','c'])
                #st.line_chart(chart)

                data=px.data.stocks()
                fig = px.line(data,height=600,width=1300,x='date',y='GOOG',labels={"date":"Datum","GOOG":"Verhältnis (100%)"},title="Anzahl Wareneingänge im Verhältnis zum Durchschnitt der letzten 30 Tage", color_discrete_sequence=px.colors.qualitative.Set1)
                fig.add_scatter( x=data.date, y=np.ones(len(data)) , mode='lines', name = 'Mittel', line = dict(color='grey', width=1.5, dash='dash'))
                st.plotly_chart(fig)

        if rad == "Prognose":
                st.title("Wareneingangsprognose")
                st.subheader("Bisherige Wareneingangsdaten:")
                st.dataframe(df)
                
                #Formular
                st.subheader("Neuen Wareneingang anlegen")
                #with st.form(key='my-form'):
        

                formcol1, formcol2 = st.columns(2)
                
                with formcol1:
                        werk = st.selectbox('Werk', ['100', '200', '300'])
                        art_nr = st.number_input('Artikelnummer', 0, 10)
                        lieferanten_nummer = st.number_input('Lieferantennummer', 0, 10)
                        liefer_menge = st.number_input('Liefermenge', 0, 10)
                        bestell_menge = st.number_input('Bestellmenge', 0, 10)
                        lieferanten_art = st.selectbox('Lieferantenart', ['100', '200', '300'])

                with formcol2:
                        lieferanten_gruppe = st.selectbox('Lieferantengruppe', ['100', '200', '300'])
                        abc = st.selectbox('ABC-Klasse', ['100', '200', '300'])
                        artikel_status = st.selectbox('Artikelstatus', ['100', '200', '300'])
                        artikel_art = st.selectbox('Artikelart', ['100', '200', '300'])
                        beschaffungskenner = st.selectbox('Beschaffungskenner', ['100', '200', '300'])
                        bauraumkenner = st.selectbox('Bauraumkenner', ['100', '200', '300'])

                

                with st.expander("Your Selected Options"):
                        
                        result = {'werk':werk,
                        'art_nr':art_nr,
                        'lieferanten_nummer':lieferanten_nummer,
                        'liefer_menge':liefer_menge,
                        'bestell_menge':bestell_menge,
                        'lieferanten_art':lieferanten_art,
                        'lieferanten_gruppe':lieferanten_gruppe,
                        'abc':abc,
                        'artikel_status':artikel_status,
                        'artikel_art':artikel_art,
                        'beschaffungskenner':beschaffungskenner,
                        'bauraumkenner':bauraumkenner}
                        st.write(result)
                        encoded_result = []
                        for i in result.values():
                                if type(i) == int:
                                        encoded_result.append(i)
                                elif i in ["Female","Male"]:
                                        res = get_value(i,gender_map)
                                        encoded_result.append(res)
                                else:
                                        encoded_result.append(get_fvalue(i))


                        # st.write(encoded_result)
                                
                        

        st.write('Press submit to have your name printed below')
        submit = st.button('Submit')
                

        if submit:
                model = wareneingang_model('model.pkl')
                df_mysql = model.load_and_clean_data('SELECT * FROM wareneingang LIMIT 10')
                #st.dataframe(df_mysql)
                st.write(model.predicted_outputs())
                st.write(f'hello {werk}')
                #st.write(insert_row(conn, 'wareneingang', werk, art_nr, lieferanten_nummer, bestell_menge,liefer_menge, lieferanten_gruppe, abc, artikel_status, artikel_art, beschaffungskenner, bauraumkenner, lieferanten_art))
	



if __name__ == '__main__':
	main()
