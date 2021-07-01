import cv2
import urllib.request
import numpy as np
from urllib import request
import pytesseract

url = 'http://secure.kakaocdn.net/dna/bUHW7Q/K6aPDwOpWD/XXX/img_org.jpg?credential=Kq0eSbCrZgKIq51jh41Uf1jLsUh7VWcz&expires=1600520745&allow_ip=&allow_referer=&signature=15q5FCzUJQzZQmWJ4SQbviZqkXg%3D'
urllib.request.urlretrieve(url, './test.png')
img = cv2.imread('./test.png')
img_g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (9, 9), 0)

thr, mask = cv2.threshold(img_g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations = 7)
contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    if len(approx) == 4:
        width, height = img.shape[:2]
        pts1 = np.array(approx, dtype = "float32")
        pts2 = np.float32([[width, 0], [0, 0], [0, height], [width, height]])

        M = cv2.getPerspectiveTransform(pts1, pts2)

        image_result = cv2.warpPerspective(img, M, (int(width), int(height)))

print(pytesseract.image_to_string(image_result, 'eng+Hangul'))
