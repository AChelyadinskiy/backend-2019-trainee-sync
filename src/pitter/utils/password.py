from hashlib import sha1


def gen_password(password: str, salt: str) -> str:
    """
    Шифрует пароль с солью
    :param password: Пароль
    :param salt: Соль
    :return:
    """
    hashed_password = sha1((password + salt).encode()).hexdigest()
    return '%s$%s' % (salt, hashed_password)


def check_password(raw_password: str, enc_password: str) -> bool:
    """
    Проверяет достоверность пароля
    :param raw_password: Пароль
    :param enc_password: Зашифрованный пароль
    :return:
    """
    salt, hsh = enc_password.split('$')
    return hsh == sha1((raw_password + salt).encode()).hexdigest()
