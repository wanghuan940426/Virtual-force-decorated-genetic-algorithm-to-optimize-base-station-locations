# -*- coding:utf-8 -*-

class record:

    def __init__(self, file_path_name):
        self.f = open(file_path_name, 'w')

    def close_file(self):
        self.f.close()

    def write_scence_para(self, para_dict):
        self.f.write(str(para_dict)+'\n')

    def write_cover_rate(self, para_list):
        self.f.write(str(para_list) + '\n')

    def my_flush(self):
        self.f.flush()