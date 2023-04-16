import numpy as np
from PIL import Image
from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity as ssim
from skimage.feature import match_template
from skimage import img_as_float

# 載入樣本圖片
sample_image = Image.open("sample_image.jpg")
sample_image = np.array(sample_image)

# 載入待比對的圖片
test_image = Image.open("test_image.jpg")
test_image = np.array(test_image)

# 將圖片轉為灰階
sample_gray = img_as_float(sample_image)
test_gray = img_as_float(test_image)

# 計算不同演算法的相似度
ssim_score = ssim(sample_gray, test_gray, multichannel=True)
mse = np.mean((sample_gray - test_gray) ** 2)
ncc_score = np.max(match_template(sample_gray, test_gray))

# 將結果記錄下來
with open("similarity_results.txt", "w") as f:
    f.write("SSIM Score: {}\n".format(ssim_score))
    f.write("Mean Squared Error: {}\n".format(mse))
    f.write("Normalized Cross-Correlation Score: {}\n".format(ncc_score))

print("相似度計算結果已經記錄到 similarity_results.txt 檔案中。")

# 上面的程式碼使用了三種不同的演算法，包括結構相似性指數（SSIM）、均方誤差（Mean Squared Error, MSE）和正規化交叉相關係數（Normalized Cross-Correlation, NCC）
# 來計算樣本圖片和待比對圖片之間的相似度。計算結果會記錄到一個名為 "similarity_results.txt" 的檔案中，
# 您可以根據需要進行後續的決策，選擇正式的城市判斷圖片相似度的演算法。請注意，這只是一個簡單的範例，實際應用中可能需要根據您的需求進一步優化和調整。