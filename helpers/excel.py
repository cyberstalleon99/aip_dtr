import xlsxwriter
import settings
from datetime import datetime

def write(sheet_name, content):
    workbook = xlsxwriter.Workbook(f'{settings.PARENT_DIR}/DTR_Extracts/DTR - {datetime.now()}.xlsx')
  
    worksheet = workbook.add_worksheet(sheet_name)

    row_count = 1
    # col = 0

    for entry in content:
        row = (entry.name, entry.location, entry.date_in, entry.date_out, entry.work, entry.time_log)
        worksheet.write_row(row_count, 0, row)

        row_count += 1 


    # for name, score in (scores):
    #     worksheet.write(row, col, name)
    #     worksheet.write(row, col + 1, score)
    #     row += 1
    
    workbook.close()
