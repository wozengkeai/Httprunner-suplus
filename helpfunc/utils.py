# -*- coding: utf-8 -*-
# @Time : 2021/8/25 10:22
# @Author : zengxiaoyan
# @File : utils.py
import logging
import os

file = __file__
def mkdir(dir_path):
    """ 创建路径
    """
    # 去除首位空格
    _dir = dir_path.strip()
    _dir = dir_path.rstrip("\\")
    _dir = dir_path.rstrip("/")

    # 判断路径是否存在
    is_exists = os.path.exists(_dir)

    if not is_exists:
        try:
            os.makedirs(_dir)
        except Exception as e:
            logging.error("Directory creation failed：%s" % e)
    else:
        # 如果目录存在则不创建，并提示目录已存在
        logging.debug("Directory already exists：%s" % str(_dir))


def create_file(file_path, content):
    """ 当文件存在时，则不再创建和覆盖
    """
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        logging.info("{} is exists!".format(file_path))


if __name__ == '__main__':

    pass