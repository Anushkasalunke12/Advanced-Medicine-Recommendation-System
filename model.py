
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

symptom_data = [
"fever cough headache",
"fever body pain weakness",
"sneezing runny nose cough",
"chest pain breath shortness fatigue",
"stomach pain nausea vomiting",
"headache dizziness nausea",
"skin rash itching redness",
"high fever chills sweating",
"joint pain swelling stiffness",
"frequent urination thirst fatigue"
]

diseases = [
"Flu",
"Viral Fever",
"Common Cold",
"Heart Disease",
"Food Poisoning",
"Migraine",
"Allergy",
"Malaria",
"Arthritis",
"Diabetes"
]

medicine_map = {
"Flu":"Paracetamol, Rest, Fluids",
"Viral Fever":"Paracetamol, Ibuprofen",
"Common Cold":"Antihistamine, Steam inhalation",
"Heart Disease":"Consult Cardiologist",
"Food Poisoning":"ORS, Ondansetron",
"Migraine":"Sumatriptan, Rest",
"Allergy":"Cetirizine",
"Malaria":"Artemisinin Combination Therapy",
"Arthritis":"Ibuprofen",
"Diabetes":"Metformin"
}

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(symptom_data)

model = MultinomialNB()
model.fit(X, diseases)

def predict_disease(symptoms):
    test = vectorizer.transform([symptoms])
    disease = model.predict(test)[0]
    return disease, medicine_map[disease]
