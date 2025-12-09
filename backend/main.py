from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    # get all contacts from sqlalchemy db
    contacts = Contact.query.all()
    
    # get list of jsonified contact objects and return them
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})


@app.route("/create_contact", methods=["POST"])
def create_contact():
    # extract fields from user post body
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    # error handling
    if not first_name or not last_name or not email:
        return (
            jsonify({'message': 'You must include a first name, last name, and email.'}),
            400,
        )
    # instatiate object
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    
    # stage and commit addition of new contact to db
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({'messge': str(e)}), 400
    
    # return confirmation for user
    return jsonify({'message': 'User created'}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"]) # endpoint is the id of the user we want to patch, flask essentially treats the last path as a parameter 
def update_contact(user_id): # match function parameter w/ path endpoint parameter
    # get db entry (python object) corresponding to the user id provided 
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({'message': 'User not found'}), 404
    
    # patch body from user
    data = request.json
    
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    # commits changes
    db.session.commit()
    
    return jsonify({'message': 'User updated'}), 200


@app.route("/delete_contact/<int:user_id", methods=["DELETE"])
def delete_contact(user_id):
    # get db entry (python object) corresponding to the user id provided 
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({'message': 'User not found'}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({'message': 'User deleted'}), 200





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)