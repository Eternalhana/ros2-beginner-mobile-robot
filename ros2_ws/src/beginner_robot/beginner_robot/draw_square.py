"""从重置后的中央出发，前进、左转，重复四次，在画布上留下正方形。"""
import math
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim.msg import Pose

SIDE = 2.0  # 边长，单位是仿真坐标单位，不是屏幕像素


class SquareDriver(Node):
    def __init__(self):
        super().__init__('square_driver')
        self.pose = None
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 1)
        self.commands = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def on_pose(self, message):
        self.pose = message  # 每收到一条报告，就记下最新位置和朝向

    def read_pose(self):
        self.pose = None
        deadline = time.monotonic() + 3
        while self.pose is None:
            rclpy.spin_once(self, timeout_sec=0.1)  # 等消息，让 on_pose 接收它
            if time.monotonic() >= deadline:
                raise RuntimeError('没有收到位置，请先启动 Turtlesim。')
        return self.pose

    def command(self, forward=0.0, turn=0.0):
        msg = Twist()
        msg.linear.x = forward  # 向前速度
        msg.angular.z = turn    # 转动速度：正值左转，负值右转
        self.commands.publish(msg)

    def drive_side(self):
        start = self.read_pose()
        deadline = time.monotonic() + 8
        while True:
            now = self.read_pose()
            distance = math.hypot(now.x - start.x, now.y - start.y)
            if distance >= SIDE:
                break
            if time.monotonic() >= deadline:
                raise RuntimeError('直行超时，可能碰到了边界；请重置画布。')
            self.command(forward=1.0)
        self.command()  # 速度归零，不要边走边转

    def face(self, target):
        deadline = time.monotonic() + 8
        while True:
            angle = self.read_pose().theta
            # 把差值换算成最短转角，避免从 +π 跨到 -π 时绕一大圈。
            error = math.atan2(math.sin(target - angle), math.cos(target - angle))
            if abs(error) < 0.008:
                break
            if time.monotonic() >= deadline:
                raise RuntimeError('转向超时，请确认没有别的程序同时控制小乌龟。')
            self.command(turn=max(-2.0, min(2.0, 4 * error)))  # 越接近目标，转得越慢
        self.command()

    def draw(self):
        p = self.read_pose()
        if abs(p.x - 5.54) > 0.15 or abs(p.y - 5.54) > 0.15 or abs(p.theta) > 0.03:
            raise RuntimeError('请先调用 /reset，让小乌龟从画布中央朝右出发。')
        for side in range(1, 5):
            self.drive_side()
            self.face(side * math.pi / 2)  # π/2 弧度就是 90°
            p = self.read_pose()
            self.get_logger().info(f'第 {side} 条边完成：x={p.x:.3f}, y={p.y:.3f}')


def main():
    rclpy.init()
    driver = SquareDriver()
    try:
        driver.draw()
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            driver.command()  # 正常结束或异常时，都尽力发停车指令
        driver.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()