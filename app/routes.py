import logging
import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.models import User, StartupIdea, Feedback, Category
from app.helpers import hash_password, check_password
from app.services.ollama_service import generate_startup_idea
from flask_cors import CORS
from bson.objectid import ObjectId
from app import mongo

main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid request"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if User.find_by_email(email):
        return jsonify({"message": "User already exists"}), 400

    password_hash = hash_password(password)
    User.create(username, email, password_hash)

    return jsonify({"message": "User registered successfully"}), 201

@main_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid request"}), 400

    email = data.get("email")
    password = data.get("password")

    user = User.find_by_email(email)
    if not user or not check_password(user["password_hash"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify({
        "access_token": access_token,
        "username": user["username"]
    }), 200

@main_routes.route("/generate-idea", methods=["POST"])
@jwt_required()
def generate_idea():
    try:
        current_user_id = get_jwt_identity()
        data = request.json

        if not data or "preferences" not in data or "categories" not in data:
            return jsonify({"message": "Invalid request"}), 400

        preferences = data["preferences"]
        categories = data["categories"]
        logging.info("Selected categories (names): %s", categories)

        category_names = ", ".join(categories) if categories else "General"
        if not categories:
            logging.warning("No categories provided. Using default: General")

        idea = generate_startup_idea(preferences, categories)

        new_idea_id = StartupIdea.create(idea, "Market analysis here", current_user_id, categories)

        return jsonify({
            "idea": idea,
            "analysis": "Market analysis here",
            "categories": category_names,
            "idea_id": str(new_idea_id)
        }), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@main_routes.route("/my-ideas", methods=["GET"])
@jwt_required()
def my_ideas():
    current_user_id = get_jwt_identity()
    ideas = StartupIdea.find_by_user(current_user_id)
    
    formatted_ideas = []
    for idea in ideas:
        cat_list = idea.get("category", [])
        cat_names = []
        for cat in cat_list:
            if isinstance(cat, str) and len(cat) == 24:
                try:
                    oid = ObjectId(cat)
                    found = Category.find_by_id(oid)
                    if found and "name" in found:
                        cat_names.append(found["name"])
                    else:
                        cat_names.append(cat)
                except Exception:
                    cat_names.append(cat)
            else:
                cat_names.append(cat)
        
        formatted_ideas.append({
            "idea": idea.get("idea", ""),
            "analysis": idea.get("analysis", ""),
            "categories": ", ".join(cat_names) if cat_names else "General",
            "idea_id": str(idea.get("_id"))
        })
    
    return jsonify(formatted_ideas), 200

@main_routes.route("/my-ideas", methods=["DELETE"])
@jwt_required()
def delete_my_ideas():
    try:
        current_user_id = get_jwt_identity()
        logging.info("Deleting ideas for user_id: %s", current_user_id)
        result = mongo.db.startup_ideas.delete_many({"user_id": current_user_id})
        logging.info("Deleted count: %s", result.deleted_count)
        return jsonify({
            "message": "History successfully deleted!",
            "deleted_count": result.deleted_count
        }), 200
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@main_routes.route("/feedback", methods=["POST"])
@jwt_required()
def feedback():
    data = request.json
    if not data:
        return jsonify({"message": "Invalid request"}), 400

    idea_id = data.get("idea_id")
    feedback_text = data.get("feedback")

    if not idea_id or not feedback_text:
        return jsonify({"message": "Idea ID and feedback are required"}), 400

    current_user_id = get_jwt_identity()
    Feedback.create(current_user_id, idea_id, feedback_text)

    return jsonify({"message": "Feedback submitted successfully"}), 201

@main_routes.route("/my-feedback", methods=["GET"])
@jwt_required()
def my_feedback():
    try:
        current_user_id = get_jwt_identity()
        feedbacks = Feedback.find_by_user(current_user_id)

        formatted_feedbacks = []
        for feedback in feedbacks:
            feedback['_id'] = str(feedback['_id'])
            formatted_feedbacks.append(feedback)

        return jsonify(formatted_feedbacks), 200
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@main_routes.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.find_all()
    return jsonify(categories), 200

@main_routes.route("/categories", methods=["POST"])
def add_category():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    Category.create(data["name"])
    return jsonify({"message": "Category added successfully"}), 201
