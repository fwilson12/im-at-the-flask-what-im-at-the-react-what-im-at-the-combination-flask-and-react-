from config import db

# class to define how we store entries in our db
class Contact(db.Model):
    # each instance variable is a column in our db
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(90), unique=False, nullable=False)
    last_name = db.Column(db.String(90), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # returns jsonified object
    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email
        }
    


