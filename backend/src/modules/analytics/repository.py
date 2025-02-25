from pymongo import MongoClient

# Setup MongoDB client; update connection parameters as needed
client = MongoClient()  # Configure your connection as needed

db = client['your_database_name']  # Replace with your MongoDB database name


def get_recruitment_process_analytics(recruitment_process_id: str):
    pipeline = [
        {
            "$match": {
                "recruitmentProcessId": recruitment_process_id
            }
        },
        {
            "$lookup": {
                "from": "skillsetsdata",
                "localField": "email",
                "foreignField": "email",
                "as": "skillsets"
            }
        },
        {
            "$lookup": {
                "from": "interviews",
                "localField": "email",
                "foreignField": "email",
                "as": "interviews"
            }
        },
        {
            "$lookup": {
                "from": "certificationsdata",
                "localField": "email",
                "foreignField": "email",
                "as": "certifications"
            }
        },
        {
            "$project": {
                "email": 1,
                "candidateName": 1,
                "salaryExpectation": {"$ifNull": ["$salaryExpectation", 0]},
                "country": 1,
                "skillsetAvg": {"$ifNull": [{"$avg": "$skillsets.skillsetRating"}, 0]},
                "interviewYes": {"$ifNull": [{"$size": {"$filter": {
                    "input": "$interviews",
                    "as": "item",
                    "cond": {"$eq": ["$$item.approved", "Yes"]}
                }}}, 0]},
                "interviewMaybe": {"$ifNull": [{"$size": {"$filter": {
                    "input": "$interviews",
                    "as": "item",
                    "cond": {"$eq": ["$$item.approved", "Pending"]}
                }}}, 0]},
                "interviewNo": {"$ifNull": [{"$size": {"$filter": {
                    "input": "$interviews",
                    "as": "item",
                    "cond": {"$eq": ["$$item.approved", "No"]}
                }}}, 0]},
                "interviewRating": {"$ifNull": [{"$avg": "$interviews.rating"}, 0]},
                "certificationCount": {"$ifNull": [{"$size": "$certifications"}, 0]}
            }
        }
    ]
    return list(db.candidates.aggregate(pipeline)) 