import os
import shutil
from time import sleep
from read_excel import *
from datetime import datetime as dt
from api import *

"""
# 본 모듈은 문제저장용 파일에서 검토용파일로 가져올 때 사용하는 모듈입니다.
# 만든이 : 이준호(a01032208149@gmail.com으로 연락주세요 :) )
"""

replace_question_to_number = { '서답형1' : 41,'서답형2' : 42, '서답형3' : 43,'서답형4' : 44,'서답형5' : 45,'서답형6' : 46,'서답형7' : 47,'서답형8' : 48,'서답형9' : 49,'서답형10' : 50,
                            '서술형1' : 51,'서술형2' : 52, '서술형3' : 53, '서술형4' : 54, '서술형5' : 55, '서술형6' : 56, '서술형7' : 57, '서술형8' : 58, '서술형9' : 59, '서술형10' : 60}
replace_number_to_question = {41 : '서1', 42 : '서2', 43 : '서3',44 : '서4',45 : '서5',46 : '서6',47 : '서7', 48 : '서8', 49 : '서9', 50 : '서10',
                              51 : '서1', 52 : '서2', 53 : '서3',54 : '서4',55 : '서5',56 : '서6',57 : '서7', 58 : '서8', 59 : '서9', 60 : '서10'}

def add_field_source_file(hwp, source : str):
    """
    (미완성) 문제저장용 파일에 각 문제에 필드를 추가하는 함수입니다.
    :param hwp: hwp 파일 exe
    :param source: 문제저장용 파일 경로
    """
    hwp.Open(f"{source}")
    hwp.MovePos(2)
    field_position = dict()
    before_page = -1
    num = 1
    while True:
        find_random_word(hwp = hwp, size = 10.0)
        current_page = hwp.XHwpDocuments.Item(0).XHwpDocumentInfo.CurrentPage
        if before_page < current_page:
            field_position[hwp.GetPos()] = "problem"
            hwp.HAction.Run("MovePageDown")
            hwp.HAction.Run("MoveUp")
            before_page += 1
            sleep(0.1)
        else:
            break

    for position in sorted(field_position.keys()):
        hwp.SetPos(*position)
        hwp.HAction.Run("SelectAll")
        hwp.HAction.Run("Move")
        hwp.HAction.Run("MoveLeft")
        add_field(hwp = hwp, field_name = f"{num}번문제")
        sleep(0.1)
        num += 1

    hwp.MovePos(2)
    field_position_2 = dict()
    num2 = 1
    for _ in range(num):
        find_random_word(hwp = hwp, size = 7.0)
        field_position_2[hwp.GetPos()] = "solution"
        hwp.HAction.Run("MovePageDown")
        sleep(0.1)

    for position in sorted(field_position_2.keys()):
        hwp.SetPos(*position)
        hwp.HAction.Run("SelectAll")
        hwp.HAction.Run("Move")
        hwp.HAction.Run("MoveLeft")
        add_field(hwp = hwp, field_name = f"{num2}번풀이")
        sleep(0.1)
        num2 += 1
    hwp.Save()

def add_problem_number_basefile(hwp, problem_array , file : str):
    hwp.Open(rf'{file}')
    field_list = [x for x in hwp.GetFieldList().split("\x02") if ('번호' in x)]
    field_list = [x for x in field_list if (int(x.replace("번풀이번호", "").replace("번문제번호", "")) < len(problem_array)+1)]
    for field in field_list:
        hwp.MoveToField(field)
        insert_text(hwp, str(problem_array[int(field[0])-1]))

