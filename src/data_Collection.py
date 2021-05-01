import requests
import pandas as pd
import mysql.connector
from datetime import date

'''
To run this Python scripte file,
Please open your terminal and use following commands to install all the required package.
Run each command at a time

pip3 install requests
pip3 install pandas
pip3 install mysql-connector-python

'''

'''
crontabe setting: 
1. type following command : which python3. 
2. Get the absoult path for python3 command. In my case it is : /Library/Frameworks/Python.framework/Versions/3.8/bin/python3. (you may replace this with your own)
3. type crontabe -e in your termial
4. Pree i key from keyboard and copy and paste following command to your crontabe.
	* * * * * /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 ~/Desktop/willitendDataProcess/src/data_Collection.py

5. Press 'ESC' key from keyborad and enter following exactly string(: is included)     :wq                
6. Press  Enter key from keyborad. 

'''


# Configure for your database
destination = "localhost"
user_name = "root"
password = "willitend.com"
datanase_name = "willitend"

# Calculates Days since vaccine was made available
startDate = date(2021, 2, 20)
endDate = date.today()
daysSince = endDate - startDate

# Holds the herd immunity percentage
herdImPercentage = 0.85


def dowload_data():
	print("############################################")
	url = "https://raw.githubusercontent.com/BloombergGraphics/covid-vaccine-tracker-data/master/data/current-usa.csv"
	df = pd.read_csv(url)
	df_cleaned = df.iloc[0:59]
	df_cleaned.to_csv("Vaccine-Info-State-By-State.csv", encoding="utf-8", index=False)
	update_info_to_database(df_cleaned)
	print("process completed")
	print("############################################")

def update_info_to_database(df_cleaned):
	data_base = mysql.connector.connect(host=destination,user=user_name,passwd=password,database = datanase_name)
	temp_cursor = data_base.cursor()
	'''
		Now pick each rows from data frame, 
		and write each row of infomation into the data base.
	'''
	for index, rows in df_cleaned.iterrows():
		insert_into_table(temp_cursor,rows)
	data_base.commit()
	temp_cursor.close()
	data_base.close()

def insert_into_table(temp_cursor,rows):
	state_name = rows['id']
	one_shot_num = int(rows['peopleVaccinated'] - rows['completedVaccination'])
	two_shot_num = int(rows['completedVaccination'])
	if (one_shot_num < 0) or (two_shot_num < 0):
		print("You are trying to write invalid data into database")
		return
	vacc_per_day = two_shot_num/daysSince.days
	state_population = int(rows['population'])
	herd_immunity_population = (int(herdImPercentage * state_population))
	days_to_herd_immunity = (herd_immunity_population-two_shot_num)/vacc_per_day
	temp_str = "INSERT INTO stateinfo (name,hDays,1Shot,2Shot,vacPerDay,hPop,pop) VALUES(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE hDays=%s,1Shot=%s,2Shot=%s,vacPerDay=%s,hPop=%s,pop=%s"
	temp_cursor.execute(temp_str,(state_name,days_to_herd_immunity,one_shot_num,two_shot_num,vacc_per_day,herd_immunity_population,state_population,days_to_herd_immunity,one_shot_num,two_shot_num,vacc_per_day,herd_immunity_population,state_population))


def main():
	dowload_data()

	
main()


