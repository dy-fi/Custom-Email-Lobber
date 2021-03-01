from flask import Flask, render_template, request
import csv
import codecs

# files import
from start import start

app = Flask(__name__)

def parseCSV(csv_file):
    """
        Parse csv file and return a list of tuples with (name, email)
    """
    result = []
    batch_reader = csv.DictReader(csv_file, dialect=csv.excel)
    try:
        for row in batch_reader:
            result.append( (row['Name'], row['Email']) )
    except:
        for row in batch_reader:
            result.append( (row['\ufeffName'], row['Email']) )
            
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        # name file readin
        names_csv = request.files["names"]
        # codecs stream
        stream = codecs.iterdecode(names_csv.stream, 'utf-8')

        message = request.form["message"]
        subject = request.form["subject"]
        # attachments optional
        attachments = None
        if request.files["attachments"]:
            attachments = request.files["attachments"]

        names_dict = parseCSV(stream)
        # start(names_dict, message, subject, attachments)
        return render_template("success.html")
        
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000", debug=True)
