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


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
