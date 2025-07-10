import math

def calculate_angle_cross_dot(line1, line2):
    """
    计算两条直线之间的角度，范围在-90度到90度之间
    -90度会被转换为90度
    
    参数:
    line1: 第一条线段的坐标 [x1, y1, x2, y2]
    line2: 第二条线段的坐标 [x1, y1, x2, y2]
    
    返回:
    两条直线之间的角度(弧度)
    """
    # 提取线段的坐标
    x1_1, y1_1, x1_2, y1_2 = line1
    x2_1, y2_1, x2_2, y2_2 = line2
    
    # 计算线段的向量
    vector1 = (x1_2 - x1_1, y1_2 - y1_1)
    vector2 = (x2_2 - x2_1, y2_2 - y2_1)
    
    # 计算向量的点积
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    
    # 计算向量的模
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    
    # 计算角度的余弦值
    cos_angle = dot_product / (magnitude1 * magnitude2)
    
    # 确保余弦值在有效范围内(-1到1)，避免数值误差导致的问题
    cos_angle = max(-1.0, min(1.0, cos_angle))
    
    # 计算向量叉积的z分量，用于确定旋转方向
    cross_product_z = vector1[0] * vector2[1] - vector1[1] * vector2[0]
    
    # 计算角度(弧度) 
    angle = math.acos(cos_angle)
    angle_degrees = math.degrees(angle) # 此处是0-180度
    assert 0 <= angle_degrees <= 180, f"angle_degrees={angle_degrees}"

    norm_degrees = -1
    # 根据叉积的z分量确定角度的正负
    if cross_product_z >= 0: # 叉积为正(在上方)，逆时针旋转，定义norm_degrees为负
        # angle = -angle
        # 如果angle in [180, 270], 则 angle = angle - 180, in [90, 180], 则 angle = - (angle -90)
        if 0 <= angle_degrees <= 90:
            norm_degrees = - angle_degrees
        elif 90 <= angle_degrees <= 180:
            norm_degrees = 180 - angle_degrees
    else:
        if 0 <= angle_degrees <= 90:
            norm_degrees = angle_degrees
        elif 90 <= angle_degrees <= 180:
            norm_degrees = angle_degrees - 180

    return angle, angle_degrees, norm_degrees, cross_product_z


def cross_dot(line1, line2):
    """_summary_

    Args:
        line1 (_type_): _description_
        line2 (_type_): _description_

    Returns:
        _type_: < 0: 顺时针旋转; > 0: 逆时针旋转; = 0: 共线
    """
    # 提取线段的坐标
    x1_1, y1_1, x1_2, y1_2 = line1
    x2_1, y2_1, x2_2, y2_2 = line2
    
    # 计算线段的向量
    vector1 = (x1_2 - x1_1, y1_2 - y1_1)
    vector2 = (x2_2 - x2_1, y2_2 - y2_1)
    # 计算向量的点积
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    
    return dot_product
    
def main():
    # 示例1：x轴和y轴上的线段 (90度)
    line1 = [0, 0, 1, 0]  # x轴上的线段
    line2 = [0, 0, 0, 1]  # y轴上的线段
    
    # 计算角度
    angle_radians = calculate_angle(line1, line2)
    angle_degrees = math.degrees(angle_radians)
    
    print(f"线段 {line1} 和 {line2} 之间的角度为:")
    print(f"{angle_radians:.4f} 弧度")
    print(f"{angle_degrees:.4f} 度")
    
    # 示例2：测试接近-90度的情况
    line3 = [0, 0, 1, 0]  # x轴上的线段
    line4 = [-0.1, -1, 0.1, 1]  # 接近y轴但在第二象限的线段
    
    angle_radians2 = calculate_angle(line3, line4)
    angle_degrees2 = math.degrees(angle_radians2)
    
    print(f"\n线段 {line3} 和 {line4} 之间的角度为:")
    print(f"{angle_radians2:.4f} 弧度")
    print(f"{angle_degrees2:.4f} 度")
    
    # 示例3：测试接近90度的情况
    line5 = [0, 0, 1, 0]  # x轴上的线段
    line6 = [-0.1, 1, 0.1, -1]  # 接近y轴但在第一象限的线段
    
    angle_radians3 = calculate_angle(line5, line6)
    angle_degrees3 = math.degrees(angle_radians3)
    
    print(f"\n线段 {line5} 和 {line6} 之间的角度为:")
    print(f"{angle_radians3:.4f} 弧度")
    print(f"{angle_degrees3:.4f} 度")
    
    # 示例4：测试135度的情况(应返回45度)
    line7 = [0, 0, 1, 0]  # x轴上的线段
    line8 = [0, 0, -1, 1]  # 第二象限的线段
    
    angle_radians4 = calculate_angle(line7, line8)
    angle_degrees4 = math.degrees(angle_radians4)
    
    print(f"\n线段 {line7} 和 {line8} 之间的角度为:")
    print(f"{angle_radians4:.4f} 弧度")
    print(f"{angle_degrees4:.4f} 度")


def print_all(line1, line2):
    angle, angle_degrees, norm_degrees, cross_product_z = calculate_angle_cross_dot(line1, line2)
    print(f"线段 {line1} 和 {line2} 之间的角度为:\n\t origin angle={angle}, angle_degrees={angle_degrees}, cross_product_z={cross_product_z}, norm_degrees={norm_degrees}")

def main1():
    # 示例1：x轴和y轴上的线段 (90度)
    line1 = [0, 0, 0, 1]  # x轴上的线段
    line2 = [0, 0, -1, -1]  # y轴上的线段
    # 计算角度
    print_all(line1, line2)
    
    line1 = [0, 0, 0, 1]  # x轴上的线段
    line2 = [0, 0, 1, 1]  # y轴上的线段
    # 计算角度
    print_all(line1, line2)
    
if __name__ == "__main__":
    main1()