def source_to_basefile_copy_problem(hwp, source, problem_number : int, copy_only_problem : bool = False):
    """
    문제저장용 파일에서 베이스파일로 문제를 복사하는 함수입니다.
    :param hwp : 아래아한글 기본파일 exe
    :param source : 문제저장용 파일경로
    :param problem_number : 문제저장용 파일에서 가져올 문제번호
    ★ 문제저장용 파일에 누름틀(Ctrl + K E)이 '1번문제' 양식으로 문제의 맨 앞에 지정되야 합니다!!!
    """
    # 오류 처리 구문
    if os.path.exists(source) == False:
        raise Exception("문제저장용 파일이 존재하지 않습니다!")
    hwp.Open(rf'{source}')
    field_list = hwp.GetFieldList().split("\x02")
    if f'{problem_number}번문제' not in field_list:
        kill_hwp()
        raise Exception(f"문제 저장용 파일에 {problem_number}번 문제가 존재하지 않습니다!")
    hwp.MoveToField(f'{problem_number}번문제')
    if (copy_only_problem == True):
        start_pos = hwp.GetPos()
        end_string = """1번, 2번, 3번, 4번, 5번, 6번, 7번, 8번, 9번, 10번,
                     11번, 12번, 13번, 14번, 15번, 16번, 17번, 18번, 19번, 20번,
                     21번, 22번, 23번, 24번, 25번, 26번, 27번, 28번, 29번, 30번,
                     31번, 32번, 33번, 34번, 35번, 36번, 37번, 38번, 39번, 40번,
                     41번, 42번, 43번, 44번, 45번, 46번, 47번, 48번, 49번, 50번
                     """
        find_word(hwp, end_string, direction = "Forward")
        hwp.HAction.Run("MoveLineEnd")
        end_pos = hwp.GetPos()
        hwp.Run("Cancel")
        hwp.SetPos(*start_pos)
        hwp.Run("Select")
        hwp.SetPos(*end_pos)
        hwp.HAction.Run("Copy")
        hwp.HAction.Run("MoveDown")
        sleep(0.1)
    else:
        start_pos = hwp.GetPos()
        hwp.HAction.Run("SelectAll")
        hwp.HAction.Run("MoveRight")
        end_pos = hwp.GetPos()
        hwp.SetPos(*start_pos)
        hwp.Run("Select")
        hwp.SetPos(*end_pos)
        hwp.HAction.Run("Copy")
        hwp.HAction.Run("MoveDown")
        sleep(0.1)

def source_to_basefile_copy_solution(hwp, source, problem_number):
    """
    문제저장용 파일에서 베이스파일로 풀이를 복사하는 함수입니다.
    :param hwp : 아래아한글 기본파일 exe
    :param source : 문제저장용 파일경로
    :param problem_number : 문제저장용 파일에서 복사할 풀이번호
    ★ 문제저장용 파일에 누름틀(Ctrl + K E)이 '1번문제' 양식으로 문제의 맨 앞에 지정되야 합니다!!!
    """
    hwp.Open(rf'{source}')
    if os.path.exists(source) == False:
        raise Exception("문제저장용 파일이 존재하지 않습니다!")
    field_list = hwp.GetFieldList().split("\x02")
    if f'{problem_number}번풀이' not in field_list:
        kill_hwp()
        raise Exception(f"문제 저장용 파일에 {problem_number}번 풀이가 존재하지 않습니다!")
    hwp.MoveToField(f'{problem_number}번풀이')
    hwp.HAction.Run("MoveSelTopLevelEnd")
    hwp.HAction.Run("Copy")
    hwp.HAction.Run("MoveDown")
    sleep(0.1)

