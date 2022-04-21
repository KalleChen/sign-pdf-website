import os
from flask import (
    Flask,
    request,
    url_for,
    send_from_directory,
    render_template,
)

from sign import (
    sign_with_timestamp,
    sign_without_timestamp,
    sign_only_timestamp,
)

if not os.path.isfile("./files"):
    os.mkdir("./files")

UPLOAD_FOLDER = "./files"
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["POST", "GET"])
def add_signature_and_timestamp():
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
            key_filename = "key.pem"
            cert_filename = "cert.pem"
            pdf_file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
            )
            key_file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], key_filename)
            )
            cert_file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], cert_filename)
            )
            signed_pdf_filename = sign_with_timestamp(
                "./files/" + pdf_filename,
                "./files/" + key_filename,
                "./files/" + cert_filename,
            )
            return render_template(
                "index.html",
                file_url=url_for("download_file", filename=signed_pdf_filename),
            )
    return render_template("index.html")


@app.route("/signature", methods=["POST", "GET"])
def add_signature():
    if request.method == "POST":
        if (
            "pdf_file" not in request.files
            or "cert_file" not in request.files
            or "key_file" not in request.files
        ):
            return render_template("signature.html", error="No file part")
        pdf_file = request.files["pdf_file"]
        key_file = request.files["key_file"]
        cert_file = request.files["cert_file"]
        if (
            (pdf_file.filename == "" or pdf_file.filename is None)
            or (cert_file.filename == "" or cert_file.filename is None)
            or (key_file.filename == "" or key_file.filename is None)
        ):
            return render_template("signature.html", error="No selected file")
        if pdf_file and cert_file:
            pdf_filename = "upload.pdf"
            key_filename = "key.pem"
            cert_filename = "cert.pem"
            pdf_file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
            )
            key_file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], key_filename)
            )
            cert_file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], cert_filename)
            )
            signed_pdf_filename = sign_without_timestamp(
                "./files/" + pdf_filename,
                "./files/" + key_filename,
                "./files/" + cert_filename,
            )
            return render_template(
                "signature.html",
                file_url=url_for("download_file", filename=signed_pdf_filename),
            )
    return render_template("signature.html")


@app.route("/timestamp", methods=["POST", "GET"])
def add_timestamp():
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return render_template("timestamp.html", error="No file part")
        pdf_file = request.files["pdf_file"]
        if pdf_file.filename == "" or pdf_file.filename is None:
            return render_template("timestamp.html", error="No selected file")
        if pdf_file:
            pdf_filename = "upload.pdf"
            pdf_file.save(
                os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
            )
            signed_pdf_filename = sign_only_timestamp(
                "./files/" + pdf_filename,
            )
            return render_template(
                "timestamp.html",
                file_url=url_for("download_file", filename=signed_pdf_filename),
            )
    return render_template("timestamp.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
