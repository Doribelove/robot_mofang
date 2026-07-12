import cv2

# 鼠标回调函数
def mouse_callback(event, x, y, flags, param):
    global img, points

    if event == cv2.EVENT_LBUTTONDOWN:
        # 获取点击位置的像素值
        pixel_value = img[y, x]
        b, g, r = pixel_value  # 分离BGR值

        # 添加坐标和像素值到列表
        points.append(((x, y), (r, g, b)))
        print(f"点 {len(points)}: 坐标 ({x}, {y}), RGB值 ({r}, {g}, {b})")

        # 在点击位置绘制圆圈
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

        # 如果已经获取了9个点,保存到文件并退出程序
        if len(points) == 9:
            save_points_to_file("points.txt", points)
            cv2.destroyAllWindows()

# 保存点的坐标和RGB值到文件
def save_points_to_file(filename, points):
    with open(filename, 'w') as file:
        for i, point in enumerate(points):
            coords, rgb = point
            # file.write(f"点 {i+1}: 坐标 {coords}, RGB值 {rgb}\n")
            # file.write(f"block_u"+str(i+1)+" = exchange("+f"{coords}"+")"+f"{rgb}\n")
            file.write(f"block_r"+str(i+1)+" = exchange("+f"{coords}"+")\n")

# 加载图像
img = cv2.imread("44.jpg")

# 创建窗口并设置鼠标回调函数
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

points = []

while True:
    # 显示图像
    cv2.imshow("Image", img)

    # 按下'q'键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭所有窗口
cv2.destroyAllWindows()


