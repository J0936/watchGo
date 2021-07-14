import cv2

#设置gstreamer管道参数
def gstreamer_pipeline(
    capture_width=1280, #摄像头预捕获的图像宽度
    capture_height=720, #摄像头预捕获的图像高度
    display_width=1280, #窗口显示的图像宽度
    display_height=720, #窗口显示的图像高度
    framerate=60,       #捕获帧率
    flip_method=0,      #是否旋转图像
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def readImage():
    global cap
    
    ret_val, img = cap.read()
    # 图像太大需要调整
    height, width = img.shape[0:2]
    print("height=",height,"width=",width)
    if width > 800:
        new_width = 640
        new_height = int(new_width/width*height)
        img = cv2.resize(img, (new_width, new_height))
    print("new_height=",new_height,"new_width=",new_width)

    
    return img

         


def watchImage():
    global cap
    capture_width = 1280
    capture_height = 720
    display_width = 1280
    display_height = 720
    framerate = 60
    flip_method = 0

    # 创建管道
    print(gstreamer_pipeline(capture_width,capture_height,display_width,display_height,framerate,flip_method))

    #管道与视频流绑定
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        
        # 逐帧显示
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            img = readImage()

            height, width = img.shape[0:2]
            print(height,width)
            cv2.imshow("CSI Camera", img)
            #print("img.shape=",img.shape)
            keyCode = cv2.waitKey(30) & 0xFF         
            if keyCode == 27:# ESC键退出
                break
        #print("img.shape=",img.shape)
        #释放资源
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("打开摄像头失败")

#def watchBoard():



if __name__ == "__main__":
    watchImage()