import cv2 as cv
import numpy as np
import pandas as pd


def pic2dots(data):
    row, _ = data.shape
    final = []
    b = data[0]
    for i in range(row):  # 每一行
        # convert = {{1: (0, 0)}, {2: (1, 0)}, {3: (2, 0)}, {4: {(0, 1)}}, {5: (1, 1)}, {6: (2, 1)}, {7: (0, 3)}, {8: (1,
        # 3)}}
        res = []  # 单行
        a = b[i]
        a = [item for item in a]
        col = len(a)
        for j in range(col):  # 每一列
            string = str(bin(ord(a[j]) - 10240))[2:]
            pos = np.zeros((4, 2))
            for index in range(len(string)):  # 图元转化
                if string[index] == '1':
                    if index < 7:
                        pos[index % 4, int(index / 4)] = 1
                    else:
                        pos[3, 1 if index % 4 == 0 else 0] = 1
            res.append(list(pos))
            fin = np.array(res[0])
        for martix in range(1, len(res)):  # 数组贴合
            m = np.array(res[martix])
            fin = np.concatenate((fin, m), axis=1)
        final.append(fin)  # 存储行
    res = np.array(final[0])
    for Rm in range(1, len(final)):
        m = np.array(final[Rm])
        res = np.concatenate((res, m), axis=0)  # 把每行的图像贴合
    row, col = res.shape
    for i in range(row):  # 重新二值化图像
        for j in range(col):
            if res[i][j] == 1:
                res[i][j] = 255
    return res


path = r'E:\新建文件夹\dots-painter\2b.txt'
if __name__ == '__main__':
    data = pd.read_table(path, header=None, encoding='utf-8')
    res = pic2dots(data)
    cv.imshow('result', res)
    cv.waitKey()
