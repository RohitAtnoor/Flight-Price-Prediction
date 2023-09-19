from flask import Flask,request,render_template,jsonify
from source.pipeline.prediction_pipeline import CustomData,PredictPipeline

application=Flask(__name__)

app=application

# creating the routes
# creating the home route.
@app.route("/")
def home_page():
    return render_template('index.html') # rendering or opening the index page. 


@app.route('/predict',methods=['GET','POST'])

def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    
    else:
        data=CustomData(
            Day=float(request.form.get('Day')),
            Month=float(request.form.get('Month')),
            Airline=(request.form.get('Airline')),
            Source=(request.form.get('Source')),
            Destination=(request.form.get('Destination')),
            Total_Stops=(request.form.get('Total_Stops')),
            Year=float(request.form.get('Year')),
            Dep_hour=float(request.form.get('Dep_hour')), 
            Dep_min=float(request.form.get('Dep_min')),
            Arival_hour=float(request.form.get('Arival_hour')),
            Arival_min=float(request.form.get('Arival_min')),
            Trveling_hour=float(request.form.get('Trveling_hour')),
            Trveling_min=float(request.form.get('Trveling_min'))
        )
        final_new_data=data.get_data_as_dataframe()
        predict_pipeline=PredictPipeline()
        pred=predict_pipeline.predict(final_new_data)

        results=round(pred[0],2)

        return render_template('results.html',final_result=results)



if __name__ == "__main__" :
    app.run(host=("0.0.0.0"),debug=True )