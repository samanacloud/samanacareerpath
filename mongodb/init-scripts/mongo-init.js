print('Starting MongoDB initialization...');

db = db.getSiblingDB('admin');

try {
    // Create root user if doesn't exist
    if (!db.getUser(process.env.MONGO_INITDB_ROOT_USERNAME)) {
        print('Creating root user:', process.env.MONGO_INITDB_ROOT_USERNAME);
        db.createUser({
            user: process.env.MONGO_INITDB_ROOT_USERNAME,
            pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
            roles: ['root'],
            mechanisms: ["SCRAM-SHA-256"]
        });
    }

    // Authenticate as root
    db.auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);

    // Switch to application database
    db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

    // Create application user if doesn't exist
    if (!db.getUser(process.env.MONGO_USER)) {
        print('Creating application user:', process.env.MONGO_USER);
        db.createUser({
            user: process.env.MONGO_USER,
            pwd: process.env.MONGO_PASSWORD,
            roles: [
                { role: 'readWrite', db: process.env.MONGO_INITDB_DATABASE }
            ],
            mechanisms: ["SCRAM-SHA-256"]
        });
    }

    // Create test collection to initialize database
    db.test_collection.insertOne({ 
        initialized: true, 
        createdAt: new Date(),
        env: process.env.CORE_ENV
    });

    print('MongoDB initialization completed successfully');
} catch (error) {
    print('Error during initialization:');
    printjson(error);
    throw error;
}