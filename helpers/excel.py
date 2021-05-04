import os
import xlsxwriter
import settings
from datetime import datetime

def write(sheet_name, content):
    workbook = xlsxwriter.Workbook(os.path.join(settings.DTR_EXTRACTS_PATH, f'DTR - {datetime.now()}.xlsx'))
    worksheet = workbook.add_worksheet(sheet_name)

    row_count = 1
    for entry in content:
        row = (entry.name, entry.location, entry.date_in, entry.date_out, entry.work, entry.time_log)
        worksheet.write_row(row_count, 0, row)

        row_count += 1 
    
    workbook.close()
