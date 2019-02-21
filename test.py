# -*- coding: utf-8 -*-
# @Time    : 2018/12/21 下午4:07
# @Author  : ChenPeng
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# If this runs wrong,don't ask me,I don't know why;  ===
# If this runs right,thank god,and I don't know why. ===
# Maybe the answer,my friend,is blowing in the wind. ===
# ======================================================
# @Project : solomon
# @FileName: test.py
# @Software: PyCharm


import re
string='C101.tex'
pattern=re.compile(r'\.')
name=pattern.split(string)[0]
a=1