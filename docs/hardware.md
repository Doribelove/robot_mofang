# 硬件部署

## 设备组成

- 一块 ODrive，`axis0` 为右腕，`axis1` 为左腕。
- 一块 Arduino，通过串口控制左右夹爪及辅助电磁铁。
- 四路 USB 摄像头，默认设备为 `/dev/video2`、`/dev/video4`、`/dev/video6`、`/dev/video8`。
- 气动/电磁执行机构和独立急停装置。

## Arduino

正式固件入口为 `firmware/gripper_controller/gripper_controller.ino`，波特率为 `115200`。
旧的不带辅助电磁铁版本保存在 `firmware/legacy/`，波特率为 `9600`，不要与当前 Python 配置混用。

上传示例（按实际板卡 FQBN 和端口替换）：

```bash
arduino-cli compile --fqbn <FQBN> firmware/gripper_controller
arduino-cli upload -p /dev/ttyUSB0 --fqbn <FQBN> firmware/gripper_controller
```

## Linux 设备权限

当前用户需要访问串口、摄像头和 ODrive USB 设备。常见发行版使用 `dialout`、`video`
用户组及 ODrive udev 规则。重新插拔设备后用以下命令确认设备名：

```bash
ls -l /dev/ttyUSB* /dev/video*
v4l2-ctl --list-devices
```

优先使用 `/dev/v4l/by-id/` 稳定链接作为相机环境变量，避免 USB 枚举顺序变化。

## 首次上机检查

1. 断开机械负载或保证双臂有充分运动空间，确认急停可用。
2. 核对 ODrive 编码器方向、索引和轴号，确认标定角 `0.122`、`0.1315` 适用于当前机构。
3. 单独验证 Arduino 每条串口命令，解决 `CP`、`OP` 固件协议缺口。
4. 单独打开四路相机，检查画面顺序、分辨率、曝光和色块采样位置。
5. 低速执行单轴 90 度动作，再进行空载完整流程，最后才允许装入魔方。
