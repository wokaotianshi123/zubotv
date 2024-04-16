import requests
import re

# 定义fofa链接
fofa_url = 'https://fofa.info/result?qbase64=dWRweHkmJmNpdHk9IkNoZW5nZHUi'

# 尝试从fofa链接提取IP地址和端口号
def extract_ip_ports(fofa_url):
    try:
        response = requests.get(fofa_url)
        html_content = response.text
        ips_ports = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)', html_content)
        return ips_ports if ips_ports else None
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 提取IP地址和端口号
ips_ports = extract_ip_ports(fofa_url)

# 如果成功提取了IP地址和端口号
if ips_ports:
    # 测试每个IP地址和端口号，直到找到一个可以访问的
    for ip_port in ips_ports:
        new_link = f'http://{ip_port}/udp/239.93.0.184:5140'
        try:
            response = requests.get(new_link, timeout=10)
            if response.status_code == 200:
                print(f'找到可访问的链接: {new_link}')
                # 采用这个IP地址和端口号进行后续操作
                new_ip_port = ip_port
                break
            else:
                print(f'链接 {new_link} 不可访问，继续尝试其他IP地址。')
        except requests.RequestException as e:
            print(f'链接 {new_link} 访问出错: {e}')
    else:
        print("没有找到可访问的IP地址和端口号。")
        exit()

    # 定义需要更新的文件列表
    files_to_update = [
        {'url': 'https://gitjs.wokaotianshi123.cloudns.org/https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuan/sichuanzubo.txt', 'filename': 'sichuanzubo.txt'},
        {'url': 'https://gitjs.wokaotianshi123.cloudns.org/https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuan/sichuanzubo.m3u', 'filename': 'sichuanzubo.m3u'}
    ]

    # 更新文件中的IP地址和端口号
    for file_info in files_to_update:
        try:
            # 读取原始文件内容
            response = requests.get(file_info['url'])
            file_content = response.text

            # 替换文件中的IP地址和端口号
            updated_content = re.sub(r'(http://\d+\.\d+\.\d+\.\d+:\d+)', f'http://{new_ip_port}', file_content)

            # 保存更新后的内容到新文件
            with open(file_info['filename'], 'w', encoding='utf-8') as file:
                file.write(updated_content)

            print(f"文件 {file_info['filename']} 已更新并保存。")
        except requests.RequestException as e:
            print(f"无法更新文件 {file_info['filename']}，错误: {e}")

else:
    print("没有提取到IP地址和端口号。")
