from google.cloud import dialogflow
import os
import pandas as pd
import warnings

writer = pd.ExcelWriter("./test.xlsx", engine='openpyxl')

warnings.filterwarnings("ignore")
Uttererance = []
Detected_intent = []
Expected_intent=[]
Detected_intent_confidence = []
Fulfillment_text = []
Entity = []
overall = []
Intent_P_F=[]
Confidence_p_f=[]
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Service key path"
DIALOGFLOW_PROJECT_ID = "project id"
SESSION_ID = 'test'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
dc = pd.read_excel('./Utterance generated/data_14_02_2023_20_57.xlsx', engine='openpyxl', sheet_name='Paraphrase')
paraphrase = list(dc['Paraphrase'])

for j in paraphrase:
    print(j)
    text_input = dialogflow.TextInput(text=j, language_code="en-US")
    query_input = dialogflow.QueryInput(text=text_input)
    context_name = "mainmenu"
    context_lifespan = 5
    context = dialogflow.Context(name=session + "/contexts/" + context_name, lifespan_count=context_lifespan)
    query_params = dialogflow.QueryParameters(contexts=[context])
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input, "query_params": query_params})
    Uttererance.append(response.query_result.query_text)
    Detected_intent.append(response.query_result.intent.display_name)
    Expected_intent.append("MainMenuMTG")
    # print(session_client.session_entity_type_path(request={"session": session, "query_input": query_input, "query_params": query_params}))
    Detected_intent_confidence.append(response.query_result.intent_detection_confidence)
    response.query_result.output_contexts
    Fulfillment_text.append(response.query_result.fulfillment_text)
    map_composite = response.query_result.parameters
    Ekey = []
    Evalue = []
    for key, value in map_composite.items():
        Ekey.append(key)
        Evalue.append(value)
    Entities = dict(zip(Ekey, Evalue))
    Entity.append(Entities)
    if response.query_result.intent.display_name == "MainMenuMTG":
        Intent_P_F.append("PASS")
        intent_pf="PASS"
    else:
        Intent_P_F.append("FAIL")
        intent_pf = "FAIL"
    if response.query_result.intent_detection_confidence > 0.5:
        conf="PASS"
        Confidence_p_f.append("PASS")

    else:
        conf = "FAIL"
        Confidence_p_f.append("FAIL")
    if intent_pf == conf:
        overall.append("PASS")
    else:
        overall.append("FAIL")
print(Uttererance, Detected_intent, Detected_intent_confidence, Fulfillment_text,Entity)
data = dict(Uttererance=Uttererance, Detected_intent=Detected_intent, Expected_intent=Expected_intent,
            Detected_intent_confidence=Detected_intent_confidence, Fulfillment_text=Fulfillment_text, Entity=Entity, Intent_P_F=Intent_P_F, Confidence_p_f=Confidence_p_f, overall=overall)
df = pd.DataFrame(data)
df.to_excel(writer, sheet_name="utterance")
writer.save()
