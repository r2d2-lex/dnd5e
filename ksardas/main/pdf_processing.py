import re
import pdfrw
from io import BytesIO

VALUE = 0
TYPE = 1


class ProcessPdf:

    def add_data_to_pdf(self, template_path, data):
        print('\nAdding data to pdf...')
        template = pdfrw.PdfReader(template_path)

        for page in template.pages:
            annotations = page['/Annots']
            if annotations is None:
                continue

            for annotation in annotations:
                if annotation['/T']:
                    key = annotation['/T'][1:-1]
                    if re.search(r'.-[0-9]+', key):
                        key = key[:-2]

                    if key in data:
                        print('Found Key: {}'.format(key))
                        try:
                            record = data[key]
                            annotation.update(
                                pdfrw.PdfDict(V=self.encode_pdf_string(record[VALUE], record[TYPE]))
                            )
                        except IndexError as err:
                            print('Error get data key or type {}'.format(err))
                    annotation.update(pdfrw.PdfDict(Ff=1))

        template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        # pdfrw.PdfWriter().write(self.temp_directory + "data.pdf", template)
        # print('Pdf saved')
        # return self.temp_directory + "data.pdf"

        output_stream = BytesIO()
        pdfrw.PdfWriter().write(output_stream, template)
        return output_stream

    def encode_pdf_string(self, value, type):
        if type == 'string':
            if value:
                return pdfrw.objects.pdfstring.PdfString.encode(value)
            else:
                return pdfrw.objects.pdfstring.PdfString.encode('')
        elif type == 'checkbox':
            if value == 'True' or value == True:
                return pdfrw.objects.pdfname.BasePdfName('/Yes')
                # return pdfrw.objects.pdfstring.PdfString.encode('Y')
            else:
                return pdfrw.objects.pdfname.BasePdfName('/No')
                # return pdfrw.objects.pdfstring.PdfString.encode('')
        return ''
