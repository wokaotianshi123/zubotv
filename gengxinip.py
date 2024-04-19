import requests
import re
import socket

# 定义fofa链接
fofa_url = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjaXR5PSJDaGVuZ2R1Ig%3D%3D'

# 尝试从fofa链接提取IP地址和端口号，并去除重复项，同时排除端口4022
def extract_unique_ip_ports(fofa_url):
    try:
        response = requests.get(fofa_url)
        html_content = response.text
        # 使用正则表达式匹配IP地址和端口号，但排除端口4022
        ips_ports = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)', html_content)
        unique_ips_ports = list(set(ips_ports))  # 去除重复的IP地址和端口号
        # 排除端口为4022的IP地址和端口组合
        unique_ips_ports = [ip_port for ip_port in unique_ips_ports if not int(ip_port.split(':')[-1]) == 4023]
        return unique_ips_ports if unique_ips_ports else None
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 检查HTTP服务的可达性
def check_http_service_connectivity(ip_port):
    try:
        # 尝试连接IP和端口
        ip, port_str = ip_port.split(':')
        port = int(port_str)
        with socket.create_connection((ip, port), timeout=5) as sock:
            if sock:
                return ip_port  # 返回可访问的服务的IP和端口
    except (socket.timeout, socket.error, ValueError):
        return None

# 更新文件中的IP地址和端口号
def update_files(accessible_ip_port, files_to_update):
    for file_info in files_to_update:
        try:
            # 读取原始文件内容
            response = requests.get(file_info['url'])
            file_content = response.text

            # 替换文件中的IP地址和端口号
            # 假设文件中的IP地址和端口号格式为 http://IP:PORT
            updated_content = re.sub(r'(http://\d+\.\d+\.\d+\.\d+:\d+)', f'http://{accessible_ip_port}', file_content)

            # 保存更新后的内容到新文件
            with open(file_info['filename'], 'w', encoding='utf-8') as file:
                file.write(updated_content)

            print(f"文件 {file_info['filename']} 已更新并保存。")
        except requests.RequestException as e:
            print(f"无法更新文件 {file_info['filename']}，错误: {e}")

# 提取唯一的IP地址和端口号
unique_ips_ports = extract_unique_ip_ports(fofa_url)

if unique_ips_ports:
    print("提取到的唯一IP地址和端口号（排除了端口4022）:")
    for ip_port in unique_ips_ports:
        print(ip_port)
    
    # 测试每个IP地址和端口号，直到找到一个可访问的
    accessible_ip_port = None
    for ip_port in unique_ips_ports:
        accessible_ip_port = check_http_service_connectivity(ip_port)
        if accessible_ip_port:
            break

    if accessible_ip_port:
        print(f"找到可访问的服务: {accessible_ip_port}")
        # 定义需要更新的文件列表
        files_to_update = [
           {'url': 'https://gitjs.wokaotianshi123.cloudns.org/https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuan/sichuanzubo.txt', 'filename': 'sichuanzubo.txt'},
           {'url': 'https://gitjs.wokaotianshi123.cloudns.org/https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuan/sichuanzubo.m3u', 'filename': 'sichuanzubo.m3u'}
        ]

        # 更新文件中的IP地址和端口号
        update_files(accessible_ip_port, files_to_update)
    else:
        print("没有找到可访问的服务。")
else:
    print("没有提取到IP地址和端口号。")
