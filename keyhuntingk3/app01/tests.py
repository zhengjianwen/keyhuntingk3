from django.test import TestCase
import xlrd
from app01 import path


data = xlrd.open_workbook(path.a)

table = data.sheets()[0]
nrows = table.nrows
# for i in range(nrows):
    # if i == 0:
    #     continue
    # for n in table.row_values(i):
    #     try:
    #         if n.strip() == '':
    #             table.row_values(i).remove(n)
    #     except Exception as e:
    #         pass
    # print(table.row_values(i))

# print(li)

#抓取所有sheet页的名称
worksheets = data.sheet_names()
print('worksheets is %s' % worksheets)

#定位到sheet1
# worksheet1 = data.sheet_by_name(worksheets[0])
# 通过索引顺序获取
worksheet1 = data.sheets()[0]
print(worksheet1)

#遍历sheet1中所有行row
num_rows = worksheet1.nrows
for curr_row in range(num_rows):
    row = worksheet1.row_values(curr_row)
    # print('row%s is %s' % (curr_row, row))
    for n in row:
        if n == '':
            row.remove(n)
    print(row)


#遍历sheet1中所有列col
# num_cols = worksheet1.ncols
# for curr_col in range(num_cols):
#     col = worksheet1.col_values(curr_col)
#     print('col%s is %s' %(curr_col ,col))


#遍历sheet1中所有单元格cell
# for rown in range(num_rows):
#     for coln in range(num_cols):
#         cell = worksheet1.cell_value(rown, coln)
#         print(cell)
