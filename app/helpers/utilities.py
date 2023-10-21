import base64


def get_txt_download_link(data):
    txt = "\n".join(str(x) for x in data)
    b64 = base64.b64encode(txt.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="sorted_data.txt">点击下载 TXT 文件</a>'
    return href


def get_csv_download_link(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="processed_data.csv">点击下载 CSV 文件</a>'
