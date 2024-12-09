# coding:utf8

from pathlib import Path
import shutil
import os
import zipfile
import img2pdf
import sys
import re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UNZIP_FOLDER = os.path.join(CURRENT_DIR, "temp")


def main():
    argv = sys.argv
    if len(argv) < 2:
        print("ZIPファイルパスを指定してください")
        return

    input_path = argv[1]

    if not os.path.exists(input_path):
        print("指定されたファイルが存在しません")
        return

    # check input path is directory or file
    if os.path.isdir(input_path):
        for file in os.listdir(input_path):
            if file.endswith(".zip"):
                zip2pdf(os.path.join(input_path, file))
    else:
        if input_path.endswith(".zip"):
            zip2pdf(input_path)
        else:
            print("指定されたファイルはZIPファイルではありません")
            return


def get_file_size(file_path):
    # ファイルサイズを取得(MB)
    file_size = os.path.getsize(file_path)
    return (f"{file_size / 1024 / 1024:.2f}MB", file_size)


def zip2pdf(zip_path):
    try:
        trim_zip_name = str(os.path.basename(zip_path)).replace(" ", "")[:-4]
        pdf_file_path = os.path.join(os.path.dirname(
            os.path.abspath(zip_path)), trim_zip_name+".pdf")

        print(f"unzip:{zip_path}({get_file_size(zip_path)[0]})")
        img_folder = unzip(zip_path)
        print("unziped:" + zip_path)

        print("Convert images to PDF")
        createPdf(img_folder, pdf_file_path)
        print("Converted images to PDF:" + pdf_file_path)

        shutil.rmtree(img_folder)
    except Exception as e:
        print(f"Error:{e}")


def unzip(zipPath):
    unzipFolderInfoCache = None
    unzipFolderPath = ""
    ZIP_FILE_NAME = str(os.path.basename(zipPath)).replace(" ", "")[:-4]

    with zipfile.ZipFile(zipPath) as extZip:
        unzipFolderInfoCache = extZip.infolist()[0]
        unzipFolderPath = UNZIP_FOLDER if unzipFolderInfoCache.is_dir(
        ) else os.path.join(UNZIP_FOLDER, ZIP_FILE_NAME)

        extZip.extractall(unzipFolderPath)

    return os.path.join(unzipFolderPath, unzipFolderInfoCache.name) if unzipFolderInfoCache.is_dir() else unzipFolderPath


def createPdf(folder_path, createPdfPath):
    imgList = list([str(s) for s in Path(folder_path).glob(
        "*") if re.search(".*\\.(jpg|jpeg|png)", str(s))])
    imgList.sort()

    print(f"image cnt:{len(imgList)}")

    with open(createPdfPath, "wb") as f:
        f.write(img2pdf.convert(list(imgList)))


if __name__ == "__main__":
    main()
