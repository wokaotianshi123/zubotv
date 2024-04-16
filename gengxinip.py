import requests
import re
import random

# 定义一个函数来获取包含特定端口的IP和端口列表
def get_unique_ip_port(port_list):
    response = requests.get('https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjaXR5PSJDaGVuZ2R1Ig%3D%3D')
    if response.status_code == 200:
        lines = response.text.split('\n')
        ips_ports = set()  # 使用集合来避免重复
        for line in lines:
            match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)', line)
            if match and any(str(port) in match.group(2) for port in port_list):
                ips_ports.add((match.group(1), match.group(2)))
        return list(ips_ports)
    return []

# 从给定的IP和端口列表中随机选择一个唯一的IP和端口
def choose_unique_ip_port(ips_ports):
    if ips_ports:
        return random.choice(ips_ports)
    return None

# 定义端口列表
port_list = ['8889', '8123']

# 获取IP和端口列表
ips_ports = get_unique_ip_port(port_list)

# 选择一个唯一的IP和端口
unique_ip_port = choose_unique_ip_port(ips_ports)

if unique_ip_port:
    # 定义文件URL集合
    file_urls = [
        'https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuanzubo.txt',
        'https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuanzubo.m3u'
    ]
    
    # 遍历URL集合，修改并保存每个文件的内容
    for url in file_urls:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            # 替换文件内容中的IP和端口
            modified_content = re.sub(r'(http://[\d\.]+):(\d+)', f'http://{unique_ip_port[0]}:{unique_ip_port[1]}', content)
            # 保存修改后的内容到本地文件
            with open(url.split('/')[-1], 'w', encoding='utf-8') as file:
                file.write(modified_content)
            print(f"File {url.split('/')[-1]} has been modified and saved.")
else:
    print("No unique IP and port available to modify the files.")
