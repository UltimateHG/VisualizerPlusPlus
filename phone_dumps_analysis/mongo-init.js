db.createUser(
    {
        user: "maltego",
        pwd: "maltego",
        roles: [
            {
                role: "readWrite",
                db: "Maltego"
            }
        ]
    }
);

db.createCollection("calls"); 
