import cv2 as cv
import numpy as np


def custom_threshold(image):
    gray = image
    h, w = gray.shape[:2]  # 求宽高
    m = np.reshape(gray, [1, w * h])  # 将图像转一维数组，一行，w*h列，转换维度要保证其size不变
    mean = m.sum() / (w * h)  # 求平均值来当做阈值，来分割图像
    print("mean :", mean)
    ret, binary = cv.threshold(gray, mean, 255, cv.THRESH_BINARY)
    return binary


def outputer(img, size):
    weights = np.array([[1, 8], [2, 16], [4, 32], [64, 128]])
    x, y = img.shape
    if (x / 4 if x % 4 == 0 else x / 4 + 1, y / 2 + y % 2) > size:  # 处理图片到达要求
        tarX, tarY = size
        Xscale = tarX * 4 / x
        Yscale = tarY * 2 / y
        img = cv.resize(img, None, fx=Xscale, fy=Yscale)
    x, y = img.shape
    xres = x % 4
    yres = y % 2
    if xres != 0:
        for i in range(4 - xres):
            img = np.concatenate((img, np.array([0 for j in range(y)])), axis=0)
    x, y = img.shape
    if yres != 0:
        for i in range(2 - yres):
            img = np.concatenate((img, np.array([0 for j in range(x)])), axis=1)
    x, y = img.shape
    res = []
    for i in range(int(x / 4)):  # every column
        tmp = []
        for j in range(int(y / 2)):  # every row
            a = img[j * 2:j * 2 + 2, i * 4:i * 4 + 4]
            val = np.vdot(img[j * 2:j * 2 + 2, i * 4:i * 4 + 4], weights)
            tmp.append(val)
        res.append(tmp)
    fin = []
    for i in range(int(x / 4)):
        tmp = ''
        for j in range(int(y / 2)):
            tmp = tmp + chr(10240 + res[i][j])
        fin.append(tmp)
    return fin


path = r'OIP.jpg'
if __name__ == '__main__':
    img = cv.imread(path)
    imGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imGray = cv.adaptiveThreshold(imGray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
    # imGray=custom_threshold(imGray)
    Xori, Yori = imGray.shape
    center = (Xori // 2, Yori // 2)
    martix = cv.getRotationMatrix2D(center, 90, 1)
    imGray = cv.warpAffine(imGray, martix, (Xori, Yori))
    for i in range(Xori):
        for j in range(Yori):
            if imGray[i, j] > 0:
                imGray[i, j] = 1
    oriSize = imGray.size
    # TODO:adding some picture compassing argiorim
    string = input("输入想要的字符画大小：(eg:长*宽)")
    x, y = [int(i) for i in string.split('*')]
    b = outputer(imGray, (x, y))
    for i in b:
        print(i)
