"""应用配置，从环境变量读取"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+asyncmy://root:password@localhost:3306/contest_platform")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 10 * 1024 * 1024))      # 10 MB
MAX_AUDIO_SIZE = int(os.getenv("MAX_AUDIO_SIZE", 100 * 1024 * 1024))     # 100 MB
MAX_VIDEO_SIZE = int(os.getenv("MAX_VIDEO_SIZE", 1024 * 1024 * 1024))    # 1 GB
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50 * 1024 * 1024))

# 允许的图片类型
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/svg+xml"}
# 允许的音频类型
ALLOWED_AUDIO_TYPES = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/aac", "audio/flac", "audio/mp4", "audio/x-m4a"}
# 允许的视频类型
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}
# 允许的文件类型
ALLOWED_FILE_TYPES = {"application/pdf", "application/zip", "application/x-zip-compressed"}
