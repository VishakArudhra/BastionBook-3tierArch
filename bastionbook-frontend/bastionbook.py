from flask import (
    Flask, request, render_template, redirect, url_for, flash
)
import json
from markupsafe import escape
import re
import requests
# import boto3

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/")
def hello_world():
    return "<p>Hello, World!!</p>"

#for passing inputs through extensions
#the decorator argument and the function argument
# have to match.
@app.route("/<name>")
def hello_name(name):
    return f"<h1>Hello, {escape(name)}!</h1>"

@app.route("/register", methods=('GET','POST'))
def register():

    #if request is GET
    # url = 'https://api.vishakarudhra.com/dynamodbmanager'
    url = 'http://backend-endpoint/'

    get_all_data = {
    'operation': 'getall'
    }
    
    response_data = requests.post(
        url,
        json=get_all_data,
        headers={'Accept': 'application/json'}
    )
    if request.method == 'POST':
        try:
            inst_name = request.form['instance_name']
            user = request.form['user']
            ipaddr = request.form['ipaddr']
            pvt_key= request.form['pvt_key']
            operation = 'create'
            
            #below are a few chained assertion statements to disallow any input misformat
            assert isinstance(user, str) and \
            "" not in (inst_name, user, ipaddr, pvt_key) and \
            not any(bool(re.search(r'^\s+$', i)) for i in (inst_name, user, ipaddr, pvt_key)) and \
            bool(re.search(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', ipaddr)) and \
            isinstance(pvt_key, str)

            print((inst_name, user, ipaddr, pvt_key))

            try:
                new_entry = {
                    'operation': str(operation),
                    'payload': {
                        'Item': {
                            'inst_name': str(inst_name),
                            'username':str(user),
                            'ip_addr':str(ipaddr),
                            'pvt_key':str(pvt_key)
                        }
                    }
                }

                response = requests.post(
                    url, 
                    json=new_entry,
                    headers={'Accept': 'application/json'}
                    )
                # print(response.json())
                assert response.json()["ResponseMetadata"]["HTTPStatusCode"] == 200
                flash('entry successful')
                return redirect(url_for('register'))
            except:
                flash('entry unsuccessful, internal error.')
                return render_template('register.html', bad_entry=True, instance_data=response_data.json())
        
        except:
            flash('entry unsuccessful, try again.')
            return render_template('register.html', bad_entry=True, instance_data=response_data.json())
         
            
    return render_template('register.html', instance_data=response_data.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0')
