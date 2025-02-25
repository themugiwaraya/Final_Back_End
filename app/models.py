from app import mongo
from bson.objectid import ObjectId
import logging

class User:
    @staticmethod
    def create(username, email, password_hash):
        user = {"username": username, "email": email, "password_hash": password_hash}
        return mongo.db.users.insert_one(user).inserted_id

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

class StartupIdea:
    @staticmethod
    def create(idea, analysis, user_id, category):
        new_idea = {"idea": idea, "analysis": analysis, "user_id": user_id, "category": category}
        return mongo.db.startup_ideas.insert_one(new_idea).inserted_id

    @staticmethod
    def find_by_user(user_id):
        return list(mongo.db.startup_ideas.find({"user_id": user_id}))

class Feedback:
    @staticmethod
    def create(user_id, idea_id, feedback_text):
        feedback = {"user_id": user_id, "idea_id": idea_id, "feedback": feedback_text}
        return mongo.db.feedbacks.insert_one(feedback).inserted_id

    @staticmethod
    def find_by_idea(idea_id):
        return list(mongo.db.feedbacks.find({"idea_id": idea_id}))

    @staticmethod
    def find_by_user(user_id):
        return list(mongo.db.feedbacks.find({"user_id": user_id}))

class Category:
    @staticmethod
    def create(name):
        return mongo.db.categories.insert_one({"name": name}).inserted_id

    @staticmethod
    def find_all():
        return list(mongo.db.categories.find({}))

    @staticmethod
    def find_by_id(category_id):
        try:
            logging.info("Converting category_id %s to ObjectId", category_id)
            oid = ObjectId(category_id)
            logging.info("Converted to ObjectId: %s", oid)
            category = mongo.db.categories.find_one({"_id": oid})
            if category:
                logging.info("Found category: %s", category)
            else:
                logging.warning("No category found with ObjectId: %s", oid)
            return category
        except Exception as e:
            logging.error("Error converting category_id %s: %s", category_id, e)
            return None