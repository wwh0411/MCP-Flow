import os
import gzip
import json
import random
import glob
import pickle

# 设置本地数据集目录
data_dir = ""
index_file = "source_index.pkl"

# 全局变量存储索引 - 改为存储文件位置而不是完整text
source_index = {}  # {source: [(file_path, line_number), ...]}
source_set = set()

def save_source_index():
    """保存source索引到文件"""
    global source_index, source_set
    
    index_data = {
        'source_index': source_index,
        'source_set': source_set
    }
    
    try:
        with open(index_file, 'wb') as f:
            pickle.dump(index_data, f)
        print(f"索引已保存到: {index_file}")
        
        # 显示索引大小
        file_size = os.path.getsize(index_file) / (1024 * 1024)  # MB
        print(f"索引文件大小: {file_size:.2f} MB")
        return True
    except Exception as e:
        print(f"保存索引失败: {e}")
        return False

def load_source_index():
    """从文件加载source索引"""
    global source_index, source_set
    
    if not os.path.exists(index_file):
        print(f"索引文件不存在: {index_file}")
        return False
    
    try:
        with open(index_file, 'rb') as f:
            index_data = pickle.load(f)
        
        source_index = index_data['source_index']
        source_set = index_data['source_set']
        
        file_size = os.path.getsize(index_file) / (1024 * 1024)  # MB
        print(f"索引已从文件加载: {index_file}")
        print(f"索引文件大小: {file_size:.2f} MB")
        print(f"加载了 {len(source_set)} 种source，共 {sum(len(positions) for positions in source_index.values())} 条数据")
        return True
    except Exception as e:
        print(f"加载索引失败: {e}")
        return False

def build_source_index():
    """构建source索引，只存储文件位置和行号"""
    global source_index, source_set
    
    print("正在构建source索引...")
    files = glob.glob(f"{data_dir}/*.json.gz")
    print(f"找到 {len(files)} 个文件")
    
    total_samples = 0
    
    for file_path in files:
        try:
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        data = json.loads(line.strip())
                        source = data.get('source', 'unknown')
                        text = data.get('text', '')
                        
                        if text:  # 确保text不为空
                            if source not in source_index:
                                source_index[source] = []
                            # 只存储文件路径和行号，不存储text内容
                            source_index[source].append((file_path, line_num))
                            source_set.add(source)
                            
                        total_samples += 1
                        
                        # 每处理10000个样本打印一次进度
                        if total_samples % 10000 == 0:
                            print(f"已处理 {total_samples} 个样本，发现 {len(source_set)} 种source...")
                            
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            continue
    
    print(f"\n索引构建完成！")
    print(f"总共处理了 {total_samples} 个样本")
    print(f"发现 {len(source_set)} 种不同的source:")
    
    # 显示每种source的数量
    for source in sorted(source_set):
        count = len(source_index[source])
        print(f"  - {source}: {count} 条数据")
    
    # 自动保存索引
    save_source_index()

def get_text_from_position(file_path, line_num):
    """根据文件路径和行号获取text内容"""
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if i == line_num:
                    data = json.loads(line.strip())
                    return data.get('text', '')
    except Exception as e:
        print(f"读取文件 {file_path} 第 {line_num} 行时出错: {e}")
        return None

def get_random_text_by_source(target_source):
    """
    根据source选择随机返回一条数据的text（快速版本）
    
    Args:
        target_source (str): 目标source名称
        
    Returns:
        str: 随机选择的text，如果没找到返回None
    """
    # 自动检查并初始化索引
    if not source_index:
        print("索引未初始化，正在自动初始化...")
        initialize_index()
    
    # mapping_dict = {
        
    # }

    # if target_source in ["file"]:
    #     target_source = ""
        
    if target_source not in source_index:
        print(f"错误: source '{target_source}' 不存在")
        print(f"可用的source: {sorted(source_set)}")
        return None
    
    # 随机选择一个位置
    positions = source_index[target_source]
    file_path, line_num = random.choice(positions)
    
    # 根据位置获取text
    selected_text = get_text_from_position(file_path, line_num)
    
    return selected_text

def get_available_sources():
    """获取所有可用的source列表"""
    # 自动检查并初始化索引
    if not source_index:
        print("索引未初始化，正在自动初始化...")
        initialize_index()
    
    return sorted(source_set)

def ensure_index_loaded():
    """确保索引已加载，如果没有则自动初始化"""
    if not source_index:
        print("索引未初始化，正在自动初始化...")
        initialize_index()
    return True

def initialize_index():
    """初始化索引：尝试加载，如果失败则构建"""
    print("正在初始化索引...")
    
    # 尝试加载现有索引
    if load_source_index():
        print("成功加载现有索引！")
        return True
    else:
        print("加载失败，开始构建新索引...")
        build_source_index()
        return True

# 初始化时构建索引
if __name__ == "__main__":
    initialize_index()
    
    # 测试函数
    print("\n" + "="*50)
    print("测试函数:")
    
    if source_set:
        example_source = sorted(source_set)[0]
        print(f"使用source '{example_source}' 作为示例:")
        
        result = get_random_text_by_source(example_source)
        if result:
            print(f"\n随机选择的text (前200字符):")
            print(f"{result[:200]}...")
    else:
        print("没有找到任何source数据")

    