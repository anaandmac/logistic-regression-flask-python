from flask import Flask, request, jsonify,render_template
# from sklearn.externals import joblib
import traceback
import pandas as pd
import numpy as np
import pickle
import csv
import datetime as dt



app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
# def hello():
#     return "API para score boleto Oi"

def index():
	return render_template('index.html')

@app.route('/data',methods=['GET','POST'])
def data():
	if request.method == 'POST':
		f=request.form['csvfile']
		if not f:
			return "Nenhum arquivo enviado"
		data=[]
		with open(f) as file:
			csvfile = csv.reader(file)
			for row in csvfile:
				data.append(row)
		data=pd.DataFrame(data)
		#removing the "index columns"
		new_header = data.iloc[0]
		data = data[1:]
		data.columns = new_header
		#get only the variables that are in the model
		old_columns = list(model_columns)
		data_modelo=data[old_columns]
		new_columns = list(data_modelo.columns)
		if len(new_columns) == len(old_columns):
		        try:
		            score=lr.predict_proba(data_modelo)[:,1]
		            score_bin=np.where(lr.predict_proba(data_modelo)[:,1]>=0.2,1,0)
		            data['score']=score
		            data['score_bin']=score_bin
		            data.to_csv('data_score'+str(dt.date.today())+'.csv')

		        except:
		            print('Error')

		return render_template('data.html',data=data.head(10).to_html(header=True))
		# return(score)

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345
    lr = pickle.load(open('modelo_reg_logistica.pkl', 'rb')) # Load "model.pkl"
    print ('Model loaded')
    model_columns = pickle.load(open('model_columns.pkl', 'rb')) # Load "model_columns.pkl"
    print ('Model columns loaded')
    app.run(port=port, debug=False)
    