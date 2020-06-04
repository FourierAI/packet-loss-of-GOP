#!/usr/bin/env python
# encoding: utf-8

# @author: Zhipeng Ye
# @contact: Zhipeng.ye19@xjtlu.edu.cn
# @file: plot_dfr.py
# @time: 2020-06-03 11:37
# @desc:

import matplotlib.pyplot as plt

if __name__ == "__main__":

    loss_rate = [float(i * 0.0001) for i in range(1, 5)]
    file_list = ["uniform_nofec.out", "uniform_fec.out", "sgm_nofec.out", "sgm_fec.out"]
    for file_name in file_list:
        dfr_list = []
        with open(file_name) as file:
            for line in file:
                if "" is not line.strip():
                    dfr = float(line.split(' ')[4])
                    dfr_list.append(dfr)

        plt.xlabel('packet loss rate')
        plt.ylabel('Decodable Frame Rate (Q)')
        plt.title(file_name)
        plt.legend()
        plt.plot(loss_rate, dfr_list, label=file_name)
        plt.savefig(file_name.split('.')[-2]+'.jpg')
        plt.show()
