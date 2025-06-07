from pathlib import Path
import shutil
import os
import zipfile
import img2pdf


class Zip2PdfConverter:
    """
    ZIPファイルをPDFに変換するためのクラス。
    指定したZIPファイルまたはディレクトリ内のZIPファイルを展開し、
    画像ファイルをPDFにまとめる。
    """
    def __init__(self, unzip_folder=None):
        """
        コンストラクタ。
        unzip_folder: 一時的にZIPを展開するフォルダのパス（省略時は./temp）
        """
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.unzip_folder = (
            unzip_folder or os.path.join(self.current_dir, "temp")
        )

    def convert(self, input_path):
        """
        指定パスがZIPファイルならPDF変換、
        ディレクトリなら中のZIPファイルをすべてPDF変換する。
        input_path: ZIPファイルまたはディレクトリのパス
        """
        if not os.path.exists(input_path):
            print("指定されたファイルが存在しません")
            return

        if os.path.isdir(input_path):
            for file in os.listdir(input_path):
                if file.endswith(".zip"):
                    self.zip2pdf(os.path.join(input_path, file))
        else:
            if input_path.endswith(".zip"):
                self.zip2pdf(input_path)
            else:
                print("指定されたファイルはZIPファイルではありません")
                return

    def get_file_size(self, file_path):
        """
        ファイルサイズをMB単位で取得する。
        戻り値: ("xx.xxMB", バイト数)
        """
        file_size = os.path.getsize(file_path)
        return (f"{file_size / 1024 / 1024:.2f}MB", file_size)

    def zip2pdf(self, zip_path):
        """
        ZIPファイルを展開し、画像をPDFに変換するメイン処理。
        zip_path: ZIPファイルのパス
        """
        try:
            trim_zip_name = (
                str(os.path.basename(zip_path)).replace(" ", "")[:-4]
            )
            pdf_file_path = os.path.join(
                os.path.dirname(os.path.abspath(zip_path)),
                trim_zip_name + ".pdf"
            )

            print(f"unzip:{zip_path}({self.get_file_size(zip_path)[0]})")
            img_folder = self.unzip(zip_path)
            print("unziped:" + zip_path)

            print("Convert images to PDF")
            self.create_pdf(img_folder, pdf_file_path)
            print("Converted images to PDF:" + pdf_file_path)

            shutil.rmtree(img_folder)
        except Exception as e:
            print(f"Error:{e}")

    def unzip(self, zip_path):
        """
        ZIPファイルを指定フォルダに展開する。
        zip_path: ZIPファイルのパス
        戻り値: 展開した画像フォルダのパス
        """
        unzip_folder_info_cache = None
        unzip_folder_path = ""
        zip_file_name = str(os.path.basename(zip_path)).replace(" ", "")[:-4]

        with zipfile.ZipFile(zip_path) as ext_zip:
            unzip_folder_info_cache = ext_zip.infolist()[0]
            unzip_folder_path = (
                self.unzip_folder
                if unzip_folder_info_cache.is_dir()
                else os.path.join(self.unzip_folder, zip_file_name)
            )
            ext_zip.extractall(unzip_folder_path)

        return (
            os.path.join(unzip_folder_path, unzip_folder_info_cache.name)
            if unzip_folder_info_cache.is_dir()
            else unzip_folder_path
        )

    def create_pdf(self, folder_path, create_pdf_path):
        """
        指定フォルダ内の画像(jpg/jpeg/png)をPDFにまとめる。
        folder_path: 画像フォルダのパス
        create_pdf_path: 出力PDFファイルのパス
        """
        img_list = [
            str(s)
            for s in Path(folder_path).iterdir()
            if s.suffix.lower() in [".jpg", ".jpeg", ".png"]
        ]
        img_list.sort()
        print(f"image cnt:{len(img_list)}")
        with open(create_pdf_path, "wb") as f:
            f.write(img2pdf.convert(list(img_list)))
