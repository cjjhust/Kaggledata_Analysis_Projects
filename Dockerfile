# 使用基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 先把依赖列表拷进去
COPY requirements.txt .

# 执行安装（这只会在构建镜像时运行一次）
RUN pip install --no-cache-dir -r requirements.txt

# 镜像构建完成后，不需要写 command 安装了
# 暴露 Streamlit 默认端口
EXPOSE 8501