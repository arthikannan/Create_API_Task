from flask import Flask, render_template
from flask import send_file
from flask import make_response
import requests
import io, csv
import json

app = Flask(__name__)

@app.route("/")
def default():
    return "Server 1!"

@app.route("/home", methods = ["POST","GET"])
def home():
    return render_template('home.html')

@app.route("/download")
def download():
    # Initialize the csv
    dest = io.StringIO()
    writer = csv.writer(dest)

    # Request the data from server
    r = requests.get("http://localhost:5002/parse")
    parsedData = json.loads(r.text)
    

    # Iterate and construct the data
    for data in parsedData:
        writer.writerow([data['Name'], data['Party'], data['Presidential term'], data['President number'], data['Ingestion Time']])

    # Respond the data
    output = make_response(dest.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == "__main__":
    app.run(debug=True, port=5001)