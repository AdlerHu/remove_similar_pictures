CREATE TABLE `all_images` (
  `img1` varchar(12),
  `img2` varchar(12),
  `aHash` int,
  `dHash` int,
  `pHash` int,
  `grayscale` float,
  `histogram` float,
  PRIMARY KEY(img1, img2)
);

-- 建立一個 user 'user1'，只給他操作 similar_images 這個資料庫的權限
CREATE USER 'user1'@'%' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON similar_images.* TO 'user1'@'%';


-- 設定變數並指定字符集(collation)
SET @img1 = '003234.PNG' COLLATE utf8mb4_0900_ai_ci;
SET @img2 = '003123.PNG' COLLATE utf8mb4_0900_ai_ci;
-- 使用變數進行查詢
INSERT INTO sample_images
SELECT *
FROM all_images
WHERE (img1 = @img1 AND img2 = @img2)
OR (img1 = @img2 AND img2 = @img1);

-- 資料表添加索引
ALTER TABLE mytable ADD INDEX index_name (column_name);

-- 查找相似圖片
SELECT * 
FROM `all_images` 
WHERE 
((`dHash` <= 10) AND (`grayscale` > 0.5)) 
OR
(( 10 < `dHash`) AND ( `dHash` < 21 ) AND (`grayscale` > 0.825));