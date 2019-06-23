from pathlib import Path

def main():
    IMG_FOLDER = "/Users/kangju/Work/program/zip2pdf/sample"

    imgList = list([str(s) for s in Path(IMG_FOLDER).glob("*.jpg")])
    imgList.sort()
    print(imgList)

if __name__ == "__main__":
    main()