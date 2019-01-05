import pandas as pd
import json
import requests
import urllib.parse
from bokeh.plotting import figure, output_file, show
import os
from flask import Flask,render_template,request,redirect
app_stock = Flask(__name__)

@app_stock.route('/index',methods=["GET","POST"])
def index():   
	if request.method == 'GET':
		return render_template('stock_pick.html')
	else:
		stock_abbr=request.form["abbr_stock"]
		date_start=request.form["start_date"]
		date_end=request.form["end_date"]
	main_url= "https://www.quandl.com/api/v3/datasets/EOD/"
	connection= "?start_date="
	middle_words= "&end_date="
	key_api= "&api_key=G8yRiWzvwHLrbT9oDPGY"
	url=main_url+stock_abbr+connection+date_start+middle_words+date_end+key_api	
	json_data=requests.get(url).json()
	list_jd=json_data['dataset']['data']
	list_date=pd.to_datetime([item[0] for item in list_jd])
	list_close=[item[4] for item in list_jd]  
	df=pd.DataFrame({"date":list_date,"closing price":list_close})
	df=df.reset_index()
	df=df.drop(['index'],axis=1)
	plot_bk=figure(height=300,width=500,x_axis_type="datetime")
	plot_bk.line(list(df['date']),list(df['closing price']),color='blue',alpha=0.5,line_width=2)
	output_file('Stock.html',title="Stock closing price")
	plot_bk.title.text="Closing Stock Price of {} in Selected Month".format(stock_abbr)
	plot_bk.xaxis.axis_label = 'Date'
	plot_bk.yaxis.axis_label = 'Closing Price'
	show(plot_bk)
	return render_template('index.html')

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app_stock.run(host='0.0.0.0', port=port)