def source_to_basefile_paste_problem(hwp, destination, problem_number, txtbox = True):
    """
    문제저장용 파일에서 베이스파일로 문제를 붙여넣기하는 함수입니다.
    :param hwp : 아래아한글 기본파일 exe
    :param destination : 검토용파일 파일경로
    :param problem_number : 검토용파일에 붙여넣기할 문제번호
    ★ 검토용파일에 누름틀(Ctrl + K E)이 '1번문제' 양식으로 들어갈 문제의 맨 앞에 지정되야 합니다!!!
    """
    hwp.Open(rf'{destination}')
    if os.path.exists(destination) == False:
        raise Exception("검토용 파일이 존재하지 않습니다!")
    field_list = hwp.GetFieldList().split("\x02")
    if txtbox == True:
        if f'{problem_number}번문제글상자' not in field_list:
            kill_hwp()
            raise Exception(f"검토용 파일에 {problem_number}번 문제가 존재하지 않습니다!")
    else:
        if f'{problem_number}번문제' not in field_list:
            kill_hwp()
            raise Exception(f"검토용 파일에 {problem_number}번 문제가 존재하지 않습니다!")
    hwp.MoveToField(f'{problem_number}번문제글상자') if txtbox == True else hwp.MoveToField(f'{problem_number}번문제')
    hwp.HAction.Run("Paste")
    hwp.HAction.Run("MoveDown")
    hwp.Save()
    sleep(0.1)

def source_to_basefile_paste_solution(hwp, destination, problem_number, txtbox = True):
    """
    문제저장용 파일에서 베이스파일로 풀이를 붙여넣기하는 함수입니다.
    :param hwp: 아래아한글 기본파일 exe
    :param destination: 검토용파일 파일경로
    :param problem_number: 검토용파일에 붙여넣기할 풀이번호
    * 검토용파일에 누름틀(Ctrl + K E)이 '1번풀이' 양식으로 들어갈 풀이의 맨 앞에 지정되야 합니다!!!
    """
    hwp.Open(rf'{destination}')
    if os.path.exists(destination) == False:
        raise Exception("검토용 파일이 존재하지 않습니다!")
    hwp.Open(rf'{destination}')
    field_list = hwp.GetFieldList().split("\x02")
    if txtbox == True:
        if f'{problem_number}번풀이글상자' not in field_list:
            kill_hwp()
            raise Exception(f"검토용 파일에 {problem_number}번 풀이가 존재하지 않습니다!")
    else:
        if f'{problem_number}번풀이' not in field_list:
            kill_hwp()
            raise Exception(f"검토용 파일에 {problem_number}번 풀이가 존재하지 않습니다!")
    hwp.MoveToField(f'{problem_number}번풀이글상자') if txtbox == True else hwp.MoveToField(f'{problem_number}번풀이')
    hwp.HAction.Run("Paste")

    # 서식 유지를 위한 실행 코드
    # shape_copy_paste(hwp)
    hwp.HAction.Run("MoveDown")
    hwp.Save()
    sleep(0.1)

