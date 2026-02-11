import cv2

def show_img(title:str,img,flag=True):
    """
    这个功能是pycharm提供的  用于解释对应的函数或者是类
    :param title:         表示标题          窗口名称
    :param img:           表示传入的图片
    :param flag:          表示bool变量      开关
    :return:              None
    """
    if flag:
        #调用一个命名的Windows窗口，传入的两个参数是名称和新窗口,这样创建的窗口可以调节大小
        cv2.namedWindow(title,cv2.WINDOW_NORMAL)
        cv2.imshow(title,img)


#读取图像
src = cv2.imread("./picture/aqgy.png")

# #动态调整图片大小
# cv2.namedWindow("input",cv2.WINDOW_NORMAL)
# cv2.resize()

#显示图像
show_img("input",src)

#灰度处理
gray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
# show_img("gray",gray)


# hsv = cv2.cvtColor(src,cv2.COLOR_BGR2HSV)

# show_img("hsv",hsv)


#加载级联分类器模型
mode = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

#检测人脸
'''
    scaleFactor是调整准确度的，值越小，检测到的人脸尺寸范围越广，但计算时间也越长  
    minNeighbors是误差值，值越大，误检率越低，但可能会漏掉一些模糊或被遮挡的人脸
    minSize检测的目标的最小尺寸（宽，高）。任何小于 宽x高 像素的区域都不会被检测。这可以过滤掉一些小的、不相关的噪点
    返回一个numpy数组：
    x: 人脸矩形左上角的 x 坐标。
    y: 人脸矩形左上角的 y 坐标。
    w: 人脸矩形的宽度。
    h: 人脸矩形的高度。
 '''
faces = mode.detectMultiScale(src,scaleFactor=1.1,minNeighbors=5,minSize=(30,30))

#标注人脸
for (x,y,w,h) in faces:
    cv2.rectangle(src,(x,y),(x+w,y+h),(0,0,255),2)#用矩形框标注  图片 左上顶点 右下顶点 颜色

show_img("input",src)



























































#cv2.waitKey(100000)等待100s，如果是0则是等待按键关闭
cv2.waitKey(0)

#资源回收
cv2.destroyAllWindows()