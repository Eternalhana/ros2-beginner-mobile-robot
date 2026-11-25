# ROS2 Beginner Mobile Robot Simulation

一个机器人工程本科生的入门练习：先用键盘控制屏幕里的小乌龟，再用一个 Python 程序接替键盘，画出边长为 2 个仿真单位的正方形。只用 ROS 2 官方 Turtlesim，不需要实体机器人。项目在 Codex 辅助下搭建、运行并记录；演示不是动画重绘。

![从真实 Turtlesim 窗口录制的自动正方形](screenshots/04-square-demo.gif)

## 功能与实测结果

| 功能 | 验证方式 |
|---|---|
| 启动仿真窗口 | Windows 上出现 TurtleSim 窗口，Ubuntu 内能读取小乌龟的位置 |
| 键盘前进、后退、左转、右转 | 四个方向键分别被送入官方键盘程序；用位置报告核对平移和转向 |
| Python 自动路线 | 订阅位置报告，发布速度指令；直行和左转交替，各做四次，最后停车 |
| 轨迹验收 | 此次起点 `(5.544445, 5.544445)`，终点 `(5.545168, 5.543655)`；距离约 `0.0011` 个仿真单位。这是一轮实测，不是每次运行的精度保证 |

[初始画面](screenshots/01-turtlesim-start.png) · [按 ↑ 后的直线](screenshots/02-keyboard-forward.png) · [正方形完成画面](screenshots/03-auto-square.png)

## 开发环境

Windows 11 → WSL2（让 Windows 运行 Linux）→ Ubuntu 24.04.5 LTS → ROS 2 Jazzy 基础版、Turtlesim、Python 3.12.3。Git 使用 Windows 版。本机 Ubuntu 和项目均放在 D 盘。项目运行不依赖截图工具或 GitHub 账号。

下面的运行步骤以已安装 ROS 2 Jazzy 的 Ubuntu 24.04 为前提。若换机器，请先按 ROS 官方的 Ubuntu 安装文档配置软件源；所需软件包为 `ros-jazzy-ros-base`、`ros-jazzy-turtlesim`、`python3-colcon-ros`。不能直接在 Windows 的 PowerShell 里运行 `ros2` 命令。

## 运行方法：先看窗口，再控制它

“终端”就是输入命令的窗口。新开一个 PowerShell 标签页后，输入 `wsl -d Ubuntu-24.04` 进入 Ubuntu。下面 A、B 各占一个 Ubuntu 标签页；每块代码的命令按行执行。关掉终端 A 会结束仿真。

### A：启动窗口（如果已有一个打开，就直接用那个）

用途：先让当前终端找到 ROS，再启动 Turtlesim。

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

看到蓝色窗口和小乌龟即成功。不要重复启动多个同名仿真节点。

### B：先试键盘

用途：在另一个 Ubuntu 终端启动键盘程序。**让这个终端保持焦点**，不要点蓝色画布后再按键。

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtle_teleop_key
```

按 `↑` 前进，`↓` 后退，`←` 原地左转，`→` 原地右转。前进指沿当前朝向走，并非一定往屏幕上方走。完成后按 `q` 退出键盘程序，保留终端 A。

### B：运行自己的 Python 节点

用途：进入工作区（存放和构建 ROS 软件包的文件夹）。本机 Windows 的 D 盘在 Ubuntu 里写作 `/mnt/d`；如果下载到了其他位置，请换成自己的路径。

```bash
cd /mnt/d/ROS2-Projects/ros2-beginner-mobile-robot/ros2_ws
```

用途：构建唯一的包，再让这个终端找到它。第一次运行和修改 Python 文件后都要重新构建。

```bash
colcon build
source install/setup.sh
```

用途：清空**仿真画布**并把小乌龟放回中央，然后启动自动画线程序。这不会删除截图或磁盘文件。

```bash
ros2 service call /reset std_srvs/srv/Empty '{}'
ros2 run beginner_robot draw_square
```

看到四条边完成的输出，画面上留下一个正方形，小乌龟停止。想再画一次，请重复这最后两行。不要在自动绘制时同时按方向键。

### 可选：听小乌龟说自己在哪里

用途：在已加载 Jazzy 的 Ubuntu 终端读取一次消息，输出后自动退出。

```bash
ros2 topic echo /turtle1/pose --once
```

`x`、`y` 是横、纵坐标，`theta` 是朝向。详情和 Git 入门见[中文学习笔记](docs/learning_notes.md)。

## 遇到的问题

- 单独探测一个 HTTPS 地址时证书名称不匹配。改按 ROS 官方发布的 `ros2-apt-source` 配置软件源，正常更新清单，没有关闭签名校验。
- 精简版 `colcon` 没有 `--packages-select` 插件，且工作区只生成 `setup.sh`。本项目只有一个包，使用 `colcon build` 和 `source install/setup.sh` 实测成功。
- 如果找不到 `/turtle1/pose`，先看终端 A 是否还在运行；如果找不到 `beginner_robot`，在终端 B 进入 `ros2_ws`，重新构建并加载环境。

## 后续练习（尚未实现）

先把边长从 `2.0` 改成 `1.0`，预测轨迹再运行；理解直行与转动后，再尝试同时给出两种速度来画圆。不引入 SLAM 或导航系统。
