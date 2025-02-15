# Dockerfile
FROM python:3.9

# Đặt thư mục làm việc
WORKDIR /app

# Cài đặt các phụ thuộc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . .

# Chạy lệnh khởi động Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]