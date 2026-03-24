from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def health_check():
    return {"status": "ok", "message": "AI Community Event Board API is running"}


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
