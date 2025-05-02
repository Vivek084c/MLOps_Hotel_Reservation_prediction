import joblib 
import numpy
from config.path_config import MODEL_OUTPUT_PATH
from flask import Flask, render_template, request

app = Flask(__name__)
model = joblib.load(MODEL_OUTPUT_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=="POST":
        lead_time = int(request.form["lead_time"])
        no_of_special_request = int(request.form["no_of_special_request"])
        avg_price_per_room = request.form["avg_price_per_room"]
        arival_month = int(request.form["arival_month"])
        arival_date = int(request.form["arival_date"])
        
        

       


