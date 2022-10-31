from tkinter import *
import tkinter.font as TKfont
from tkinter.messagebox import Message 
from _tkinter import TclError
from functools import partial
import datetime
import pyautogui
import time
import os


class timeFrame:
    hourF = 0
    minuteF = 0
    hourT = 0
    minuteT = 0
    mS = 0
    mD = 0
    mI = 0
    def __init__(self):
        return None

# Hàm giải mã mật khẩu trong file.
def readPassword(filein):
    e = int(filein.readline())
    m = filein.readline()
    n = len(m)
    result = ""
    for i in range(n):
        result += chr(ord(m[i]) - e)
    return result

# Hàm đọc file để lấy mật khẩu phụ huynh và trẻ em ra.
def get_password():
    file1 = open("C:/Users/Admin/OneDrive/data/Children_password.txt",'r')
    file2 = open("C:/Users/Admin/OneDrive/data/Parent_password.txt",'r')

    Children=readPassword(file1)

    Parent=readPassword(file2)

    file1.close()
    file2.close()
    return Parent,Children

# Hàm đọc file lưu thời gian.
def readTimeframeFile():
    filein = open("C:/Users/Admin/OneDrive/data/Time.txt",'r')
    result = []
    while True:
        data = filein.readline()
        if data == "":
            break
        n = len(data)
        t = timeFrame()
        for i in range(n):
            if data[i] == 'F':
                t.hourF = int(data[i + 1]) * 10 + int(data[i + 2])
                t.minuteF = int(data[i + 4]) * 10 + int(data[i + 5])
            elif data[i] == 'T':
                t.hourT = int(data[i + 1]) * 10 + int(data[i + 2])
                t.minuteT = int(data[i + 4]) * 10 + int(data[i + 5])
            elif data[i] == 'S':
                j = i + 1
                while (data[j] >= '0' and data[j] <= '9'):
                    t.mS = int(data[j]) + t.mS * 10
                    j += 1
            elif data[i] == 'D':
                j = i + 1
                while (data[j] >= '0' and data[j] <= '9'):
                    t.mD = int(data[j]) + t.mD * 10
                    j += 1
            elif data[i] == 'I':
                j = i + 1
                while (data[j] >= '0' and data[j] <= '9'):
                    t.mI = int(data[j]) + t.mI * 10
                    j += 1
        result.append(t)
    filein.close()
    return result

# Hàm so sách 2 mốc thời gian A và B theo giờ và phút xem A có lớn hơn hoặc bằng B không.
# Nếu có trả về 1, nếu không trả về 0.
def compare(A_hour,A_minute,B_hour,B_minute):
    if A_hour > B_hour:
        return 1
    elif A_hour == B_hour:
        if A_minute >= B_minute:
            return 1
        else:
            return 0
    else:
        return 0


# Kiểm tra thời gian hiện tại có trong khung giờ được sử dụng máy không.
# Nếu hiện tại có thuộc 1 khung giờ trong file Time thì trả về id của khung giờ đó .
# Nếu hiện tại không thuộc một khung giờ nào hết thì trả về thời gian gần nhất được phép dùng máy.
def Check(Time_list):
    hour_to_start = 0
    minute_to_start = 0
    result = 0
    dt = datetime.datetime.now()

    # Time_list là một list lưu các khoản thời gian được phép sử dụng máy.
    for i in range(len(Time_list)):
        temp = 0
        # Nếu thời gian hiện tại lớn hơn thời gian bắt đầu cho temp=1.
        if compare(dt.hour,dt.minute,Time_list[i].hourF,Time_list[i].minuteF) == 1:
            temp = 1

        # Ngược lại thì thời gian hiện tại ko nằm trong khoản được dùng máy.
        # Tiến hành xét và lưu thời điểm bắt đầu của khoản, để có thể xuất ra thời gian có thể sử dụng.
        else:
            if hour_to_start == 0 and minute_to_start == 0:
                hour_to_start = Time_list[i].hourF
                minute_to_start = Time_list[i].minuteF
            elif compare(hour_to_start,minute_to_start,Time_list[i].hourF,Time_list[i].minuteF) == 1:
                hour_to_start = Time_list[i].hourF
                minute_to_start = Time_list[i].minuteF

        # Nếu temp = 1 có nghĩa thời gian hiện tại lớn hơn thời điểm bắt đầu.
        # Tiếp tục xét có nhỏ hơn thời gian kết thúc không để quyết định có cho sử dụng hay không.
        if temp == 1:
            if compare(dt.hour,dt.minute,Time_list[i].hourT,Time_list[i].minuteT) == 0:
                temp = 1
            else:
                temp = 0
        
        # nếu thời gian hiện tại được sử dụng thì trả về.
        if temp == 1:
            result = i
            break
    # Nếu không trong thời gian được sử dụng thì trả về list gồm giờ và phút thể hiện đến khi nào mới được sử dụng.
    if temp == 0:
        result = [hour_to_start,minute_to_start]

    return result

