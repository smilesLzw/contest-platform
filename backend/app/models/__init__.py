from app.models.user import User
from app.models.major import Major
from app.models.work import Work
from app.models.news import News
from app.models.ai_category import AiCategory
from app.models.ai_tool import AiTool
from app.models.operation_log import OperationLog
from app.models.bg_music import BackgroundMusic

__all__ = [
    "User", "Major", "Work", "News",
    "AiCategory", "AiTool", "OperationLog", "BackgroundMusic",
]
