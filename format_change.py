import re

def read_markdown_file(file_path):
    """读取Markdown文件的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return None

def process_markdown(content):
    """处理Markdown内容：读取文章标题、升级标题、替换数学公式"""
    updated_lines = []
    inline_math_pattern = r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)'

    # 读取并处理文章标题
    article_title = content[0].strip().lstrip('# ').replace(' ', '_')
    
    for line in content:
        # 升级标题
        if line.startswith('#'):
            line = '#' + line

        # 替换内联数学公式
        line = re.sub(inline_math_pattern, lambda m: r'\\(' + m.group(1) + r'\\)', line)

        updated_lines.append(line)

    return ''.join(updated_lines)

def save_updated_content(content, output_path):
    """将更新后的内容保存到新的文件中"""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    file_path = 'E:\OneDrive\Github Pages\Buezwqwg\content\docs\EMCS_Engineering Chemistry & Materials Science\MCMS5.FurtherOnStressStrain\index.md'  # 指定原文件路径
    output_path = file_path  # 指定输出文件路径
    
    # 读取文件内容
    content = read_markdown_file(file_path)
    
    if content:
        # 处理标题升级、数学公式替换
        updated_content = process_markdown(content)
        
        # 保存更新后的内容
        save_updated_content(updated_content, output_path)
        print("内容已更新并保存到:", output_path)
