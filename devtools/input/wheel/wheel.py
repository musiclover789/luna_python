import math


class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UNKNOWN = 4


class ScrollPoint:
    def __init__(self, distance, duration):
        self.distance = distance
        self.duration = duration


def get_scroll_point(total_distance, is_negative):
    # 鼠标滚动样本数据
    data_samples = [
        ScrollPoint(2, 0),
        ScrollPoint(8, 7),
        ScrollPoint(8, 0),
        ScrollPoint(18, 8),
        ScrollPoint(34, 8),
        ScrollPoint(44, 9),
        ScrollPoint(78, 8),
        ScrollPoint(86, 8),
        ScrollPoint(98, 8),
        ScrollPoint(116, 8),
        ScrollPoint(124, 8),
        ScrollPoint(124, 8),
        ScrollPoint(150, 8),
        ScrollPoint(172, 16),
        ScrollPoint(198, 8),
        ScrollPoint(190, 8),
        ScrollPoint(182, 9),
        ScrollPoint(174, 8),
        ScrollPoint(168, 8),
        ScrollPoint(164, 8),
        ScrollPoint(148, 8),
        ScrollPoint(146, 8),
        ScrollPoint(142, 9),
        ScrollPoint(140, 8),
        ScrollPoint(140, 8),
        ScrollPoint(134, 9),
        ScrollPoint(132, 8),
        ScrollPoint(130, 8),
        ScrollPoint(128, 8),
        ScrollPoint(124, 8),
        ScrollPoint(124, 8),
        ScrollPoint(120, 8),
        ScrollPoint(118, 8),
        ScrollPoint(116, 8),
        ScrollPoint(114, 9),
        ScrollPoint(110, 8),
        ScrollPoint(112, 8),
        ScrollPoint(106, 8),
        ScrollPoint(104, 9),
        ScrollPoint(104, 8),
        ScrollPoint(98, 8),
        ScrollPoint(98, 8),
        ScrollPoint(94, 9),
        ScrollPoint(92, 7),
        ScrollPoint(90, 8),
        ScrollPoint(90, 8),
        ScrollPoint(86, 8),
        ScrollPoint(82, 8),
        ScrollPoint(82, 8),
        ScrollPoint(76, 8),
        ScrollPoint(76, 8),
        ScrollPoint(76, 8),
        ScrollPoint(72, 12),
        ScrollPoint(68, 5),
        ScrollPoint(68, 8),
        ScrollPoint(64, 9),
        ScrollPoint(62, 8)
    ]
    return interpolate_scroll_data(data_samples, total_distance, is_negative)


def interpolate_scroll_data(data_samples, total_distance, is_negative):
    interpolated_data = []
    current_distance = 0

    for i in range(len(data_samples) - 1):
        curr_sample = data_samples[i]
        next_sample = data_samples[i + 1]

        # 计算两个样本之间的时间间隔差
        duration_diff = next_sample.duration - curr_sample.duration

        # 计算当前段的距离和时间间隔
        distance = next_sample.distance - curr_sample.distance

        # 计算当前段的距离比例
        distance_ratio = distance / total_distance
        # 调整距离比例，增加起伏
        distance_ratio *= transform_number(total_distance)
        # 插值生成滚动数据
        for t in range(0, 11, 1):
            t /= 10.0
            # 根据贝塞尔曲线插值算法计算距离和时间间隔
            interpolated_distance = int(
                round(curr_sample.distance + distance_ratio * bezier_interpolation(t) * total_distance / 4))
            interpolated_duration = int(round(curr_sample.duration + duration_diff * bezier_interpolation(t)))

            # 检查生成的距离是否超过了目标距离的剩余量
            if current_distance + interpolated_distance > total_distance:
                interpolated_distance = total_distance - current_distance

            # 将当前点的距离和时间间隔添加到结果中
            interpolated_distance_v = interpolated_distance
            if not is_negative:
                interpolated_distance_v = convert_to_negative(interpolated_distance_v)
            interpolated_data.append(ScrollPoint(interpolated_distance_v, interpolated_duration))
            current_distance += interpolated_distance

            # 如果已达到目标距离，则退出循环
            if current_distance >= total_distance:
                break

        # 如果已达到目标距离，则退出循环
        if current_distance >= total_distance:
            break

    return interpolated_data


def convert_to_negative(num):
    return num * -1


def transform_number(num):
    k = 0.5  # 调整斜率参数 k 的值，根据需要进行适当调整
    # 应用 S 形曲线函数
    result = int(160 / (1 + math.exp(-k * num)))
    return result


def bezier_interpolation(t):
    # 调整贝塞尔曲线的控制点，增加起伏程度
    control_points = [0.0, 0.25, 0.25, 1.0]
    return math.pow(1 - t, 3) * control_points[0] + 3 * math.pow(1 - t, 2) * t * control_points[1] + 3 * (
            1 - t) * math.pow(t, 2) * control_points[2] + math.pow(t, 3) * control_points[3]


# for item in get_scroll_point(200, False):
#     print(item.distance, item.duration)
