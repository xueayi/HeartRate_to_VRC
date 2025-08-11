import asyncio
import time

from bleak import BleakScanner, BleakClient
from pythonosc.udp_client import SimpleUDPClient
import configparser

# --- 配置区 ---
# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

OSC_IP = config.get('DATABASE', 'osc_ip')
OSC_PORT = config.getint('DATABASE','osc_port')
OSC_int = config.get('DATABASE', 'osc_int')
OSC_float = config.get('DATABASE', 'osc_float')
HR_min = config.getint('DATABASE','hr_min')
HR_max = config.getint('DATABASE','hr_max')
OSC_bool = config.get('DATABASE', 'osc_bool')
Dev_name = config.get('DATABASE', 'device_name')
OBS_mode = config.getint('DATABASE','obs_mode')

# BLE (蓝牙)
# 将所有可能的目标设备名称片段放入这个列表中
# 脚本会连接第一个名字包含列表中任意一个字符串的设备
TARGET_DEVICE_NAMES = [Dev_name]
XIAOMI_HEARTRATE_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# --- 初始化客户端 ---
osc_client = SimpleUDPClient(OSC_IP, OSC_PORT)


def send_osc(heart_rate):
    """
    格式化心率数据并通过OSC发送.
    """
    percent = heart_rate
    percent_f = min(heart_rate / HR_max,HR_min)
    osc_client.send_message(OSC_bool, True)
    osc_client.send_message(OSC_int, percent)
    osc_client.send_message(OSC_float, percent_f)
    # 返回格式化后的字符串，方便在主循环中打印
    return f"心率整数值: {heart_rate}; 心率浮点值: {percent_f:.2f}"


async def notification_handler(sender, data):
    """
    处理从手环收到的心率通知.
    蓝牙GATT心率服务规范:
    - data[0] 是 Flags 字节.
    - data[1] 是心率值 (当Flags的最低位为0时，格式为UINT8).
    """
    if len(data) >= 2:
        heart_rate = data[1]
        vrc_status = send_osc(heart_rate)
        # 将所有状态信息在一行内打印，并使用 \r 回车符实现原地刷新
        if OBS_mode == 0:
            print(f"\r实时心率 -> {vrc_status}", end="")
        elif OBS_mode == 1:
            print(f"\r实时心率 -> {vrc_status},正在输出txt.", end="")
            with open("rate.txt", "w", encoding="utf-8") as frate:
                frate.write(f"{heart_rate}")




async def find_target_device():
    """
    扫描并查找名称包含目标关键字列表中的任意一个的设备。
    """
    scan = 1
    print("开始扫描蓝牙心率设备，共5次。\n")
    time.sleep(3)
    while scan <= 5 :
        print(f"\r正在扫描蓝牙设备...第{scan}次")
        devices = await BleakScanner.discover()  # timeout=20.0

        for device in devices:
            # 确保设备有名称 (device.name 不为 None)
            if device.name:
                for target_name in TARGET_DEVICE_NAMES:
                    if target_name in device.name:
                        print(f"成功找到目标设备: {device.name} ({device.address})")
                        return device  # 返回找到的第一个匹配设备
        print(f"第{scan}次扫描结束，未找到指定设备，开始下一次扫描。")
        time.sleep(1)
        scan += 1
    return None  # 如果循环结束仍未找到，则返回 None


async def main_loop():
    """
    主循环，负责设备查找、连接和自动重连。
    """
    device = await find_target_device()

    if not device:
        print(f"错误：扫描结束，未找到名称包含 {TARGET_DEVICE_NAMES} 的设备。")
        print("请检查设备是否在附近、已开启蓝牙且未被其他程序连接。")
        print("程序将在10秒后退出。")
        time.sleep(10)
        return

    print("准备连接并获取心率数据...")

    while True:  # 自动重连循环
        try:
            async with BleakClient(device.address) as client:
                if client.is_connected:
                    print("\n设备连接成功！正在监听心率...")
                    # <--- 新增功能: 在此处输出OSC目标地址
                    print(f"正在向 OSC 地址 {OSC_IP}:{OSC_PORT} 发送当前心率。如需退出请按Ctrl+C。")

                    await client.start_notify(XIAOMI_HEARTRATE_CHAR_UUID, notification_handler)
                    # 保持连接状态
                    while client.is_connected:
                        await asyncio.sleep(1)
        except Exception as e:
            print(f"\n连接断开或发生错误: {e}")
            print("将在5秒后尝试重新连接...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n程序被用户手动停止。")
        osc_client.send_message(OSC_bool, False)
    except Exception as e:
        print(f"\n程序出现未处理的异常: {e}")