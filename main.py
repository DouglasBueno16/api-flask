from flask import Flask, request, jsonify

app = Flask(__name__)

# Armazenamento em memória
users = []
_next_id = 1


def _find_user(uid: int):
	for u in users:
		if u["id"] == uid:
			return u
	return None

@app.route("/")
def index():
    return "Bem-vindo à API de Usuários!", 200

@app.route("/users", methods=["GET"])
def list_users():
	return jsonify(users), 200


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


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