# def source_to_problem_execute(hwp, excel : str, grade_number : int, test_name : str, basefile :bool = True):
#     start_time = dt.now()
#     dst = new_basefile(test_name) if basefile == False else new_basefile_no_number(test_name)
#     problems = get_problem_list(excel=excel, grade=grade_number, test_name=test_name)
#     # print(problems)
#     dst_problem_number_for_field = [x for x in range(1, len(readexcel(excel, grade = grade_number)[test_name])+1)]
#     for i in range(problems.shape[0]):
#         problem_set = problems.iloc[i]
#         src = array_to_problem_directory(problem_set, grade=grade_number, test_name = test_name)
#         # print(src)
#         problem_directory, src_problem_number, dst_problem_number, src_problem_score = src[0], src[1], src[2], src[3]
#         print(f"{dst_problem_number_for_field[i]}번 입력중...({i+1}번째 입력)")
#         source_to_basefile_problem(hwp, source = problem_directory , source_number = src_problem_number, destination = dst, destination_number = dst_problem_number_for_field[i])
#         source_to_basefile_solution(hwp, source = problem_directory, source_number = src_problem_number, destination = dst, destination_number = dst_problem_number_for_field[i])
#         hwp.PutFieldText(Field = f"{i+1}번문제번호", Text = str(replace_number_to_question[int(dst_problem_number)]) if int(dst_problem_number) >= 41 else str(int(dst_problem_number)))
#         hwp.PutFieldText(Field = f"{i+1}번풀이번호", Text = str(replace_number_to_question[int(dst_problem_number)]) if int(dst_problem_number) >= 41 else str(int(dst_problem_number)))
#         print(f"{dst_problem_number_for_field[i]}번 입력완료! ({i+1}번째 입력완료)")
#         hwp.Save()
#     if basefile == True:
#         hwp.PutFieldText(Field = "검토용파일이름", Text = test_name)
#         hwp.Save()
#     hwp.Save()
#     sleep(0.2)
#     end_time = dt.now()
#     elapsed_time = end_time - start_time
#     print(f'입력을 완료하였습니다. 약 {elapsed_time.seconds}초 소요되었습니다.')
#
# def source_to_problem_change_basefile(hwp, excel : str, grade_number : int, test_name_from : str, test_name_to : str):
#     dst = new_basefile_no_number(test_name_to)
#     problems_not_intersect = get_problem_list_change(excel = excel, grade = grade_number, test_name_from = test_name_from, test_name_to = test_name_to)[1]
#     problem_number_list = []
#     for i in range(problems_not_intersect.shape[0]):
#         src = array_to_problem_directory(problems_not_intersect[i, :], grade=grade_number)
#         src_problem_number = problems_not_intersect[i][3]
#         dst_problem_number = i+1
#         print(f"{dst_problem_number}번 입력중...({i+1}번째 입력)")
#         source_to_basefile_problem(hwp, source=src, source_number=src_problem_number, destination=dst, destination_number=dst_problem_number)
#         source_to_basefile_solution(hwp, source=src, source_number=src_problem_number, destination=dst, destination_number=dst_problem_number)
#         print(f"{dst_problem_number}번 입력완료! ({i+1}번째 입력완료)")
#         problem_number_list.append(int(problems_not_intersect[i][4]))
#     problem_number_list =[replace_number_to_question[x] if int(x) > 40 else int(x) for x in problem_number_list]
#     add_problem_number_basefile(hwp, problem_array = problem_number_list, file = dst)
#     hwp.Save()

def source_to_basefile_problem(hwp, source, source_number, destination, destination_number, txtbox = True):
    """
    # 문제저장용 파일에서 베이스파일로 문제를 복사, 붙여넣기하는 함수입니다.
    # 위의 함수를 활용하였기에 copy, paste 함수만 잘 작동하면 됩니다!
    # hwp : 아래아한글 기본파일
    # source : 문제저장용 파일경로
    # source_number : 문제저장용에서 가져올 문제 번호
    # destination : 검토용파일 파일경로
    # destination_number : 검토용파일에 넣을 문제번호
    """
    source_to_basefile_copy_problem(hwp, source, source_number)
    source_to_basefile_paste_problem(hwp, destination, destination_number, txtbox = txtbox)

def source_to_basefile_solution(hwp, source, source_number, destination, destination_number, txtbox = True):
    """
       # 문제저장용 파일에서 베이스파일로 풀이를 복사, 붙여넣기하는 함수입니다.
       # 위의 함수를 활용하였기에 copy, paste 함수만 잘 작동하면 됩니다!
       # hwp : 아래아한글 기본파일
       # source : 문제저장용 파일경로
       # source_number : 문제저장용에서 가져올 문제 번호
       # destination : 검토용파일 파일경로
       # destination_number : 검토용파일에 넣을 문제번호
       """
    source_to_basefile_copy_solution(hwp, source, source_number)
    source_to_basefile_paste_solution(hwp, destination, destination_number, txtbox = txtbox)

def new_basefile(file_name : str):
    source_directory = os.getcwd() + r'\태풍\기출_문제+답지_원본_2문제씩_번호o.hwp'
    shutil.copyfile(source_directory, os.getcwd() + rf'\태풍\{file_name}_검토용파일_(문제+답지).hwp')
    new_file = os.getcwd() + rf'\태풍\{file_name}_검토용파일_(문제+답지).hwp'
    return new_file

