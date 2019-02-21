# -*- coding: utf-8 -*-
# @Time    : 2019/1/20 下午4:32
# @Author  : ChenPeng
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# If this runs wrong,don't ask me,I don't know why;  ===
# If this runs right,thank god,and I don't know why. ===
# Maybe the answer,my friend,is blowing in the wind. ===
# ======================================================
# @Project : solomon
# @FileName: processResult.py
# @Software: PyCharm
import re
import os
import pandas as pd

# 建立模式一
patternStr = '问题类型:(\d+).问题编号：(.*?),主问题节点：(.*?),运行时间:(.*?),运行结果：(.*?),车辆类型：(型\d+数\d+)+'
pattern = re.compile(patternStr, re.DOTALL)

# 建立模式二
patternStr2 = '-C(\d+)F'
pattern2 = re.compile(patternStr2)
# os.listdir()函数得到的是仅当前路径下的文件名，不包括子目录中的文件，所有需要使用递归的方法得到全


root_path = "/Users/chenpeng/Documents/工作/Love/java/BAP-MEVRPTWMP/Instance/out"
reuslts_list1 = []
reuslts_list2 = []

# 获得所有文件
for file in os.listdir(root_path):
    file_path = os.path.join(root_path, file)
    # 如果是文件夹，则递归打开
    if (file_path.endswith(".txt")):
        if os.path.isdir(file_path):
            continue
        if os.path.isfile(file_path):
            customer_num = pattern2.findall(file)
            if (len(customer_num) != 0 and int(customer_num[0]) != 15):
                continue
            else:
                a = 1
            # 读取数据
            with open(file_path, 'r') as rf:
                readTxt = rf.read()
                results = pattern.findall(readTxt)
                # 判断是否两个问题都解决
                if len(results) < 2:
                    continue
                # 如果问题2的解要大于问题 1的解 则跳过
                if float(results[0][4]) < float(results[1][4]):
                    continue
                for r in results:
                    # 添加到list中
                    if int(r[0]) == 1:
                        reuslts_list1.append(r)
                    else:
                        reuslts_list2.append(r)

# 保存数据
columns = ['问题类型', '实例类型', '节点数', '求解时间', 'cost', 'solution']
data1 = pd.DataFrame(reuslts_list1, columns=columns)
data2 = pd.DataFrame(reuslts_list2, columns=columns)

data = data1.merge(data2, on=('实例类型'), suffixes=('_r', '_l'))

# 合并两个dataFram

# 保存数据路径
# save_path1 = '/Users/chenpeng/Documents/学习/论文写作/LateX/部分充电资料/小规模1.csv'
# save_path2 = '/Users/chenpeng/Documents/学习/论文写作/LateX/部分充电资料/小规模2.csv'
save_path3 = '/Users/chenpeng/Documents/学习/论文写作/LateX/部分充电资料/小规模合并15.csv'
data.to_csv(save_path3, index=False, encoding='UTF-8')
# data1.to_csv(save_path1, index=False, encoding='UTF-8')
# data2.to_csv(save_path2, index=False, encoding='UTF-8')
