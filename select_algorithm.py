# 計算我所有的圖片，所有的圖片組合，所有的相似度演算法結果
# 將所有計算結果寫入 DB，以供選擇合適的演算法
import cv2
from algorithm import ahash_similarity, dhash_similarity, phash_similarity, grayscale_similarity, histogram_similarity
import os
import itertools
import threading
from utils.connection import connect_db
from utils.tables import My_Images
from sqlalchemy.orm import sessionmaker


# 給定兩張圖片，計算這兩張圖片的均值哈希、差值哈希、感知哈希、灰度直方圖相似度、三通道直方圖相似度
def run_all_image_similary(img1_path, img2_path):
    # cv2.imread 讀取圖片
    img1, img2 = cv2.imread(img1_path), cv2.imread(img2_path)
 
    dhash = dhash_similarity(img1, img2)
    # 實測發現 dHash 運算速度最快，所以用 dHash 來判斷兩張圖是不是完全一樣
    # 完全一樣的兩張圖就不用繼續運算
    if dhash == 0:
        return 0, 0, 0, 1.0, 1.0

    ahash = ahash_similarity(img1, img2)
    phash = phash_similarity(img1, img2)
    grayscale = grayscale_similarity(img1, img2)
    histogram = histogram_similarity(img1, img2)
    return ahash, dhash, phash, grayscale, histogram


# 將先前處理好的圖片組列表，計算每組圖片的所有相似度演算法結果，然後寫入資料庫
def run_all_images(pic_dir, pair_list):
    engine = connect_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    # 緩存準備寫入資料庫的資料
    data = []
    counter = 0
    try:
        for pair in pair_list:
            img1_path, img2_path = os.path.join(pic_dir, pair[0]), os.path.join(pic_dir, pair[1])

            ahash, dhash, phash, grayscale, histogram = run_all_image_similary(img1_path, img2_path)
            image_pair = {
                'img1': pair[0],
                'img2': pair[1],
                'aHash': ahash,
                'dHash': dhash,
                'pHash': phash,
                'grayscale': grayscale,
                'histogram': histogram
            }
            data.append(image_pair)
            counter += 1

            # 每處理好 100000 對圖片，寫入資料庫
            if counter % 100000 == 0:
                print('commit')
                session.bulk_insert_mappings(My_Images, data)
                session.commit()
                # 重製 data 列表，清出記憶體
                data = []  

        # 寫入剩餘的資料
        session.bulk_insert_mappings(My_Images, data)  
        session.commit()
    except Exception as e:
        print("Error occurred: ", e)
        session.rollback()
    finally:
        session.close()
        engine.dispose()


def split_list_by_mod(lst, mod):
    """
    將一個list按餘數切分成多個子list
    """
    return [lst[i::mod] for i in range(mod)]


# 將圖片目錄裡的圖片切成兩兩不重複的圖片組的list，再將這個 list 切成跟線程數一樣多的幾個小 list
# 確保每個線程不會處理到重複的圖片組
def prepare_all_sample_images(pic_dir, threading_number):
    img_list = os.listdir(pic_dir)
    img_list.sort(key=len)

    # 將圖片目錄裡的圖片，分成兩兩不重複的組
    all_pair_list = list(itertools.combinations(img_list, 2))    
    return split_list_by_mod(all_pair_list, threading_number)


def main(pic_dir, threading_number):
    pair_lists = prepare_all_sample_images(pic_dir, threading_number)

    # 創建多線程
    threads = []
    for i in range(threading_number):
        t = threading.Thread(target=run_all_images, args=(pic_dir, pair_lists[i]))
        threads.append(t)

    # 啟動線程
    for t in threads:
        t.start()

    # 等待線程完成
    for t in threads:
        t.join()
    print('Done')


if __name__ == "__main__":
    pic_dir = 'pics/'
    # threading_number: 預計跑的線程數
    main(pic_dir, threading_number=8)
