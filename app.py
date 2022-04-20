import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
    render_template,
)

UPLOAD_FOLDER = "./uploads"
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        if (
            "pdf_file" not in request.files
            or "cert_file" not in request.files
            or "key_file" not in request.files
        ):
            return render_template("index.html", error="No file part")
        pdf_file = request.files["pdf_file"]
        key_file = request.files["key_file"]
        cert_file = request.files["cert_file"]
        if (
            (pdf_file.filename == "" or pdf_file.filename is None)
            or (cert_file.filename == "" or cert_file.filename is None)
            or (key_file.filename == "" or key_file.filename is None)
        ):
            return render_template("index.html", error="No selected file")
        if pdf_file and cert_file:
            pdf_filename = "upload.pdf"
            pdf_file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
            )
            return render_template(
                "index.html",
                file_url=url_for("download_file", filename=pdf_filename),
            )
    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
