FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# 复制所有文件到容器中
COPY . .

# 设置环境变量
ENV PORT 8501

# 运行Streamlit应用
CMD streamlit run app.py --server.port $PORT
