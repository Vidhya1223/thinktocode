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


#curl http://127.0.0.1:5000/patient?patient_id=8c95253e-8ee8-9ae8-6d40-021d702dc78e
@app.route('/patientinfo', methods = ['GET'])
def get_patient_details():
	
	id = request.args.get('patient_id')
	info = fhir.PATIENT[fhir.PATIENT.PatientUID == id]
	#print(info, id)
	if len(info.index) > 0 :
		details = info.iloc[0]
		#print(details)
		return jsonify({'PatientUID':details[0], 'NameFamily':details[1], 'NameGiven':details[2], 'DOB':details[0],'Gender':details[3]})
	else :
		return jsonify({'data': "No data found"})

@app.route('/patientconditions', methods = ['GET'])
def get_patient_conditions():
	
	id = request.args.get('patient_id')
	info = fhir.CONDITION[fhir.CONDITION.PatientUID == id]["ConditionText", "ConditionOnsetDates"]
	#print(info, id)
	if len(info.index) > 0 :
		details = info.to_json()
		print(details)
		return jsonify({'data' : details})
	else :
		return jsonify({'data': "No data found"})

@app.route('/patientobservations', methods = ['GET'])
def get_patient_observations():
	
	id = request.args.get('patient_id')
	info = fhir.OBSERVATION[fhir.OBSERVATION.PatientUID == id]
	print(info, id)
	if len(info.index) > 0 :
		details = info.filter(["ObservationText", "ObservationValue", "ObservationUnit", "ObservationDate"]).to_json()
		print(details)
		return jsonify({'data' : details})
	else :
		return jsonify({'data': "No data found"})

@app.route('/patientmedication', methods = ['GET'])
def get_patient_medications():
	
	id = request.args.get('patient_id')
	info = fhir.MEDICATION[fhir.MEDICATION.PatientUID == id]
	print(info, id)
	if len(info.index) > 0 :
		details = info.filter(["MedicationText", "MedicationDates"]).to_json()
		print(details)
		return jsonify({'data' : details})
	else :
		return jsonify({'data': "No data found"})

@app.route('/patientprocedure', methods = ['GET'])
def get_patient_prodecure():
	
	id = request.args.get('patient_id')
	info = fhir.PROCEDURE[fhir.PROCEDURE.PatientUID == id]
	print(info, id)
	if len(info.index) > 0 :
		details = info.filter(["ProcedureText", "ProcedureDates"]).to_json()
		print(details)
		return jsonify({'data' : details})
	else :
		return jsonify({'data': "No data found"})

@app.route('/patientencounter', methods = ['GET'])
def get_patient_encounter():
	
	id = request.args.get('patient_id')
	info = fhir.ENCOUNTER[fhir.ENCOUNTER.PatientUID == id]
	print(info, id)
	if len(info.index) > 0 :
		details = info.filter(['EncountersText', 'EncounterLocation', 'EncounterProvider','EncounterDates']).to_json()
		print(details)
		return jsonify({'data' : details})
	else :
		return jsonify({'data': "No data found"})
	
@app.route('/patienteclaim', methods = ['GET'])
def get_patient_claim():
	
	id = request.args.get('patient_id')
	info = fhir.CLAIM[fhir.CLAIM.PatientUID == id]
	print(info, id)
	if len(info.index) > 0 :
		details = info.filter(['ClaimProvider', 'ClaimInsurance', 'ClaimDate', 'ClaimType','ClaimItem', 'ClaimUSD']).to_json()
		print(details)
		return jsonify({'data' : details})
	else :
		return jsonify({'data': "No data found"})



if __name__ == '__main__':

	fhir.load_data()
	app.run(debug = True)
