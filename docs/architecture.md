# 系统架构

## 主流程

```text
四路 USB 摄像头
      |
      v
vision_.py -- 颜色识别 --> 54 位魔方状态
      |                         |
      |                         v
      |                  RubikTwoPhase 求解
      |                         |
      v                         v
Function.py --> jixiecost.py --> 机械动作序列
                                      |
                         +------------+------------+
                         v                         v
                    moving.py                  hardware.py
                         |                  ODrive + Arduino
                         +------------+------------+
                                      v
                                双臂与夹爪动作
```

## 模块职责

| 模块 | 职责 |
| --- | --- |
| `main.py` | 初始化、等待人工确认、启动识别与收尾释放 |
| `vision_.py` | 四路图像采集、色块采样、状态合法性判断 |
| `Function.py` | 串联识别、求解、动作优化和执行 |
| `jixiecost.py` | 将魔方公式转成更低机械代价的动作 |
| `moving.py` | 执行左右手腕和夹爪的动作序列 |
| `hardware.py` | ODrive 轴控制和 Arduino 串口协议 |
| `KociembaTrans.py` | 早期公式到机械动作的转换实现，仍被部分模块引用 |

## 坐标与标定

视觉采样坐标和四组颜色阈值目前写在 `src/vision_.py` 中，对应获奖设备的相机位置、
光照和分辨率。更换相机、支架、曝光或背景后必须重新标定。辅助标点工具位于
`tools/calibration/point.py`，公式与机械坐标说明见 `docs/assets/cube-notation.png`
和 `docs/coordinate-system.txt`。

## 已知工程约束

1. 正式代码会发送 `CP`、`OP`、`RC`、`RO`、`LC`、`LO`、`AC`、`AO` 命令。
2. 仓库中的 Arduino 固件实现了 `RC`、`RO`、`LC`、`LO`、`AC`、`AO`、`LP`、`RP`、`AP`，
   但没有实现 `CP` 和 `OP`。这说明比赛现场的最终控制器固件可能未完整回存；上机前必须核对，
   不能假定当前固件与 Python 端完全匹配。
3. ODrive 参数快照来源较多，`config/odrive/` 保留原始命名和内容，不应未经台架测试直接批量写入。
4. 这是实时硬件程序，普通 CI 只能验证语法和纯求解逻辑，无法证明机械安全或时序正确。
