import time
import random
import base64
import hashlib

from autotest.utils.utils import str_eval


def installment_random():
    return str(round(time.time() * 1000)) + str(random.randint(1000, 9999))


def sleep(seconds):
    time.sleep(int(seconds))


def file_base64(filename):
    with open(filename, 'rb') as fin:
        image_data = fin.read()
        base64_data = base64.b64encode(image_data)

    return base64_data.decode("UTF-8")

#       879f30c4b1641142c6192acc23cfb733

def signature(params, NewSalt="MAaFS5Zc6ZIEapnmhurNyLLFwf3xWm"):
    sign_params = params if isinstance(params, dict) else str_eval(params)

    # sign_keys = sorted(sign_params.keys())
    sort_str_list = []
    for key, values in sign_params.items():
        if isinstance(values, list):
            for i in range(len(values)):
                sort_str_list.append(key + "="+str(values[i]))
        else:
            sort_str_list.append(key+"="+str(values))
    sign_str_list = sorted(sort_str_list)
    sign_str_new = '&'.join(sign_str_list)
    
    m = hashlib.md5((sign_str_new+NewSalt).encode(encoding="utf-8"))
    return m.hexdigest()


# aa = {"a": "1111", "b": "22222", "c": [1, 3]}
#
# print(signature(aa))

