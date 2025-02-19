import pandas as pd
import uuid
from datetime import datetime

# 读取原始CSV文件
input_file = '../data/classified_data.csv'
df = pd.read_csv(input_file)

# 创建新的DataFrame来存储转换后的数据
new_df = pd.DataFrame()

# 添加id字段，按顺序排列
new_df['id'] = range(1, len(df) + 1)

# 添加sys_platform字段，均填为xhs
new_df['sys_platform'] = 'xhs'

# 添加uuid字段，由系统生成
new_df['uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]

# 添加bstudio_create_time字段，使用当前时间
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
new_df['bstudio_create_time'] = [current_time] * len(df)

# 添加main字段，为原始的desc内容
new_df['main'] = df['desc']

# 添加tag字段，为原始的标签内容
new_df['tag'] = df['标签']

# 将转换后的数据保存为新的CSV文件
output_file = '../data/output.csv'
new_df.to_csv(output_file, index=False)

print(f"转换完成，结果已保存到 {output_file}")