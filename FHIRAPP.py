from flask import Flask, jsonify, request
from FHIRLIB import FHIR
fhir = FHIR()
app = Flask(__name__)

#curl http://127.0.0.1:5000/
@app.route('/', methods = ['GET', 'POST'])
def greeting():
	if(request.method == 'GET'):

		data = "Greetings. "
		return jsonify({'data': data})

#curl http://127.0.0.1:5000/home/10
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):

	return jsonify({'data': num**2})

#curl http://127.0.0.1:5000/home/10
@app.route('/patient', methods = ['GET'])
def gene():
	
	id = request.args.get('patient_id')
	info = fhir.PATIENT[fhir.PATIENT.PatientUID == id]
	#print(info, id)
	if len(info.index) > 0 :
		details = info.iloc[0]
		#print(details)
		return jsonify({'PatientUID':details[0], 'NameFamily':details[1], 'NameGiven':details[2], 'DOB':details[0],'Gender':details[3]})
	else :
		return jsonify({'data': "No data found"})


	
if __name__ == '__main__':

	fhir.load_data()
	app.run(debug = True)
