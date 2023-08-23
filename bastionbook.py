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
    return "<p>Hello, World!!!</p>"

#for passing inputs through extensions
#the decorator argument and the function argument
# have to match.
@app.route("/<name>")
def hello_name(name):
    return f"<h1>Hello, {escape(name)}!</h2>"

@app.route("/register", methods=('GET','POST'))
def register():
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
                url = 'https://25a55it941.execute-api.us-west-2.amazonaws.com/test/dynamodbmanager'
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
                    data=json.dumps(new_entry)
                    )
                assert response.content.decode() == 'null'
                flash('entry successful')
                return render_template('register.html', bad_entry=False)
            except:
                flash('entry unsuccessful, internal error.')
                return render_template('register.html', bad_entry=True)
        
        except:
            flash('entry unsuccessful, try again.')
            return render_template('register.html', bad_entry=True)
                
            
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
