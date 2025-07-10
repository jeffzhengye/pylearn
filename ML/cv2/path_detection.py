import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

from line_angle_calculator import calculate_angle_cross_dot

class PVPanelLineDetector:
    def __init__(self, 
                 line_color_lower=(0, 0, 150), 
                 line_color_upper=(180, 30, 255),
                 roi_height=0.7,  # 底部ROI高度占比
                 blur_kernel=(5, 5),
                 canny_threshold1=50,
                 canny_threshold2=150,
                 max_angle=60):  # 最大允许角度（度）
        self.line_color_lower = line_color_lower  # 线条颜色的HSV下限
        self.line_color_upper = line_color_upper  # 线条颜色的HSV上限
        self.roi_height = roi_height  # 底部ROI高度
        self.blur_kernel = blur_kernel
        self.canny_threshold1 = canny_threshold1
        self.canny_threshold2 = canny_threshold2
        self.max_angle = max_angle  # 过滤大角度线条
        
    def load_image(self, image_path):
        """加载图像并转换为RGB格式"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法加载图像: {image_path}")
        # 转换为RGB格式（OpenCV默认是BGR）
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def preprocess_image(self, image):
        """预处理图像，提取线条"""
        # 转换为HSV颜色空间
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        # 创建颜色掩码（仅保留线条）
        mask = cv2.inRange(hsv, self.line_color_lower, self.line_color_upper)
        # 应用高斯模糊减少噪声
        blur = cv2.GaussianBlur(mask, self.blur_kernel, 0)
        # 应用Canny边缘检测
        edges = cv2.Canny(blur, self.canny_threshold1, self.canny_threshold2)
        return edges
    
    def extract_roi(self, image):
        """提取图像底部的感兴趣区域(ROI)"""
        height, width = image.shape
        roi_y = int(height * (1 - self.roi_height))
        roi = image[roi_y:height, 0:width]
        return roi, roi_y
    
    def does_line_intersect_center(self, line, image_width, roi_y):
        """检查线条是否与图像中线相交"""
        if line is None:
            return False
            
        # 正确解包线条坐标
        x1, y1, x2, y2 = line[0]
        
        # 转换到原图坐标系
        y1 += roi_y
        y2 += roi_y
        
        # 图像中线的x坐标
        center_x = image_width / 2
        
        # 检查线的两端点是否在中线两侧
        if (x1 - center_x) * (x2 - center_x) <= 0:
            return True
        
        # 如果线是垂直的且经过中线
        if x1 == x2 and x1 == center_x:
            return True
            
        # 计算线的斜率
        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
            # 计算线与中线的交点y坐标
            intersect_y = y1 + slope * (center_x - x1)
            # 检查交点是否在线段范围内
            if min(y1, y2) <= intersect_y <= max(y1, y2):
                return True
                
        return False
    
    def calculate_line_to_center_angle(self, line, image_width):
        """计算线与图像中线的角度"""
        assert line is not None
        # 确保正确处理线条格式
        if len(line) == 1:  # 如果是嵌套格式
            x1, y1, x2, y2 = line[0]
        else:
            x1, y1, x2, y2 = line
        
        line1 = x1, y1, x2, y2
        line2 = image_width, 1, image_width, 0

        angle, angle_degrees, norm_degrees, cross_product_z = calculate_angle_cross_dot(line1, line2)
        return angle, angle_degrees, norm_degrees, cross_product_z
    
    def find_nearest_line(self, roi, roi_y, original_image):
        """找到最接近摄像头、角度合适且与中线相交的线"""
        # 霍夫线变换检测直线
        # lines = cv2.HoughLinesP(roi, 1, np.pi/180, 50, minLineLength=50, maxLineGap=10)
        lines = cv2.HoughLinesP(
            roi,                  # 输入图像
            1,                    # 距离分辨率
            np.pi/180,            # 角度分辨率
            threshold=30,         # 累加器阈值，降低以检测更多线段
            minLineLength=20,     # 最小线段长度，降低以检测更短线段
            maxLineGap=50         # 最大线段间隙，增大以合并更远的线段
        )
        if lines is None:
            print("didn't find any lines")
            return None, None, None
        else:
            print(f"found {len(lines)} lines")
        
        # 找到最接近摄像头、角度合适且与中线相交的线
        nearest_line = None
        max_y = 0
        valid_angle = 0
        min_angle = 90  # 初始化最小角度为180度
        top_k_list = []
        
        for i, line in enumerate(lines):
            if i == 0:
                print(f"line 0 data is like ={line}")
            
            # 正确解包线条坐标
            x1, y1, x2, y2 = line[0]
            
            # 计算线的平均y坐标（相对于原始图像）
            avg_y = ((y1 + y2) / 2) + roi_y
            
            # 计算线与垂直线的角度
            if x2 - x1 != 0:
                slope = (y2 - y1) / (x2 - x1)
                angle = np.degrees(np.arctan(slope))
            else:
                angle = 90  # 垂直线
            
            print(f"line {i}, angle={angle}")
            
            
            # 过滤掉角度过大的线
            if True or abs(angle) <= self.max_angle:
                # 检查线是否与中线相交
                if True or self.does_line_intersect_center(line, original_image.shape[1], roi_y):
                    # 计算与中线的夹角
                    angle, angle_degrees, norm_degrees, cross_product_z = self.calculate_line_to_center_angle(line, original_image.shape[1])
                    # 确保与中线的夹角也在允许范围内
                    if abs(norm_degrees) <= self.max_angle:
                        print(f"\tline {i}, angle={angle}, angle_to_center={angle_degrees}, norm_degrees={norm_degrees}, cross_product_z={cross_product_z}")
                        if True or avg_y > max_y:
                            if abs(norm_degrees) < min_angle:
                                min_angle = abs(norm_degrees)
                            else:
                                # continue
                                pass
                            average_x = (x1 + x2) / 2
                            x_dist = abs(original_image.shape[1]/2 - average_x)
                            top_k_list.append((norm_degrees, x_dist, cross_product_z, line[0]))
                            
                            max_y = avg_y
                            nearest_line = line[0]
                            
                            valid_angle = angle
                            
                            # # 在原图上标记找到的线
                            # cv2.line(original_image, 
                            #          (int(x1), int(y1 + roi_y)), 
                            #          (int(x2), int(y2 + roi_y)), 
                            #          (0, 255, 0), 2)
                            
                            # # 标记线的中点
                            # mid_x = (x1 + x2) // 2
                            # mid_y = (y1 + y2) // 2 + roi_y
                            # cv2.circle(original_image, (mid_x, mid_y), 5, (255, 0, 0), -1)
                            # # 在中点位置标记线的编号i和角度
                            # cv2.putText(original_image, f"line_{i}", (mid_x, mid_y),
                            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                            # cv2.putText(original_image, f"{angle:.1f}°", (mid_x, mid_y + 15),
                            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                            
                            # # 标记线与中线的交点
                            # center_x = original_image.shape[1] // 2
                            # if (x1 - center_x) * (x2 - center_x) <= 0:
                            #     # 线的两端点在中线两侧，计算交点
                            #     if x2 - x1 != 0:
                            #         slope = (y2 - y1) / (x2 - x1)
                            #         intersect_y = y1 + slope * (center_x - x1) + roi_y
                            #         cv2.circle(original_image, (int(center_x), int(intersect_y)), 7, (255, 255, 0), -1)
        
        sorted_list = sorted(top_k_list, key=lambda x: x[1]) # 按x_dist排序
        nearest_line = sorted_list[0][3]
        
        def annotate(k):
            for i in range(k):
                angle, x_dist, cross_product_z, line = sorted_list[i]
                x1, y1, x2, y2 = line
                
                # 在原图上标记找到的线
                cv2.line(original_image, 
                            (int(x1), int(y1 + roi_y)), 
                            (int(x2), int(y2 + roi_y)), 
                            (0, 255, 0), 2)
                
                # 标记线的中点
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2 + roi_y
                cv2.circle(original_image, (mid_x, mid_y), 14, (255, 0, 0), -1)
                # 在中点位置标记线的编号i和角度
                cv2.putText(original_image, f"line_{i}", (mid_x, mid_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(original_image, f"{angle:.1f}", (mid_x+50, mid_y + 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                # 标记线与中线的交点
                # center_x = original_image.shape[1] // 2
                # if (x1 - center_x) * (x2 - center_x) <= 0:
                #     # 线的两端点在中线两侧，计算交点
                #     if x2 - x1 != 0:
                #         slope = (y2 - y1) / (x2 - x1)
                #         intersect_y = y1 + slope * (center_x - x1) + roi_y
                #         cv2.circle(original_image, (int(center_x), int(intersect_y)), 7, (255, 255, 0), -1)
                        
        annotate(1)
        
        return nearest_line, valid_angle, max_y
    
    def get_steering_adjustment(self, angle, speed=0.3):
        """根据角度计算转向调整"""
        # 简单的比例控制
        kp = 0.01  # 比例系数，可根据实际情况调整
        
        # 计算转向值（正值表示右转，负值表示左转）
        steering = angle * kp
        
        # 计算左右轮速度
        left_speed = speed - steering
        right_speed = speed + steering
        
        # 限制速度范围
        left_speed = max(0, min(1.0, left_speed))
        right_speed = max(0, min(1.0, right_speed))
        
        return left_speed, right_speed, steering
    
    def process_image(self, image_path, show_steps=False):
        """处理单张图片并返回结果"""
        # 加载原始图像
        original_image = self.load_image(image_path)
        result_image = original_image.copy()
        
        # 预处理图像
        edges = self.preprocess_image(original_image)
        
        # 提取感兴趣区域
        roi, roi_y = self.extract_roi(edges)
        
        # 找到最接近且角度合适、与中线相交的线
        nearest_line, line_angle, y_position = self.find_nearest_line(roi, roi_y, result_image)
        
        # 计算线与中线的角度
        angle_to_center = None
        if nearest_line is not None:
            angle, angle_degrees, norm_degrees, cross_product_z = self.calculate_line_to_center_angle(nearest_line, original_image.shape[1])
            angle_to_center = norm_degrees
            # 标记图像中线
            center_x = original_image.shape[1] // 2
            cv2.line(result_image, 
                     (center_x, 0), 
                     (center_x, original_image.shape[0]), 
                     (255, 0, 0), 2)
            
            # 显示角度信息
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(result_image, f"Angle to Center: {angle_to_center:.1f}", 
                       (10, 30), font, 1, (255, 0, 0), 2)
            
            # 显示最大角度限制
            cv2.putText(result_image, f"Max Allowed Angle: {self.max_angle}", 
                       (10, 70), font, 0.7, (255, 0, 0), 2)
            
            # 显示与中线相交状态
            cv2.putText(result_image, "Intersects Center: Yes", 
                       (10, 110), font, 0.7, (0, 255, 0), 2)
            
            # 计算转向调整
            left_speed, right_speed, steering = self.get_steering_adjustment(angle_to_center)
            cv2.putText(result_image, f"Left: {left_speed:.2f}  Right: {right_speed:.2f}", 
                       (10, 150), font, 0.7, (255, 0, 0), 2)
        else:
            # 显示未找到合适线的信息
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(result_image, f"No valid line found (angle to center <= {self.max_angle} and intersects center)", 
                       (10, 30), font, 0.7, (255, 0, 0), 2)
        
        # 在Jupyter Notebook中显示结果
        plt.figure(figsize=(12, 8))
        
        if show_steps:
            # 显示原始图像
            plt.subplot(2, 2, 1)
            plt.title("original image")
            plt.imshow(original_image)
            plt.axis('off')
            
            # 显示预处理后的边缘
            plt.subplot(2, 2, 2)
            plt.title("edge detect")
            plt.imshow(edges, cmap='gray')
            plt.axis('off')
            
            # 显示ROI区域
            plt.subplot(2, 2, 3)
            plt.title("roi")
            plt.imshow(roi, cmap='gray')
            plt.axis('off')
            
            # 显示结果
            plt.subplot(2, 2, 4)
            plt.title("detect results")
            plt.imshow(result_image)
            plt.axis('off')
        else:
            plt.title("detect results")
            plt.imshow(result_image)
            plt.axis('off')
            
        plt.tight_layout()
        plt.show()
        
        return result_image, angle_to_center, nearest_line


# 使用示例
def detect_reference_line(image_path, show_steps=False, max_angle=60):
    """便捷函数：检测图像中的参考线并显示结果"""
    detector = PVPanelLineDetector(max_angle=max_angle, roi_height=0.5)
    result_image, angle, line = detector.process_image(image_path, show_steps)
    
    if line is not None:
        print(f"找到参考线！与中线角度: {angle:.2f}°")
        left_speed, right_speed, steering = detector.get_steering_adjustment(angle)
        print(f"转向调整: {steering:.2f}")
        print(f"左轮速度: {left_speed:.2f}, 右轮速度: {right_speed:.2f}")
    else:
        print(f"未检测到与中线夹角在±{max_angle}°范围内且与中线相交的参考线")
    
    return result_image, angle    


if __name__ == "__main__":
    # 示例用法
    image_path = "/mnt/d/wps/公司项目/宴志威/清洗机器人/images/6.png"
    image_path = "/mnt/d/wps/公司项目/宴志威/清洗机器人/images/5.jpg"

    ret = detect_reference_line(image_path, show_steps=False)
