import os


def to_pdf(docx_file: str):
    """
    Converts docx file to pdf and saves it in the same location
    :param docx_file: Path of docx file
    :return: Path to generated PDF
    """
    file_ext = '.docx'
    if docx_file[-1*len(file_ext):] == file_ext:
        os.system('abiword --to=pdf '+docx_file)
    else:
        raise Exception("Given file isn't " + file_ext)
