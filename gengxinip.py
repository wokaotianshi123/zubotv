import requests
import re

# 定义fofa链接
fofa_url = 'https://fofa.info/result?qbase64=InVkcHh5IiAmJiBjaXR5PSJDaGVuZ2R1Ig%3D%3D'

# 尝试从fofa链接提取IP地址和端口号
def extract_ip_port(fofa_url):
    try:
        response = requests.get(fofa_url)
        html_content = response.text
        match = re.search(r'(\d+\.\d+\.\d+\.\d+:\d+)', html_content)
        return match.group(1) if match else None
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

# 提取IP地址和端口号
new_ip_port = extract_ip_port(fofa_url)

# 如果成功提取了新的IP地址和端口号
if new_ip_port:
    # 定义两个在线文件的原始URL
    original_file_urls = [
        'https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuan/sichuanzubo.txt',
        'https://raw.githubusercontent.com/wokaotianshi123/zubotv/main/sichuan/sichuanzubo.m3u'
    ]

    # 遍历原始URL列表，并生成新的文件
    for original_file_url in original_file_urls:
        try:
            # 读取原始文件内容
            response = requests.get(original_file_url)
            file_content = response.text

            # 替换文件中的IP地址和端口号
            updated_content = re.sub(r'(http://\d+\.\d+\.\d+\.\d+:\d+)', f'http://{new_ip_port}', file_content)

            # 保存更新后的内容到新文件
            filename = original_file_url.split('/')[-1]
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(updated_content)

            print(f"文件 {filename} 已更新并保存。")
        except requests.RequestException as e:
            print(f"无法更新文件 {original_file_url}，错误: {e}")
else:
    print("没有提取到新的IP地址和端口号。")
