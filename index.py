from re import template
from flask import Flask, request, jsonify, render_template, url_for, redirect, session
import pandas as pd
import numpy as np
import tensorflow as tf
import re
import random
import math

# model = tf.keras.models.load_model(
#     "C:/Users/PC/Desktop/College/8th level/CSC 497/static/model2years", custom_objects=None, compile=True, options=None
# )
# pred = model.predict(dataset).reshape(-1) > 0.1

app = Flask(__name__)
app.secret_key = "CSC497_Bankruptcy_Detection_Using_a_TimeSeries_Approach_Secret_Key"
attributes = ["Current assets", "Cost of goods sold", "Depreciation and amortization",
              "Earnings before interest, taxes, depreciation and amortization", "Inventory", "Net Income",
              "Total Receivables", "Market value", "Net sales", "Total assets", "Total Long term debt",
              "Earnings before interest and taxes", "Gross Profit", "Total Current Liabilities", "Retained Earnings",
              "Total Revenue", "Total Liabilities", "Total Operating Expenses"]


@app.route('/')
def index():
    session['globalData'] = []
    session['counter'] = 0
    session['number_of_years'] = 0
    session['years'] = ""
    session['result'] = 0
    session['selected'] = 0
    session['submitted'] = 0
    session['percentage'] = 1
    return render_template('main.html', years=session['years'], percentage=session['percentage'], selected=session['selected'])


@app.route('/count', methods=["POST", "GET"])
def count():
    session['number_of_years'] = int(request.form['Number of Years'])
    session['years'] = "Please submit " + \
        str((session['number_of_years']-session['counter'])) + \
        " years worth of data."
    session['selected'] = session['number_of_years']-1
    return render_template('main.html', years=session['years'], percentage=session['percentage'], selected=session['selected'])

@app.route('/submit', methods=["POST", "GET"])
def submit():
    data = []
    data.append("Company")
    data.append(request.form['X1'])
    data.append(request.form['X2'])
    data.append(request.form['X3'])
    data.append(request.form['X4'])
    data.append(request.form['X5'])
    data.append(request.form['X6'])
    data.append(request.form['X7'])
    data.append(request.form['X8'])
    data.append(request.form['X9'])
    data.append(request.form['X10'])
    data.append(request.form['X11'])
    data.append(request.form['X12'])
    data.append(request.form['X13'])
    data.append(request.form['X14'])
    data.append(request.form['X15'])
    data.append(request.form['X16'])
    data.append(request.form['X17'])
    data.append(request.form['X18'])
    session['counter'] += 1
    session['percentage'] = 1 - (session['counter']/session['number_of_years'])
    session['submitted'] = 1
    if (session['number_of_years']-session['counter'] > 1):
        session['years'] = "Please submit " + \
            str((session['number_of_years']-session['counter'])) + \
            " years worth of data."
    elif (session['number_of_years']-session['counter'] == 1):
        session['years'] = "Please submit " + \
        str((session['number_of_years']-session['counter']))+" year worth of data."
    else:
        session['years'] = ""
    session['globalData'].append(data)
    if (session['counter'] < session['number_of_years']):
        return render_template('main.html', years=session['years'], percentage=session['percentage'], selected=session['selected'])
    else:
        company_and_year = company_names(session['globalData'])
        dataset = create_dataset_for_raw_input(
            session['globalData'], length=company_and_year[1])
        dataset = np.array(dataset)
        results = get_company_and_value(dataset, company_and_year[0])
        pred = prediction(dataset, company_and_year[1])
        percent = []
        for i in range(len(pred)):
            percent.append(round(pred[i][0].item(), 4))
        session.clear()
        return render_template('index.html', percent=percent, company_and_value=results)


@app.route('/upload', methods=["POST", "GET"])
def upload():
    file = request.files.get('filename')
    raw_dataset = pd.read_csv(file).values.tolist()
    company_and_year = company_names(raw_dataset)
    dataset = create_dataset(raw_dataset, length=company_and_year[1])
    dataset = np.array(dataset)
    results = get_company_and_value(dataset, company_and_year[0])
    pred = prediction(dataset, company_and_year[1])
    percent = []
    for i in range(len(pred)):
        percent.append(round(pred[i][0].item(), 4))
    print(percent)
    return render_template('index.html', percent=percent, company_and_value=results)


def prediction(dataset, year):
    model = model_initialization(year)
    pred = model.predict(dataset)
    return pred


def get_company_and_value(dataset, company):
    results = []
    companies = company
    for i in range(dataset.shape[0]):
        temp = []
        for j in range(dataset.shape[1]):
            for k in range(dataset.shape[2]):
                if j == 0:
                    temp.append(dataset[i][j][k])
                else:
                    temp[k] += dataset[i][j][k]
        length = (dataset.shape[1])
        for t in range(18):
            temp[t] = round(temp[t]/length, 2)
        features = []
        for z in range(18):
            features.append([attributes[z], temp[z]])
        results.append([companies[i], features])
    return results


def company_names(data):
    dataForEachCompany = []
    name = data[0][0]
    dataForEachCompany.append(name)
    count = 0
    noYears = []
    for i in range(len(data)):
        if data[i][0] != name:
            name = data[i][0]
            dataForEachCompany.append(name)
            noYears.append(count)
            count = 1
        else:
            count += 1
    noYears.append(count)
    noYears.sort()
    min = noYears[0]
    year = 0
    if (min > 2):
        if (min > 3):
            if (min > 4):
                year = 5
            else:
                year = 4
        else:
            year = 3
    else:
        year = 2
    return [dataForEachCompany, year]


def create_dataset(raw_dataset, length=5):
    names = []
    X = []
    i = 0
    count = 0
    while i < len(raw_dataset) - length + 1:
        name = raw_dataset[i][0]
        if (name in names):
            i += 1
            continue
        date = raw_dataset[i][1]
        instance = []
        for j in range(length):
            current_name = raw_dataset[i + j][0]
            current_date = raw_dataset[i + j][1]
            if current_name == name and int(current_date) == int(date) + j:
                instance.append([k for count, k in enumerate(
                    raw_dataset[i + j]) if count > 1])
        last_name = raw_dataset[i + length - 1][0]
        last_date = raw_dataset[i + length - 1][1]

        if name == last_name and last_date == date + length - 1:
            X.append(instance)
            names.append(name)
        i += length

    return X


def model_initialization(year):
    path = "model"+str(year)+"years"
    model = tf.keras.models.load_model(
        path, custom_objects=None, compile=True, options=None)
    return model


def create_dataset_for_raw_input(raw_dataset, length=5):
    X = []
    i = 0
    count = 0
    while i < len(raw_dataset) - length + 1:
        instance = []
        for j in range(length):
            instance.append([k for count, k in enumerate(
                raw_dataset[i + j]) if count > 0])

        for k in range(len(instance)):
            for j in range(18):
                instance[k][j] = float(instance[k][j])

        X.append(instance)
        i += length

    return X


if __name__ == "__main__":
    app.run(debug=True)
