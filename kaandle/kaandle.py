import streamlit as st
import google.generativeai as genai
# Page Configuration (Must be first)
st.set_page_config(
    page_title="Kaandle",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)
# Gemini API Setup (Takes the key from Streamlit Secrets)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    ai_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    ai_model = None

def get_sarcastic_response(actual_disease, clues, user_guess):
    if not ai_model:
        return "Our AI Professor is currently on a coffee break. I'll just say: 'Wrong answer'."
    
    # Combine the revealed clues into a single string
    clues_text = " ".join([clue["text"] for clue in clues])
    
    prompt = f"""
    You are the world's most brilliant but arrogant, sarcastic, and witty medical professor (like Dr. House). 
    Your medical student (the player) just made a terribly wrong diagnosis for a patient.
    
    Actual Disease of the Patient: {actual_disease}
    Student's Ridiculous Guess: {user_guess}
    Patient's Revealed Clues/Findings: {clues_text}

    Your tasks:
    1. Mock the student's guess with a witty, sarcastic, and condescending (but not overly offensive) tone.
    2. Explain WHY this guess makes absolutely no sense based ONLY on the provided clues/findings.
    3. NEVER REVEAL THE ACTUAL DISEASE! Just make them think and realize their mistake.
    4. Keep your response short and punchy (Maximum 3-4 sentences). Respond completely in English.
    """
    
    try:
        response = ai_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Hata Detayı: {str(e)}"
