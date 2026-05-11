"""应用配置，从环境变量读取"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+asyncmy://root:password@localhost:3306/contest_platform")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 5 * 1024 * 1024))
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50 * 1024 * 1024))

# 允许的图片类型
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
# 允许的文件类型
ALLOWED_FILE_TYPES = {"application/pdf", "application/zip", "application/x-zip-compressed"}
