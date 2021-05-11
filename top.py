import win32com.client as win32
from datetime import datetime as dt
from source_to_basefile import *
from basefile_to_exam import *
import os
from read_excel import *

def init_hwp():
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")
    hwp.XHwpWindows.Item(0).Visible = True
    hwp.HAction.GetDefault("ViewZoom", hwp.HParameterSet.HViewProperties.HSet)
    hwp.HParameterSet.HViewProperties.ZoomType = hwp.HwpZoomType("FitPage")
    hwp.HAction.Execute("ViewZoom", hwp.HParameterSet.HViewProperties.HSet)
    return hwp

hwp = init_hwp()
directory = os.getcwd()
excel_test = directory + r'\태풍\내신주문서.xlsx'

grade_number = 1 # 고1
dst = directory + r"\태풍\testbench_dst.hwp"

# Test Code
start_time = dt.now()
source_to_problem_execute(hwp, excel = excel_test, grade_number = grade_number, test_name = "테스트 시험지", dst = dst)
usage_exclude(hwp, destination = dst, grade = grade_number)
end_time = dt.now()
elapsed_time = end_time - start_time
print(f'입력을 완료하였습니다. 약 {elapsed_time.seconds}초 소요되었습니다.')