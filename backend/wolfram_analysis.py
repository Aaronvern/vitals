from wolframclient.language import wl
from wolframclient.evaluation import WolframLanguageSession
from config import WORKOUTS_COLLECTION_ID
from database import list_documents
from appwrite.query import Query

wolfram_session = WolframLanguageSession()

def wolfram_analyze(user: dict):
    workouts = list_documents(WORKOUTS_COLLECTION_ID, queries=[Query.equal("user_id", user["$id"])])["documents"]
    reps_list = [w["reps"] for w in workouts]
    calories_list = [w["calories"] for w in workouts]
    form_scores = [w["form_score"] for w in workouts]
    
    if not reps_list:
        return {"insights": "No workout data available"}
    
    
    print(f"Reps: {reps_list}, Calories: {calories_list}, Form scores: {form_scores}")
    
    
    analysis = wolfram_session.evaluate(
        wl.ToString(
            wl.StringJoin(
                wl.ToString(wl.Total(reps_list)), " total reps, ",
                wl.ToString(wl.Mean(calories_list)), " avg calories, ",
                wl.ToString(wl.Times(wl.Mean(form_scores), 100)), "% avg form accuracy"
            )
        )
    )
    
    
    print(f"wo hooo wolfram analysis result: {analysis}")
    
    return {"insights": analysis}