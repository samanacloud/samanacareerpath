from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

# Create MongoDB client using settings
client = None
db = None

async def init_db():
    global client, db
    try:
        client = AsyncIOMotorClient(settings.get_mongodb_url)
        db = client[settings.MONGO_INITDB_DATABASE]
        await client.admin.command('ping')
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

async def check_db_connection():
    try:
        if client is None:
            await init_db()
        await client.admin.command('ping')
        return True, "Connected"
    except Exception as e:
        return False, str(e)

async def get_database():
    if db is None:
        await init_db()
    return db

async def close_db():
    if client:
        client.close() 