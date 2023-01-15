########### NOTE: #####################
# Install packages from requirements.txt only otherwise it will give version error
from wsgiref import simple_server
# import atexit
# import uuid
# import pandas as pd
import os
from flask import Flask, session, request, Response, jsonify, render_template,redirect,url_for,flash,Markup,send_file
import json

from uploadsValidation import Validation
from json_values import Json_values
from prediction import Prediction_from_csv
from prediction import Prediction_from_link

app = Flask(__name__)
# file_name = ''
# app.secret_key = "super secret key"

@app.route('/',methods = ['GET'])
def home_page():
    return render_template('home.html')

@app.route('/columns_details',methods =['GET'])
def cols():
    # json_values_obj = Json_values('cols_details.json')
    json_values_obj = Json_values('predict_cols_validation.json')
    keys, values,description = json_values_obj.data()

    # data = {keys}
    # ,keys,values
    # with open('file_validation.json', 'r') as f:
    with open('predict_cols_validation.json', 'r') as f:
        dic = json.load(f)
        f.close()
    return render_template('column_details.html',values= values,keys = keys,description = description)

@app.route('/predict_main',methods = ['GET'])
def prediction_main():
    return render_template('predict_main.html')

##################### NO NEED FOR TRAINING OF THE DATA SET AS OF NOW##########################
# @app.route('/add_data',methods = ['POST','GET'])
# def add():
#     if(request.method == 'GET'):
#         return render_template('add_csv.html')
#     elif(request.method == 'POST'):
#         try:
#
#             validation = Validation(request.files['csvfile'],'uploads','file_validation.json')
#             validation.save()
#             numberofcols,col_name,check = validation.checkFile()
#             print(col_name)
#             if(check):
#                 strr = "Number of columns are not equal. Number of Columns should be " + str(numberofcols) + '.'
#                 return render_template('result_of_add.html',data = strr)
#
#             # return redirect(request.url)
#
#             return render_template('result_of_add.html',data = "Data Has been added and file is validated",check = False)
#
#         except (UnicodeDecodeError,TypeError) as x:
#             # return Response("Error : %s"% UnicodeDecodeError)
#             return render_template('result_of_add.html',data = "Please enter a .csv extension",check = False)
#
#         except ValueError:
#             return render_template('result_of_add.html', data = 'Column are not matching!',check = False)
#         except Exception as e:
#             print("Exception is: ",repr(e))
#             # return Response("Error : %s"% Exception)
#             return e


@app.route('/predict_from_csv',methods =['GET','POST'])
def predict():
    if(request.method == 'GET'):
        return render_template('predict_from_csv.html')
    elif(request.method == 'POST'):
        try:
            validation = Validation(request.files['csvfile'],'predict_uploads','predict_cols_validation.json')

            validation.save()
            numberofcols, col_name,check = validation.checkFile()
            print("num", numberofcols)

            if(check):
                strr = "Number of columns are not equal. Number of Columns should be " + str(numberofcols) + '.'
                return render_template('result_of_add.html',data = strr)
            # print(request.files['csvfile'].filename)
            predict_obj = Prediction_from_csv(request.files['csvfile'].filename)
            global output_filename
            output_filename = predict_obj.predict_data()
            # file_name = output_filename
            print(output_filename)

            return render_template('result_of_add.html',data = "Data Has been added and file is validated",check = True)

        except (UnicodeDecodeError,TypeError) as x:
            print("checking")
            return render_template('result_of_add.html',data = "Please enter a .csv extension",check = False)
        except Exception:
            print("Exception checking",repr(Exception))
            render_template('result_of_add.html',data = "Exception",check = False)


@app.route('/predict_from_link',methods = ['GET','POST'])
def predict_from_link():
    if(request.method == 'GET'):
        return render_template('predict_from_link.html')
    elif(request.method == 'POST'):
        try:
            link = request.form.get("link")
            predict_obj = Prediction_from_link(link)
            phishing = predict_obj.predict()
            print("Phishing or not:" + str(phishing[0]))

            # if (phishing[0] == "4" or phishing[0] == "2" or phishing[0] == "3"):
            #     return render_template('result_predict_link.html',result = str(phishing[0]),link = link)


            return render_template('result_predict_link.html',result = str(phishing[0]),link = link)


        except Exception as e:
            print(e)


@app.route('/download',methods = ['GET'])
def download_file():
    return send_file(output_filename,as_attachment=True)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

port =int(os.getenv("PORT",5001))

if __name__ == '__main__':
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host, port = port, app = app)
    print("http://localhost:5001/" )
    httpd.serve_forever()


