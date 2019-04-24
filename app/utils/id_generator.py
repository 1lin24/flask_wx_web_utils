from datetime import datetime
import base64
import hashlib

def mix_code(code, mix_numbers):
    current_idx = 0
    max_idx = len(code) - 1
    for idx in mix_numbers:
        current_idx += int(idx)
        current_idx %= max_idx
        letter = code[current_idx]
        code1 = code[:current_idx]
        code2 = code[current_idx+1:]
        code = letter + code1 + code2
    return code

def hash_code(code):
    md5 = hashlib.md5()
    md5.update(code.encode('utf-8'))
    return md5.hexdigest()

def base64_code(code):
    bs = code.encode('utf-8')
    en64 = base64.b64encode(bs)
    res = en64.decode('utf-8').replace('=','')
    return res

def generate_id(salt='salt'):
    time_stamp = datetime.now().timestamp()
    time_item = str(time_stamp).split('.')
    time_head = time_item[0]
    time_tail = '{:2<6}'.format(time_item[1])

    salty_time = '{}{}{}'.format(time_head, salt, time_tail)
    code = hash_code(salty_time)
    code = mix_code(code, time_tail)
    code = code[-10:]
    return code

if __name__ == '__main__':
    count = 10
    while count:
        count -=1
        code = generate_id('salt1231231231')
