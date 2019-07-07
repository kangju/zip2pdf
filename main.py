from pathlib import Path
import shutil
import os
import zipfile
import img2pdf
import datetime
import sys
import json


UNZIP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)) , "temp")

def main():
    argv = sys.argv
    if len(argv) < 2:
        print("ZIPファイルパスを指定してください")
        return 

    ZIP_PATH = argv[1]
    ZIP_FILE_NAME = str(os.path.basename(ZIP_PATH)).replace(" ","")[:-4]
    PDF_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(ZIP_PATH)) , ZIP_FILE_NAME+".pdf")

    print("unzip:" + ZIP_PATH)
    imgfolder = unzip(ZIP_PATH)
    print("unziped:" + ZIP_PATH)

    print("Convert images to PDF")
    createPdf(imgfolder,PDF_FILE_PATH)
    print("Converted images to PDF:" + PDF_FILE_PATH)

def unzip(zipPath):
    unzipFolderNameCache = ""

    with zipfile.ZipFile(zipPath) as extZip:
        unzipFolderNameCache = extZip.namelist()[0]
        extZip.extractall(UNZIP_FOLDER)

    return os.path.join(UNZIP_FOLDER,unzipFolderNameCache)

def createPdf(folderpath,createPdfPath):
    imgList = list([str(s) for s in Path(folderpath).glob("*.jpg")])
    imgList.sort()

    with open(createPdfPath,"wb") as f:
        f.write(img2pdf.convert(list(imgList)))

if __name__ == "__main__":
    main()