# Hàm hiện messagebox và cài cho messagebox tự tắt trong thời gian nhất định.
def Show_messagebox(mess):
    TIME_TO_WAIT = 3000 # in milliseconds 
    root = Tk() 
    root.withdraw()
    try:
        root.after(TIME_TO_WAIT, root.destroy) 
        Message(title="Thông báo", message=mess, master=root).show()
    except TclError:
        pass


# Hàm kiểm tra xem mật khẩu đươc nhập có khớp với phụ huynh hoặc trẻ em không.
def Password(State):
    password = E.get()

    # Nếu trước đó chưa nhập mật khẩu nào hết (lần đầu yêu cầu nhập).
    if State[0] == 0 or State[0] == 1:
        
        # Nhập đúng mật khẩu phụ huynh.
        if Parent == password:

            # Dừng tắt máy
            os.system(f"shutdown -a")

            W.withdraw()
            W.quit()
            mess='Nhập thành công mật khẩu phụ huynh!!!'
            Show_messagebox(mess)
            State[0]=1

        # Nhập đúng mật khẩu trẻ.
        elif Children == password:

            # Dừng tắt máy
            os.system(f"shutdown -a")

            State[0]=2

            # Kiểm tra xem có trong thời gian trẻ được sử dụng không.
            Time_list = readTimeframeFile()
            temp = Check(Time_list)

            # Nếu không nằm trong thời gian được sử dụng.
            if type(temp) != int:
                E.delete(0,'end')

                os.system(f"shutdown -s -t 15 -f")

                # Hiện thông báo đến khi nào mới được dùng hoặc đã hết thời gian sử dụng.
                if temp[0] == 0 and temp [1] == 0:
                    mess='Hôm nay đã hết thời gian sử dụng.'
                    Show_messagebox(mess)
                else:
                    mess='Đến '+ str(temp[0]) +' giờ '+ str(temp[1]) +' phút mới được sử dụng.'
                    Show_messagebox(mess)

                # Cho chạy lại hàm để yêu cầu nhập mật khẩu phụ huynh.
                Password(State)
            
            else:
                W.destroy()
        elif password != '':
            L3.configure(text = 'Nhập sai mật khẩu!!!')

    # Nếu trước đó đã nhập mật khẩu trẻ em và sau kiểm tra thấy không trong thời gian được dùng.
    elif State[0] == 2:
        L3.configure(text = '')
        L2.configure(text = "Trong 15 giây nếu như không nhập đúng\n mật khẩu phụ huynh máy sẽ tắt!!!")

        # Nhập đúng mật khẩu phụ huynh.
        if Parent == password:
            # dừng tắt máy.
            os.system(f"shutdown -a")

            L2.configure(text = "  Trong 30 giây nếu như không nhập \n  đúng mật khẩu máy sẽ tắt!!!")
            W.withdraw()
            W.quit()
            mess='Nhập thành công mật khẩu phụ huynh!!!'
            Show_messagebox(mess)
            State[0]=1
        elif password != '':
            L3.configure(text = 'Nhập sai mật khẩu!!!')

def Password_display():
    os.system(f"shutdown -s -t 30 -f")
    W.mainloop()

# Vòng lặp khi phụ huynh sử dụng
def Parent_loop():
    while True:
        # Kiểm tra mỗi 60p
        time.sleep(3600)
        L3.configure(text = '')
        E.delete(0,'end')
        W.deiconify()

        # Sau mỗi 60p sẽ yêu cầu nhập lại mật khẩu.
        Password_display()

# Hàm tính ra số phút còn lại khi truyền vào 2 mốc thời gian.
def Time_left(Time,dt):
    h = Time.hourT - dt.hour
    m = Time.minuteT - dt.minute
    return h * 60 + m

