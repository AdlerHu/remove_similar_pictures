import cv2
import numpy as np


def calculate_hamming_distance(hash1, hash2):
    """
    計算兩個哈希值的漢明距離

    參數:
        hash1 (str): 第一張圖片處理後的哈希值
        hash2 (str): 第二張圖片處理後的哈希值

    返回:
        漢明距離(int)，範圍在 0 ~ 64 ，越小兩張圖越相似
    """
    # 算法中1、0順序組合起來的即是圖片的指紋hash。順序不固定，但是比較時必須是相同的順序
    # 對比兩張圖的指紋計算漢明距離，即兩個64位的hash值有多少是不一樣的，不同的位數越小，圖片越相似
    # 漢明距離:一組二進制數據變成另一組所需要的步驟，可以衡量兩圖的差異，漢明距離越小，相似度越高。漢明距離為0，兩張圖完全一樣
    hamming_distance = 0
    # 兩個哈希值長度不同則返回 -1，代表傳參出錯
    if len(hash1) != len(hash2):
        return -1
    # hamming_distance 為最終相似度
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            hamming_distance += 1
    return hamming_distance


def ahash_similarity(img1, img2):
    """
    計算兩張圖片的均值哈希(aHash)相似度

    參數:
        img1 (ndarray): 第一個圖片，使用 cv2.imread 函數加載後的圖片
        img2 (ndarray): 第二個圖片，使用 cv2.imread 函數加載後的圖片

    返回:
        漢明距離(int)，範圍在 0 ~ 64 ，越小兩張圖越相似
    """
    return calculate_hamming_distance(aHash(img1), aHash(img2))


def dhash_similarity(img1, img2):
    """
    計算兩張圖片的差值哈希(dHash)相似度

    參數:
        img1 (ndarray): 第一個圖片，使用 cv2.imread 函數加載後的圖片
        img2 (ndarray): 第二個圖片，使用 cv2.imread 函數加載後的圖片

    返回:
        漢明距離(int)，範圍在 0 ~ 64 ，越小兩張圖越相似
    """
    return calculate_hamming_distance(dHash(img1), dHash(img2))


def phash_similarity(img1, img2):
    """
    計算兩張圖片的感知哈希(pHash)相似度

    參數:
        img1 (ndarray): 第一個圖片，使用 cv2.imread 函數加載後的圖片
        img2 (ndarray): 第二個圖片，使用 cv2.imread 函數加載後的圖片

    返回:
        漢明距離(int)，範圍在 0 ~ 64 ，越小兩張圖越相似
    """
    return calculate_hamming_distance(pHash(img1), pHash(img2))


def grayscale_similarity(img1, img2):
    """
    計算兩張圖片的灰度直方圖算法相似度

    參數:
        img1 (ndarray): 第一個圖片，使用 cv2.imread 函數加載後的圖片
        img2 (ndarray): 第二個圖片，使用 cv2.imread 函數加載後的圖片

    返回:
        灰度直方圖相似度 (float)，範圍在 0 ~ 1 ，越大兩張圖越相似
    """
    # 計算單通道的直方圖的相似值
    hist1 = cv2.calcHist([img1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0.0, 255.0])
    # 計算直方圖的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return round(float(degree), 2)


def histogram_similarity(img1, img2):
    """
    計算兩張圖片的三通道直方圖算法相似度

    參數:
        img1 (ndarray): 第一個圖片，使用 cv2.imread 函數加載後的圖片
        img2 (ndarray): 第二個圖片，使用 cv2.imread 函數加載後的圖片

    返回:
        3 通道灰度直方圖相似度平均值 (float)，範圍在 0 ~ 1 ，越大兩張圖越相似
    """
    # 比較 R、G、B 三個通道，每個通道的灰度直方圖相似度
    # 返回 3 個通道的灰度直方圖相似度平均值
    # 返回值 0 ~ 1，越大越相似
    # 將圖片 resize後，分離為RGB三個通道，再計算每個通道的相似值
    img1 = cv2.resize(img1, (256, 256))
    img2 = cv2.resize(img2, (256, 256))
    sub_image1 = cv2.split(img1)
    sub_image2 = cv2.split(img2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += grayscale_similarity(im1, im2)
    sub_data = sub_data / 3
    return round(sub_data, 2)


def aHash(img):
    """
    均值哈希算法，將圖片轉換成哈希值

    參數:
        img (ndarray): 使用 cv2.imread 函數加載後的圖片

    返回:
        均值哈希值 (str)
    """
    # 縮放為 8*8
    img = cv2.resize(img, (8, 8))
    # 轉換為灰度圖
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s 為像素和，初值為0，hash_str為hash值，初值為''
    s = 0
    hash_str = ''
    # 累加求像素和
    for i in range(8):
        for j in range(8):
            s += gray[i, j]
    # 求平均灰度
    avg = s/64
    # 灰度大於平均值為1，反之為0，生成圖片hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str += '1'
            else:
                hash_str += '0'
    return hash_str


def dHash(img):
    """
    差值哈希算法，將圖片轉換成哈希值

    參數:
        img (ndarray): 使用 cv2.imread 函數加載後的圖片

    返回:
        差值哈希值 (str)
    """
    # 縮放為 8*8
    img = cv2.resize(img, (8, 8))
    # 轉換為灰度圖
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一個像素大於後一個像素為1，反之為0，生成hash
    for i in range(8):
        for j in range(7):
            if gray[i, j] > gray[i, j+1]:
                hash_str += '1'
            else:
                hash_str += '0'
    return hash_str


def pHash(img):
    """
    感知哈希算法，將圖片轉換成哈希值

    參數:
        img (ndarray): 使用 cv2.imread 函數加載後的圖片

    返回:
        感知哈希值 (str)
    """
    # 縮放為 32*32
    img = cv2.resize(img, (32, 32))

    # 轉換為灰度圖
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 將灰度圖轉為float，再進行 dct 變換
    dct = cv2.dct(np.float32(gray))
    # opencv實現的掩碼操作
    dct_roi = dct[0:8, 0:8]

    hash_str = ''
    avreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash_str += '1'
            else:
                hash_str += '0'
    return hash_str
