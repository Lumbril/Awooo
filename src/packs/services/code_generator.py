import random


def generate_code():
    rnd = random.SystemRandom()

    code = ''.join(list(str(rnd.randint(1000000, 9999999)))[1:])

    return code
