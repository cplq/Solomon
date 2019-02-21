# -*- coding: utf-8 -*-
# @Time    : 2018/12/3 下午3:09
# @Author  : ChenPeng
# @Desc : ==============================================
# 用基本的solomon benchmark instances generate EVRPTW 的实例信息
# ======================================================
# @Project : solomon
# @FileName: EVRPTW.py
# @Software: PyCharm
import numpy as np
import pandas as pd
import os
import re
import random


class ProcessSolomon:
    def __init__(self):
        pass

    def EVRPTW(self):
        '''
        用于构造EVRPTW的实例,分别用六类数据进行生成。
        类型：顾客数量5；充电站的个数[3,4,5]
             顾客数量15；充电站的个数[3,4,5]
             顾客数量20；充电站的个数[3,4,5]
        :return:
        '''
        pattern = re.compile(r"\d+\.?\d*", re.MULTILINE)
        type_pattern = re.compile('\.')
        # 获得当前数据的文件夹
        current_path = '/Users/chenpeng/PycharmProjects/Solomon/data/in/solomon/25'
        # getting all filenames in the current path
        fileNames = os.listdir(current_path)
        # 对每一个文件进行操作
        for fn in fileNames:
            file_path = current_path + '/' + fn
            # getting type of data
            data_type = type_pattern.split(fn)[0]
            # read data from file
            lines = []
            with open(file_path, 'r') as rf:
                lines = rf.readlines()
                # 遍历数据，将数据进行格式化保存
                infos = []
                for i in range(9, lines.__len__() - 1):
                    inf = pattern.findall(lines[i])
                    infos.append([int(j) for j in inf])
                # 采用pandas进行数据处理与存储
                column = ["ID", "X", "Y", "pack_total_weight", "first_receive_tm", "last_receive_tm", "SERVICE"]
                # data information
                Data = pd.DataFrame(infos, columns=column)
                # insert of column name 'type' repretation node style
                lineNum = len(infos)
                type = [1] + [2] * (lineNum - 1)
                Data["type"] = type
                # the number of node
                node_num = Data.shape[0]
                # except the index of depot
                node_size = range(1, node_num)
                # the number of customers
                for n in [5]:
                    # the number of stations
                    for m in range(3, 6):
                        # the number instance
                        for k in range(3):
                            # 随机选择m个点做充电站
                            ran_m = random.sample(node_size, m)
                            # 除去充电站点，随机选择n个点做顾客点
                            total_node_cus = list(set(node_size).difference(set(ran_m)))
                            ran_n = random.sample(total_node_cus, n)
                            # 重新构造数据集
                            new_list = [0]
                            new_list.extend(ran_n)
                            new_list.extend(ran_m)
                            # 将行选择出来
                            new_data = Data.iloc[new_list, :]
                            # 修改station的类型
                            new_data.ix[ran_m, "type"] = 3
                            # 修改新数据集的索引，修改IP
                            ids = range(len(new_list))
                            new_data["ID"] = ids
                            new_data.index = pd.Series(ids)

                            # 修改充电站的时间信息
                            new_data.loc[new_data["type"] == 3,"first_receive_tm"]=new_data.ix[0, "first_receive_tm"]
                            new_data.loc[new_data["type"] == 3, "last_receive_tm"] = new_data.ix[0, "last_receive_tm"]
                            new_data.loc[new_data["type"] == 3, "SERVICE"] = new_data.ix[0, "SERVICE"]

                            # 求距离
                            length = new_data.shape[0];
                            distance = np.zeros((length, length))
                            for i in range(length):
                                a_x = new_data.ix[i, "X"]
                                a_y = new_data.ix[i, "Y"]
                                for j in range(i, length):
                                    b_x = new_data.ix[j, "X"]
                                    b_y = new_data.ix[j, "Y"]
                                    # check data is illegal
                                    if (a_x == None or a_y == None or b_x == None or b_y == None):
                                        print("illegal data exists")
                                    distance[i, j] = np.square(a_x - b_x) + np.square(a_y - b_y)
                            distance = np.sqrt(distance)
                            distance = np.around(distance, decimals=2)
                            for i in range(length):
                                for j in range(i, length):
                                    distance[j, i] = distance[i, j]

                            # 进行保存
                            lines = "from_node,to_node,distance,speed_tm" + "\n"
                            for i in range(length):
                                for j in range(length):
                                    lines += str(i) + "," + str(j) + "," + str(distance[i, j]) + "," + str(
                                        distance[i, j]) + "\n"
                            name = data_type + "-C{0}F{1}_{2}".format(n, m, k)
                            new_column = ['ID', 'type', 'X', 'Y', 'pack_total_weight', 'first_receive_tm',
                                          'last_receive_tm', 'SERVICE']
                            new_data = new_data.reindex(columns=new_column)
                            # 写入文件
                            writePath = '/Users/chenpeng/PycharmProjects/Solomon/data/out/withTimeSame_5/' + name + "-DT" + ".csv";

                            with open(writePath, 'w') as wf:
                                wf.write(lines)
                            writePath = '/Users/chenpeng/PycharmProjects/Solomon/data/out/withTimeSame_5/' + name + "-Node" + ".csv";
                            new_data.to_csv(writePath, index=False)
                            print("转换完成")


if __name__ == '__main__':
    # 建立对象
    solomon = ProcessSolomon()
    solomon.EVRPTW();
