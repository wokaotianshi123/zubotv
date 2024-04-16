import requests
import socket
import re

# 定义fofa链接
fofa_url = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjaXR5PSJDaGVuZ2R1Ig%3D%3D'

# 尝试从fofa链接提取IP地址和端口号，并去除重复项
def extract_unique_ip_ports(fofa_url):
    try:
        response = requests.get(fofa_url)
        html_content = response.text
        ips_ports = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)', html_content)
        unique_ips_ports = list(set(ips_ports))  # 去除重复的IP地址和端口号
        return unique_ips_ports if unique_ips_ports else None
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 检查IP地址和端口的连通性
def check_ip_port_connectivity(ip_port):
    try:
        # 解析IP地址和端口
        ip, port_str = ip_port.split(':')
        port = int(port_str)
        # 目标地址
        target_address = f'/udp/239.93.0.184:5140'
        # 创建UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # 尝试连接
            s.settimeout(5)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f'IP地址 {ip_port} 与目标 {target_address} 连通。')
                return True
            else:
                print(f'IP地址 {ip_port} 与目标 {target_address} 不连通。')
                return False
    except Exception as e:
        print(f'检查 {ip_port} 时出错: {e}')
        return False

# 提取唯一的IP地址和端口号
unique_ips_ports = extract_unique_ip_ports(fofa_url)

# 如果成功提取了唯一的IP地址和端口号
if unique_ips_ports:
    print("提取到的唯一IP地址和端口号:")
    for ip_port in unique_ips_ports:
        print(ip_port)
    
    # 测试每个IP地址和端口号，直到找到一个可访问的
    accessible_ip_port = None
    for ip_port in unique_ips_ports:
        if check_ip_port_connectivity(ip_port):
            accessible_ip_port = ip_port
            break

    if accessible_ip_port:
        # 定义需要更新的文件列表
        files_to_update = [
            {'url': 'https://gitjs.wokaotianshi123.cloudns.org/https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuanzubo.txt', 'filename': 'sichuanzubo.txt'},
            {'url': 'https://gitjs.wokaotianshi123.cloudns.org/https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuanzubo.m3u', 'filename': 'sichuanzubo.m3u'}
        ]

        # 更新文件中的IP地址和端口号
        for file_info in files_to_update:
            try:
                # 读取原始文件内容
                response = requests.get(file_info['url'])
                file_content = response.text

                # 替换文件中的IP地址和端口号
                updated_content = re.sub(r'(http://\d+\.\d+\.\d+\.\d+:\d+)', f'http://{accessible_ip_port}', file_content)

                # 保存更新后的内容到新文件
                with open(file_info['filename'], 'w', encoding='utf-8') as file:
                    file.write(updated_content)

                print(f"文件 {file_info['filename']} 已更新并保存。")
            except requests.RequestException as e:
                print(f"无法更新文件 {file_info['filename']}，错误: {e}")

    else:
        print("没有找到可访问的IP地址和端口号。")
else:
    print("没有提取到IP地址和端口号。")
