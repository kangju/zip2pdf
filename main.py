# coding:utf8
import sys
from zip2pdfconverter import Zip2PdfConverter


def main():
    argv = sys.argv
    if len(argv) < 2:
        print("ZIPファイルパスを指定してください")
        return
    input_path = argv[1]
    converter = Zip2PdfConverter()
    converter.convert(input_path)


if __name__ == "__main__":
    main()
