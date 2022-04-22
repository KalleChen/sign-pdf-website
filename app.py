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
from validate import validate_pdf

UPLOAD_FOLDER = "./files"

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["POST", "GET"])
def add_signature_and_timestamp():
    try:
        if request.method == "POST":
            if (
                "pdf_file" not in request.files
                or "cert_file" not in request.files
                or "key_file" not in request.files
            ):
                return render_template("index.html", error="No file part")
            if "tsa_url" not in request.values:
                return render_template("index.html", error="No tsa_url")
            pdf_file = request.files["pdf_file"]
            key_file = request.files["key_file"]
            cert_file = request.files["cert_file"]
            tsa_url = request.values["tsa_url"]
            if (
                (pdf_file.filename == "" or pdf_file.filename is None)
                or (cert_file.filename == "" or cert_file.filename is None)
                or (key_file.filename == "" or key_file.filename is None)
            ):
                return render_template("index.html", error="No selected file")
            if pdf_file and cert_file and key_file:
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
                    tsa_url,
                )
                if signed_pdf_filename is None:
                    return render_template(
                        "signature.html", error="Error while signing"
                    )
                return render_template(
                    "index.html",
                    file_url=url_for(
                        "download_file", filename=signed_pdf_filename
                    ),
                )
    except Exception as e:
        return render_template("index.html", error=str(e))
    return render_template("index.html")


@app.route("/signature", methods=["POST", "GET"])
def add_signature():
    try:
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
                return render_template(
                    "signature.html", error="No selected file"
                )
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
                if signed_pdf_filename is None:
                    return render_template(
                        "signature.html", error="Error while signing"
                    )
                return render_template(
                    "signature.html",
                    file_url=url_for(
                        "download_file", filename=signed_pdf_filename
                    ),
                )
    except Exception as e:
        return render_template("signature.html", error=str(e))
    return render_template("signature.html")


@app.route("/timestamp", methods=["POST", "GET"])
def add_timestamp():
    try:
        if request.method == "POST":
            if "pdf_file" not in request.files:
                return render_template("timestamp.html", error="No file part")
            if "tsa_url" not in request.values:
                return render_template("timestamp.html", error="No tsa url")
            pdf_file = request.files["pdf_file"]
            tsa_url = request.values["tsa_url"]
            if pdf_file.filename == "" or pdf_file.filename is None:
                return render_template(
                    "timestamp.html", error="No selected file"
                )
            if pdf_file:
                pdf_filename = "upload.pdf"
                pdf_file.save(
                    os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
                )
                signed_pdf_filename = sign_only_timestamp(
                    "./files/" + pdf_filename,
                    tsa_url,
                )
                if signed_pdf_filename is None:
                    return render_template(
                        "timestamp.html", error="Error while signing"
                    )
                return render_template(
                    "timestamp.html",
                    file_url=url_for(
                        "download_file", filename=signed_pdf_filename
                    ),
                )
    except Exception as e:
        return render_template("timestamp.html", error=str(e))
    return render_template("timestamp.html")


@app.route("/validate", methods=["POST", "GET"])
def validate():
    try:
        if request.method == "POST":
            if "pdf_file" not in request.files:
                return render_template("validate.html", error="No file part")
            if "cert_file" not in request.files:
                return render_template("validate.html", error="No cert file")
            if "tsa_cert_file" not in request.files:
                return render_template(
                    "validate.html", error="No tsa cert file"
                )
            pdf_file = request.files["pdf_file"]
            cert_file = request.files["cert_file"]
            tsa_cert_file = request.files["tsa_cert_file"]
            if pdf_file.filename == "" or pdf_file.filename is None:
                return render_template(
                    "validate.html", error="No selected file"
                )
            cert_filename = ""
            tsa_cert_filename = ""
            if cert_file:
                cert_filename = "cert.pem"
                cert_file.save(
                    os.path.join(app.config["UPLOAD_FOLDER"], cert_filename)
                )
            if tsa_cert_file:
                tsa_cert_filename = "tsa_cert.pem"
                tsa_cert_file.save(
                    os.path.join(app.config["UPLOAD_FOLDER"], tsa_cert_filename)
                )
            if pdf_file:
                pdf_filename = "upload.pdf"
                pdf_file.save(
                    os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
                )
                valid, validate_result = validate_pdf(
                    "./files/" + pdf_filename,
                    "./files/" + cert_filename,
                    "./files/" + tsa_cert_filename,
                )
                if not valid:
                    return render_template(
                        "validate.html", error=validate_result
                    )
                return render_template(
                    "validate.html",
                    result=validate_result.split("\n"),
                )
    except Exception as e:
        return render_template("validate.html", error=str(e))
    return render_template("validate.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
