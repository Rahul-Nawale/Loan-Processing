import re
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import glob
import os
from os import listdir
from os.path import isfile, join
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import shutil
from pathlib import Path

popplerPath = r'C:\Users\rrhl2\Downloads\poppler-0.68.0\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

dir = r"C:\Users\rrhl2\Documents\loan processing sample docs"
image_save = r"C:\Users\rrhl2\PycharmProjects\practice\\"##IMPORTANT Double "\\" at the end IMPORTANT
# text_save = r"C:\Users\rrhl2\Desktop\\"##IMPORTANT Double "\\" at the end IMPORTANT


DL_list = []
Tax_page1_list = []
Tax_page2_list = []
Payslip_list = []

subfolders = [ f.path for f in os.scandir(dir) if f.is_dir() ]

for subfolder in subfolders:
    files = [f4 for f4 in listdir(subfolder) if isfile(join(subfolder, f4))]
    for file in files:
        filename1, file_extension = os.path.splitext(os.path.basename(file))
        if file.__contains__(".pdf"):
            file1 = subfolder+"/" + str(file)
            pages = convert_from_path(file1, 500, poppler_path=popplerPath)

            image_counter = 1

            for page in pages:
                filename = "page_" + str(image_counter) + ".jpg"
                name = filename1 + "_" + filename
                page.save(image_save + filename1 + "_page_" + str(image_counter) + ".jpg",
                    'JPEG')
                image_counter = image_counter + 1

            filelimit = image_counter - 1

            for i in range(1, filelimit + 1):
                # outfile = text_save + filename1 + "_page_" + str(i) + ".txt"
                #
                # f3 = open(outfile, "w")
                filename = image_save + filename1 + "_page_" + str(i) + ".jpg"
                text = str(((pytesseract.image_to_string(Image.open(filename)))))
                text = text.replace('-\n', '')
                # f3.write(text)
                # f3.close()


                if "driver license" in text.lower():
                    DL_list.append(i-1)
                elif "net pay" in text.lower():
                    Payslip_list.append(i-1)
                elif "filing status" in text.lower():
                    Tax_page1_list.append(i-1)
                elif "amount you owe" in text.lower():
                    Tax_page2_list.append(i-1)



            if DL_list:
                infile = PdfFileReader(file1, 'rb')
                output = PdfFileWriter()

                for a in DL_list:
                    p = infile.getPage(a)
                    output.addPage(p)
                newpath = subfolder + '/DL'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                DLpath = newpath + '/DL.pdf'
                if os.path.exists(DLpath):
                    counter = 1
                    filename11 = newpath + "/DL" + str(counter) + ".pdf"
                    while os.path.isfile(filename11):
                        counter += 1
                    DLpath = newpath + "/DL" + str(counter) + ".pdf"
                else:
                    DLpath = newpath + '/DL.pdf'
                with open(DLpath, 'wb') as f2:
                    output.write(f2)
                DL_list.clear()

            if Payslip_list:
                infile1 = PdfFileReader(file1, 'rb')
                output1 = PdfFileWriter()

                for b in Payslip_list:
                    p1 = infile1.getPage(b)
                    output1.addPage(p1)
                new1path = subfolder + '/Payslip'
                if not os.path.exists(new1path):
                    os.makedirs(new1path)

                Payslippath = new1path + '/Payslip.pdf'
                if os.path.exists(Payslippath):
                    Payslippath1 = new1path + '/Payslip1.pdf'
                    os.rename(Payslippath, Payslippath1)
                    Payslippath2 = new1path + '/Payslip2.pdf'
                    with open(Payslippath2, 'wb') as f1:
                        output1.write(f1)


                    xx = [e for e in os.listdir(new1path) if e.endswith(".pdf")]

                    merger2 = PdfFileMerger()

                    for pdf in xx:
                        pdfz = new1path+"/"+pdf
                        merger2.append(open(pdfz, 'rb'))

                    with open(Payslippath, "wb") as fout:
                        merger2.write(fout)

                    os.remove(Payslippath1)
                    os.remove(Payslippath2)

                else:
                    Payslippath = new1path + '/Payslip.pdf'
                    with open(Payslippath, 'wb') as f221:
                        output1.write(f221)
                Payslip_list.clear()

            if Tax_page1_list:
                if Tax_page2_list:
                    Tax_list = Tax_page1_list + Tax_page2_list
                    infile2 = PdfFileReader(file1, 'rb')
                    output2 = PdfFileWriter()

                    for c in Tax_list:
                        p2 = infile2.getPage(c)
                        output2.addPage(p2)
                    new2path = subfolder + '/Tax'
                    if not os.path.exists(new2path):
                        os.makedirs(new2path)
                    Taxpath = new2path + '/Tax.pdf'
                    if os.path.exists(Taxpath):
                        Taxpath1 = new2path + '/Tax1.pdf'
                        os.rename(Taxpath, Taxpath1)
                        Taxpath2 = new2path + '/Tax2.pdf'
                        with open(Taxpath2, 'wb') as f142:
                            output2.write(f142)

                        xx1 = [h for h in os.listdir(new2path) if h.endswith(".pdf")]

                        merger4 = PdfFileMerger()

                        for pdf in xx1:
                            pdfz1 = new2path + "/" + pdf
                            merger4.append(open(pdfz1, 'rb'))

                        with open(Taxpath, "wb") as fout3:
                            merger4.write(fout3)

                        os.remove(Taxpath1)
                        os.remove(Taxpath2)
                    else:
                        Taxpath = new2path + '/Tax.pdf'
                        with open(Taxpath, 'wb') as f12:
                            output2.write(f12)
                    Tax_list.clear()
                    Tax_page1_list.clear()
                    Tax_page2_list.clear()

            for f6 in os.listdir(image_save):
                if not f6.endswith(".jpg"):
                    continue
                os.remove(os.path.join(image_save, f6))

            # for f7 in os.listdir(text_save):
            #     if not f7.endswith(".txt"):
            #         continue
            #     os.remove(os.path.join(text_save, f7))

                # print(text)

        elif file.__contains__(".jpg"):
            # outfile = text_save + filename1 + ".txt"
            #
            # f8 = open(outfile, "w")
            file1 = subfolder+"/" + str(file)
            filename = file1
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            text = text.replace('-\n', '')

            # f8.write(text)
            # f8.close()

            if "driver license" in text.lower():
                newpath = subfolder + '/DL'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                DLpathimage = newpath + '/DL.jpg'
                if os.path.exists(DLpathimage):
                    counter = 1
                    filenameimage11 = newpath + "/DL" + str(counter) + ".jpg"
                    while os.path.isfile(filenameimage11):
                        counter += 1
                    DLpathimage = newpath + "/DL" + str(counter) + ".jpg"
                else:
                    DLpathimage = newpath + '/DL.jpg'
                shutil.move(file1, DLpathimage)


            elif "net pay" in text.lower():
                image_1 = Image.open(file1)
                im_1 = image_1.convert('RGB')

                new1path = subfolder + '/Payslip'
                if not os.path.exists(new1path):
                    os.makedirs(new1path)

                Payslippathimage = new1path + '/Payslip.pdf'
                if os.path.exists(Payslippathimage):
                    Payslippathimage1 = new1path + '/Payslip1.pdf'
                    os.rename(Payslippathimage, Payslippathimage1)
                    Payslippathimage2 = new1path + '/Payslip2.pdf'
                    im_1.save(Payslippathimage2)
                    xx = [g for g in os.listdir(new1path) if g.endswith(".pdf")]

                    merger3 = PdfFileMerger()

                    for pdf in xx:
                        pdfzz = new1path + "/" + pdf
                        merger3.append(open(pdfzz, 'rb'))

                    with open(Payslippathimage, "wb") as fout1:
                        merger3.write(fout1)

                    os.remove(Payslippathimage1)
                    os.remove(Payslippathimage2)

                else:
                    Payslippathimage = new1path + '/Payslip.pdf'
                    im_1.save(Payslippathimage)


            # elif "filing status" in text.lower():
            #     Tax_page1_list.append(i - 1)
            # elif "amount you owe" in text.lower():
            #     Tax_page2_list.append(i - 1)


        # for f9 in os.listdir(text_save):
        #     if not f9.endswith(".txt"):
        #         continue
        #     os.remove(os.path.join(text_save, f9))

finish_path = dir+"/finish.txt"
with open(finish_path, "w") as file:
    file.write("successful")


        # print(text)

