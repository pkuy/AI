# Class chưa thông tin của khung thời gian
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

#Hàm đọc file time
def readTimeframeFile(filein):
    data = filein.read()
    return data

#Hàm nhập khung giờ
def inputTimeframe():
    print("Enter amount of timeFrame: ")
    amount = int(input())
    result = []
    for i in range(amount):
        print("Times: ",i+1)
        t = timeFrame()
        print("Enter hour from: ")
        t.hourF = int(input())
        print("Enter minute from: ")
        t.minuteF = int(input())
        print("Enter hour to: ")
        t.hourT = int(input())
        print("Enter minute to: ")
        t.minuteT = int(input())
        print("Enter duration: ")
        t.mD = int(input())
        print("Enter interrupt_time: ")
        t.mI = int(input())
        print("Enter sum: ")
        t.mS = int(input())
        result.append(t)
    return result

#Hàm thay đổi khung giờ
def changeTimeframe(result,fileout):
    for i in range(len(result)):
        fileout.write("F")
        s = str(result[i].hourF)
        if len(s) == 1:
            s = "0" + s
        fileout.write(s + ":")
        s = str(result[i].minuteF)
        if len(s) == 1:
            s = "0" + s
        fileout.write(s + " T")
        s = str(result[i].hourT)
        if len(s) == 1:
            s = "0" + s
        fileout.write(s + ":")
        s = str(result[i].minuteT)
        if len(s) == 1:
            s = "0" + s
        fileout.write(s)
        if result[i].mD > 0:
            fileout.write(" D" + str(result[i].mD))
        if result[i].mI > 0:
            fileout.write(" I" + str(result[i].mI))
        if result[i].mS > 0:
            fileout.write(" S" + str(result[i].mS))
        fileout.write("\n")

# Hàm tạo pass mặc định 123456
def createDefaultPassword(fileout):
    fileout.write('3\n')
    fileout.write("456789")

# Hàm mã hóa pass. 
def EncryptPassword(e: int, m): # e là key, m là password cần mã hóa
    n = len(m)
    result = ""
    for i in range(n):
        result += chr(ord(m[i])+ e)
    return result

#Hàm đọc password
def readPassword(filein):
    e = int(filein.readline())
    m = filein.readline()
    n = len(m)
    result = ""
    for i in range(n):
        result += chr(ord(m[i]) - e)
    return result


# filein = open(r'C:\Users\ASUS\OneDrive\data\time.txt')
# result = readFile(filein)
# Hàm thay đổi password
def changePassword(fileout):
    count = 0
    while(count < 3):
        print("Enter new password: ")
        password = input()
        print("Reenter new password: ")
        password1 = input()
        if password == password1:
            fileout.write("3\n")
            password = EncryptPassword(3, password)
            print("success")
            fileout.write(password)
            break
        else:
            print('error')
            count += 1
    if count == 3:
        print("failed")
        createDefaultPassword(fileout)



#Hàm main
def main():
    #Tạo pass mặc định khi chưa có pass
    filein = open(r'C:\Users\Admin\OneDrive\data\Parent_password.txt')
    data = filein.read()
    if data =="":
        filein.close()
        fileout = open(r'C:\Users\Admin\OneDrive\data\Parent_password.txt', 'w')
        createDefaultPassword(fileout)
        fileout.close()
    else :
        filein.close()

    filein = open(r'C:\Users\Admin\OneDrive\data\Children_password.txt')
    data = filein.read()
    if data == "":
        filein.close()
        fileout = open(r'C:\Users\Admin\OneDrive\data\Children_password.txt', 'w')
        createDefaultPassword(fileout)
        fileout.close()
    else:
        filein.close()
    while(1):
        print("\n\nEnter 1: Read parent's password ")
        print("Enter 2: Change parent's password")
        print("Enter 3: Read children's password ")
        print("Enter 4: Change children's password")
        print("Enter 5: Read time frame")
        print("Enter 6: Change time frame")
        print("Your choose: ")
        choose = int(input())
        if choose == 1:
            filein = open(r'C:\Users\Admin\OneDrive\data\Parent_password.txt')
            result = readPassword(filein)
            print("Your password: ")
            print(result)
            filein.close()
        elif choose == 2:
            fileout = open(r'C:\Users\Admin\OneDrive\data\Parent_password.txt', 'w')
            changePassword(fileout)
            fileout.close()
        elif choose == 3:
            filein = open(r'C:\Users\Admin\OneDrive\data\Children_password.txt')
            result = readPassword(filein)
            print("Your password: ")
            print(result)
            filein.close()
        elif choose == 4:
            fileout = open(r'C:\Users\Admin\OneDrive\data\Children_password.txt', 'w')
            changePassword(fileout)
            fileout.close()
        elif choose == 5:
            filein = open(r'C:\Users\Admin\OneDrive\data\Time.txt')
            data = readTimeframeFile(filein)
            filein.close()
            print(data)
        elif choose == 6:
            result = inputTimeframe()
            if len(result) > 0:
                fileout = open(r'C:\Users\Admin\OneDrive\data\Time.txt','w')
                changeTimeframe(result,fileout)
                fileout.close()
        else:
            break
main()