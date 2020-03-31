import cv2
import numpy as np
from array import array
from PIL import ImageGrab


        
class ImgUtils():

    encryptPath = "./cache/encypt.bmp"  # 加密后的图片
    decryptPath = "./cache/decrypt.bmp" # 解密后的图片


    # 图片秘钥
    def getImgKey(self, width, height, deep):
        key = 'greewqnmlgbdctmd'  # key 字符串
        charStr = [0] * len(key)  # 新建key对应的数组字符串
        for i in range(0, len(key)):
            charStr[i] = ord(key[i])

       
        # 2.创建秘钥文件 -----------自定义key方法----------------
        # ------------算法是将秘钥数组，轮流赋值到每一个像素点mark中--------
        # ------------赋值的同时，要处理一下数值--------------------------
        img = np.ones((width, height, deep))  # 新建三维数组，且初始值为1

        img_key = np.array(img, dtype='uint8') # 转为uint8格式
        index = 0  
        for i in range(0, width):
            for j in range(0, height):
                for k in range(0, deep):
                    if index % 3 == 0:
                        img_key[i, j, k] = charStr[index % len(charStr)] * (j + 1) - i * 100
                    else:
                        img_key[i,j,k]=charStr[index % len(charStr)] /  ( j + 1 ) + 100 * i
                    index+=1
        # print(img_key) # 打印key
        return img_key


    # 加密图片的路径
    # fromPath -- 图片源路径
    # toPath -- 图片输出路径
    def imgEncrypt(self,fromPath,toPath):
        encryptPath = "./cache/encypt.bmp"  # 加密后的图片


        if toPath == '':
            toPath = "./cache/in.bmp"
        img_src = cv2.imread(fromPath)
        width,height,deep = img_src.shape
        img_key = self.getImgKey(width, height, deep)
        img_encrypted = cv2.bitwise_xor(img_src, img_key)
        cv2.imwrite(toPath, img_encrypted, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        return img_encrypted


    # 解密图片的 
    # fromPath -- 图片源路径
    # toPath -- 图片输出路径
    def imgDecrypt(self,fromPath,toPath):
        decryptPath = "./cache/decrypt.bmp" # 解密后的图片
        if toPath == '':
            toPath = "./cache/out.bmp" # 默认输出为out.bmp
        img_encrypted = cv2.imread(fromPath)
        width, height, deep = img_encrypted.shape
        img_key = self.getImgKey( width, height, deep)
        img_decrypt = cv2.bitwise_xor(img_encrypted, img_key)
        cv2.imwrite(toPath, img_decrypt, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        return img_decrypt

