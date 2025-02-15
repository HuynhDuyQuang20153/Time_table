# Sử dụng hình ảnh Python chính thức
FROM python:3.13.1-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép mã nguồn vào container
COPY . .

USER root

# Cài đặt các công cụ cần thiết trước khi cài đặt thư viện Python
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libmariadb-dev \
    gcc \
    && apt-get clean

# Cài đặt các thư viện cần thiết
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Mở cổng 5000 cho Flask
EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["python", "app.py"]