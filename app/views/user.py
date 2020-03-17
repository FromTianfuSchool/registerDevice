"""
@author: Giraffe
@Contact :   gental_j@163.com
@time    :   2020/3/9 14:40:23
@file    :   user.py
@desc    :   
"""

# from flask import Blueprint
from collections import namedtuple


# user = Blueprint('user', __name__)


class UserManager(list):
    """
    对set add方法重写,
    """

    def __init__(self, *args):
        super(list, self).__init__()
        self.user_info_name = args[0]
        self.UserInfo = namedtuple('UserInfo', args[0])

    def append(self, item_dict):
        """
        新增家数据时，判断是否已经存在对应的user，如果存在就更新
        """
        if not isinstance(item_dict, dict):
            raise TypeError("append error, need dict type")
        _name_tuple = self.UserInfo(**item_dict)

        if _name_tuple.username in self:
            self.remove(_name_tuple.username)
            print('removed', _name_tuple.username)
        # print(_name_tuple.username)
        super(UserManager, self).append(_name_tuple)

    def __contains__(self, username):
        _temp = self.copy()
        while 1:
            try:
                exists = _temp.pop(0)
                if username == exists.username:
                    return True
            except IndexError:
                return False

    def remove(self, username):
        return super(UserManager, self).remove(self.__getitem__(username))

    def __getitem__(self, username):
        return super(UserManager, self).__getitem__(self.index(username))

    def index(self, username):
        if username not in self:
            raise IndexError("item not in object")
            # return True
        for exists in self:
            if username == exists.username:
                return super(UserManager, self).index(exists)
