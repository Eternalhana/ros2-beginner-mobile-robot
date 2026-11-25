from setuptools import setup

setup(
    name='beginner_robot',
    version='0.1.0',
    packages=['beginner_robot'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/beginner_robot']),
        ('share/beginner_robot', ['package.xml']),
    ],
    install_requires=['setuptools'],
    entry_points={'console_scripts': [
        'draw_square = beginner_robot.draw_square:main',
    ]},
)