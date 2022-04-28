# Source: https://pdfminersix.readthedocs.io/en/latest/howto/acro_forms.html

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text


def decode_value(value):

    # decode PSLiteral, PSKeyword
    if isinstance(value, (PSLiteral, PSKeyword)):
        value = value.name

    # decode bytes
    if isinstance(value, bytes):
        value = decode_text(value)

    return value

def fetch_form_fields(file_path):

    data = {}

    with open(file_path, 'rb') as fp:
        parser = PDFParser(fp)

        doc = PDFDocument(parser)
        res = resolve1(doc.catalog)

        if 'AcroForm' not in res:
            raise ValueError("No AcroForm Found")

        # may need further resolving        
        fields = resolve1(doc.catalog['AcroForm'])['Fields']

        for f in fields:
            field = resolve1(f)
            name, values = field.get('T'), field.get('V')

            # decode name
            name = decode_text(name)

            # resolve indirect obj
            values = resolve1(values)

            # decode value(s)
            if isinstance(values, list):
                values = [decode_value(v) for v in values]
            else:
                values = decode_value(values)

            data.update({name: values})

    return data

if __name__ == '__main__':

    file_path = '.\\form-02\\'
    file_path += '220119 АНКЕТА НЕЦУ-1.pdf'

    data = fetch_form_fields(file_path)

