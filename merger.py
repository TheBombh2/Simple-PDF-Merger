from PyPDF2 import PdfMerger

def mergePDFs(pdfDict,pdfsInOrder,savePath) -> bool:
    merger = PdfMerger()
    try:
        for key in pdfsInOrder:
            pdfToMerge = pdfDict[key]
            merger.append(pdfToMerge)
        merger.write(f"{savePath}\\merged.pdf")
        return True
    except:
        return False