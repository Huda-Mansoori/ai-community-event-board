from flask import Flask
from config import Config
from controllers.event_controller import event_bp


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(event_bp)


@app.route("/")
def health_check():
    return {"status": "ok", "message": "AI Community Event Board API is running"}

@app.route("/")
def home():
    return "AI Community Event Board - Huda (60304645)"


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
