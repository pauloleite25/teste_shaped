import secrets
import string


def generate_link_hask():
    length = 20
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(length))
    return token
