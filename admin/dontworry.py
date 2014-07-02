__author__ = 'mkaplenko'


def dump(object):
    for item in object.__dict__:
        print(item, ' ==> ', object.__dict__[item])
    print('===================================')