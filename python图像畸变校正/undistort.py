import cv2
import pickle

if __name__ == '__main__':
    # 获取矫正参数
    f = pickle.load(open('parameter', 'rb'))  # 读取矫正参数
    ret, mtx, dist, rvecs, tvecs = f['ret'], f['mtx'], f['dist'], f['rvecs'], f['tvecs']

    # 获取图像尺寸
    img = cv2.imread('img\\1.jpg')
    h, w = img.shape[:2]
    new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    x, y, w, h = roi      # roi 提取的不准确，可能需要手动调整
    vid = cv2.VideoCapture(0)
    while True:
        state, src = vid.read()
        cv2.imshow('src', src)
        dst = cv2.undistort(src, mtx, dist, None, new_camera_mtx)
        cv2.imshow('img1', dst)
        dst = dst[y:y + h, x:x + w]
        cv2.imshow('img2', dst)
        cv2.waitKey(1)

