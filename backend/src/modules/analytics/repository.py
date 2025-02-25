from pymongo import MongoClient
import os
from database import get_database

# Get MongoDB connection string from environment variable or use a default
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'samana_cloud')

# Setup MongoDB client with proper connection string
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]


async def get_recruitment_process_analytics(recruitment_process_id: str):
    """
    Get analytics for all candidates in a specific recruitment process.
    
    Args:
        recruitment_process_id: The ID of the recruitment process to analyze
        
    Returns:
        A list of dictionaries with candidate analytics data
    """
    db = await get_database()
    
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
                "skillsetAvg": {
                    "$ifNull": [{"$avg": "$skillsets.skillsetRating"}, 0]
                },
                "interviewYes": {
                    "$ifNull": [{
                        "$size": {
                            "$filter": {
                                "input": "$interviews",
                                "as": "item",
                                "cond": {"$eq": ["$$item.approved", "Yes"]}
                            }
                        }
                    }, 0]
                },
                "interviewMaybe": {
                    "$ifNull": [{
                        "$size": {
                            "$filter": {
                                "input": "$interviews",
                                "as": "item",
                                "cond": {"$eq": ["$$item.approved", "Pending"]}
                            }
                        }
                    }, 0]
                },
                "interviewNo": {
                    "$ifNull": [{
                        "$size": {
                            "$filter": {
                                "input": "$interviews",
                                "as": "item",
                                "cond": {"$eq": ["$$item.approved", "No"]}
                            }
                        }
                    }, 0]
                },
                "interviewRating": {
                    "$ifNull": [{"$avg": "$interviews.rating"}, 0]
                },
                "certificationCount": {
                    "$ifNull": [{"$size": "$certifications"}, 0]
                }
            }
        }
    ]
    
    # Execute the aggregation pipeline
    results = await db.candidates.aggregate(pipeline).to_list(length=None)
    return results


async def get_candidate_analytics(email: str):
    """
    Get analytics for a specific candidate by email.
    
    Args:
        email: The email of the candidate to analyze
        
    Returns:
        A dictionary with candidate analytics data
    """
    db = await get_database()
    
    pipeline = [
        {
            "$match": {
                "email": email
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
                "skillsetAvg": {
                    "$ifNull": [{"$avg": "$skillsets.skillsetRating"}, 0]
                },
                "interviewYes": {
                    "$ifNull": [{
                        "$size": {
                            "$filter": {
                                "input": "$interviews",
                                "as": "item",
                                "cond": {"$eq": ["$$item.approved", "Yes"]}
                            }
                        }
                    }, 0]
                },
                "interviewMaybe": {
                    "$ifNull": [{
                        "$size": {
                            "$filter": {
                                "input": "$interviews",
                                "as": "item",
                                "cond": {"$eq": ["$$item.approved", "Pending"]}
                            }
                        }
                    }, 0]
                },
                "interviewNo": {
                    "$ifNull": [{
                        "$size": {
                            "$filter": {
                                "input": "$interviews",
                                "as": "item",
                                "cond": {"$eq": ["$$item.approved", "No"]}
                            }
                        }
                    }, 0]
                },
                "interviewRating": {
                    "$ifNull": [{"$avg": "$interviews.rating"}, 0]
                },
                "certificationCount": {
                    "$ifNull": [{"$size": "$certifications"}, 0]
                }
            }
        }
    ]
    
    # Execute the aggregation pipeline
    results = list(await db.candidates.aggregate(pipeline).to_list(length=None))
    return results[0] if results else {} 