#處理指令
def deal_BYTE(line: list):
    mod = line[-1][0]
    val = line[-1][2:-1]
    objCode = ''
    if (mod == 'C'):
        for i in val:
            objCode += (hex(ord(i))[2:]).upper().zfill(2)
    elif (mod == 'X'):
        objCode += val
    else:
        print('BYTE Error')

    index_add = (len(objCode)//2)
    return index_add, objCode
        
def deal_WORD(value):
    if (int(value) >= 0):
        objCode = hex(int(value)).upper()[2:].zfill(6)
    else:
        full_hex = 16777216 # hex: 1000000
        objCode = hex(full_hex + int(value))[2:].upper().zfill(6)
    index_add = (len(objCode)//2)
    return index_add, objCode

def deal_RESB(value):
    objCode = ''
    index_add = int(value)
    return index_add, objCode

def deal_RESW(value):
    objCode = ''
    index_add = (int(value) * 3)
    return index_add, objCode




#處理註解
def deal_comment(line: list) -> list:
    tmp = []
    for chunk in line:
        if chunk[0] == ".":
            break
        else:
            tmp.append(chunk)
    return tmp

#檢查start
def check_start(start: list) -> bool:
    if (start[-2] != "START"):
        return False 
    else:
        return True