# Hàm hiện thông báo cho trẻ em.
# Tính toán và hiện lên số phút còn lại đến khi máy tắt và đến khi nào mới mở lên được.
def Notification(Time_list,id,dt):
    temp = Time_left(Time_list[id],dt)

    hour_to_start = 0
    minute_to_start = 0
    for i in range(len(Time_list)):
        if compare(dt.hour,dt.minute,Time_list[i].hourF,Time_list[i].minuteF) == 0:
            if hour_to_start == 0 and minute_to_start == 0:
                hour_to_start = Time_list[i].hourF
                minute_to_start = Time_list[i].minuteF
            elif compare(hour_to_start,minute_to_start,Time_list[i].hourF,Time_list[i].minuteF) == 1:
                hour_to_start = Time_list[i].hourF
                minute_to_start = Time_list[i].minuteF
    temp = str(temp)

    if hour_to_start == 0 and minute_to_start == 0:
        mess='Còn '+ temp+' phút nữa máy sẽ tắt. Hôm nay đã hết thời gian sử dụng'
        Show_messagebox(mess)
    else:
        hour_to_start =str(hour_to_start)
        minute_to_start = str(minute_to_start)
        mess='Còn '+ temp+' phút nữa máy sẽ tắt. Và đến ' + hour_to_start + ' giờ '+ minute_to_start +' phút mới được mở lại.'
        Show_messagebox(mess)

# Hàm chụp màng hình.
def Screenshot(dt):
    a = 'C:/Users/Admin/OneDrive/data/screenshot/'
    b = '.png'
    c = a + str(dt.hour) +'h'+ str(dt.minute)+'m' + b
    myScreenshot = pyautogui.screenshot(c)

# Vòng lặp khi trẻ em sử dụng.
def Children_loop():

    # Hiện thông báo đầu khi trẻ vừa nhập mật khẩu thành công
    Time_list = readTimeframeFile()
    id = Check(Time_list)
    dt = datetime.datetime.now()
    Notification(Time_list,id,dt)
    change_time = os.stat("C:/Users/Admin/OneDrive/data/Time.txt").st_mtime
    k=0

    while True:
        # Thực hiện kiểm tra và chụp màng hình sau mỗi 1p.
        time.sleep(59) # 1 giây trừ hao cho chương trình chạy và hiện thông báo.
        k+=1
        print(k)
        dt = datetime.datetime.now()
        temp = Time_left(Time_list[id],dt)

        # Chụp màng hình.
        Screenshot(dt)

        # Kiểm tra xem có sự thay đổi j của phụ huynh hay không.
        temp2=os.stat("C:/Users/Admin/OneDrive/data/Time.txt").st_mtime
        if change_time != temp2:
            change_time = temp2
            Time_list = readTimeframeFile()

            temp = Check(Time_list)

            # Nếu không nằm trong thời gian sử dụng thì tắt máy
            if type(temp) != int:
                os.system(f"shutdown -s -t 15 -f")

                if temp[0] == 0 and temp [1] == 0:
                    mess='Hôm nay đã hết thời gian sử dụng.'
                    Show_messagebox(mess)
                else:
                    mess='Đến '+ str(temp[0]) +' giờ '+ str(temp[1]) +' phút mới được sử dụng.'
                    Show_messagebox(mess)
            else:
                Notification(Time_list,id,dt)

        else:
            # nếu còn 1 phút gọi thông báo.
            if temp == 1:
                Notification(Time_list,id,dt)
            if temp == 0 or temp < 0:
                os.system(f"shutdown -s -t 0 -f")

# State để lưu trang thái hiện tại của chương trình.
# State[0]=0 (Chưa nhập mât khẩu nào hết).
# State[0]=1 (Đã nhập mật khẩu phụ huynh).
# State[0]=2 (Đã nhập mật khẩu phụ huynh).
State = [0]
Parent,Children=get_password()

#---------------------------------
# giao diện nhập mật khẩu .
W = Tk()
W.geometry('500x400')
fonstyle = TKfont.Font(family='arial',size=15)
W.title("Kiểm tra mật khẩu")

L1 = Label(W,text = 'Nhập mật khẩu: ',font = fonstyle)
L1.place(x=140,y=100)

L2 = Label(W,text = '   Trong 30 giây nếu như không nhập \n  đúng mật khẩu máy sẽ tắt!!!',font = fonstyle)
L2.place(x=25,y=30)

L3 = Label(W,text = '',font = fonstyle)
L3.place(x=120,y=280)

E=Entry(master=W,font=fonstyle,width=20,show='*')
E.place(x=100,y=150)

B = Button(master=W,text='ĐỒNG Ý',width=13,height=2,fg='white',bg='blue',command=partial(Password,State))
B.place(x=180,y=210)
#---------------------------------

Password_display()

if State[0]==1:
    Parent_loop()
else:
    Children_loop()
