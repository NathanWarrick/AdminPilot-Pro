import os
import pypdf
import tkinter as tk

from tkinter import filedialog

# import plugins.seqta as sqt


def split_documents():
    if os.path.exists("ADD DOCUMENTS HERE") == False:
        os.mkdir("ADD DOCUMENTS HERE")
        exit()
    else:
        pass
    names = []
    # Get the name of the file
    for root, dirs, files in os.walk("ADD DOCUMENTS HERE"):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            if extension == ".pdf":
                fullpath = root + "\\" + basename + extension
                # print(fullpath)

                reader = pypdf.PdfReader(fullpath)

                names = []
                filepaths = []
                pages = len(reader.pages)

                for i in range(len(reader.pages)):
                    output = pypdf.PdfWriter()
                    output.add_page(reader.pages[i])

                    page = reader.pages[i]
                    text = page.extract_text()

                    name = text[: text.index("[")]
                    name = name.strip()

                    try:
                        firstname = name[name.index(",") + 1 :].strip()
                    except:
                        firstname = name[name.index(".") + 1 :].strip()

                    try:
                        lastname = name[: name.index(",")].upper()
                    except:
                        lastname = name[: name.index(".")].upper()

                    fullname = lastname + ", " + firstname
                    filename = "documents/" + basename + "/" + fullname + ".pdf"

                    output_pdf = pypdf.PdfWriter()
                    output_pdf.add_page(reader.pages[i])
                    try:
                        output_pdf.write(filename)
                    except:
                        if os.path.exists("documents") == False:
                            os.mkdir("documents")
                        os.mkdir("documents/" + basename)
                        output_pdf.write(filename)

                    names.append(fullname)
                    filepaths.append(filename)

                    percent = ((i + 1) / pages) * 100
                    print(
                        str(i + 1) + "/" + str(pages) + "  " + str(round(percent)) + "%"
                    )
                    print(filepaths[i])
    return names, filepaths


def split_document():
    """
    Split a single edval timetable sheet into individual timetables.\n
    Opens a dialog to select the master pdf document

    :return: names, filepaths
    :rtype: list
    """
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    filename = os.path.basename(file_path)
    basename, extension = os.path.splitext(filename)

    try:
        reader = pypdf.PdfReader(file_path)
    except FileNotFoundError:
        print("File Not Found")
        exit()

    names = []
    filepaths = []
    pages = len(reader.pages)

    for i in range(len(reader.pages)):
        output = pypdf.PdfWriter()
        output.add_page(reader.pages[i])

        page = reader.pages[i]
        text = page.extract_text()

        name = text[: text.index("[")]
        name = name.strip()

        try:
            firstname = name[name.index(",") + 1 :].strip()
        except:
            firstname = name[name.index(".") + 1 :].strip()

        try:
            lastname = name[: name.index(",")].upper()
        except:
            lastname = name[: name.index(".")].upper()

        fullname = lastname + ", " + firstname
        filename = "documents/" + basename + "/" + fullname + ".pdf"

        output_pdf = pypdf.PdfWriter()
        output_pdf.add_page(reader.pages[i])
        try:
            output_pdf.write(filename)
        except:
            if os.path.exists(r"documents") == False:
                os.mkdir("documents")
            os.mkdir(r"documents/" + basename)
            output_pdf.write(filename)

        names.append(fullname)
        filepaths.append(filename)

        percent = ((i + 1) / pages) * 100
        print(str(i + 1) + "/" + str(pages) + "  " + str(round(percent)) + "%")
        print(filepaths[i])
    return names, filepaths
