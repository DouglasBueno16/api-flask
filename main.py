from flask import Flask, request, jsonify
from dbConfig import db, User, init_db

app = Flask(__name__)
init_db(app)

@app.route("/")
def index():
    return "Bem-vindo à API de Usuários!", 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users], 200)

@app.route("/users", methods=["POST"])
def create_user():
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    
    if not name or not email:
        return jsonify({"error": "Both 'name' and 'email' are required"}), 400

    # Verifica se o email já existe
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Usuário {user.id}: {user.name} foi deletado"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
