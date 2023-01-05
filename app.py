


from datetime import datetime
from flask import Flask,  render_template, request, session, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename
 

from email_validator import validate_email
ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = os.path.join('uploads')
OUTPUT_FOLDER = os.path.join('output')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'flask-email-validate'
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
data = []
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',  methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        # upload file flask
        uploaded_df = request.files['uploaded-file']
 
        # Extracting uploaded data file name
        data_filename = secure_filename(uploaded_df.filename)
 
        # flask upload file to database (defined uploaded folder in static path)
        uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
 
    
        
        
 
    return render_template('index2.html')





@app.route("/validate_email")
def read_file():
    data_file_path = session.get('uploaded_data_file_path', None)
  
    df = pd.read_csv(data_file_path)
    email_col = df.loc[:, "Emails"]
    
    for emails in email_col:
        
        emailObject = validate_email(emails)
        emails = emailObject.email
        data.append([emails])
        valid_email = pd.DataFrame(data, columns = ['valid Email Only'])
           
        valid_email.to_csv(data_file_path  + '.csv' , index=False)
            
        csv_html = valid_email.to_html()
        session.clear()
            
        
    return render_template('validating.html' ,data_var = csv_html)
    

if __name__ == '__main__':
    app.run(threaded=True)