def new_basefile_no_number(file_name : str):
    source_directory = os.getcwd() + r'\태풍\기출_문제+답지_원본_2문제씩_번호x.hwp'
    shutil.copyfile(source_directory, os.getcwd() + rf'\태풍\{file_name}_검토용파일_(문제+답지).hwp')
    new_file = os.getcwd() + rf'\태풍\{file_name}_검토용파일_(문제+답지).hwp'
    return new_file

def basefile_to_source(hwp, basefile : str, grade_number, excel = None):
    start_time = dt.now()
    hwp.Open(rf'{basefile}')
    # 검토용파일 존재하는지 검사
    if os.path.exists(basefile) == False:
        raise Exception("검토용파일이 존재하지 않습니다!")

    test_name = hwp.GetFieldText("검토용파일이름")
    print(test_name+" 반영 진행중...")
    problems = get_problem_list(excel=excel, grade=grade_number, test_name=test_name)
    field_list = hwp.GetFieldList().split("\x02")
    field_list_problem_number = [x for x in field_list if "번문제번호" in x]
    field_list_solution_number = [x for x in field_list if "번풀이번호" in x]
    field_list_change_problem_number = []
    field_list_change_solution_number = []

    for field_problem_number in field_list_problem_number:
        hwp.MoveToField(field_problem_number, start = False)
        hwp.HAction.Run("SelectAll")
        if hwp.CharShape.Item("TextColor") == 255: # 빨간색일 경우
            hwp.HAction.Run("MoveLeft")
            field_list_change_problem_number.append(hwp.GetCurFieldName())
        else:
            pass

    for field_solution_number in field_list_solution_number:
        hwp.MoveToField(field_solution_number, start=False)
        hwp.HAction.Run("SelectAll")
        if hwp.CharShape.Item("TextColor") == 255: # 빨간색일 경우
            hwp.HAction.Run("MoveLeft")
            field_list_change_solution_number.append(hwp.GetCurFieldName())
        else:
            pass
    field_list_change_problem_number = list(map(lambda y : int(y)-1, list(map(lambda x: x[:-5], field_list_change_problem_number))))
    field_list_change_solution_number = list(map(lambda y : int(y)-1, list(map(lambda x: x[:-5], field_list_change_solution_number))))
    problem_change_problem = problems.iloc[field_list_change_problem_number]
    problem_change_solution = problems.iloc[field_list_change_solution_number]
    for i in range(problem_change_problem.shape[0]):
        problem_change_problem_set = problem_change_problem.iloc[i]
        src = array_to_problem_directory(problem_change_problem_set, grade=grade_number, test_name = test_name)
        problem_directory, src_problem_number, dst_problem_number, src_problem_score = src[0], src[1], src[2], src[3]
        print(f"{field_list_change_problem_number[i]+1}번문제 반영중...({i+1}번째 입력)")
        hwp.Open(rf'{basefile}')
        hwp.MoveToField(f"{field_list_change_problem_number[i]+1}번문제", start = True)
        start_pos = hwp.GetPos()
        hwp.Run("Cancel")
        hwp.MoveToField(f"{field_list_change_problem_number[i]+1}번문제", start = False)
        end_pos = hwp.GetPos()
        hwp.Run("Cancel")
        hwp.SetPos(*start_pos)
        hwp.Run("Select")
        hwp.SetPos(*end_pos)
        hwp.HAction.Run("Copy")
        hwp.HAction.Run("MoveDown")

        hwp.Open(rf"{problem_directory}")
        if os.path.exists(problem_directory) == False:
            raise Exception(f"{field_list_change_problem_number[i]+1}번문제 문제저장용 파일이 존재하지 않습니다!")
        hwp.MoveToField(f"{src[1]}번문제")
        hwp.HAction.Run("MoveRight")
        start_pos = hwp.GetPos()
        hwp.HAction.Run("SelectAll")
        hwp.HAction.Run("MoveRight")
        end_pos = hwp.GetPos()
        hwp.SetPos(*start_pos)
        hwp.Run("Select")
        hwp.SetPos(*end_pos)
        hwp.Run("DeleteBack")
        hwp.SetPos(*start_pos)
        hwp.Run("Paste")
        #출처 삽입
        hwp.Save()
        print(f"{field_list_change_problem_number[i] + 1}번문제 반영완료! ({i + 1}번째 입력)")
        sleep(0.2)

    for i in range(problem_change_solution.shape[0]):
        problem_change_solution_set = problem_change_solution.iloc[i]
        src = array_to_problem_directory(problem_change_solution_set, grade=grade_number, test_name = test_name)
        problem_directory, src_problem_number, dst_problem_number, src_problem_score = src[0], src[1], src[2], src[3]
        print(f"{field_list_change_solution_number[i]+1}번문제 반영중...({i+1}번째 입력)")
        hwp.Open(rf'{basefile}')
        hwp.MoveToField(f"{field_list_change_solution_number[i]+1}번풀이", start = True)
        start_pos = hwp.GetPos()
        hwp.Run("Cancel")
        hwp.MoveToField(f"{field_list_change_solution_number[i]+1}번풀이", start = False)
        end_pos = hwp.GetPos()
        hwp.Run("Cancel")
        hwp.SetPos(*start_pos)
        hwp.Run("Select")
        hwp.SetPos(*end_pos)
        hwp.HAction.Run("Copy")
        hwp.HAction.Run("MoveDown")

        hwp.Open(rf"{problem_directory}")
        if os.path.exists(problem_directory) == False:
            raise Exception(f"{field_list_change_solution_number[i]+1}번문제 문제저장용 파일이 존재하지 않습니다!")
        hwp.MoveToField(f"{src[1]}번풀이")
        hwp.HAction.Run("MoveRight")
        start_pos = hwp.GetPos()
        hwp.HAction.Run("SelectAll")
        hwp.HAction.Run("MoveRight")
        end_pos = hwp.GetPos()
        hwp.SetPos(*start_pos)
        hwp.Run("Select")
        hwp.SetPos(*end_pos)
        hwp.Run("DeleteBack")
        hwp.SetPos(*start_pos)
        hwp.Run("Paste")
        hwp.Save()
        print(f"{field_list_change_solution_number[i] + 1}번문제 반영완료! ({i + 1}번째 입력)")
        sleep(0.2)

    end_time = dt.now()
    elapsed_time = end_time - start_time
    print(f'입력을 완료하였습니다. 약 {elapsed_time.seconds}초 소요되었습니다.')

