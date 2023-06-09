import os
import re
import sqlite3
import PyPDF2
from docx import Document


repertoire_documents = './fichiers_source/'
db = sqlite3.connect('drwh.db')

def extraire_texte_pdf(fichier):
    with open(fichier, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        #print("reader.pages", reader.pages)
        for page in reader.pages:
            text += page.extract_text()
        return text


def extraire_texte_docx(fichier):
    doc = Document(fichier)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extraire_date(phrase):
    #pattern : dd/mm/yyyy ou dd/mm/yy
    pattern = r"\d{2}/\d{2}/\d{2,4}\b"
    match = re.search(pattern, phrase)
    if match:
        date = match.group()  # On récupère la date correspondante
        return date
    
    return None

cursor = db.cursor()
document_num = 1

#print("list directory", os.listdir(repertoire_documents))

for fichier in os.listdir(repertoire_documents):
    print(fichier)

    #Si le fichier est un pdf ou un docx
    if fichier.endswith('.pdf'):
        ipp, id_document = fichier[:-4].split('_')
        source = 'DOSSIER_PATIENT'
        chemin_fichier = os.path.join(repertoire_documents, fichier)
        texte = extraire_texte_pdf(chemin_fichier)
    elif fichier.endswith('.docx'):
        ipp, id_document = fichier[:-5].split('_')
        source = 'RADIOLOGIE_SOFTWARE'
        chemin_fichier = os.path.join(repertoire_documents, fichier)
        texte = extraire_texte_docx(chemin_fichier)
    else:
        continue
    
    #On extrait la date si il y a une des deux phrases dans le texte
    date = None
    lignes = texte.split('\n')
    for ligne in lignes:
        if 'Compte de rendu de consultation' in ligne or 'Compte-Rendu d\'hospitalisation' in ligne:
            date = extraire_date(ligne)
            if date:
                break

    # On vérifie la dernière ligne pour savoir si c'est l'auteur
    author = 'NO AUTHOR'
    for ligne in lignes[-10:]:
        dernier_ligne = ligne.strip()
        if dernier_ligne.startswith('Dr') or dernier_ligne.startswith('DR'):
            author = dernier_ligne
            

    # print("ipp", ipp)
    # print("id_document", id_document)
    # print("fichier", fichier)
    # print("source", source)
    # print("date", date)
    # print("author", author)
    # print("------------------------")

    

    cursor.execute('INSERT INTO DWH_DOCUMENT (DOCUMENT_NUM, PATIENT_NUM, TITLE, DOCUMENT_DATE, ID_DOC_SOURCE, DISPLAYED_TEXT, AUTHOR) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (id_document, ipp, fichier, date, source, texte, author))
    document_num += 1

cursor.execute('SELECT DOCUMENT_NUM, PATIENT_NUM, TITLE, DOCUMENT_DATE, ID_DOC_SOURCE, AUTHOR FROM DWH_DOCUMENT')
resultats = cursor.fetchall()
for resultat in resultats:
    print(resultat)

db.commit()
db.close()