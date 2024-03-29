#coding:utf8

from pathlib import Path
import shutil
import os
import zipfile
import img2pdf
import sys
import re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UNZIP_FOLDER = os.path.join(CURRENT_DIR , "temp")

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

    shutil.rmtree(imgfolder)

def unzip(zipPath):
    unzipFolderInfoCache = None
    unzipFolderPath = ""
    ZIP_FILE_NAME = str(os.path.basename(zipPath)).replace(" ","")[:-4]

    with zipfile.ZipFile(zipPath) as extZip:
        unzipFolderInfoCache = extZip.infolist()[0]
        unzipFolderPath = UNZIP_FOLDER if unzipFolderInfoCache.is_dir() else os.path.join(UNZIP_FOLDER,ZIP_FILE_NAME)

        extZip.extractall(unzipFolderPath)

    return os.path.join(unzipFolderPath,unzipFolderInfoCache.name) if unzipFolderInfoCache.is_dir() else unzipFolderPath


def createPdf(folderpath,createPdfPath):
    imgList = list([str(s) for s in Path(folderpath).glob("*") if re.search(".*\.(jpg|jpeg|png)",str(s))])
    imgList.sort()

    print(f"image cnt:{len(imgList)}")

    with open(createPdfPath,"wb") as f:
        f.write(img2pdf.convert(list(imgList)))

if __name__ == "__main__":
    main()