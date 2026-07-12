# 工具脚本

这些脚本直接复用 `src/` 中的模块，因此从仓库根目录运行时需要设置 `PYTHONPATH`：

```bash
PYTHONPATH=src python tools/diagnostics/vision_test.py
PYTHONPATH=src python tools/diagnostics/hardwaretest.py
PYTHONPATH=src python tools/diagnostics/odrive_test.py
PYTHONPATH=src python tools/diagnostics/adjust_odrive_speed.py
```

上述诊断脚本大多会直接连接或驱动硬件。运行前应阅读代码、移除机械负载并准备急停。

`calibration/point.py` 用于在图像上点击并记录视觉采样坐标。它沿用原程序行为，默认读取
当前目录的 `44.jpg`，并将点击结果写入当前目录的 `points.txt`：

```bash
python tools/calibration/point.py
```
