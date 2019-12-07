# -*- coding:utf-8 -*-

import os


def read_data(root):
    file_name_list = []
    for i in os.listdir(root):
        if i[-4:] == '.txt':
            file_name_list.append(i)
    scence_para_list = []
    cover_rate_list = []
    for file_name in file_name_list:
        f = open(root+file_name)
        data = f.read()
        f.close()
        data = data.split('\n')
        scence_para = eval(data[0])
        cover_rate = []
        for tmp in range(1, len(data)):
            if data[tmp]:
                cover_rate.append(eval(data[tmp])[1])
        scence_para_list.append(scence_para)
        cover_rate_list.append(cover_rate)
    return (scence_para_list, cover_rate_list)





if __name__ == '__main__':

    root = './record/'

    scence_para_list, cover_rate_list = read_data(root)

    # index = []
    # for idx, i in enumerate(scence_para_list):
    #     if (i['w1'] in [0.02, 0.2])and (i['w2'] == 20):
    #         index.append(idx)


    print('debug')
