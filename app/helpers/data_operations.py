import pandas as pd
import re

def extract_and_sort_row(df, row_number, sort_method):
    # 提取指定行的内容并确保所有数据都是字符串类型
    data_row = [str(item) for item in df.iloc[row_number].tolist()]

    # 根据所选的排序方法进行排序
    if sort_method == "字母顺序":
        return sorted(data_row)
    elif sort_method == "字母逆序":
        return sorted(data_row, reverse=True)
    elif sort_method == "长度递增":
        return sorted(data_row, key=len)
    elif sort_method == "长度递减":
        return sorted(data_row, key=len, reverse=True)
    else:
        return data_row
    
# 定义一个函数来处理每一行的文本内容
def remove_proci(line):
    for i in range(20, 0, -1):
        line = line.replace(f"proc{i}", "")
    line = re.sub(r"_+", "_", line)
    line = line.strip("_")
    return line
