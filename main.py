# 挑選出一個目錄下，有相似的圖片，移動到另一個目錄，可以自行決定要保留哪些圖片
import cv2
from algorithm import dhash_similarity, grayscale_similarity
import os
import itertools
import threading
import shutil


# 緩存讀取過的圖片
cache = {}

# 儲存有相似的圖片檔名，最後再一次將有相似的圖片移動到相似圖片目錄
similar_images_set = set()


def split_list_by_mod(lst, mod):
    """
    將一個list按餘數切分成多個子list
    """
    return [lst[i::mod] for i in range(mod)]


# 將圖片目錄裡的圖片切成兩兩不重複的圖片組的list，再將這個 list 切成跟線程數一樣多的幾個小 list
# 確保每個線程不會處理到重複的圖片組
def prepare_all_image_pairs(img_dir, threading_number):
    img_list1 = os.listdir(img_dir)
    img_list1.sort(key=len)

    # 將圖片目錄裡的圖片，分成兩兩不重複的組
    all_pair_list = list(itertools.combinations(img_list1, 2))    
    return split_list_by_mod(all_pair_list, threading_number)


# 用 opencv 讀取過的圖片存進緩存，下次要讀取同樣的圖片就不需要讀取
def read_image(image_path):
    if image_path in cache:
        return cache[image_path]
    else:
        img = cv2.imread(image_path)
        cache[image_path] = img
        return img


# 判斷兩張圖片是否相似
def is_images_similar(image1, image2):
    img1, img2 = read_image(image1), read_image(image2)

    dhash = dhash_similarity(img1, img2)
    
    # 兩張圖片 dHash 值為 0，表示兩張圖片完全一樣
    if dhash == 0:
        return True

    # 兩張圖片 dHash 值太大，幾乎不可能相似
    if dhash > 20:
        return False

    grayscale = grayscale_similarity(img1, img2)

    if (dhash <= 10) and (grayscale > 0.5):
        return True
    elif (10 < dhash < 21) and (grayscale > 0.825):
        return True
    else:
        return False


# 將先前處理好的圖片組列表，判斷每組圖片是否相似，如果圖片相似就加到similar set
def run_all_images(img_dir, pair_list):
    for pair in pair_list:
        img1 = img_dir + pair[0]
        img2 = img_dir + pair[1]

        if is_images_similar(img1, img2):
            similar_images_set.add(img1)
            similar_images_set.add(img2)



def move_similar_images(similar_images_dir):
    for image in similar_images_set:
        shutil.move(image, similar_images_dir)


def main(img_dir, similar_images_dir, threading_number):
    pair_lists = prepare_all_image_pairs(img_dir, threading_number)

    # 創建多線程寫入數據
    threads = []
    for i in range(threading_number):
        t = threading.Thread(target=run_all_images, args=(img_dir, pair_lists[i]))
        threads.append(t)

    # 啟動線程
    for t in threads:
        t.start()

    # 等待線程完成
    for t in threads:
        t.join()

    move_similar_images(similar_images_dir)
    print('Done')


if __name__ == '__main__':
    # 要去重複的圖片放這
    img_dir = 'pics/'
    # 被挑選出有重複的圖片放這
    similar_images_dir = 'similar_images/'
    main(img_dir, similar_images_dir, threading_number=8)
