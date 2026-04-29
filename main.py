from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQL ALCHEMY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# SQL ALCHEMY MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


def _find_user(uid: int):
	user = User.query.get(uid)
	if not user:
		return jsonify({"error": "User not found"}), 404
	return user


@app.route("/")
def index():
    return "Bem-vindo à API de Usuários!", 200


@app.route("/health", methods=["GET"])
def health():
	return jsonify({"status": "ok"}), 200


@app.route("/users", methods=["GET"])
def list_users():
	return User.query.all(), 200


@app.route("/users", methods=["POST"])
def create_user():
	global _next_id
	if not request.is_json:
		return jsonify({"error": "JSON body required"}), 400
	data = request.get_json()
	name = data.get("name")
	email = data.get("email")
	if not name or not email:
		return jsonify({"error": "Both 'name' and 'email' are required"}), 400
	user = {"id": _next_id, "name": name, "email": email}
	_next_id += 1
	users.append(user)
	return jsonify(user), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
	user = _find_user(user_id)
	if not user:
		return jsonify({"error": "User not found"}), 404
	return jsonify(user), 200


@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
	user = _find_user(user_id)
	if not user:
		return jsonify({"error": "User not found"}), 404
	users.remove(user)
	return jsonify({"message": f"Usuário {user['id']}:{user['name']} foi deletado"}), 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
