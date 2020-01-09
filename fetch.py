from bs4 import BeautifulSoup as bs
from datetime import datetime
import ssl
import pandas as pd 
import urllib.request
import re


def get_num_launches(output_path):
	#skipping SSL verification
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	#Reading the HTML
	wiki_page = urllib.request.urlopen("https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches",context=ctx).read()

	#Convert HTML table into dataframe
	table_df = pd.read_html(wiki_page)[3]

	data_dict = {}

	for index, row in table_df.iterrows():
		outcome = row[-1]
		try:
			date_with_time = re.search(r'\d+\s[a-zA-Z]+\d?\d?\:?\d?\d?:?\d?\d?',row[0]).group(0)
			date = datetime.strptime('2019 '+re.search(r'\d+\s[a-zA-Z]+',row[0]).group(0),'%Y %d %B')
		except AttributeError:
			continue
		if date not in data_dict.keys():
			if date=="7 December":
				print(outcome)
			if outcome ==  'Successful' or outcome == 'Operational' or outcome == 'En Route':
				data_dict[date] = [1,[date_with_time]]
			else:
				data_dict[date] = [0,[]]
		else:
			if outcome ==  'Successful' or outcome == 'Operational' or outcome == 'En Route':
				if date_with_time not in data_dict[date][1]:
					data_dict[date][1].append(date_with_time)
					data_dict[date][0] = data_dict[date][0]+1

	#Generating date range for the output
	
	date1 = '2019-01-01'
	date2 = '2019-12-31'
	dates = pd.date_range(date1, date2).tolist()

	output_csv = open(output_path,'w')

	for ind_date in dates:
		day = ind_date.to_pydatetime()
		if day in data_dict:
			output_csv.write(str(day.isoformat())+'.00:00'+","+str(data_dict[day][0])+"\n")
		else:
			output_csv.write(str(day.isoformat())+'.00:00'+",0\n")

	output_csv.close()

if __name__ == "__main__":
	get_num_launches("./output.csv")
	
	
