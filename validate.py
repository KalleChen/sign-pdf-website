import os
from pyhanko.sign.general import load_cert_from_pemder
from pyhanko_certvalidator import ValidationContext
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import (
    validate_pdf_signature,
)


def validate_pdf(pdf, root_cert, tsa_cert):
    try:
        if not os.path.isfile(root_cert) and not os.path.isfile(tsa_cert):
            raise Exception("Certificates not found")
        vc = None
        tsa_vc = None
        if os.path.isfile(root_cert):
            root_cert = load_cert_from_pemder(root_cert)
            vc = ValidationContext(trust_roots=[root_cert])
        if os.path.isfile(tsa_cert):
            tsa_root_cert = load_cert_from_pemder(tsa_cert)
            tsa_vc = ValidationContext(trust_roots=[tsa_root_cert])

        with open(pdf, "rb") as doc:
            r = PdfFileReader(doc)
            sig = r.embedded_signatures[0]
            status = validate_pdf_signature(sig, vc, tsa_vc)
            result = "{} \nIs valid: {}\n".format(
                status.pretty_print_details(),
                status.trusted,
            )
            if status.timestamp_validity:
                result = "{}\nTimestamp is valid: {}\n".format(
                    result, str(status.timestamp_validity.trusted)
                )
            return True, result
    except Exception as e:
        print(e)
        return False, str(e)
