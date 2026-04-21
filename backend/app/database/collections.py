# Collection names
ANALYSIS_HISTORY = "analysis_history"
USER_RISK_SCORES = "user_risk_scores"
USER_BEHAVIOR_LOGS = "user_behavior_logs"

def get_collection(db, name: str):
    return db[name]
