import uuid

from commons.constants import UUID_DIGIT_STARTS_SENSITIVE


def uniqid():
    return uuid.uuid3(uuid.uuid1(), uuid.uuid4().hex).hex


def node_uniqid():
    uid = uniqid()
    return "n%s" % uid[1:] if UUID_DIGIT_STARTS_SENSITIVE else uid


def line_uniqid():
    uid = uniqid()
    return "l%s" % uid[1:] if UUID_DIGIT_STARTS_SENSITIVE else uid
