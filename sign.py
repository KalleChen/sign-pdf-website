from pyhanko.sign import signers, timestamps
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

tsa_url = "https://freetsa.org/tsr"


def sign_with_timestamp(pdf, key, cert, tsa_url):
    try:
        cms_signer = signers.SimpleSigner.load(key, cert)

        tst_client = timestamps.HTTPTimeStamper(tsa_url)

        with open(pdf, "rb") as inf:
            if cms_signer:
                with open("./files/signed.pdf", "wb") as outf:
                    w = IncrementalPdfFileWriter(inf)
                    signers.sign_pdf(
                        w,
                        signers.PdfSignatureMetadata(field_name="Signature1"),
                        signer=cms_signer,
                        timestamper=tst_client,
                        output=outf,
                    )
        return "signed.pdf"
    except Exception as e:
        print(e)
        return None


def sign_without_timestamp(pdf, key, cert):
    try:
        cms_signer = signers.SimpleSigner.load(key, cert)

        with open(pdf, "rb") as inf:
            if cms_signer:
                with open("./files/signed_without_timestamp.pdf", "wb") as outf:
                    w = IncrementalPdfFileWriter(inf)
                    signers.sign_pdf(
                        w,
                        signers.PdfSignatureMetadata(field_name="Signature1"),
                        signer=cms_signer,
                        output=outf,
                    )
        return "signed_without_timestamp.pdf"
    except Exception as e:
        print(e)
        return None


def sign_only_timestamp(pdf, tsa_url):
    try:
        tst_client = timestamps.HTTPTimeStamper(tsa_url)
        with open(pdf, "rb") as inf:
            with open("./files/only_timestamp.pdf", "wb") as outf:
                w = IncrementalPdfFileWriter(inf)
                signer = signers.pdf_signer.PdfTimeStamper(
                    timestamper=tst_client
                )
                signer.timestamp_pdf(
                    md_algorithm="sha256",
                    pdf_out=w,
                    timestamper=tst_client,
                    output=outf,
                )
        return "only_timestamp.pdf"
    except Exception as e:
        print(e)
        return None
