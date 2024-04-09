from flask import Flask, render_template

googleMapsTest = Flask(__name__)


@googleMapsTest.route('/', methods=['GET', 'POST'])
def testApi():
    return render_template('googleMap.html')

if __name__ == "__main__":
    # to run me from the command line: <flask --app main run> or <python app.py>
    #                             
    googleMapsTest.run(host='0.0.0.0', port=5000, debug=True)