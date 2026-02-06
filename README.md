# HeartRate to VRC

VRC心率OSC工具 - 支持 BLE 蓝牙和 Pulsoid 双数据源

## 功能特性

- **BLE 蓝牙模式**：通过 PC 蓝牙连接支持标准心率广播协议的设备（如小米手环）
- **Pulsoid 模式**：通过 Pulsoid/Stromno WebSocket API 获取心率数据
- **OSC 输出**：实时发送心率数据到 VRChat
- **OBS 模式**：输出心率到 `rate.txt` 文件，便于 OBS 调用

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 方式一：BLE 蓝牙模式

1. 打开手环的心率广播功能
2. 确保电脑蓝牙已开启
3. 在"配置"标签页设置设备名称（支持模糊匹配）
4. 点击"连接并发送参数"

### 方式二：Pulsoid 模式

1. 访问 [pulsoid.net](https://pulsoid.net) 注册并获取 Widget ID
2. 在"配置"标签页选择数据源为 "Pulsoid"
3. 输入 Widget ID
4. 点击"连接并发送参数"

## 配置说明

### OSC 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| IP 地址 | 127.0.0.1 | OSC 目标地址 |
| 端口 | 9000 | VRChat OSC 默认端口 |
| int 参数 | /avatar/parameters/HR | 心率整数值 |
| float 参数 | /avatar/parameters/HRF | 心率百分比 (0.0-1.0) |
| bool 参数 | /avatar/parameters/isHRActive | 连接状态 |

### 心率范围

- **最低心率 / 最高心率**：仅影响 float 参数的计算

### 工作模式

- **普通模式**：仅发送 OSC
- **OBS 模式**：同时输出 `rate.txt` 文件

## 界面预览

<img width="578" height="452" alt="配置界面" src="https://github.com/user-attachments/assets/6251d020-1854-4e45-a7a3-893f925e4a69" />

<img width="502" height="632" alt="监控界面" src="https://github.com/user-attachments/assets/31ed0798-bad3-434a-880e-65a3e6540f0e" />