# Custom CSS for a better UI
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Helvetica Neue', sans-serif;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #6B7280;
        margin-bottom: 30px;
    }
    .clue-box {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 6px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        font-size: 16px;
        color: #1F2937;
    }
    .clue-header {
        color: #2563EB;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .archive-card {
        border: 1px solid #E5E7EB;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .medical-image {
        max-width: 100%;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 10px;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# StatPearls Style Medical Database
# Kaandle Medical Database - Part 1 (Cases 1-15)
if 'cases' not in st.session_state:
    st.session_state.cases = [
        {
            "id": 1,
            "disease": "Acute Myocardial Infarction",
            "accepted_answers": ["myocardial infarction", "mi", "stemi", "heart attack", "akut miyokard enfarktüsü", "kalp krizi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 62-year-old male presents with acute, crushing substernal chest pain radiating to his left jaw and arm for the past 45 minutes."},
                {"title": "History & Physical Exam", "text": "The pain was not relieved by rest or sublingual nitroglycerin. He is diaphoretic, pale, and apprehensive. Auscultation reveals a new S4 gallop."},
                {"title": "Basic Labs", "text": "Basic metabolic panel and CBC are normal. A stat portable chest x-ray shows no widened mediastinum."},
                {"title": "Imaging / ECG", "text": "Immediate 12-lead ECG shows >2 mm ST-segment elevations in leads V2-V5 with reciprocal ST depressions in inferior leads."},
                {"title": "Specific/Advanced Labs", "text": "Initial cardiac-specific Troponin I is elevated. He is taken emergently to the cath lab for primary PCI."}
            ]
        },
        {
            "id": 2,
            "disease": "Pulmonary Embolism",
            "accepted_answers": ["pulmonary embolism", "pe", "pulmoner emboli", "akciğer embolisi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 65-year-old male presents to the ER with sudden onset of severe dyspnea and right-sided pleuritic chest pain."},
                {"title": "History & Physical Exam", "text": "He recently returned from a 12-hour flight. On exam, he is tachycardic (115 bpm) and tachypneic. His right calf is mildly swollen and tender."},
                {"title": "Basic Labs", "text": "Arterial blood gas reveals hypoxia and respiratory alkalosis. D-dimer is markedly elevated (>4000 ng/mL)."},
                {"title": "Imaging / ECG", "text": "ECG shows sinus tachycardia and an S1Q3T3 pattern. Chest X-ray reveals a wedge-shaped pleural-based opacification (Hampton's hump)."},
                {"title": "Specific/Advanced Labs", "text": "CT pulmonary angiography demonstrates a large filling defect in the right main pulmonary artery."}
            ]
        },
        {
            "id": 3,
            "disease": "Community Acquired Pneumonia",
            "accepted_answers": ["pneumonia", "community acquired pneumonia", "cap", "pnömoni", "zatürre"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 58-year-old male presents with a 3-day history of high fever, shaking chills, and a productive cough with rust-colored sputum."},
                {"title": "History & Physical Exam", "text": "He has a history of heavy smoking. On physical exam, his temperature is 39.2°C. Auscultation reveals bronchial breath sounds, egophony, and crackles over the right lower lung field."},
                {"title": "Basic Labs", "text": "CBC shows a significant leukocytosis (18,000/µL) with a left shift (bandemia)."},
                {"title": "Imaging / ECG", "text": "Chest X-ray reveals a dense lobar consolidation in the right lower lobe with distinct air bronchograms."},
                {"title": "Specific/Advanced Labs", "text": "Urinary antigen test is positive for Streptococcus pneumoniae. Sputum culture grows alpha-hemolytic, optochin-sensitive diplococci."}
            ]
        },
        {
            "id": 4,
            "disease": "Congestive Heart Failure",
            "accepted_answers": ["heart failure", "congestive heart failure", "chf", "kalp yetmezliği", "ky"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 72-year-old female presents with progressively worsening shortness of breath over the past 2 weeks, particularly when lying flat (orthopnea)."},
                {"title": "History & Physical Exam", "text": "She reports waking up gasping for air at night (PND). Exam reveals elevated JVP, bilateral basilar crackles, and 2+ pitting edema in her legs."},
                {"title": "Basic Labs", "text": "Basic metabolic panel shows mild hyponatremia. Liver enzymes are slightly elevated due to hepatic congestion."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows cardiomegaly, bilateral pleural effusions, and prominent vascular markings in the upper lung zones (cephalization)."},
                {"title": "Specific/Advanced Labs", "text": "B-type Natriuretic Peptide (BNP) is >1000 pg/mL. Echocardiogram reveals a severely reduced ejection fraction of 30%."}
            ]
        },
        {
            "id": 5,
            "disease": "Asthma",
            "accepted_answers": ["asthma", "astım", "bronchial asthma"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 22-year-old female comes to the clinic complaining of episodic chest tightness and a dry cough, which worsens at night."},
                {"title": "History & Physical Exam", "text": "She reports these symptoms often occur after jogging in the cold air or exposure to pet dander. Exam reveals diffuse, high-pitched expiratory wheezes bilaterally."},
                {"title": "Basic Labs", "text": "CBC reveals a mild eosinophilia (7%). Arterial blood gas shows a mild respiratory alkalosis due to hyperventilation."},
                {"title": "Imaging / ECG", "text": "Chest X-ray is mostly normal, with mild hyperinflation. No focal infiltrates or effusions are seen."},
                {"title": "Specific/Advanced Labs", "text": "Pulmonary function testing (Spirometry) shows an FEV1/FVC ratio of 65%. Following administration of inhaled albuterol, her FEV1 improves by 20%."}
            ]
        },
        {
            "id": 6,
            "disease": "Chronic Obstructive Pulmonary Disease",
            "accepted_answers": ["copd", "koah", "chronic obstructive pulmonary disease", "emphysema", "chronic bronchitis"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 65-year-old male presents with chronic, progressive exertional dyspnea and a daily productive cough for the last 3 years."},
                {"title": "History & Physical Exam", "text": "He has a 45 pack-year smoking history. Exam reveals a barrel-shaped chest, use of accessory respiratory muscles, and prolonged expiratory phase with distant breath sounds."},
                {"title": "Basic Labs", "text": "Arterial blood gas reveals chronic CO2 retention (pCO2 52 mmHg) with a compensatory metabolic alkalosis (Bicarbonate 30 mEq/L)."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows hyperinflated lungs, flattened hemidiaphragms, and a narrow cardiac silhouette."},
                {"title": "Specific/Advanced Labs", "text": "Spirometry demonstrates a post-bronchodilator FEV1/FVC ratio of 0.55 and an FEV1 that is 45% of predicted, confirming irreversible airflow limitation."}
            ]
        },
        {
            "id": 7,
            "disease": "Tuberculosis",
            "accepted_answers": ["tuberculosis", "tb", "tüberküloz", "verem"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 40-year-old recent immigrant presents with a 2-month history of chronic cough, low-grade afternoon fevers, and profound night sweats."},
                {"title": "History & Physical Exam", "text": "He complains of a 10 kg (22 lbs) unintentional weight loss and recent episodes of coughing up blood (hemoptysis). Exam shows a cachectic man with apical crackles."},
                {"title": "Basic Labs", "text": "Mild normocytic anemia is present. ESR and CRP are markedly elevated. HIV test is negative."},
                {"title": "Imaging / ECG", "text": "Chest X-ray reveals a cavitary lesion in the apical segment of the right upper lobe, with surrounding nodular opacities."},
                {"title": "Specific/Advanced Labs", "text": "Sputum smear is positive for acid-fast bacilli (AFB) using the Ziehl-Neelsen stain. Interferon-gamma release assay (IGRA) is positive."}
            ]
        },
        {
            "id": 8,
            "disease": "Peptic Ulcer Disease",
            "accepted_answers": ["peptic ulcer disease", "pud", "peptic ulcer", "gastric ulcer", "duodenal ulcer", "peptik ülser", "ülser"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 45-year-old male complains of a burning, gnawing epigastric pain that frequently wakes him up at 2:00 AM."},
                {"title": "History & Physical Exam", "text": "He notes that the pain temporarily improves after eating food or taking antacids. He takes ibuprofen regularly. He has mild epigastric tenderness on palpation."},
                {"title": "Basic Labs", "text": "CBC shows a mild microcytic anemia (Hemoglobin 11.2 g/dL) suggestive of chronic, occult blood loss. Fasting serum gastrin is normal."},
                {"title": "Imaging / ECG", "text": "Upright abdominal X-ray is unremarkable. No free air under the diaphragm is seen, ruling out a perforation."},
                {"title": "Specific/Advanced Labs", "text": "Urea breath test is positive. Upper GI endoscopy reveals a 1 cm ulceration in the duodenal bulb with a clean base. Biopsy confirms H. pylori infection."}
            ]
        },
        {
            "id": 9,
            "disease": "Acute Pancreatitis",
            "accepted_answers": ["acute pancreatitis", "pancreatitis", "akut pankreatit", "pankreatit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 55-year-old male presents with severe, steady, boring pain in the epigastric region that radiates directly to his back."},
                {"title": "History & Physical Exam", "text": "He has a history of heavy alcohol consumption. He is leaning forward to relieve the pain. Exam reveals diminished bowel sounds and a faint blue discoloration around the umbilicus (Cullen's sign)."},
                {"title": "Basic Labs", "text": "WBC count is elevated at 16,000/µL. Calcium level is mildly decreased at 7.8 mg/dL. Triglycerides are normal."},
                {"title": "Imaging / ECG", "text": "Abdominal CT with IV contrast is obtained, revealing marked peripancreatic inflammatory stranding, edema, and fluid collections."},
                {"title": "Specific/Advanced Labs", "text": "Serum lipase and amylase levels are >3 times the upper limit of normal. Liver function tests show a mild transaminitis."}
            ]
        },
        {
            "id": 10,
            "disease": "Cirrhosis",
            "accepted_answers": ["cirrhosis", "siroz", "hepatic cirrhosis", "liver cirrhosis"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 54-year-old male is brought to the clinic by his wife due to increasing fatigue, yellowing of his eyes, and abdominal swelling."},
                {"title": "History & Physical Exam", "text": "He has a 20-year history of heavy alcohol use. Exam reveals scleral icterus, spider angiomas on his chest, palmar erythema, and a distended abdomen with a positive fluid wave."},
                {"title": "Basic Labs", "text": "AST is 120 U/L and ALT is 50 U/L (ratio >2:1). Serum albumin is low (2.5 g/dL). Prothrombin time (PT/INR) is prolonged."},
                {"title": "Imaging / ECG", "text": "Abdominal ultrasound demonstrates a shrunken, nodular liver, splenomegaly, and a large amount of free fluid in the abdomen."},
                {"title": "Specific/Advanced Labs", "text": "Diagnostic paracentesis yields transudative fluid with a Serum-Ascites Albumin Gradient (SAAG) >1.1 g/dL, confirming portal hypertension."}
            ]
        },
        {
            "id": 11,
            "disease": "Diabetic Ketoacidosis",
            "accepted_answers": ["diabetic ketoacidosis", "dka", "diyabetik ketoasidoz"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 19-year-old male with known Type 1 diabetes is brought to the ER with extreme fatigue, nausea, vomiting, and abdominal pain."},
                {"title": "History & Physical Exam", "text": "He stopped taking his insulin due to a recent illness. Exam reveals deep, rapid breathing (Kussmaul respirations) and a fruity, acetone odor on his breath."},
                {"title": "Basic Labs", "text": "Serum glucose is 550 mg/dL. Basic metabolic panel shows a severe high anion-gap metabolic acidosis (pH 7.15, Bicarbonate 10 mEq/L)."},
                {"title": "Imaging / ECG", "text": "ECG shows peaked T-waves, which correlates with his laboratory findings. Chest X-ray is clear."},
                {"title": "Specific/Advanced Labs", "text": "Serum ketones (beta-hydroxybutyrate) are strongly positive. His initial serum potassium level is falsely elevated at 5.8 mEq/L due to the acidosis and lack of insulin."}
            ]
        },
        {
            "id": 12,
            "disease": "Graves' Disease",
            "accepted_answers": ["graves disease", "graves", "graves' disease", "hyperthyroidism", "hipertiroidi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 32-year-old female presents with palpitations, unintended weight loss despite an increased appetite, and severe heat intolerance."},
                {"title": "History & Physical Exam", "text": "She complains of feeling anxious. Exam reveals a fine resting tremor, a diffusely enlarged, non-tender thyroid gland with a bruit, and prominent eyes (exophthalmos)."},
                {"title": "Basic Labs", "text": "Basic chemistry is normal except for mild hypercalcemia. ECG shows sinus tachycardia at 115 bpm."},
                {"title": "Imaging / ECG", "text": "Thyroid radioactive iodine uptake (RAIU) scan demonstrates diffusely increased uptake uniformly throughout the entire gland."},
                {"title": "Specific/Advanced Labs", "text": "TSH is completely suppressed (<0.01 mIU/L). Free T4 and T3 are markedly elevated. Thyroid-stimulating immunoglobulins (TSI) are highly positive."}
            ]
        },
        {
            "id": 13,
            "disease": "Acute Appendicitis",
            "accepted_answers": ["appendicitis", "acute appendicitis", "apandisit", "akut apandisit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 24-year-old male arrives at the ER complaining of severe abdominal pain that started around his umbilicus and has now migrated to his right lower quadrant."},
                {"title": "History & Physical Exam", "text": "He has anorexia and vomited once. He has a low-grade fever. Exam reveals exquisite point tenderness at McBurney's point and positive rebound tenderness."},
                {"title": "Basic Labs", "text": "CBC shows a mild leukocytosis (13,000/µL) with a left shift (increased neutrophils). Urinalysis is normal, making a kidney stone less likely."},
                {"title": "Imaging / ECG", "text": "Abdominal CT scan with contrast demonstrates a dilated, thick-walled, blind-ending tubular structure (diameter >6 mm) with surrounding fat stranding."},
                {"title": "Specific/Advanced Labs", "text": "An appendicolith (calcified fecalith) is seen obstructing the base of the structure on the CT scan. Patient is prepped for immediate laparoscopic surgery."}
            ]
        },
        {
            "id": 14,
            "disease": "Ischemic Stroke",
            "accepted_answers": ["ischemic stroke", "stroke", "cva", "cerebrovascular accident", "inme", "felç", "iskemik inme"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 68-year-old male is brought to the ER by his wife due to sudden onset of right-sided weakness and inability to speak clearly (aphasia)."},
                {"title": "History & Physical Exam", "text": "His symptoms started exactly 90 minutes ago. He has a history of atrial fibrillation but has been non-compliant with his anticoagulation. Exam shows right facial droop and right hemiparesis."},
                {"title": "Basic Labs", "text": "Fingerstick blood glucose is 110 mg/dL, ruling out hypoglycemia. Coagulation profile (PT/INR) is normal."},
                {"title": "Imaging / ECG", "text": "Immediate non-contrast head CT shows no evidence of intracranial hemorrhage or large established infarct, making him a potential candidate for thrombolytics."},
                {"title": "Specific/Advanced Labs", "text": "CT Angiography reveals an abrupt cutoff (thrombus) in the M1 segment of the left Middle Cerebral Artery (MCA)."}
            ]
        },
        {
            "id": 15,
            "disease": "Bacterial Meningitis",
            "accepted_answers": ["meningitis", "bacterial meningitis", "meningococcal meningitis", "menenjit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 19-year-old college student living in a dormitory is brought in by his roommate due to fever, severe headache, and confusion evolving rapidly over 12 hours."},
                {"title": "History & Physical Exam", "text": "The patient is lethargic and photophobic. Neck resists passive flexion (nuchal rigidity). You notice a diffuse petechial rash on his trunk and lower extremities."},
                {"title": "Basic Labs", "text": "Peripheral WBC count is 22,000/µL with 85% neutrophils and 10% bands. Blood cultures are drawn immediately."},
                {"title": "Imaging / ECG", "text": "A stat head CT is completely normal, showing no mass effect or midline shift, clearing the way for a safe lumbar puncture."},
                {"title": "Specific/Advanced Labs", "text": "CSF shows opening pressure >200 mmH2O, WBC 4,500/µL (95% PMNs), glucose 20 mg/dL, and protein 150 mg/dL. Gram stain reveals gram-negative diplococci."}
            ]
        },{
            "id": 16,
            "disease": "Multiple Sclerosis",
            "accepted_answers": ["multiple sclerosis", "ms", "sclerosis", "multipl skleroz"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 28-year-old female presents with sudden blurring of vision in her left eye and pain upon eye movement."},
                {"title": "History & Physical Exam", "text": "She reports that 6 months ago, she had an episode of weakness and numbness in her right leg that resolved on its own. Physical exam reveals a relative afferent pupillary defect (Marcus Gunn pupil) in the left eye and brisk deep tendon reflexes."},
                {"title": "Basic Labs", "text": "Routine blood work, including B12, TSH, and ANA, is unremarkable."},
                {"title": "Imaging / ECG", "text": "Brain MRI with contrast reveals multiple hyperintense ovoid lesions in the periventricular and juxtacortical white matter, some of which enhance with gadolinium."},
                {"title": "Specific/Advanced Labs", "text": "Lumbar puncture is performed, and CSF analysis reveals the presence of oligoclonal bands that are not present in the serum."}
            ]
        },
        {
            "id": 17,
            "disease": "Rheumatoid Arthritis",
            "accepted_answers": ["rheumatoid arthritis", "ra", "romatoid artrit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 42-year-old female complains of progressive pain, swelling, and stiffness in her hands and wrists for the past 4 months."},
                {"title": "History & Physical Exam", "text": "She states the stiffness is worst in the morning, lasting for about 2 hours before improving with use. Exam reveals symmetric, boggy swelling of the MCP and PIP joints, sparing the DIP joints."},
                {"title": "Basic Labs", "text": "CBC shows a mild normocytic anemia. Inflammatory markers (ESR and CRP) are significantly elevated."},
                {"title": "Imaging / ECG", "text": "X-rays of the hands show periarticular osteopenia and early marginal erosions at the MCP joints."},
                {"title": "Specific/Advanced Labs", "text": "Rheumatoid factor (RF) is positive, and Anti-cyclic citrullinated peptide (anti-CCP) antibodies are highly positive."}
            ]
        },
        {
            "id": 18,
            "disease": "Systemic Lupus Erythematosus",
            "accepted_answers": ["systemic lupus erythematosus", "sle", "lupus", "sistemik lupus eritematozus"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 25-year-old African American female presents with extreme fatigue, joint pain, and a rash on her face."},
                {"title": "History & Physical Exam", "text": "She reports the rash worsens in the sun (photosensitivity). Exam reveals painless oral ulcers and an erythematous, raised rash over her cheeks and nasal bridge, sparing the nasolabial folds."},
                {"title": "Basic Labs", "text": "CBC reveals leukopenia and autoimmune hemolytic anemia. Urinalysis shows 3+ protein and red blood cell casts."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows small bilateral pleural effusions, consistent with serositis. Echocardiogram is normal."},
                {"title": "Specific/Advanced Labs", "text": "Antinuclear antibody (ANA) is positive at a high titer (1:640). Anti-dsDNA and Anti-Smith antibodies are also positive. Complement levels (C3, C4) are low."}
            ]
        },
        {
            "id": 19,
            "disease": "Parkinson's Disease",
            "accepted_answers": ["parkinson's disease", "parkinson disease", "parkinsons", "parkinson", "parkinson hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 68-year-old male is brought in by his family who noticed he has been moving very slowly and dragging his right foot."},
                {"title": "History & Physical Exam", "text": "He has a mask-like facial expression, speaks in a soft voice (hypophonia), and his handwriting has become very small (micrographia). Exam reveals a 'pill-rolling' resting tremor in his right hand and cogwheel rigidity in his arms."},
                {"title": "Basic Labs", "text": "Comprehensive metabolic panel, TSH, and vitamin B12 levels are within normal limits."},
                {"title": "Imaging / ECG", "text": "Brain MRI is structurally normal, ruling out stroke, hydrocephalus, or a mass lesion."},
                {"title": "Specific/Advanced Labs", "text": "A clinical trial of Levodopa/Carbidopa is initiated, and the patient shows dramatic improvement in his bradykinesia and rigidity."}
            ]
        },
        {
            "id": 20,
            "disease": "Crohn's Disease",
            "accepted_answers": ["crohn's disease", "crohn disease", "crohns", "crohn", "crohn hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 24-year-old male presents with a 6-month history of crampy right lower quadrant abdominal pain, non-bloody diarrhea, and a 15-lb weight loss."},
                {"title": "History & Physical Exam", "text": "He occasionally feels feverish. On physical exam, he has a low-grade fever and a palpable, tender mass in the right lower quadrant. Inspection of the perianal area reveals a complex fistula."},
                {"title": "Basic Labs", "text": "CBC shows a mild anemia and thrombocytosis. CRP is elevated. Stool cultures for infectious pathogens are negative."},
                {"title": "Imaging / ECG", "text": "CT enterography shows thickening of the terminal ileum with a 'string sign' and creeping fat. Skip lesions are noted in the colon."},
                {"title": "Specific/Advanced Labs", "text": "Colonoscopy reveals patchy, transmural inflammation with deep linear ulcerations creating a 'cobblestone' appearance. Non-caseating granulomas are seen on biopsy."}
            ]
        },
        {
            "id": 21,
            "disease": "Ulcerative Colitis",
            "accepted_answers": ["ulcerative colitis", "uc", "ülseratif kolit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 27-year-old female presents with a 3-month history of frequent, small-volume bloody diarrhea associated with intense urgency (tenesmus) and lower abdominal cramping."},
                {"title": "History & Physical Exam", "text": "She reports feeling fatigued and having joint pains. Exam reveals lower abdominal tenderness but no palpable masses. Rectal exam shows gross blood."},
                {"title": "Basic Labs", "text": "CBC shows microcytic anemia. ESR is elevated. Comprehensive stool testing is negative for C. difficile, Salmonella, Shigella, and Campylobacter."},
                {"title": "Imaging / ECG", "text": "Abdominal X-ray shows loss of normal colonic haustral markings ('lead pipe' appearance) but no toxic megacolon."},
                {"title": "Specific/Advanced Labs", "text": "Flexible sigmoidoscopy reveals continuous, circumferential mucosal inflammation, erythema, and friability starting from the rectum and extending proximally. Biopsies show crypt abscesses."}
            ]
        },
        {
            "id": 22,
            "disease": "Hashimoto's Thyroiditis",
            "accepted_answers": ["hashimoto's thyroiditis", "hashimoto thyroiditis", "hashimoto", "hypothyroidism", "hashimotos", "haşimato", "hipotiroidi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 45-year-old female comes to the clinic complaining of worsening fatigue, cold intolerance, and constipation over the last 8 months."},
                {"title": "History & Physical Exam", "text": "She has gained 10 lbs despite a poor appetite and complains of dry skin and hair loss. Physical exam reveals a firm, rubbery, diffusely enlarged, non-tender thyroid gland. Deep tendon reflexes show delayed relaxation."},
                {"title": "Basic Labs", "text": "Basic metabolic panel shows mild hypercholesterolemia. CBC is normal."},
                {"title": "Imaging / ECG", "text": "Thyroid ultrasound reveals a diffusely heterogeneous, hypoechoic gland without distinct nodules."},
                {"title": "Specific/Advanced Labs", "text": "TSH is markedly elevated (25 mIU/L), and Free T4 is low. Anti-thyroid peroxidase (anti-TPO) antibodies are strongly positive."}
            ]
        },
        {
            "id": 23,
            "disease": "Cushing's Syndrome",
            "accepted_answers": ["cushing's syndrome", "cushing syndrome", "cushings", "cushing sendromu"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 38-year-old female presents with rapid, unexplained weight gain primarily around her abdomen, and new-onset easy bruising."},
                {"title": "History & Physical Exam", "text": "She complains of muscle weakness, particularly when trying to stand up from a chair. Exam reveals central obesity, a 'buffalo hump', facial plethora (moon facies), and wide, purple abdominal striae."},
                {"title": "Basic Labs", "text": "Blood pressure is elevated at 155/95 mmHg. Fasting blood glucose is elevated (diabetic range). Potassium is slightly low (hypokalemia)."},
                {"title": "Imaging / ECG", "text": "DEXA scan shows premature osteoporosis. Brain MRI later reveals a 6 mm microadenoma in the anterior pituitary gland."},
                {"title": "Specific/Advanced Labs", "text": "24-hour urine free cortisol is elevated. A low-dose dexamethasone suppression test fails to suppress serum cortisol, confirming the diagnosis."}
            ]
        },
        {
            "id": 24,
            "disease": "Addison's Disease",
            "accepted_answers": ["addison's disease", "addison disease", "addisons", "primary adrenal insufficiency", "adrenal insufficiency", "addison hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 35-year-old female complains of profound fatigue, anorexia, weight loss, and dizziness upon standing for the past 4 months."},
                {"title": "History & Physical Exam", "text": "She notes she has been craving salty foods. Exam reveals orthostatic hypotension and striking hyperpigmentation of her skin, particularly in the palmar creases, knuckles, and oral mucosa."},
                {"title": "Basic Labs", "text": "Basic metabolic panel is highly suspicious: it shows hyponatremia (Na 128 mEq/L) and hyperkalemia (K 5.6 mEq/L). Mild non-anion gap metabolic acidosis is present."},
                {"title": "Imaging / ECG", "text": "Abdominal CT scan reveals bilateral small, atrophic adrenal glands."},
                {"title": "Specific/Advanced Labs", "text": "An 8:00 AM serum cortisol level is inappropriately low. A Cosyntropin (ACTH) stimulation test shows no significant increase in cortisol levels. Baseline ACTH is markedly elevated."}
            ]
        },
        {
            "id": 25,
            "disease": "Iron Deficiency Anemia",
            "accepted_answers": ["iron deficiency anemia", "ida", "demir eksikliği anemisi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 30-year-old female presents with generalized weakness, fatigue, and decreased exercise tolerance."},
                {"title": "History & Physical Exam", "text": "She has a history of heavy menstrual bleeding (menorrhagia) and reports a strange craving for chewing ice (pica). Exam reveals pale conjunctivae and brittle, spoon-shaped nails (koilonychia)."},
                {"title": "Basic Labs", "text": "CBC shows Hemoglobin 9.0 g/dL, MCV 72 fL (microcytic), and an elevated Red Cell Distribution Width (RDW)."},
                {"title": "Imaging / ECG", "text": "Peripheral blood smear shows microcytic, hypochromic red blood cells with central pallor."},
                {"title": "Specific/Advanced Labs", "text": "Serum ferritin is extremely low (<15 ng/mL). Total iron-binding capacity (TIBC) is elevated, and transferrin saturation is low."}
            ]
        },
        {
            "id": 26,
            "disease": "Vitamin B12 Deficiency",
            "accepted_answers": ["vitamin b12 deficiency", "b12 deficiency", "pernicious anemia", "cobalamin deficiency", "b12 eksikliği"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 65-year-old male presents with fatigue, a smooth, sore tongue (glossitis), and a 'pins and needles' sensation in his feet."},
                {"title": "History & Physical Exam", "text": "He follows a strict vegan diet without supplementation. Neurological exam reveals decreased vibratory and position sense in his lower extremities, and a wide-based, unsteady gait."},
                {"title": "Basic Labs", "text": "CBC shows Hemoglobin 10.5 g/dL with a significantly elevated MCV of 115 fL (macrocytic). Mild pancytopenia is also noted."},
                {"title": "Imaging / ECG", "text": "Peripheral blood smear reveals large, oval red blood cells (macro-ovalocytes) and hypersegmented neutrophils (>5 lobes)."},
                {"title": "Specific/Advanced Labs", "text": "Serum cobalamin (Vitamin B12) is low. Serum methylmalonic acid (MMA) and homocysteine levels are both markedly elevated."}
            ]
        },
        {
            "id": 27,
            "disease": "Sickle Cell Anemia",
            "accepted_answers": ["sickle cell anemia", "sickle cell disease", "scd", "orak hücreli anemi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 22-year-old African American male presents to the ER with excruciating pain in his lower back, ribs, and legs."},
                {"title": "History & Physical Exam", "text": "He has a known history of a genetic blood disorder. The pain started after he became dehydrated while playing basketball. Exam shows scleral icterus and tenderness over the long bones."},
                {"title": "Basic Labs", "text": "CBC reveals a normocytic anemia with a high reticulocyte count (8%). Total bilirubin and LDH are elevated, indicating hemolysis."},
                {"title": "Imaging / ECG", "text": "Peripheral blood smear reveals characteristic crescent-shaped red blood cells and Howell-Jolly bodies (indicating functional asplenia)."},
                {"title": "Specific/Advanced Labs", "text": "Hemoglobin electrophoresis confirms the presence of mostly HbS with absent HbA."}
            ]
        },
        {
            "id": 28,
            "disease": "Deep Vein Thrombosis",
            "accepted_answers": ["deep vein thrombosis", "dvt", "derin ven trombozu"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 55-year-old female presents with sudden swelling, pain, and redness in her left leg."},
                {"title": "History & Physical Exam", "text": "She recently underwent orthopedic surgery (hip replacement) and has been largely bedbound for a week. Exam shows unilateral left calf swelling with pitting edema, erythema, and a positive Homan's sign (pain on dorsiflexion)."},
                {"title": "Basic Labs", "text": "CBC and chemistry are normal. D-dimer is highly elevated (>2000 ng/mL)."},
                {"title": "Imaging / ECG", "text": "Compression Doppler ultrasound of the lower extremities shows a lack of compressibility and lack of normal blood flow in the left popliteal and femoral veins."},
                {"title": "Specific/Advanced Labs", "text": "Hypercoagulability workup (Factor V Leiden, Prothrombin gene mutation) is drawn for future evaluation, but therapeutic anticoagulation is started immediately."}
            ]
        },
        {
            "id": 29,
            "disease": "Infective Endocarditis",
            "accepted_answers": ["infective endocarditis", "endocarditis", "bacterial endocarditis", "enfektif endokardit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 34-year-old male presents with a 2-week history of spiking fevers, chills, fatigue, and night sweats."},
                {"title": "History & Physical Exam", "text": "He has a history of intravenous drug use. Exam reveals a new, loud holosystolic murmur at the cardiac apex. You also note painful red nodules on his fingertips (Osler nodes) and painless erythematous lesions on his palms (Janeway lesions)."},
                {"title": "Basic Labs", "text": "CBC shows leukocytosis and normocytic anemia. ESR and CRP are elevated. Urinalysis shows microscopic hematuria."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows multiple patchy pulmonary infiltrates, suggesting septic emboli (especially common in right-sided valve involvement, though this patient's murmur suggests left)."},
                {"title": "Specific/Advanced Labs", "text": "Three sets of blood cultures drawn from different sites all grow Staphylococcus aureus. Transesophageal echocardiogram (TEE) reveals a 1.5 cm mobile vegetation on the mitral valve."}
            ]
        },
        {
            "id": 30,
            "disease": "Gout",
            "accepted_answers": ["gout", "gouty arthritis", "got", "gut", "gut hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 50-year-old male is awakened in the middle of the night by excruciating pain, redness, and swelling in his right big toe."},
                {"title": "History & Physical Exam", "text": "He states he attended a steak and seafood dinner with heavy alcohol consumption the night before. Exam reveals an exquisitely tender, erythematous, warm, and swollen 1st metatarsophalangeal (MTP) joint (podagra)."},
                {"title": "Basic Labs", "text": "Serum uric acid level is surprisingly within the upper limits of normal during this acute attack. CBC shows mild leukocytosis."},
                {"title": "Imaging / ECG", "text": "X-ray of the foot shows soft tissue swelling but no acute fractures. Punched-out erosions with overhanging edges ('rat bite' erosions) are not yet present as this is a first-time attack."},
                {"title": "Specific/Advanced Labs", "text": "Arthrocentesis (joint aspiration) is performed. Synovial fluid analysis reveals numerous polymorphonuclear leukocytes and strongly negative-birefringent, needle-shaped crystals under polarized light microscopy."}
            ]
        },{
            "id": 31,
            "disease": "Acute Kidney Injury",
            "accepted_answers": ["acute kidney injury", "aki", "acute renal failure", "arf", "akut böbrek yetmezliği", "akut böbrek hasarı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 68-year-old male is admitted to the hospital with severe dizziness, confusion, and significantly decreased urine output over the last 48 hours."},
                {"title": "History & Physical Exam", "text": "He had a severe bout of gastroenteritis with intractable vomiting and diarrhea for 3 days prior to admission. Exam reveals dry mucous membranes, poor skin turgor, and orthostatic hypotension."},
                {"title": "Basic Labs", "text": "Serum creatinine has acutely risen from a baseline of 0.9 mg/dL to 3.2 mg/dL. BUN is 80 mg/dL (BUN/Cr ratio > 20:1)."},
                {"title": "Imaging / ECG", "text": "Renal ultrasound is normal with no evidence of hydronephrosis, ruling out a post-renal obstruction."},
                {"title": "Specific/Advanced Labs", "text": "Urinalysis reveals a high specific gravity and hyaline casts, but no RBCs or WBCs. Fractional excretion of sodium (FeNa) is <1%, consistent with a prerenal etiology."}
            ]
        },
        {
            "id": 32,
            "disease": "Chronic Kidney Disease",
            "accepted_answers": ["chronic kidney disease", "ckd", "chronic renal failure", "kronik böbrek yetmezliği", "kby"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 60-year-old female presents to her primary care physician for a routine check-up, feeling generally fatigued and noting generalized itching (pruritus)."},
                {"title": "History & Physical Exam", "text": "She has a 20-year history of poorly controlled Type 2 Diabetes and Hypertension. Exam reveals pallor and trace bilateral pedal edema."},
                {"title": "Basic Labs", "text": "Serum creatinine is 2.8 mg/dL (stable from 6 months ago). eGFR is 22 mL/min. She has hyperphosphatemia and hypocalcemia."},
                {"title": "Imaging / ECG", "text": "Renal ultrasound demonstrates bilateral small, echogenic kidneys with thinned out cortex."},
                {"title": "Specific/Advanced Labs", "text": "Urinalysis shows 3+ proteinuria. CBC reveals a normocytic, normochromic anemia due to decreased erythropoietin production."}
            ]
        },
        {
            "id": 33,
            "disease": "Nephrotic Syndrome",
            "accepted_answers": ["nephrotic syndrome", "nefrotik sendrom"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 45-year-old male presents with worsening swelling around his eyes (periorbital edema) in the mornings and massive swelling of his legs."},
                {"title": "History & Physical Exam", "text": "He noticed his urine appears very frothy. Exam confirms 3+ pitting edema up to his thighs and moderate ascites."},
                {"title": "Basic Labs", "text": "Serum albumin is profoundly low at 2.1 g/dL. Lipid panel reveals severe hypercholesterolemia (Total Cholesterol > 400 mg/dL)."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows small bilateral pleural effusions (transudative) but a normal heart size."},
                {"title": "Specific/Advanced Labs", "text": "24-hour urine collection confirms massive proteinuria at 4.5 grams/day. Renal biopsy is performed to determine the specific histological subtype (e.g., Membranous nephropathy)."}
            ]
        },
        {
            "id": 34,
            "disease": "Nephrolithiasis",
            "accepted_answers": ["nephrolithiasis", "kidney stone", "renal calculi", "böbrek taşı", "ürolitiazis"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 35-year-old male arrives at the ER writhing in pain, unable to find a comfortable position. He describes sudden, agonizing, colicky pain in his right flank that radiates to his groin."},
                {"title": "History & Physical Exam", "text": "He has been nauseous and vomited twice. Exam reveals significant right costovertebral angle (CVA) tenderness. He is completely afebrile."},
                {"title": "Basic Labs", "text": "CBC and chemistry are normal. Urinalysis reveals gross hematuria with numerous RBCs, but no nitrites or leukocyte esterase."},
                {"title": "Imaging / ECG", "text": "Non-contrast spiral CT of the abdomen and pelvis reveals a 5 mm radiopaque density in the right ureterovesical junction (UVJ) with mild proximal hydroureter."},
                {"title": "Specific/Advanced Labs", "text": "Stone analysis (if passed) usually reveals calcium oxalate composition, the most common type."}
            ]
        },
        {
            "id": 35,
            "disease": "Pyelonephritis",
            "accepted_answers": ["pyelonephritis", "acute pyelonephritis", "piyelonefrit", "akut piyelonefrit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 28-year-old female presents with high fever, chills, nausea, and left-sided flank pain for the past 24 hours."},
                {"title": "History & Physical Exam", "text": "She reports having burning with urination (dysuria) and urinary frequency for three days prior to the onset of fever. Exam shows severe left costovertebral angle (CVA) tenderness."},
                {"title": "Basic Labs", "text": "CBC shows significant leukocytosis with a left shift. Blood cultures are drawn."},
                {"title": "Imaging / ECG", "text": "Imaging is typically not needed for classic presentations, but a renal ultrasound could show a swollen, edematous kidney."},
                {"title": "Specific/Advanced Labs", "text": "Urinalysis shows pyuria (many WBCs), positive leukocyte esterase, positive nitrites, and the pathognomonic finding of WBC casts. Urine culture grows E. coli >100,000 CFU/mL."}
            ]
        },
        {
            "id": 36,
            "disease": "Lyme Disease",
            "accepted_answers": ["lyme disease", "lyme", "borreliosis", "lyme hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 32-year-old male presents to the clinic with fatigue, low-grade fever, muscle aches, and a distinct skin rash."},
                {"title": "History & Physical Exam", "text": "He recently returned from a camping trip in the northeastern United States (Connecticut). Exam reveals a large, expanding, erythematous rash with central clearing (target-like appearance) on his thigh."},
                {"title": "Basic Labs", "text": "Basic blood work including CBC and CMP is completely normal."},
                {"title": "Imaging / ECG", "text": "ECG is performed to rule out early cardiac involvement (like AV block), which is currently normal."},
                {"title": "Specific/Advanced Labs", "text": "The pathognomonic rash (Erythema migrans) is sufficient for clinical diagnosis. Serology (ELISA followed by Western Blot for Borrelia burgdorferi) is sent but may be negative in this early localized stage."}
            ]
        },
        {
            "id": 37,
            "disease": "Syphilis",
            "accepted_answers": ["syphilis", "primary syphilis", "sifiliz", "frengi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 26-year-old male presents with a painless ulcer on his penis that he noticed 2 weeks ago."},
                {"title": "History & Physical Exam", "text": "He reports recent unprotected sexual encounters with a new partner. Exam reveals a single, firm, indurated, painless ulcer (chancre) with a clean base on the glans penis, and bilateral non-tender inguinal lymphadenopathy."},
                {"title": "Basic Labs", "text": "Routine labs are normal. HIV and Hepatitis screening are performed simultaneously."},
                {"title": "Imaging / ECG", "text": "No imaging is indicated for this condition."},
                {"title": "Specific/Advanced Labs", "text": "Dark-field microscopy of exudate from the lesion shows motile spirochetes. Non-treponemal tests (RPR/VDRL) and Treponemal-specific tests (FTA-ABS) are positive."}
            ]
        },
        {
            "id": 38,
            "disease": "Cellulitis",
            "accepted_answers": ["cellulitis", "selülit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 50-year-old male presents with a rapidly spreading, red, swollen, and painful area on his lower right leg."},
                {"title": "History & Physical Exam", "text": "He has a history of Tinea pedis (athlete's foot). He feels feverish. Exam reveals an ill-defined, erythematous, warm, exquisitely tender plaque on the anterior tibia. No fluctuance or purulence is noted."},
                {"title": "Basic Labs", "text": "CBC shows mild leukocytosis. Inflammatory markers (CRP) are elevated."},
                {"title": "Imaging / ECG", "text": "Ultrasound of the leg rules out deep vein thrombosis (DVT) and shows subcutaneous edema but no deep fluid collection/abscess."},
                {"title": "Specific/Advanced Labs", "text": "Blood cultures are rarely positive. Diagnosis is primarily clinical, targeting skin flora (Streptococcus pyogenes and Staphylococcus aureus) with empiric oral antibiotics."}
            ]
        },
        {
            "id": 39,
            "disease": "Pneumocystis Pneumonia",
            "accepted_answers": ["pneumocystis pneumonia", "pcp", "pjp", "pneumocystis jirovecii pneumonia", "pnömosistis pnömonisi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 35-year-old male presents with a progressive dry, non-productive cough, worsening exertional dyspnea, and low-grade fever over the past 3 weeks."},
                {"title": "History & Physical Exam", "text": "He has a history of untreated HIV infection. He appears cachectic and is tachypneic. Lung auscultation is surprisingly clear despite his significant hypoxia."},
                {"title": "Basic Labs", "text": "Arterial blood gas shows significant hypoxia. CD4 count is checked and comes back critically low at 120 cells/mm3."},
                {"title": "Imaging / ECG", "text": "Chest X-ray reveals diffuse, bilateral, symmetrical interstitial infiltrates radiating from the hila in a 'bat-wing' or 'ground-glass' pattern."},
                {"title": "Specific/Advanced Labs", "text": "Elevated serum Lactate Dehydrogenase (LDH) is noted. Bronchoalveolar lavage (BAL) fluid stained with methenamine silver reveals characteristic cysts, confirming the fungus."}
            ]
        },
        {
            "id": 40,
            "disease": "Malaria",
            "accepted_answers": ["malaria", "sıtma", "plasmodium falciparum"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 40-year-old female presents to the ER with cyclical high fevers, severe shaking chills (rigors), and drenching sweats occurring every 48 hours."},
                {"title": "History & Physical Exam", "text": "She returned from a business trip to sub-Saharan Africa 2 weeks ago and admits she forgot to take her prophylactic medication. Exam reveals pallor, mild jaundice, and splenomegaly."},
                {"title": "Basic Labs", "text": "CBC shows hemolytic anemia and thrombocytopenia. CMP shows elevated indirect bilirubin and elevated transaminases."},
                {"title": "Imaging / ECG", "text": "Abdominal ultrasound confirms splenomegaly. Chest X-ray is clear."},
                {"title": "Specific/Advanced Labs", "text": "Thick and thin Giemsa-stained peripheral blood smears demonstrate intracellular parasites (ring forms and banana-shaped gametocytes), confirming Plasmodium falciparum infection."}
            ]
        },
        {
            "id": 41,
            "disease": "Herpes Zoster",
            "accepted_answers": ["herpes zoster", "shingles", "zona", "zona zoster"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 65-year-old female presents with severe, burning, neuropathic pain on the right side of her chest that started 3 days ago, followed by a new rash today."},
                {"title": "History & Physical Exam", "text": "She has a history of childhood chickenpox. Exam reveals grouped vesicular lesions on an erythematous base strictly following the T4 dermatome on the right, not crossing the midline."},
                {"title": "Basic Labs", "text": "Standard laboratory tests are normal and usually unnecessary for this classic clinical presentation."},
                {"title": "Imaging / ECG", "text": "No imaging is required."},
                {"title": "Specific/Advanced Labs", "text": "Though the diagnosis is clinical, a Tzanck smear from the base of a vesicle would show multinucleated giant cells. Viral culture or PCR would confirm Varicella-Zoster Virus (VZV) reactivation."}
            ]
        },
        {
            "id": 42,
            "disease": "Melanoma",
            "accepted_answers": ["melanoma", "malignant melanoma", "melanom"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 55-year-old fair-skinned male comes in for a routine skin check and points out a 'mole' on his back that has been changing over the past 6 months."},
                {"title": "History & Physical Exam", "text": "He has a history of frequent severe sunburns in his youth. Exam reveals a 9 mm pigmented lesion on his upper back that is asymmetrical, has irregular borders, and features multiple colors (black, brown, and blue)."},
                {"title": "Basic Labs", "text": "Standard blood tests are normal."},
                {"title": "Imaging / ECG", "text": "A PET-CT scan may be ordered later if the diagnosis is confirmed and staging is required to check for metastasis."},
                {"title": "Specific/Advanced Labs", "text": "An excisional biopsy with narrow margins is performed. Histopathology reveals malignant melanocytes invading the dermis (Breslow depth 1.5 mm)."}
            ]
        },
        {
            "id": 43,
            "disease": "Basal Cell Carcinoma",
            "accepted_answers": ["basal cell carcinoma", "bcc", "bazal hücreli karsinom"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 70-year-old male farmer presents with a slow-growing bump on his nose that occasionally bleeds when he washes his face."},
                {"title": "History & Physical Exam", "text": "He has spent most of his life working outdoors without sun protection. Exam reveals a 6 mm pearly, pink, translucent papule on the nasal ala with prominent telangiectasias (visible tiny blood vessels) and a central rolled border."},
                {"title": "Basic Labs", "text": "Blood tests are not indicated."},
                {"title": "Imaging / ECG", "text": "No imaging is indicated as this tumor practically never metastasizes, though it is locally destructive."},
                {"title": "Specific/Advanced Labs", "text": "A shave or punch biopsy confirms nests of basaloid cells with peripheral palisading extending from the epidermis into the dermis."}
            ]
        },
        {
            "id": 44,
            "disease": "Osteoarthritis",
            "accepted_answers": ["osteoarthritis", "oa", "degenerative joint disease", "djd", "osteoartrit", "kireçlenme"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 68-year-old overweight female complains of deep, aching pain in both knees that worsens with activity and improves with rest."},
                {"title": "History & Physical Exam", "text": "She experiences morning stiffness in her knees lasting less than 30 minutes. Exam reveals bony enlargement of the knees, crepitus on passive range of motion, and Heberden's nodes on her distal interphalangeal (DIP) joints."},
                {"title": "Basic Labs", "text": "ESR, CRP, and Rheumatoid Factor are all completely normal, ruling out an inflammatory or autoimmune etiology."},
                {"title": "Imaging / ECG", "text": "Weight-bearing X-rays of the knees demonstrate asymmetric joint space narrowing, subchondral sclerosis, and osteophyte formation (bone spurs)."},
                {"title": "Specific/Advanced Labs", "text": "If synovial fluid were aspirated, it would be non-inflammatory (WBC < 2,000/µL) and clear/yellow."}
            ]
        },
        {
            "id": 45,
            "disease": "Osteoporosis",
            "accepted_answers": ["osteoporosis", "osteoporoz", "kemik erimesi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 72-year-old postmenopausal female presents to the ER after suffering a fracture of her distal radius (Colles' fracture) from a simple fall from a standing height."},
                {"title": "History & Physical Exam", "text": "She has noted a loss of 2 inches in height over the last decade and increased forward curvature of her upper back (kyphosis). She is thin and frail."},
                {"title": "Basic Labs", "text": "Serum calcium, phosphate, parathyroid hormone (PTH), and alkaline phosphatase levels are surprisingly entirely normal."},
                {"title": "Imaging / ECG", "text": "X-rays confirm the distal radius fracture. Lateral spine X-ray incidentally reveals a wedge compression fracture of the T12 vertebra."},
                {"title": "Specific/Advanced Labs", "text": "A Dual-Energy X-ray Absorptiometry (DEXA) scan is performed, revealing a T-score of -2.8 at the femoral neck and lumbar spine, confirming severe reduction in bone mineral density."}
            ]
        },{
            "id": 46,
            "disease": "Celiac Disease",
            "accepted_answers": ["celiac disease", "coeliac disease", "gluten enteropathy", "çölyak", "çölyak hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 28-year-old female complains of chronic diarrhea, bloating, abdominal pain, and weight loss over the past year."},
                {"title": "History & Physical Exam", "text": "She reports her stools are bulky, foul-smelling, and difficult to flush. She also has intensely itchy, grouped vesicular lesions on her elbows and knees (dermatitis herpetiformis)."},
                {"title": "Basic Labs", "text": "CBC shows microcytic anemia due to iron deficiency. CMP shows mild transaminitis and decreased serum calcium/Vitamin D."},
                {"title": "Imaging / ECG", "text": "A bone density scan (DEXA) reveals early-onset osteopenia, likely due to chronic malabsorption of calcium and Vitamin D."},
                {"title": "Specific/Advanced Labs", "text": "IgA tissue transglutaminase (tTG-IgA) and endomysial antibodies are highly positive. Upper endoscopy with duodenal biopsy confirms crypt hyperplasia and villous atrophy."}
            ]
        },
        {
            "id": 47,
            "disease": "Gastroesophageal Reflux Disease",
            "accepted_answers": ["gerd", "gastroesophageal reflux disease", "reflux", "reflü", "gastroözofageal reflü"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 45-year-old overweight male presents with a chronic, burning sensation in his mid-chest that radiates toward his neck."},
                {"title": "History & Physical Exam", "text": "He states the pain typically starts 30 minutes after eating heavy meals and is significantly worse when he lies down to sleep. He also reports a frequent sour taste in his mouth."},
                {"title": "Basic Labs", "text": "Cardiac enzymes (Troponin) and CBC are perfectly normal, ruling out an acute coronary syndrome or GI bleed."},
                {"title": "Imaging / ECG", "text": "An ECG is performed in the clinic to rule out cardiac ischemia; it shows normal sinus rhythm with no ST-T wave changes."},
                {"title": "Specific/Advanced Labs", "text": "A trial of Proton Pump Inhibitors (PPIs) completely resolves his symptoms. An upper endoscopy (EGD) is planned to rule out Barrett's esophagus due to his chronic symptoms."}
            ]
        },
        {
            "id": 48,
            "disease": "Peripheral Arterial Disease",
            "accepted_answers": ["peripheral arterial disease", "pad", "peripheral vascular disease", "pvd", "periferik arter hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 65-year-old male with a long history of smoking complains of a cramping, aching pain in his right calf that occurs strictly when walking."},
                {"title": "History & Physical Exam", "text": "The pain forces him to stop and rest, after which it completely resolves within 5 minutes (intermittent claudication). Exam reveals cool lower extremities, loss of hair on the shins, and non-palpable dorsalis pedis pulses."},
                {"title": "Basic Labs", "text": "Lipid panel shows hyperlipidemia. Fasting blood glucose is elevated, consistent with newly diagnosed Type 2 Diabetes."},
                {"title": "Imaging / ECG", "text": "Arterial duplex ultrasound of the lower extremities shows significant stenosis in the superficial femoral artery."},
                {"title": "Specific/Advanced Labs", "text": "Ankle-Brachial Index (ABI) is calculated and found to be 0.65 in the right leg (normal > 0.9), confirming severe occlusive disease."}
            ]
        },
        {
            "id": 49,
            "disease": "Abdominal Aortic Aneurysm",
            "accepted_answers": ["abdominal aortic aneurysm", "aaa", "abdominal aort anevrizması"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 70-year-old male former smoker comes to the clinic for a routine check-up. He is entirely asymptomatic."},
                {"title": "History & Physical Exam", "text": "His past medical history includes hypertension and hyperlipidemia. On deep abdominal palpation, you feel a prominent, pulsatile, non-tender mass slightly to the left of the midline, above the umbilicus."},
                {"title": "Basic Labs", "text": "Routine blood tests (CBC, CMP) are normal. There is no evidence of acute hemorrhage or infection."},
                {"title": "Imaging / ECG", "text": "An abdominal ultrasound is immediately ordered and demonstrates a localized dilation of the infrarenal aorta measuring 5.5 cm in diameter."},
                {"title": "Specific/Advanced Labs", "text": "A CT angiography of the abdomen and pelvis is ordered for preoperative planning before referring him to vascular surgery for repair."}
            ]
        },
        {
            "id": 50,
            "disease": "Aortic Dissection",
            "accepted_answers": ["aortic dissection", "aort diseksiyonu", "thoracic aortic dissection"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 60-year-old male with poorly controlled hypertension presents to the ER with sudden, agonizing, 'tearing' chest pain that radiates straight to his back between his shoulder blades."},
                {"title": "History & Physical Exam", "text": "He appears acutely ill and diaphoretic. Physical exam reveals a blood pressure of 190/110 mmHg in his right arm, but only 110/70 mmHg in his left arm. A new decrescendo diastolic murmur is heard at the right sternal border."},
                {"title": "Basic Labs", "text": "Troponin is negative. D-dimer is elevated, which can be seen in this condition due to activation of the coagulation cascade by the false lumen."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows a prominently widened mediastinum. ECG shows left ventricular hypertrophy but no acute ischemic changes."},
                {"title": "Specific/Advanced Labs", "text": "CT Angiography of the chest reveals an intimal flap in the ascending aorta extending into the aortic arch (Stanford Type A). He is rushed to emergent cardiovascular surgery."}
            ]
        },
        {
            "id": 51,
            "disease": "Acute Pericarditis",
            "accepted_answers": ["acute pericarditis", "pericarditis", "akut perikardit", "perikardit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 35-year-old male presents with sharp, severe, pleuritic chest pain that started yesterday."},
                {"title": "History & Physical Exam", "text": "He reports having a viral upper respiratory infection a week ago. The pain worsens when he takes a deep breath or lies flat on his back, and improves significantly when he leans forward. Auscultation reveals a scratching, high-pitched extra heart sound (friction rub)."},
                {"title": "Basic Labs", "text": "Troponin levels are normal or only minimally elevated. ESR and CRP are high."},
                {"title": "Imaging / ECG", "text": "ECG reveals widespread, diffuse ST-segment elevations across almost all leads, with PR-segment depressions."},
                {"title": "Specific/Advanced Labs", "text": "Echocardiogram shows a small, trace pericardial effusion without signs of tamponade. He is treated successfully with NSAIDs and Colchicine."}
            ]
        },
        {
            "id": 52,
            "disease": "Atrial Fibrillation",
            "accepted_answers": ["atrial fibrillation", "afib", "af", "atriyal fibrilasyon"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 68-year-old female complains of sudden onset 'fluttering' in her chest, mild shortness of breath, and feeling tired."},
                {"title": "History & Physical Exam", "text": "She has a history of hypertension. On examination, her pulse is rapid (130 bpm) and irregularly irregular. No distinct murmurs are heard."},
                {"title": "Basic Labs", "text": "TSH is checked and is normal, ruling out hyperthyroidism as a secondary cause of her arrhythmia."},
                {"title": "Imaging / ECG", "text": "ECG confirms an irregularly irregular rhythm with narrow QRS complexes and a complete absence of distinct P waves. Fibrillatory waves are seen in lead V1."},
                {"title": "Specific/Advanced Labs", "text": "An Echocardiogram is ordered to evaluate left atrial size and left ventricular ejection fraction. Her CHA2DS2-VASc score is calculated to decide on anticoagulation therapy."}
            ]
        },
        {
            "id": 53,
            "disease": "Spontaneous Pneumothorax",
            "accepted_answers": ["spontaneous pneumothorax", "pneumothorax", "pnömotoraks", "spontan pnömotoraks"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 21-year-old male, who is notably tall and thin, presents to the ER with sudden onset of right-sided chest pain and shortness of breath that occurred while watching TV."},
                {"title": "History & Physical Exam", "text": "He is a smoker but has no prior lung disease. Exam shows decreased chest excursion, hyperresonance to percussion, and absent breath sounds strictly over the right hemithorax."},
                {"title": "Basic Labs", "text": "Pulse oximetry shows 94% on room air. ABG is generally unrevealing."},
                {"title": "Imaging / ECG", "text": "Upright Chest X-ray demonstrates a visible visceral pleural line with absent lung markings peripheral to this line on the right side. Trachea is midline (no tension)."},
                {"title": "Specific/Advanced Labs", "text": "No advanced labs needed. He is treated with supplemental oxygen and chest tube placement, likely due to a ruptured subpleural apical bleb."}
            ]
        },
        {
            "id": 54,
            "disease": "Obstructive Sleep Apnea",
            "accepted_answers": ["obstructive sleep apnea", "osa", "sleep apnea", "uyku apnesi", "obstrüktif uyku apnesi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 52-year-old obese male is brought to the clinic by his wife, who complains of his extremely loud, disruptive snoring."},
                {"title": "History & Physical Exam", "text": "The patient complains of waking up with morning headaches and feeling exhausted all day, often falling asleep during meetings. His wife reports he frequently stops breathing for 20-30 seconds during sleep. Exam reveals a thick neck (circumference > 17 inches) and a crowded oropharynx."},
                {"title": "Basic Labs", "text": "CBC shows secondary polycythemia (elevated hematocrit) due to chronic nocturnal hypoxia."},
                {"title": "Imaging / ECG", "text": "Echocardiogram shows signs of early right ventricular hypertrophy (cor pulmonale) secondary to hypoxic pulmonary vasoconstriction."},
                {"title": "Specific/Advanced Labs", "text": "An overnight Polysomnography (sleep study) demonstrates an Apnea-Hypopnea Index (AHI) of 35 episodes per hour. CPAP therapy is initiated."}
            ]
        },
        {
            "id": 55,
            "disease": "Sarcoidosis",
            "accepted_answers": ["sarcoidosis", "sarkoidoz"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 35-year-old African American female presents with a progressive dry cough, shortness of breath, and fatigue over the last 3 months."},
                {"title": "History & Physical Exam", "text": "She recently noticed painful, red, raised nodules on the anterior surface of her lower legs (erythema nodosum). She also complains of blurry vision. Exam is otherwise largely unremarkable."},
                {"title": "Basic Labs", "text": "Comprehensive metabolic panel reveals hypercalcemia. CBC is normal."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows prominent, symmetric bilateral hilar and right paratracheal lymphadenopathy."},
                {"title": "Specific/Advanced Labs", "text": "Serum Angiotensin-Converting Enzyme (ACE) levels are elevated. Bronchoscopy with transbronchial biopsy reveals widespread non-caseating granulomas."}
            ]
        },
        {
            "id": 56,
            "disease": "Polycystic Ovary Syndrome",
            "accepted_answers": ["polycystic ovary syndrome", "pcos", "polikistik over sendromu", "pcos sendromu"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 24-year-old female presents to the gynecology clinic complaining of irregular, infrequent menstrual periods (oligomenorrhea) and difficulty losing weight."},
                {"title": "History & Physical Exam", "text": "She also complains of worsening acne and increased coarse hair growth on her upper lip and chin (hirsutism). Exam reveals a BMI of 32 and dark, velvety skin patches on the back of her neck (acanthosis nigricans)."},
                {"title": "Basic Labs", "text": "Fasting glucose and insulin levels are elevated, indicating insulin resistance."},
                {"title": "Imaging / ECG", "text": "Pelvic ultrasound reveals enlarged ovaries with multiple small, peripherally arranged cysts resembling a 'string of pearls'."},
                {"title": "Specific/Advanced Labs", "text": "Hormone profile shows an abnormally elevated LH-to-FSH ratio (often >2:1) and elevated serum free testosterone levels."}
            ]
        },
        {
            "id": 57,
            "disease": "Diabetes Insipidus",
            "accepted_answers": ["diabetes insipidus", "di", "şekersiz diyabet", "diyabetes insipidus"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 30-year-old male presents with extreme thirst (polydipsia) and constant, large-volume urination (polyuria) occurring day and night."},
                {"title": "History & Physical Exam", "text": "He drinks up to 8 liters of water a day. He recently suffered a severe closed head injury in a motorcycle accident. He is currently thirsty but his exam is otherwise normal, without signs of dehydration because he is actively drinking water."},
                {"title": "Basic Labs", "text": "Fasting blood glucose and HbA1c are completely normal. Serum sodium is high-normal to mildly elevated (hypernatremia)."},
                {"title": "Imaging / ECG", "text": "Brain MRI focusing on the pituitary gland shows an absence of the normal posterior pituitary 'bright spot' on T1-weighted imaging."},
                {"title": "Specific/Advanced Labs", "text": "Urine specific gravity and osmolality are extremely low despite his elevated serum osmolality. A Water Deprivation Test confirms the diagnosis, and administering exogenous ADH (Desmopressin) rapidly concentrates his urine."}
            ]
        },
        {
            "id": 58,
            "disease": "Primary Hyperparathyroidism",
            "accepted_answers": ["primary hyperparathyroidism", "hyperparathyroidism", "primer hiperparatiroidi", "hiperparatiroidi"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 55-year-old female presents with bone pain, recent onset of constipation, frequent urination, and feeling mildly depressed ('bones, stones, abdominal groans, and psychic moans')."},
                {"title": "History & Physical Exam", "text": "She has a history of recurrent calcium oxalate kidney stones over the past two years. Physical exam is mostly unremarkable; the neck reveals no palpable masses."},
                {"title": "Basic Labs", "text": "Routine chemistry panel shows hypercalcemia (Ca: 11.8 mg/dL) and hypophosphatemia (Phos: 2.1 mg/dL)."},
                {"title": "Imaging / ECG", "text": "Hand X-rays show subperiosteal bone resorption on the radial aspect of the middle phalanges. DEXA scan reveals osteoporosis."},
                {"title": "Specific/Advanced Labs", "text": "Intact Parathyroid Hormone (PTH) level is inappropriately elevated despite the high serum calcium. A Sestamibi neck scan reveals increased uptake in a single adenoma behind the lower pole of the right thyroid lobe."}
            ]
        },
        {
            "id": 59,
            "disease": "Myasthenia Gravis",
            "accepted_answers": ["myasthenia gravis", "mg", "miyasteni", "miyastenia gravis"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 32-year-old female presents with drooping of her eyelids (ptosis) and double vision (diplopia) that fluctuates throughout the day."},
                {"title": "History & Physical Exam", "text": "She notes her symptoms are mild in the morning but progressively worsen by the evening. She also feels her jaw gets tired halfway through chewing a meal. Exam confirms asymmetric ptosis and easily fatigable proximal muscles."},
                {"title": "Basic Labs", "text": "Basic blood tests, including TSH and CK (creatine kinase), are within normal limits."},
                {"title": "Imaging / ECG", "text": "CT scan of the chest reveals an anterior mediastinal mass, identified as a thymoma."},
                {"title": "Specific/Advanced Labs", "text": "Application of an ice pack to her droopy eyelid for 2 minutes significantly improves the ptosis. Serology is strongly positive for Acetylcholine Receptor (AChR) antibodies."}
            ]
        },
        {
            "id": 60,
            "disease": "Guillain-Barre Syndrome",
            "accepted_answers": ["guillain-barre syndrome", "gbs", "guillain barre", "guillain-barré sendromu", "gbs sendromu"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 40-year-old male presents to the ER with progressive weakness and tingling in both of his legs that started 2 days ago."},
                {"title": "History & Physical Exam", "text": "He reports having a severe diarrheal illness (Campylobacter jejuni) about 3 weeks ago. On exam, he has symmetric, flaccid weakness in his lower extremities. Deep tendon reflexes (DTRs) at the knees and ankles are completely absent (areflexia)."},
                {"title": "Basic Labs", "text": "Routine CBC and chemistry are normal. Potassium levels are normal, ruling out hypokalemic periodic paralysis."},
                {"title": "Imaging / ECG", "text": "MRI of the spine with contrast shows enhancement of the spinal nerve roots (cauda equina)."},
                {"title": "Specific/Advanced Labs", "text": "Lumbar puncture is performed. CSF analysis reveals a very high protein level (>100 mg/dL) with a normal white blood cell count, classic for albuminocytologic dissociation."}
            ]
        },{
            "id": 61,
            "disease": "Acute HIV Infection",
            "accepted_answers": ["hiv", "acute hiv infection", "hiv infection", "human immunodeficiency virus", "akut hiv enfeksiyonu"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 25-year-old male presents with a 4-day history of fever, severe sore throat, diffuse non-pruritic maculopapular rash, and fatigue."},
                {"title": "History & Physical Exam", "text": "He reports unprotected sexual intercourse with a new partner 2 weeks ago. He thought he had 'mono'. Exam reveals generalized non-tender lymphadenopathy and painful mucocutaneous ulcers in the mouth."},
                {"title": "Basic Labs", "text": "CBC shows mild leukopenia, thrombocytopenia, and atypical lymphocytes. Monospot test for EBV is negative."},
                {"title": "Imaging / ECG", "text": "Chest X-ray is clear. No focal consolidation or adenopathy in the chest."},
                {"title": "Specific/Advanced Labs", "text": "4th generation HIV Ag/Ab combination assay is positive due to high p24 antigen, although HIV-1/HIV-2 differentiation antibody assay is indeterminate. HIV RNA viral load is extremely high (>1,000,000 copies/mL)."}
            ]
        },
        {
            "id": 62,
            "disease": "Hodgkin Lymphoma",
            "accepted_answers": ["hodgkin lymphoma", "hodgkin's lymphoma", "hodgkins", "hodgkin lenfoma"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 22-year-old female presents with a painless swelling in her neck that has been slowly growing over the past 3 months."},
                {"title": "History & Physical Exam", "text": "She complains of drenching night sweats, intermittent fevers, and unintentional weight loss (B symptoms). Curiously, she notes the neck mass becomes painful after drinking alcohol. Exam shows firm, non-tender, rubbery cervical lymphadenopathy."},
                {"title": "Basic Labs", "text": "CBC is largely normal, but ESR is markedly elevated. LDH is also mildly elevated."},
                {"title": "Imaging / ECG", "text": "Chest X-ray and subsequent CT scan of the chest reveal a large, prominent anterior mediastinal mass."},
                {"title": "Specific/Advanced Labs", "text": "An excisional lymph node biopsy is performed. Histopathology reveals the classic binucleated Reed-Sternberg cells ('owl-eye' appearance) in a background of inflammatory cells."}
            ]
        },
        {
            "id": 63,
            "disease": "Multiple Myeloma",
            "accepted_answers": ["multiple myeloma", "myeloma", "multipl myelom"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 68-year-old male complains of severe, persistent lower back pain, profound fatigue, and recent constipation."},
                {"title": "History & Physical Exam", "text": "He states the pain is worse with movement and not relieved by rest. Exam reveals pallor and bony tenderness over the lumbar spine and ribs."},
                {"title": "Basic Labs", "text": "Labs reveal the 'CRAB' criteria: Calcium is elevated (12.5 mg/dL), Renal function is impaired (Cr 2.1 mg/dL), and Anemia is present (Hb 9.5 g/dL). Total serum protein is very high despite normal albumin."},
                {"title": "Imaging / ECG", "text": "Skeletal survey (X-rays) reveals classic 'punched-out' lytic bone lesions in the skull, spine, and pelvis."},
                {"title": "Specific/Advanced Labs", "text": "Serum Protein Electrophoresis (SPEP) reveals a monoclonal spike (M-spike) in the gamma region. Bone marrow biopsy shows >10% clonal plasma cells."}
            ]
        },
        {
            "id": 64,
            "disease": "Immune Thrombocytopenia",
            "accepted_answers": ["immune thrombocytopenia", "itp", "idiopathic thrombocytopenic purpura", "immün trombositopeni"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 30-year-old female presents to the clinic after noticing numerous tiny red spots on her legs and easy bruising from minor bumps."},
                {"title": "History & Physical Exam", "text": "She had a mild upper respiratory viral infection two weeks ago. She feels perfectly fine otherwise and has no fever or weight loss. Exam reveals a diffuse petechial rash on her lower extremities but NO splenomegaly."},
                {"title": "Basic Labs", "text": "CBC shows profound, isolated thrombocytopenia (Platelets 15,000/µL). Hemoglobin and WBC counts are completely normal. PT and PTT are normal."},
                {"title": "Imaging / ECG", "text": "Abdominal ultrasound is normal, confirming the absence of splenomegaly (which helps rule out leukemia/lymphoma)."},
                {"title": "Specific/Advanced Labs", "text": "Peripheral blood smear shows severely reduced platelets, but the few present are enlarged (megathrombocytes). Anti-platelet IgG antibodies are presumed positive. Treated initially with corticosteroids."}
            ]
        },
        {
            "id": 65,
            "disease": "Hemophilia A",
            "accepted_answers": ["hemophilia a", "hemophilia", "factor viii deficiency", "hemofili", "hemofili a"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "An 18-year-old male presents to the ER with massive swelling, severe pain, and restricted movement in his right knee."},
                {"title": "History & Physical Exam", "text": "He bumped his knee against a desk yesterday. He has a history of delayed bleeding after dental extractions. His maternal uncle has a known bleeding disorder. Exam reveals a tense, warm, blood-filled joint (hemarthrosis)."},
                {"title": "Basic Labs", "text": "Platelet count, Prothrombin Time (PT), and bleeding time are all strictly within normal limits. However, the activated Partial Thromboplastin Time (aPTT) is significantly prolonged."},
                {"title": "Imaging / ECG", "text": "X-ray of the right knee shows a large joint effusion but no acute fractures."},
                {"title": "Specific/Advanced Labs", "text": "A mixing study (adding normal plasma to his plasma) corrects the prolonged aPTT. Specific factor assays reveal a critically low level of Factor VIII activity (<1%), with normal von Willebrand factor levels."}
            ]
        },
        {
            "id": 66,
            "disease": "Von Willebrand Disease",
            "accepted_answers": ["von willebrand disease", "vwd", "von willebrand hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 24-year-old female presents with a lifelong history of heavy menstrual bleeding (menorrhagia) and frequent, prolonged nosebleeds."},
                {"title": "History & Physical Exam", "text": "She mentions that her father and sister also bruise very easily and have bleeding issues. Exam reveals scattered ecchymoses on her arms and legs but is otherwise normal."},
                {"title": "Basic Labs", "text": "Platelet count and PT are completely normal. The aPTT is mildly prolonged or at the upper limit of normal."},
                {"title": "Imaging / ECG", "text": "Pelvic ultrasound is normal, ruling out structural gynecological causes (like fibroids) for her menorrhagia."},
                {"title": "Specific/Advanced Labs", "text": "Bleeding time is prolonged. Ristocetin cofactor assay shows poor platelet agglutination. vWF antigen level is low, confirming the most common inherited bleeding disorder."}
            ]
        },
        {
            "id": 67,
            "disease": "Primary Biliary Cholangitis",
            "accepted_answers": ["primary biliary cholangitis", "pbc", "primary biliary cirrhosis", "primer biliyer kolanjit", "primer biliyer siroz"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 50-year-old female presents with overwhelming fatigue and intense, generalized itching (pruritus) that is worse at night."},
                {"title": "History & Physical Exam", "text": "She does not drink alcohol. Exam reveals excoriations all over her skin from scratching, mild jaundice, and yellow cholesterol deposits around her eyelids (xanthelasma). Liver edge is firm and palpable."},
                {"title": "Basic Labs", "text": "Alkaline phosphatase (ALP) is markedly elevated (>4 times normal). AST and ALT are only mildly elevated. Total bilirubin is slightly high."},
                {"title": "Imaging / ECG", "text": "Right upper quadrant ultrasound demonstrates a normal gallbladder and normal extrahepatic bile ducts (no stones or obstruction)."},
                {"title": "Specific/Advanced Labs", "text": "Anti-mitochondrial antibodies (AMA) are highly positive in high titers. Liver biopsy shows destruction of small intrahepatic bile ducts with a florid duct lesion."}
            ]
        },
        {
            "id": 68,
            "disease": "Primary Sclerosing Cholangitis",
            "accepted_answers": ["primary sclerosing cholangitis", "psc", "primer sklerozan kolanjit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 35-year-old male presents with worsening fatigue, itching, right upper quadrant discomfort, and yellowing of the eyes."},
                {"title": "History & Physical Exam", "text": "He has a known medical history of Ulcerative Colitis (UC). Exam reveals scleral icterus, hepatomegaly, and excoriations."},
                {"title": "Basic Labs", "text": "Hepatic panel shows a cholestatic pattern: markedly elevated Alkaline Phosphatase and GGT, with conjugated hyperbilirubinemia. p-ANCA is positive."},
                {"title": "Imaging / ECG", "text": "Magnetic Resonance Cholangiopancreatography (MRCP) reveals alternating areas of stricturing and dilation of both intrahepatic and extrahepatic bile ducts, giving a classic 'beaded' appearance."},
                {"title": "Specific/Advanced Labs", "text": "Endoscopic Retrograde Cholangiopancreatography (ERCP) confirms the strictures. Liver biopsy, if done, shows 'onion-skin' fibrosis surrounding the bile ducts."}
            ]
        },
        {
            "id": 69,
            "disease": "Wilson Disease",
            "accepted_answers": ["wilson disease", "wilson's disease", "hepatolenticular degeneration", "wilson hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 22-year-old male is brought to the clinic by his family due to new-onset resting tremor, slurred speech (dysarthria), and mild jaundice."},
                {"title": "History & Physical Exam", "text": "His younger sister died of unexplained liver failure at age 20. He has been acting impulsively lately. Neurological exam reveals a wing-beating tremor and rigidity."},
                {"title": "Basic Labs", "text": "Transaminases (AST, ALT) are elevated. CBC shows a Coombs-negative hemolytic anemia."},
                {"title": "Imaging / ECG", "text": "Brain MRI demonstrates hyperintensities in the basal ganglia (putamen and globus pallidus), reflecting toxic metal deposition."},
                {"title": "Specific/Advanced Labs", "text": "Slit-lamp examination of the eyes reveals golden-brown Kayser-Fleischer rings in the cornea. Serum ceruloplasmin is extremely low, and 24-hour urinary copper excretion is markedly elevated."}
            ]
        },
        {
            "id": 70,
            "disease": "Hemochromatosis",
            "accepted_answers": ["hemochromatosis", "hereditary hemochromatosis", "bronze diabetes", "hemokromatoz"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 55-year-old male complains of severe fatigue, joint pain (especially in his knuckles), and new-onset erectile dysfunction."},
                {"title": "History & Physical Exam", "text": "He was recently diagnosed with Type 2 Diabetes despite being lean. Exam reveals a noticeable generalized darkening of his skin (a 'bronze' hue) and a firm, enlarged liver."},
                {"title": "Basic Labs", "text": "Fasting blood glucose is elevated. Liver enzymes (AST/ALT) are mildly elevated. Testosterone levels are low (hypogonadism)."},
                {"title": "Imaging / ECG", "text": "MRI of the abdomen with specialized sequencing (T2*) shows a darkened liver and pancreas due to massive heavy metal deposition. X-ray of the hands shows hook-like osteophytes."},
                {"title": "Specific/Advanced Labs", "text": "Serum ferritin is extremely high (>1000 ng/mL) and transferrin saturation is >60%. Genetic testing is positive for the homozygous C282Y mutation in the HFE gene."}
            ]
        },
        {
            "id": 71,
            "disease": "Ankylosing Spondylitis",
            "accepted_answers": ["ankylosing spondylitis", "as", "ankilozan spondilit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 25-year-old male complains of chronic, dull lower back pain and stiffness that has been worsening over the last 6 months."},
                {"title": "History & Physical Exam", "text": "He specifically notes the pain is worst in the morning upon waking up, takes hours to loosen up, improves significantly with exercise, and is not relieved by rest. Exam shows restricted forward flexion of the lumbar spine (positive Schober's test)."},
                {"title": "Basic Labs", "text": "Inflammatory markers (ESR and CRP) are elevated. Rheumatoid factor and ANA are negative."},
                {"title": "Imaging / ECG", "text": "X-ray of the pelvis shows bilateral fusion and sclerosis of the sacroiliac joints (sacroiliitis). A lateral spine X-ray shows squaring of vertebral bodies, heading toward a 'bamboo spine'."},
                {"title": "Specific/Advanced Labs", "text": "Genetic testing reveals he is positive for the HLA-B27 antigen."}
            ]
        },
        {
            "id": 72,
            "disease": "Giant Cell Arteritis",
            "accepted_answers": ["giant cell arteritis", "temporal arteritis", "dev hücreli arterit", "temporal arterit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 75-year-old female presents to the ER with a severe, new-onset unilateral throbbing headache and extreme scalp tenderness (she cannot comb her hair)."},
                {"title": "History & Physical Exam", "text": "She complains of intense pain in her jaw when chewing food (jaw claudication) and reports a brief episode of temporary vision loss in her right eye (amaurosis fugax) earlier today. Exam reveals a thickened, prominent, and tender temporal artery."},
                {"title": "Basic Labs", "text": "ESR is remarkably high (>100 mm/hr). CRP is also significantly elevated. CBC shows a mild normocytic anemia."},
                {"title": "Imaging / ECG", "text": "Color Doppler ultrasound of the temporal artery shows a hypoechoic 'halo sign', indicating wall edema."},
                {"title": "Specific/Advanced Labs", "text": "High-dose systemic corticosteroids are started immediately to prevent permanent blindness. A temporal artery biopsy is performed a few days later, showing granulomatous inflammation with multinucleated giant cells."}
            ]
        },
        {
            "id": 73,
            "disease": "Polymyalgia Rheumatica",
            "accepted_answers": ["polymyalgia rheumatica", "pmr", "polimiyalji romatika"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 70-year-old female presents with severe, bilateral aching pain and profound stiffness in her shoulders, neck, and hips."},
                {"title": "History & Physical Exam", "text": "The stiffness is terrible in the morning, making it hard for her to get out of bed or raise her arms above her head. She has no headaches or vision changes. Exam reveals limited active range of motion due to pain, but muscle strength is fully intact (no true weakness)."},
                {"title": "Basic Labs", "text": "ESR and CRP are significantly elevated. Creatine Kinase (CK) and aldolase levels are completely normal, ruling out primary muscle breakdown (myopathy)."},
                {"title": "Imaging / ECG", "text": "Joint X-rays are generally unremarkable, showing only mild age-related osteoarthritis."},
                {"title": "Specific/Advanced Labs", "text": "She is given a trial of low-dose oral prednisone (corticosteroids) and her symptoms disappear almost miraculously within 48 hours, confirming the diagnosis."}
            ]
        },
        {
            "id": 74,
            "disease": "Fibromyalgia",
            "accepted_answers": ["fibromyalgia", "fibromiyalji"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 45-year-old female presents with chronic, widespread musculoskeletal pain, profound fatigue, and non-restorative sleep for the past 2 years."},
                {"title": "History & Physical Exam", "text": "She says 'I just hurt all over, all the time.' She has a history of migraines and irritable bowel syndrome. She complains of brain fog. Physical exam reveals absolutely no joint swelling or inflammation, but she has exquisite tenderness at multiple specific trigger points (e.g., trapezius, lateral epicondyles)."},
                {"title": "Basic Labs", "text": "Extensive lab workup including CBC, CMP, ESR, CRP, TSH, and ANA are all perfectly normal, frustrating the patient."},
                {"title": "Imaging / ECG", "text": "X-rays and MRIs of her painful joints and spine show no structural abnormalities."},
                {"title": "Specific/Advanced Labs", "text": "Diagnosis is strictly clinical, based on the Widespread Pain Index and Symptom Severity scale, after ruling out other inflammatory or endocrine conditions."}
            ]
        },
        {
            "id": 75,
            "disease": "Systemic Sclerosis",
            "accepted_answers": ["systemic sclerosis", "scleroderma", "sistemik skleroz", "skleroderma"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 40-year-old female complains that her fingers turn white, then blue, then painfully red when she goes out into the cold (Raynaud's phenomenon)."},
                {"title": "History & Physical Exam", "text": "She also suffers from severe heartburn (GERD) and difficulty swallowing solids. Exam reveals thickened, shiny, tightly stretched skin on her fingers (sclerodactyly) making it hard to make a full fist. She has multiple tiny red spots (telangiectasias) on her face."},
                {"title": "Basic Labs", "text": "CBC shows mild anemia. Basic metabolic panel is normal. Urinalysis is normal (currently no renal crisis)."},
                {"title": "Imaging / ECG", "text": "A barium swallow study shows decreased peristalsis and diminished tone in the lower two-thirds of the esophagus."},
                {"title": "Specific/Advanced Labs", "text": "Antinuclear antibody (ANA) is positive. Anti-centromere antibodies are highly positive (consistent with the limited cutaneous form / CREST syndrome)."}
            ]
        },{
            "id": 76,
            "disease": "Myocarditis",
            "accepted_answers": ["myocarditis", "miyokardit", "viral myocarditis"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 28-year-old previously healthy male presents with chest pain, fatigue, and feeling short of breath with minimal exertion over the last 3 days."},
                {"title": "History & Physical Exam", "text": "He reports having a severe flu-like illness with fever and muscle aches a week ago. On exam, he is tachycardic out of proportion to his lack of fever. A subtle S3 gallop is audible."},
                {"title": "Basic Labs", "text": "Troponin is elevated, indicating myocardial injury, but he has no risk factors for coronary artery disease. Inflammatory markers (ESR, CRP) are high."},
                {"title": "Imaging / ECG", "text": "ECG shows sinus tachycardia with non-specific ST-T wave changes globally, without a clear vascular territory."},
                {"title": "Specific/Advanced Labs", "text": "Echocardiogram reveals global hypokinesis and a reduced ejection fraction. Cardiac MRI shows delayed gadolinium enhancement characteristic of myocardial inflammation."}
            ]
        },
        {
            "id": 77,
            "disease": "Idiopathic Pulmonary Fibrosis",
            "accepted_answers": ["idiopathic pulmonary fibrosis", "ipf", "pulmonary fibrosis", "idiyopatik pulmoner fibrozis"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 65-year-old male presents with a gradual onset of progressively worsening shortness of breath and a chronic, dry, hacking cough over the past year."},
                {"title": "History & Physical Exam", "text": "He has no history of occupational exposures to asbestos or silica, and no history of smoking. Exam reveals clubbing of the fingers and fine, 'Velcro-like' inspiratory crackles at the lung bases."},
                {"title": "Basic Labs", "text": "Routine blood work, including an autoimmune panel (ANA, Rheumatoid Factor), is completely negative, ruling out secondary causes of interstitial lung disease."},
                {"title": "Imaging / ECG", "text": "High-Resolution CT (HRCT) of the chest reveals peripheral, subpleural reticular opacities with prominent 'honeycombing' and traction bronchiectasis."},
                {"title": "Specific/Advanced Labs", "text": "Pulmonary function tests (PFTs) demonstrate a restrictive pattern: reduced Total Lung Capacity (TLC), reduced FVC, a normal/high FEV1/FVC ratio, and a severely reduced DLCO."}
            ]
        },
        {
            "id": 78,
            "disease": "Amyotrophic Lateral Sclerosis",
            "accepted_answers": ["amyotrophic lateral sclerosis", "als", "lou gehrig's disease", "amiyotrofik lateral skleroz"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 55-year-old male presents with progressive weakness in his right hand, making it difficult to turn keys or button his shirt, along with frequent muscle twitching."},
                {"title": "History & Physical Exam", "text": "He notes his voice has become slightly slurred and he occasionally chokes on liquids. Exam is remarkable: he has muscle atrophy and fasciculations in his hands (lower motor neuron signs), but paradoxically hyperactive deep tendon reflexes and a positive Babinski sign (upper motor neuron signs)."},
                {"title": "Basic Labs", "text": "CK levels are mildly elevated due to muscle breakdown. Vitamin B12, heavy metal screens, and syphilis testing are all normal."},
                {"title": "Imaging / ECG", "text": "Brain and complete spinal MRI are completely normal, ruling out structural compression, multiple sclerosis, or stroke."},
                {"title": "Specific/Advanced Labs", "text": "Electromyography (EMG) shows widespread acute and chronic denervation in multiple muscle groups across different regions, confirming anterior horn cell degeneration."}
            ]
        },
        {
            "id": 79,
            "disease": "Huntington's Disease",
            "accepted_answers": ["huntington's disease", "huntington disease", "huntingtons", "huntington", "huntington hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 42-year-old male is brought to the neurologist by his wife due to personality changes, severe irritability, and uncontrolled bodily movements."},
                {"title": "History & Physical Exam", "text": "His father died in his 50s from a similar, progressive neurological condition. Exam reveals constant, rapid, jerky, involuntary, and purposeless movements of his face and limbs (chorea)."},
                {"title": "Basic Labs", "text": "Routine lab investigations (CMP, CBC, TSH) are completely normal."},
                {"title": "Imaging / ECG", "text": "Brain MRI reveals profound, symmetric atrophy of the caudate nucleus and putamen, with secondary enlargement of the lateral ventricles (boxcar ventricles)."},
                {"title": "Specific/Advanced Labs", "text": "Genetic testing confirms a CAG trinucleotide repeat expansion (>40 repeats) on chromosome 4."}
            ]
        },
        {
            "id": 80,
            "disease": "Alzheimer's Disease",
            "accepted_answers": ["alzheimer's disease", "alzheimers", "alzheimer", "alzheimer hastalığı"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 72-year-old female is brought in by her daughter because she has been increasingly forgetful over the past 3 years."},
                {"title": "History & Physical Exam", "text": "She repeatedly asks the same questions, forgets recent conversations, and recently got lost driving in her own neighborhood. She denies any depressive symptoms. Neurological exam is non-focal; she has no motor or sensory deficits. Mini-Mental State Examination (MMSE) score is 18/30."},
                {"title": "Basic Labs", "text": "Reversible causes of dementia are ruled out: Vitamin B12, TSH, RPR, and basic chemistry are all normal."},
                {"title": "Imaging / ECG", "text": "Brain MRI shows generalized cortical atrophy, which is particularly prominent in the medial temporal lobes and hippocampi."},
                {"title": "Specific/Advanced Labs", "text": "Diagnosis is largely clinical after ruling out other causes. If a CSF analysis were performed or an autopsy done later, it would show decreased amyloid-beta and increased hyperphosphorylated tau proteins."}
            ]
        },
        {
            "id": 81,
            "disease": "Acute Respiratory Distress Syndrome",
            "accepted_answers": ["acute respiratory distress syndrome", "ards", "akut solunum sıkıntısı sendromu"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 45-year-old female is currently in the ICU for severe acute pancreatitis. On hospital day 3, she rapidly develops severe, refractory shortness of breath."},
                {"title": "History & Physical Exam", "text": "She is in profound respiratory distress. Exam reveals diffuse, bilateral crackles. Despite being placed on 100% oxygen via a non-rebreather mask, her oxygen saturation remains critically low at 82%."},
                {"title": "Basic Labs", "text": "Arterial blood gas shows a profoundly low PaO2. Her PaO2/FiO2 ratio is calculated to be 110 mmHg (severe hypoxia)."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows rapid onset of diffuse, bilateral alveolar infiltrates ('white-out' lungs) with a completely normal heart size and no pleural effusions."},
                {"title": "Specific/Advanced Labs", "text": "Echocardiogram is completely normal, confirming this is non-cardiogenic pulmonary edema caused by massive inflammatory disruption of the alveolar-capillary membrane. She requires prompt intubation and mechanical ventilation."}
            ]
        },
        {
            "id": 82,
            "disease": "Choledocholithiasis",
            "accepted_answers": ["choledocholithiasis", "common bile duct stone", "koledokolitiazis"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 50-year-old female presents with severe, colicky right upper quadrant pain, nausea, and new-onset yellowing of her skin."},
                {"title": "History & Physical Exam", "text": "She states she has had similar but milder, self-resolving pain after eating fatty foods in the past. Exam reveals right upper quadrant tenderness without a palpable mass, prominent scleral icterus, and jaundice. She is afebrile."},
                {"title": "Basic Labs", "text": "Liver panel shows significantly elevated Direct (Conjugated) Bilirubin, markedly elevated Alkaline Phosphatase, and a mild elevation in AST/ALT."},
                {"title": "Imaging / ECG", "text": "Right upper quadrant ultrasound reveals multiple stones in the gallbladder and a dilated common bile duct (CBD) measuring 12 mm."},
                {"title": "Specific/Advanced Labs", "text": "MRCP confirms an obstructing 8mm calculus lodged in the distal common bile duct. She is scheduled for an urgent ERCP to remove the obstruction."}
            ]
        },
        {
            "id": 83,
            "disease": "Acute Cholecystitis",
            "accepted_answers": ["acute cholecystitis", "cholecystitis", "akut kolesistit", "kolesistit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 45-year-old overweight female presents with steady, severe right upper quadrant abdominal pain that has been constant for the last 12 hours."},
                {"title": "History & Physical Exam", "text": "She is nauseous, has vomited several times, and feels feverish. On physical exam, she has a low-grade fever. Palpation of the right subcostal area during deep inspiration causes her to suddenly halt her breath due to sharp pain (positive Murphy's sign)."},
                {"title": "Basic Labs", "text": "CBC shows a significant leukocytosis (15,000/µL) with a left shift. Liver enzymes and bilirubin are strictly normal, ruling out bile duct obstruction."},
                {"title": "Imaging / ECG", "text": "Abdominal ultrasound demonstrates gallstones, a thickened gallbladder wall (>4 mm), and a rim of pericholecystic fluid. The sonographer notes a sonographic Murphy's sign."},
                {"title": "Specific/Advanced Labs", "text": "A HIDA scan (if ultrasound was equivocal) would show failure of the gallbladder to visualize, confirming cystic duct obstruction. She is prepped for a laparoscopic cholecystectomy."}
            ]
        },
        {
            "id": 84,
            "disease": "Acute Diverticulitis",
            "accepted_answers": ["diverticulitis", "acute diverticulitis", "divertikülit", "akut divertikülit"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 60-year-old male presents with steady, deep, cramping pain in his left lower quadrant that started yesterday and is steadily worsening."},
                {"title": "History & Physical Exam", "text": "He has a history of chronic constipation and a low-fiber diet. He complains of nausea, subjective fever, and altered bowel habits. Exam reveals marked tenderness, guarding, and localized rigidity in the left lower quadrant."},
                {"title": "Basic Labs", "text": "CBC shows mild leukocytosis. CRP is elevated. Urinalysis is normal."},
                {"title": "Imaging / ECG", "text": "CT scan of the abdomen and pelvis with IV and oral contrast demonstrates bowel wall thickening of the sigmoid colon, prominent outpouchings, and adjacent pericolic fat stranding."},
                {"title": "Specific/Advanced Labs", "text": "Colonoscopy is completely contraindicated at this acute stage due to the high risk of iatrogenic perforation. He is treated with IV antibiotics."}
            ]
        },
        {
            "id": 85,
            "disease": "Achalasia",
            "accepted_answers": ["achalasia", "akalazya"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 38-year-old female presents with a 6-month history of progressive difficulty swallowing (dysphagia) to both solids and liquids simultaneously."},
                {"title": "History & Physical Exam", "text": "She frequently regurgitates undigested, foul-smelling food from hours earlier, and often wakes up coughing at night. She has lost 10 lbs. Physical exam is entirely unremarkable."},
                {"title": "Basic Labs", "text": "Routine labs, including CBC and chemistry, are normal."},
                {"title": "Imaging / ECG", "text": "A barium swallow study shows esophageal dilation proximally and a smooth, tapering narrowing at the gastroesophageal junction, classically described as a 'bird's beak' appearance."},
                {"title": "Specific/Advanced Labs", "text": "Upper endoscopy shows a dilated esophagus with retained food, but no mechanical stricture or mass. Esophageal manometry is the gold standard and reveals aperistalsis of the esophageal body and failure of the lower esophageal sphincter (LES) to relax."}
            ]
        },
        {
            "id": 86,
            "disease": "Zollinger-Ellison Syndrome",
            "accepted_answers": ["zollinger-ellison syndrome", "zes", "gastrinoma", "zollinger ellison"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 45-year-old male complains of severe, burning, unrelenting upper abdominal pain and chronic, watery diarrhea."},
                {"title": "History & Physical Exam", "text": "He has a history of recurrent peptic ulcers that do not respond to standard high-dose proton pump inhibitor (PPI) therapy. He also tested negative for H. pylori and doesn't take NSAIDs. Exam reveals epigastric tenderness."},
                {"title": "Basic Labs", "text": "Basic metabolic panel is normal. Fasting serum gastrin level is checked and is profoundly elevated (>1000 pg/mL)."},
                {"title": "Imaging / ECG", "text": "Endoscopy reveals multiple large ulcers in the stomach, duodenum, and even the proximal jejunum, along with thick, hypertrophied gastric folds."},
                {"title": "Specific/Advanced Labs", "text": "A secretin stimulation test is performed; instead of decreasing gastrin levels (normal response), the administration of secretin causes a paradoxical and massive spike in serum gastrin. A somatostatin receptor scintigraphy (OctreoScan) identifies a small neuroendocrine tumor in the pancreas."}
            ]
        },
        {
            "id": 87,
            "disease": "Pheochromocytoma",
            "accepted_answers": ["pheochromocytoma", "feokromositoma"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 35-year-old female comes to the clinic reporting terrifying, unprovoked 'spells' of a pounding heart, severe headaches, and profuse sweating."},
                {"title": "History & Physical Exam", "text": "She says these attacks happen suddenly, last about 15 minutes, and leave her exhausted. During her clinic visit, her blood pressure is severely elevated at 210/115 mmHg, and her heart rate is 115 bpm. She appears anxious and diaphoretic."},
                {"title": "Basic Labs", "text": "Routine chemistry and CBC are normal. TSH is checked and is normal, ruling out hyperthyroidism."},
                {"title": "Imaging / ECG", "text": "Following laboratory confirmation, an abdominal CT or MRI is performed and reveals a highly vascular 4 cm mass in the right adrenal medulla."},
                {"title": "Specific/Advanced Labs", "text": "24-hour urine collection shows massively elevated levels of fractionated metanephrines and catecholamines. She must be treated with an alpha-blocker (phenoxybenzamine) prior to beta-blockade before surgical resection."}
            ]
        },
        {
            "id": 88,
            "disease": "Acromegaly",
            "accepted_answers": ["acromegaly", "akromegali"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 48-year-old male presents for a routine check-up complaining of frequent headaches, joint pain, and an observation that his wedding ring and shoes no longer fit."},
                {"title": "History & Physical Exam", "text": "His wife notes that his facial features have changed significantly over the last 5 years, becoming much more prominent. Exam reveals a protruding jaw (prognathism), a large nose, macroglossia (enlarged tongue), and large, doughy, sweaty hands."},
                {"title": "Basic Labs", "text": "He is incidentally found to have newly elevated fasting blood glucose levels (secondary diabetes)."},
                {"title": "Imaging / ECG", "text": "Brain MRI reveals a 1.5 cm macroadenoma in the anterior pituitary gland."},
                {"title": "Specific/Advanced Labs", "text": "Serum Insulin-like Growth Factor 1 (IGF-1) is markedly elevated. An oral glucose tolerance test is performed, which fails to suppress his profoundly elevated Growth Hormone (GH) levels."}
            ]
        },
        {
            "id": 89,
            "disease": "Hyperosmolar Hyperglycemic State",
            "accepted_answers": ["hyperosmolar hyperglycemic state", "hhs", "honk", "hiperosmolar hiperglisemik durum", "hhs sendromu"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 75-year-old male with poorly managed Type 2 Diabetes is brought to the ER from his nursing home due to severe lethargy, confusion, and profound weakness."},
                {"title": "History & Physical Exam", "text": "He had a mild pneumonia last week. The staff notes he has been urinating constantly and drinking little water. Exam reveals an obtunded patient with extremely dry mucous membranes, delayed capillary refill, and severe hypotension."},
                {"title": "Basic Labs", "text": "Blood glucose is astonishingly high at 950 mg/dL. Serum sodium is 150 mEq/L, and BUN is 65 mg/dL. Calculated serum osmolality is dangerously high at >340 mOsm/kg."},
                {"title": "Imaging / ECG", "text": "Chest X-ray shows resolving basilar infiltrates from his recent pneumonia, the likely trigger for his current state."},
                {"title": "Specific/Advanced Labs", "text": "Unlike DKA, his arterial pH is 7.35, serum bicarbonate is 22 mEq/L, and both serum and urine ketones are strictly negative. He needs massive, aggressive IV fluid resuscitation before insulin."}
            ]
        },
        {
            "id": 90,
            "disease": "Carcinoid Syndrome",
            "accepted_answers": ["carcinoid syndrome", "karsinoid sendrom", "carcinoid tumor"],
            "clues": [
                {"title": "Demographics & Chief Complaint", "text": "A 52-year-old male presents with episodes of sudden, intense facial flushing, chronic watery diarrhea, and a feeling of wheezing in his chest."},
                {"title": "History & Physical Exam", "text": "He states the flushing is sometimes triggered by eating certain foods or drinking alcohol. Exam reveals telangiectasias on his face. Cardiac auscultation reveals a new systolic murmur at the lower left sternal border (tricuspid regurgitation)."},
                {"title": "Basic Labs", "text": "Routine labs are largely unrevealing. He has mild niacin deficiency (pellagra-like dermatitis on his arms) due to tryptophan diversion."},
                {"title": "Imaging / ECG", "text": "Abdominal CT reveals a small mass in the terminal ileum with multiple target-like, hypervascular lesions in the liver, indicating metastasis."},
                {"title": "Specific/Advanced Labs", "text": "A 24-hour urine collection is highly positive for 5-HIAA (5-hydroxyindoleacetic acid), the primary breakdown product of serotonin. His symptoms improve dramatically with octreotide therapy."}
            ]
        }
    ]
    

