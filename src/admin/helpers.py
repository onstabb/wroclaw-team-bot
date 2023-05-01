import logging
import os.path

# import pywintypes
# from aiogram import types
#
# import win32com.client
#
# from src.admin.exceptions import ExcelConversionError
#
# logger: logging.Logger = logging.getLogger(__name__)
#
#
#
# def check_excel_file(document: types.Document) -> bool:
#
#     _split: list[str] = document.file_name.split(".")
#
#     if len(_split) < 2:
#         return False
#
#     file_ext: str = _split[-1]
#     if file_ext in ("xls", "xlsx"):
#         return True
#
#     return False
#
#
#
# def convert_excel_to_pdf(excel_path: str) -> str:
#
#     filename: str = os.path.basename(excel_path).split(".")[0]
#     dir_name: str = os.path.dirname(excel_path)
#     # PDF path when saving
#     path_pdf = os.path.join(dir_name, f"{filename}.pdf")
#
#     excel = win32com.client.Dispatch("Excel.Application")
#     excel.Visible = False
#
#     work_sheets_index_list: list[int] = [1]
#     sheets = excel.Workbooks.Open(excel_path)
#     try:
#         sheets.WorkSheets(work_sheets_index_list).Select()
#         # Save
#         sheets.ActiveSheet.ExportAsFixedFormat(0, path_pdf)
#         return path_pdf
#     except pywintypes.com_error as com_error:  # noqa
#         logger.error(com_error)
#         os.remove(path_pdf)
#         raise ExcelConversionError
#
#     finally:
#         sheets.Close()
#         excel.Quit()
