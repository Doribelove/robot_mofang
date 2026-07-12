环境说明：
	python		3.7.1
	opencv-python 	4.5.4-dev
	odrive 		0.5.1.post0
	RubikTwoPhase
	
环境配置：
	1.安装python3.7 
	2.pip install opencv-python
	3.pip install odrive==0.5.1.post0
	4.pip install RubikTwoPhase


RubikTwoPhase: https://github.com/hkociemba/RubiksCube-TwophaseSolver


操作注意：
	1初始化后使用夹子固定双爪
	2放魔方时手必须挡住魔方色块，避免被相机识别到魔方状态
	3手移开后，相机识别到魔方，自动夹魔方，夹子自动掉落，开始复原（注意安全）