# Game State Initialization
if 'current_case_id' not in st.session_state:
    st.session_state.current_case_id = 0
if 'current_clue_index' not in st.session_state:
    st.session_state.current_clue_index = 1
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'won' not in st.session_state:
    st.session_state.won = False
if 'guesses' not in st.session_state:
    st.session_state.guesses = []
if 'roast_message' not in st.session_state:
    st.session_state.roast_message = None
def reset_game(case_id):
    st.session_state.current_case_id = case_id
    st.session_state.current_clue_index = 1
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.guesses = []

# --- SIDEBAR: NAVIGATION & ARCHIVE ---
st.sidebar.title("🩺 Kaandle Menu")
page = st.sidebar.radio("Navigation", ["Play Mode", "Archive"])

if page == "Archive":
    st.markdown("<h1 class='main-title'>📂 Case Archive</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Select a past clinical case to replay.</p>", unsafe_allow_html=True)
    
    for i, case_data in enumerate(st.session_state.cases):
        with st.container():
            st.markdown(f"### Case #{case_data['id']}")
            if st.button(f"Play Case #{case_data['id']}", key=f"play_{i}"):
                reset_game(i)
                st.sidebar.success("Case loaded! Click 'Play Mode' to start.")
            st.markdown("---")

elif page == "Play Mode":
    # Current Case
    case = st.session_state.cases[st.session_state.current_case_id]
    total_clues = len(case['clues'])

    st.markdown("<h1 class='main-title'>🩺 Kaandle</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-title'>Case #{case['id']} | Guess the disease. 5 clues available!</p>", unsafe_allow_html=True)

    # Display Clues
    for i in range(st.session_state.current_clue_index):
        clue = case['clues'][i]
        
        # Eğer resim varsa HTML formatında gösteriyoruz
        image_html = ""
        if 'image_url' in clue:
            image_html = f"<img src='{clue['image_url']}' class='medical-image' alt='Clinical Finding'>"
            
        st.markdown(f"""
        <div class='clue-box'>
            <div class='clue-header'>Clue {i+1}: {clue['title']}</div>
            <div>{clue['text']}</div>
            {image_html}
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # YAPAY ZEKA CEVABINI EKRANDA GÖSTER
    if st.session_state.roast_message:
        st.error(f"👨‍⚕️ **The Professor says:**\n\n{st.session_state.roast_message}")

# User Input & Buttons
    if not st.session_state.game_over:
        guess = st.text_input("What is your diagnosis?", placeholder="Type disease name...").strip().lower()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Submit Diagnosis", use_container_width=True, type="primary"):
                if guess:
                    st.session_state.guesses.append(guess)
                    if any(accepted in guess for accepted in case['accepted_answers']):
                        st.session_state.won = True
                        st.session_state.game_over = True
                        st.session_state.roast_message = None # Doğru bilirse laf sokmayı sil
                        st.rerun()
                    else:
                        # YANLIŞ CEVAP - PROFESÖRÜ ÇAĞIR!
                        with st.spinner("The Professor is frowning, preparing a roast..."):
                            revealed_clues = case["clues"][:st.session_state.current_clue_index]
                            roast = get_sarcastic_response(
                                actual_disease=case["disease"],
                                clues=revealed_clues,
                                user_guess=guess
                            )
                            st.session_state.roast_message = roast # Cevabı hafızaya al
                        
                        if st.session_state.current_clue_index < total_clues:
                            st.session_state.current_clue_index += 1
                        else:
                            st.session_state.game_over = True
                        st.rerun()
                else:
                    st.warning("Please enter a diagnosis!")

        with col2:
            if st.button("Skip / Next Clue", use_container_width=True):
                st.session_state.guesses.append("Skipped")
                st.session_state.roast_message = None # Pas geçerse eski laf sokmayı sil
                if st.session_state.current_clue_index < total_clues:
                    st.session_state.current_clue_index += 1
                else:
                    st.session_state.game_over = True
                st.rerun()
 

    # Game Over Screen
    if st.session_state.game_over:
        if st.session_state.won:
            st.success(f"🎉 **Correct Diagnosis!** The disease is: **{case['disease']}**")
            st.balloons()
        else:
            st.error(f"❌ **Case Closed.** The correct diagnosis was: **{case['disease']}**")
        
        # Show remaining clues
        if st.session_state.current_clue_index < total_clues:
            st.info("Unrevealed clinical findings:")
            for i in range(st.session_state.current_clue_index, total_clues):
                st.write(f"- **{case['clues'][i]['title']}:** {case['clues'][i]['text']}")
                if 'image_url' in case['clues'][i]:
                    st.markdown(f"<img src='{case['clues'][i]['image_url']}' class='medical-image'>", unsafe_allow_html=True)

        st.divider()
        col_retry, col_next = st.columns(2)
        
        with col_retry:
            if st.button("🔄 Retry This Case", use_container_width=True):
                reset_game(st.session_state.current_case_id)
                st.rerun()
                
        with col_next:
            if st.session_state.current_case_id < len(st.session_state.cases) - 1:
                if st.button("⏭️ Next Case", use_container_width=True, type="primary"):
                    reset_game(st.session_state.current_case_id + 1)
                    st.rerun()
            else:
                st.success("You have completed all available cases in the database!")

    # Display Guess History
    if st.session_state.guesses:
        st.write("### Your Guesses:")
        for idx, g in enumerate(st.session_state.guesses):
            if g == "Skipped":
                st.caption(f"Attempt {idx+1}: *Skipped*")
            else:
                st.caption(f"Attempt {idx+1}: **{g.upper()}**")
