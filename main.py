# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 20:55:05 2020

@author: Yash Joshi
"""

from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

app = Flask(__name__)
# __name__ is a Flask module which tells where to collect templates and files
model = pickle.load(open('RF1','rb'))
# print(model)

@app.route('/')
# as soon as the local url is clicked, it'll bring the to the home page/route (/) and this'll render the html page
def getModel():
    return(render_template('loanform.html')) # to create HTML file
    
@app.route('/prediction', methods = ["POST"])
# As soon as Get Prediction is clicked, the form action will bring to /prediction url and this function gets executed
def predict():
    data=pd.read_csv("Loan_data.csv")
    # saving mean and standard deviation for each numerical columns from which model is trained to scale down the
    # input features in the range of 0-1
    
    dependents = request.form["Dependents"] # 0, 1, 2 3+ : Label Encoding
    education = request.form["Education"] # graduate- 0, not graduate- 1: Label Encoding
    selfemp = request.form["Self Employed"] # no- 0, yes- 1: Label Encoding
    appincome = float(request.form["Applicant Income"]) # minmax scaler
    coappincome = float(request.form["Coapplicant Income"]) # minmax scaler
    loanamount = float(request.form["Loan Amount"]) # minmax scaler
    loanterm = float(request.form["Loan Amount Term"]) # minmax scaler
    credithist = float(request.form["Credit History"])
    proparea = request.form["Property Area"] # Label Encoding
    
    input_variables = []
    
    if dependents == '0':
        dependents=0
    elif dependents == '1':
        dependents = 1
    elif dependents == '2':
        dependents = 2
    elif dependents == '3 or more':
        dependents = 3
        
    input_variables.append(dependents)
    
    if education == 'Graduate':
        education = 0
    elif education == 'Not Graduate':
        education = 1
    
    input_variables.append(education)
    
    if selfemp == 'No':
        selfemp = 0
    elif selfemp == 'Yes':
        selfemp = 1
        
    input_variables.append(selfemp)
    
    applicantincome = (appincome - data['ApplicantIncome'].min())/(data['ApplicantIncome'].max() - data['ApplicantIncome'].min())
    input_variables.append(applicantincome)
    
    coapplicantincome = (coappincome - data['CoapplicantIncome'].min())/(data['CoapplicantIncome'].max() - data['CoapplicantIncome'].min())
    input_variables.append(coapplicantincome)
    
    la = (loanamount - data['LoanAmount'].min())/(data['LoanAmount'].max() - data['LoanAmount'].min())
    input_variables.append(la)
    
    lat = (loanterm - data['Loan_Amount_Term'].min())/(data['Loan_Amount_Term'].max() - data['Loan_Amount_Term'].min())
    input_variables.append(lat)
    input_variables.append(credithist)
    
    if proparea == 'Rural':
        proparea = 0
    elif proparea == 'Semiurban':
        proparea = 1
    elif proparea == 'Urban':
        proparea = 2
    
    input_variables.append(proparea)
    
    pred = model.predict([input_variables])
    if pred == 0:
        return("Sorry! You are not eligible for loan")
    else:
        return("Great! You are eligible for loan")
    
            
if __name__ == '__main__':
    app.run()