from flask import Flask, render_template
from config import Config
from controllers.event_controller import event_bp


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

app.register_blueprint(event_bp)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/health")
def health_check():
    return {"status": "ok", "message": "AI Community Event Board API is running"}

@app.route("/health/db")
def db_check():
    import os
    from pymongo import MongoClient
    uri = os.environ.get("MONGO_URI", "NOT SET")
    safe_uri = uri[:30] + "..." if len(uri) > 30 else uri
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return {"status": "ok", "uri_prefix": safe_uri}
    except Exception as e:
        return {"status": "error", "uri_prefix": safe_uri, "error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
