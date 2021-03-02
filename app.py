from flask import Flask, render_template, request
from flaskwebgui import FlaskUI
import csv
import codecs
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# files import
from start import start

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)   

# freezing
if getattr(sys, 'frozen', False):
    template_folder =resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)


ui = FlaskUI(app)
app._static_folder = './static'


def parseCSV(csv_file):
    """
        Parse csv file and return a list of tuples with (name, email)
    """
    result = []
    batch_reader = csv.DictReader(csv_file, dialect=csv.excel)

    for row in batch_reader:
        print(row)
        try:
            result.append( (row['Name'], row['Email']) )
        # hacky workaround to re-encoding csv
        # recognizes unparsed file start
        except KeyError:
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
        print(names_dict)
        start(names_dict, message, subject, attachments)
        return render_template("success.html")
        
    
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port="8000", debug=True)
    ui.run()