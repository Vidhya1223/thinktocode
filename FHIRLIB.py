from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.condition import Condition
from fhir.resources.observation import Observation
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.procedure import Procedure
from fhir.resources.encounter import Encounter
from fhir.resources.claim import Claim
from fhir.resources.immunization import Immunization
import numpy as np  
import pandas as pd 
import json
from datetime import date
import os


class FHIR : 

	#_instance = None

	def __int__(self) :

		#Creating Singleton Class to ensure no copies of instance of this class are created
		#if self._instance == None :
		#	self._instance = super(load_FHIR, self).__new__(self)
		#return self._instance
		print()

		

	def load_data(self) :

		#Seperate dataframes for different segments of data
		self.PATIENT = pd.DataFrame(columns=['PatientUID', 'NameFamily', 'NameGiven', 'DoB', 'Gender'])
		self.CONDITION = pd.DataFrame(columns=['ConditionText', 'ConditionOnsetDates', 'PatientUID'])
		self.OBSERVATION = pd.DataFrame(columns=['ObservationText', 'ObservationValue', 'ObservationUnit','ObservationDate', 'PatientUID'])
		self.MEDICATION = pd.DataFrame(columns=['MedicationText', 'MedicationDates', 'PatientUID'])
		self.PROCEDURE = pd.DataFrame(columns=['ProcedureText', 'ProcedureDates', 'PatientUID'])
		self.ENCOUNTER = pd.DataFrame(columns=['EncountersText', 'EncounterLocation', 'EncounterProvider','EncounterDates', 'PatientUID'])
		self.CLAIM = pd.DataFrame(columns=['ClaimProvider', 'ClaimInsurance', 'ClaimDate', 'ClaimType','ClaimItem', 'ClaimUSD', 'PatientUID'])
		self.IMMUNIZATION = pd.DataFrame(columns=['Immunization', 'ImmunizationDates', 'PatientUID'])

		file_path = 'D:\\EMIS_Assessment\\FHIRDATA\\'
		files = os.listdir(file_path)
		for file in files :
			f = open(file_path+file, encoding='utf-8')
			json_obj = json.load(f)
	
			oneBundle = Bundle.parse_obj(json_obj)
	
			resources = []
			if oneBundle.entry is not None:
				for entry in oneBundle.entry:
					resources.append(entry.resource)
	    
			onePatient = Patient.parse_obj(resources[0])
	
			# Patient demographics
			onePatientID = onePatient.id
			self.PATIENT.loc[len(self.PATIENT.index)] = [onePatientID, onePatient.name[0].family,onePatient.name[0].given[0], onePatient.birthDate, onePatient.gender] 
	    
	    		# Condition resources
			resCondition = []
			for j in range(len(resources)):
				if resources[j].__class__.__name__ == 'Condition':
					resCondition.append(resources[j])
	
			conditions = []
			conditionOnsetDates = []
			for j in range(len(resCondition)):
				oneCondition = Condition.parse_obj(resCondition[j])
				conditions.append(oneCondition.code.text)
				conditionOnsetDates.append(str(oneCondition.onsetDateTime.date()))  
	
			onePatConditions = pd.DataFrame()
			onePatConditions['ConditionText'] = conditions
			onePatConditions['ConditionOnsetDates'] = conditionOnsetDates
			onePatConditions['PatientUID'] = onePatientID
	
			self.CONDITION = pd.concat([self.CONDITION, onePatConditions], ignore_index = True, axis=0)
			self.CONDITION.reset_index()
	    
			# Find Observation resources ########################################
			resObservation = []
			for j in range(len(resources)):
				if resources[j].__class__.__name__ == 'Observation':
					resObservation.append(resources[j])
	
			obsText = []
			obsValue = []
			obsUnit = []
			obsDate = []
	
			for j in range(len(resObservation)):
				oneObservation = Observation.parse_obj(resObservation[j])
				obsText.append(oneObservation.code.text)
				if oneObservation.valueQuantity:
					obsValue.append(round(oneObservation.valueQuantity.value,2))
					obsUnit.append(oneObservation.valueQuantity.unit)
				else:
					obsValue.append('None')
					obsUnit.append('None')
				obsDate.append(oneObservation.issued.date())
	  
			onePatObs = pd.DataFrame()
			onePatObs['ObservationText'] = obsText
			onePatObs['ObservationValue'] = obsValue
			onePatObs['ObservationUnit'] = obsUnit
			onePatObs['ObservationDate'] = obsDate
			onePatObs['PatientUID'] = onePatientID
	
			self.OBSERVATION = pd.concat([self.OBSERVATION, onePatObs], ignore_index = True, axis=0)
			self.OBSERVATION.reset_index()
	    
			# Medication resources
			resMedicationRequest = []
			for j in range(len(resources)):
				if resources[j].__class__.__name__ == 'MedicationRequest':
					resMedicationRequest.append(resources[j])
	
			meds = []
			medsDates = []
			for j in range(len(resMedicationRequest)):
				oneMed = MedicationRequest.parse_obj(resMedicationRequest[j])
				if oneMed.medicationCodeableConcept is not None:
					meds.append(oneMed.medicationCodeableConcept.text)
					medsDates.append(str(oneMed.authoredOn.date()))  
	
			onePatMeds = pd.DataFrame()
			onePatMeds['MedicationText'] = meds
			onePatMeds['MedicationDates'] = medsDates
			onePatMeds['PatientUID'] = onePatientID
	    
			self.MEDICATION = pd.concat([self.MEDICATION, onePatMeds], ignore_index = True, axis=0)
			self.MEDICATION.reset_index()
	    
			# Procedure resources
			resProcedures = []
			for j in range(len(resources)):
				if resources[j].__class__.__name__ == 'Procedure':
					resProcedures.append(resources[j])
	
			procs = []
			procDates = []
			for j in range(len(resProcedures)):
				oneProc = Procedure.parse_obj(resProcedures[j])
				procs.append(oneProc.code.text)
				procDates.append(str(oneProc.performedPeriod.start.date()))  
	
			onePatProcs = pd.DataFrame()
			onePatProcs['ProcedureText'] = procs
			onePatProcs['ProcedureDates'] = procDates
			onePatProcs['PatientUID'] = onePatientID
	
	
			self.PROCEDURE = pd.concat([self.PROCEDURE, onePatProcs], ignore_index = True, axis=0)
			self.PROCEDURE.reset_index()
	    
			# Find Encounter resources ########################################
			resEncounters = []
			for j in range(len(resources)):
				if resources[j].__class__.__name__ == 'Encounter':
					resEncounters.append(resources[j])
	
			encounters = []
			encountDates = []
			encountLocation = []
			encountProvider = []
	
			for j in range(len(resEncounters)):
				oneEncounter = Encounter.parse_obj(resEncounters[j])
				encounters.append(oneEncounter.type[0].text)
				encountLocation.append(oneEncounter.serviceProvider.display)
				if oneEncounter.participant:
					encountProvider.append(oneEncounter.participant[0].individual.display)
				else:
					encountProvider.append('None')
				encountDates.append(str(oneEncounter.period.start.date()))  
	
			onePatEncounters = pd.DataFrame()
			onePatEncounters['EncountersText'] = encounters
			onePatEncounters['EncounterLocation'] = encountLocation
			onePatEncounters['EncounterProvider'] = encountProvider
			onePatEncounters['EncounterDates'] = encountDates
			onePatEncounters['PatientUID'] = onePatientID
	    
			self.ENCOUNTER = pd.concat([self.ENCOUNTER, onePatEncounters], ignore_index = True, axis=0)
			self.ENCOUNTER.reset_index()
	    
			# Find Claim resources
			resClaims = []
			for j in range(len(resources)):
				if resources[j].__class__.__name__ == 'Claim':
					resClaims.append(resources[j])
		
			claimProvider = []
			claimInsurance = []
			claimDate = []
			claimType = []
			claimItem = []
			claimUSD = []
	
			for j in range(len(resClaims)):
				oneClaim = Claim.parse_obj(resClaims[j])
				# Inner loop over claim items:
				for i in range(len(resClaims[j].item)):
					claimProvider.append(oneClaim.provider.display)
					claimInsurance.append(oneClaim.insurance[0].coverage.display)
					claimDate.append(str(oneClaim.billablePeriod.start.date()))
					claimType.append(oneClaim.type.coding[0].code)
					claimItem.append(resClaims[j].item[i].productOrService.text)
					if resClaims[j].item[i].net:
						claimUSD.append(str(resClaims[j].item[i].net.value))
					else:
						claimUSD.append('None')
	
			onePatClaims = pd.DataFrame()
			onePatClaims['ClaimProvider'] = claimProvider
			onePatClaims['ClaimInsurance'] = claimInsurance
			onePatClaims['ClaimDate'] = claimDate
			onePatClaims['ClaimType'] = claimType
			onePatClaims['ClaimItem'] = claimItem
			onePatClaims['ClaimUSD'] = claimUSD
			onePatClaims['PatientUID'] = onePatientID
	    
			self.CLAIM = pd.concat([self.CLAIM, onePatClaims], ignore_index = True, axis=0)
			self.CLAIM.reset_index()
	
			# Find Immunization resources
			resImmunization = []
			for j in range(len(resources)):
				if resources[j].__class__.__name__ == 'Immunization':
					resImmunization.append(resources[j])
	
			immun = []
			immunDates = []
			for j in range(len(resImmunization)):
				oneImmun = Immunization.parse_obj(resImmunization[j])
				immun.append(oneImmun.vaccineCode.coding[0].display)
				immunDates.append(str(oneImmun.occurrenceDateTime.date()))  
	
			onePatImmun = pd.DataFrame()
			onePatImmun['Immunization'] = immun
			onePatImmun['ImmunizationDates'] = immunDates
			onePatImmun['PatientUID'] = onePatientID
	    
			self.IMMUNIZATION = pd.concat([self.IMMUNIZATION, onePatImmun], ignore_index = True, axis=0)
			self.IMMUNIZATION.reset_index()
	
	
			#def get_general_info(self, patient_id):
			
