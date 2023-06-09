import pandas as pd
import sqlite3


fichier_excel = './fichiers_source/export_patient.xlsx'

db = sqlite3.connect('drwh.db')

#Exercice 1

dataframe = pd.read_excel(fichier_excel, engine='openpyxl')     # Lecture du fichier excel

dataframe_patient = dataframe[[
    'NOM',
    'PRENOM',
    'DATE_NAISSANCE',
    'SEXE',
    'NOM_JEUNE_FILLE',
    'ADRESSE',
    'TEL',
    'CP',
    'VILLE',
    'PAYS',
    'DATE_MORT'
    ]]
dataframe_patient.columns = [
    'LASTNAME',
    'FIRSTNAME',
    'BIRTH_DATE',
    'SEX',
    'MAIDEN_NAME',
    'RESIDENCE_ADDRESS',
    'PHONE_NUMBER',
    'ZIP_CODE',
    'RESIDENCE_CITY',
    'BIRTH_COUNTRY',
    'DEATH_DATE'
]

dataframe_patient.to_sql('DWH_PATIENT', db, if_exists='replace', index=False)   #charge dans la table DWH_PATIENT les lignes de dataframe_patient

dataframe_patient_ipphist = dataframe[[
    'NOM',
    'HOSPITAL_PATIENT_ID'
    ]]
dataframe_patient_ipphist.columns = [
    'LASTNAME',
    'HOSPITAL_PATIENT_ID'
]

#print(dataframe_patient_ipphist)

dataframe_patient_ipphist.to_sql('DWH_PATIENT_IPPHIST', db, if_exists='replace', index=False) #charge dans la table DWH_PATIENT_IPPHIST les lignes de dataframe_patient_ipphist


print(pd.read_sql_query("SELECT * FROM DWH_PATIENT", db))

db.close()