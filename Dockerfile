# 選擇基礎映像
FROM python:3.9

# 設定工作目錄為/app
WORKDIR /app

# 複製專案代碼到容器中的/app目錄
COPY . /app

# 更新apt-get
RUN apt-get update -y 

# 改成台北時區
RUN apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

# 安裝相關套件
RUN pip install -r requirements.txt

# # 監聽 port號
# EXPOSE 5002

# 定義容器啟動後要執行的命令
CMD ["python", "app.py"]