def source_reference(hwp, excel, grade_number, test_name):
    problems = get_problem_list(excel=excel, grade=grade_number, test_name=test_name)
    for j in range(problems.shape[0]):
        problem_problem_set = problems.iloc[j]
        src = array_to_problem_directory(problem_problem_set, grade=grade_number, test_name=test_name)
        problem_directory, src_problem_number, dst_problem_number, src_problem_score = src[0], src[1], src[2], src[3]
        print(f"{j + 1}번문제 출처표시중...({j + 1}번째 입력)")
        hwp.Open(rf"{src[0]}")
        hwp.MoveToField(f"{src[1]}번문제")
        hwp.HAction.Run("SelectAll")
        hwp.HAction.Run("MoveRight")
        hwp.HAction.Run("BreakPara")
        hwp.HAction.GetDefault("InsertText", hwp.HParameterSet.HInsertText.HSet)
        hwp.HParameterSet.HInsertText.Text = test_name
        hwp.HAction.Execute("InsertText", hwp.HParameterSet.HInsertText.HSet)
        hwp.HAction.Run("StyleShortcut6")
        hwp.Save()
        print(f"{j + 1}번문제 출처표시완료! ({j + 1}번째 입력)")

if __name__ == "__main__":
    excelfile_directory = os.getcwd() + r'\태풍\내신주문서.xlsx'