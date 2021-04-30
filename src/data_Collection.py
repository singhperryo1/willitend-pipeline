import requests
import pandas as pd
'''
pip3 install requests
pip3 install pandas
'''


def dowload_data():
	url = "https://raw.githubusercontent.com/BloombergGraphics/covid-vaccine-tracker-data/master/data/current-usa.csv"
	df = pd.read_csv(url)
	df_cleaned = df.iloc[0:59]
	df_cleaned.to_csv('Vaccine-Info-State-By-State.csv', encoding='utf-8', index=False)

def update_info_to_database():
	pass


def main():
	dowload_data()
	update_info_to_database()
	
main()


