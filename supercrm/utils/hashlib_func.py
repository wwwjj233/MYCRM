import hashlib

def mymd5(values):
    """
    md5加密
    :param values: 需要被加密的字符串
    :return:
    """
    secret_key='username'.encode('utf-8')
    md5_value=hashlib.md5(secret_key)
    md5_value.update(values.encode('utf-8'))
    return md5_value.hexdigest()