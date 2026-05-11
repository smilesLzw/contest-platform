"""初始化数据库：创建表、插入初始数据"""
import asyncio
from sqlalchemy import select, func
from app.database import engine, async_session, Base
from app.models import User, Major, AiCategory
from app.core.security import hash_password


async def init():
    """创建表并插入初始数据"""
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        # 检查是否已有管理员
        result = await db.execute(select(func.count(User.id)))
        user_count = result.scalar() or 0
        if user_count == 0:
            admin = User(
                username="admin",
                password_hash=hash_password("Admin@123456"),
                role="admin",
                name="超级管理员",
                department="学院办公室",
                status=1,
            )
            db.add(admin)

        # 插入专业数据
        cnt = await db.scalar(select(func.count(Major.id)))
        if cnt == 0:
            majors = [
                Major(name="计算机科学与技术", sort_order=1),
                Major(name="软件工程", sort_order=2),
                Major(name="数字媒体技术", sort_order=3),
                Major(name="人工智能", sort_order=4),
                Major(name="网络工程", sort_order=5),
            ]
            db.add_all(majors)

        # 插入AI工具分类
        cnt = await db.scalar(select(func.count(AiCategory.id)))
        if cnt == 0:
            categories = [
                AiCategory(name="编程开发", icon="Monitor", sort_order=1),
                AiCategory(name="图像生成与处理", icon="Picture", sort_order=2),
                AiCategory(name="写作与文案", icon="Edit", sort_order=3),
                AiCategory(name="视频制作", icon="VideoCamera", sort_order=4),
                AiCategory(name="数据分析", icon="DataAnalysis", sort_order=5),
                AiCategory(name="演示文稿", icon="Presentation", sort_order=6),
                AiCategory(name="语音与音频", icon="Microphone", sort_order=7),
                AiCategory(name="综合大模型", icon="ChatDotRound", sort_order=8),
            ]
            db.add_all(categories)

        await db.commit()
        print("✅ 数据库初始化完成：表已创建，初始数据已插入")


if __name__ == "__main__":
    asyncio.run(init())
