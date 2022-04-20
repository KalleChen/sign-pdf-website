from pyhanko.sign import signers, timestamps
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

tsa_url = "https://freetsa.org/tsr"


def sign_with_timestamp(pdf, key, cert):
    cms_signer = signers.SimpleSigner.load(key, cert)

    tst_client = timestamps.HTTPTimeStamper("https://freetsa.org/tsr")

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
