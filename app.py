from flask import Flask

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(["pdf"])
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return "<h1>Hello World!</h1>"


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
