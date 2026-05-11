"""批量导入AI工具数据（含logo、国内优先排序）"""
import asyncio
from sqlalchemy import select, func, delete
from app.database import async_session
from app.models.ai_tool import AiTool
from app.models.ai_category import AiCategory

def favicon(domain):
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=64"

def data():
    """返回所有工具: (name, url, logo_url, description, category_key, is_free, rating, sort_order)"""
    D = "国内"
    I = "国际"
    return [
        # ==================== 综合大模型 ====================
        # ---- 国内 ----
        ("DeepSeek", "https://chat.deepseek.com", favicon("chat.deepseek.com"),
         "深度求索出品，国产开源大模型，超低API成本，OpenAI兼容接口，编程推理能力出众", "综合大模型", 1, 5, 1, D),
        ("通义千问 (Qwen)", "https://tongyi.aliyun.com", favicon("tongyi.aliyun.com"),
         "阿里云出品，中英文双语优秀，开源可商用，阿里云生态深度集成，支持160+语言", "综合大模型", 1, 5, 2, D),
        ("文心一言 (ERNIE Bot)", "https://yiyan.baidu.com", favicon("yiyan.baidu.com"),
         "百度出品，中文理解能力领先，深度整合百度搜索和文心生态，支持多模态交互", "综合大模型", 1, 4, 3, D),
        ("Kimi", "https://kimi.moonshot.cn", favicon("kimi.moonshot.cn"),
         "月之暗面出品，超长上下文窗口，擅长长文档分析和联网搜索，国内高人气AI助手", "综合大模型", 1, 4, 4, D),
        ("豆包 (Doubao)", "https://www.doubao.com", favicon("doubao.com"),
         "字节跳动出品，国内MAU最高的AI应用，集成浏览器插件，拍照答题等功能", "综合大模型", 1, 4, 5, D),
        ("智谱清言 (ChatGLM)", "https://chatglm.cn", favicon("chatglm.cn"),
         "智谱AI出品，基于GLM架构，支持多模态和智能体，清华系技术背景", "综合大模型", 1, 4, 6, D),
        ("讯飞星火 (Spark)", "https://xinghuo.xfyun.cn", favicon("xinghuo.xfyun.cn"),
         "科大讯飞出品，语音交互能力领先，多模态理解，教育办公场景深度优化", "综合大模型", 1, 4, 7, D),
        # ---- 国际 ----
        ("ChatGPT", "https://chatgpt.com", favicon("chatgpt.com"),
         "OpenAI旗舰产品，全球用户最多的AI助手，支持对话写作编程图像生成网页搜索", "综合大模型", 1, 5, 11, I),
        ("Claude", "https://claude.ai", favicon("claude.ai"),
         "Anthropic出品，最佳写作质量和代码能力，200K上下文，支持Projects和Skills", "综合大模型", 1, 5, 12, I),
        ("Gemini", "https://gemini.google.com", favicon("gemini.google.com"),
         "Google原生多模态大模型，2M超长上下文，深度集成搜索/Workspace/Android生态", "综合大模型", 1, 5, 13, I),
        ("Grok", "https://grok.com", favicon("grok.com"),
         "xAI出品，实时信息获取，独特幽默风格，深度集成X平台（Twitter）", "综合大模型", 1, 4, 14, I),
        ("Perplexity", "https://perplexity.ai", favicon("perplexity.ai"),
         "AI搜索引擎，实时联网回答附带引用来源，适合学术研究和事实核查", "综合大模型", 1, 4, 15, I),

        # ==================== 编程开发 ====================
        # ---- 国内 ----
        ("通义灵码 (Lingma)", "https://tongyi.aliyun.com/lingma", favicon("tongyi.aliyun.com"),
         "阿里云出品，免费AI编程助手，支持VS Code/JetBrains，中文代码理解出色", "编程开发", 1, 4, 1, D),
        ("文心快码 (Comate)", "https://comate.baidu.com", favicon("comate.baidu.com"),
         "百度出品，基于文心大模型，支持多IDE，中文注释生成代码，企业版可私有部署", "编程开发", 1, 4, 2, D),
        # ---- 国际 ----
        ("GitHub Copilot", "https://github.com/features/copilot", favicon("github.com"),
         "最大AI编程助手，15M+用户，多模型切换（Claude/Codex/Gemini），深度GitHub集成", "编程开发", 1, 5, 11, I),
        ("Cursor", "https://cursor.com", favicon("cursor.com"),
         "AI原生IDE（VS Code分支），代码库级索引，Composer多文件编辑，8并行子代理", "编程开发", 1, 5, 12, I),
        ("Claude Code", "https://claude.ai/code", favicon("claude.ai"),
         "终端AI编程代理，SWE-bench最佳（80.8%），Agent Teams多代理协作", "编程开发", 1, 5, 13, I),
        ("Windsurf", "https://windsurf.com", favicon("windsurf.com"),
         "40+IDE支持，Cascade跨会话记忆，免费无限代码补全，13x速度优势", "编程开发", 1, 4, 14, I),
        ("OpenAI Codex", "https://github.com/openai/codex", favicon("github.com"),
         "云端沙箱AI代理，Terminal-Bench最佳（77.3%），开源Rust CLI，62K+ Star", "编程开发", 1, 4, 15, I),
        ("v0 by Vercel", "https://v0.dev", favicon("v0.dev"),
         "Vercel出品，专注前端UI生成，React/Tailwind/Native输出，设计稿转代码", "编程开发", 1, 4, 16, I),
        ("Devin", "https://devin.ai", favicon("devin.ai"),
         "全自主AI工程师，异步后台任务，代码迁移重构，价格从$500降至$20/月", "编程开发", 0, 3, 17, I),
        ("Aider", "https://aider.chat", favicon("aider.chat"),
         "开源Git原生CLI编辑工具，BYOK模式，Git提交工作流，成本可控", "编程开发", 1, 4, 18, I),

        # ==================== 图像生成与处理 ====================
        # ---- 国内 ----
        ("通义万相 (Tongyi Wanxiang)", "https://tongyi.aliyun.com/wanxiang", favicon("tongyi.aliyun.com"),
         "阿里云出品，支持文生图/图生图/风格迁移，中文提示词理解精准，商用友好", "图像生成与处理", 1, 4, 1, D),
        # ---- 国际 ----
        ("Midjourney", "https://midjourney.com", favicon("midjourney.com"),
         "最佳美学质量AI图像生成，V7版大幅改进手脚面部渲染，个性化风格系统", "图像生成与处理", 0, 5, 11, I),
        ("Adobe Firefly", "https://firefly.adobe.com", favicon("firefly.adobe.com"),
         "商业安全首选，授权内容训练，IP赔偿保障，深度集成Photoshop等Creative Cloud", "图像生成与处理", 1, 5, 12, I),
        ("FLUX", "https://blackforestlabs.ai", favicon("blackforestlabs.ai"),
         "最佳摄影精度，hex色彩精确控制，开源可用（Apache 2.0），多模态扩展能力强", "图像生成与处理", 1, 5, 13, I),
        ("Ideogram", "https://ideogram.ai", favicon("ideogram.ai"),
         "最佳文字渲染（90-95%准确率），Logo/海报/T恤设计，3.0版大幅提升质量", "图像生成与处理", 1, 4, 14, I),
        ("Leonardo.AI", "https://leonardo.ai", favicon("leonardo.ai"),
         "多模型工作室，自定义LoRA训练，角色一致性生成，支持动态视频生成", "图像生成与处理", 1, 4, 15, I),
        ("Canva AI", "https://canva.com", favicon("canva.com"),
         "免费全能设计平台，海量模板素材字体，AI背景移除/图像编辑/批量生成", "图像生成与处理", 1, 5, 16, I),

        # ==================== 写作与文案 ====================
        # ---- 国内 ----
        ("秘塔写作猫", "https://xiezuocat.com", favicon("xiezuocat.com"),
         "中文AI写作助手，错别字检测/文风改写/中英翻译/学术写作润色/AI查重", "写作与文案", 1, 4, 1, D),
        # ---- 国际 ----
        ("Jasper AI", "https://jasper.ai", favicon("jasper.ai"),
         "营销文案专用AI，品牌声音定制，多渠道内容适配，团队协作和审批流程", "写作与文案", 0, 4, 11, I),
        ("Notion AI", "https://notion.so", favicon("notion.so"),
         "工作空间集成AI写作，文档协作+知识库搜索，AI自动总结生成翻译", "写作与文案", 1, 5, 12, I),
        ("Grammarly", "https://grammarly.com", favicon("grammarly.com"),
         "AI写作助手，语法拼写检查/语气调整/风格优化，多平台浏览器扩展集成", "写作与文案", 1, 5, 13, I),
        ("Writesonic", "https://writesonic.com", favicon("writesonic.com"),
         "SEO内容营销平台，AI批量生成文章/关键词优化/改写，多语言支持", "写作与文案", 1, 4, 14, I),
        ("Sudowrite", "https://sudowrite.com", favicon("sudowrite.com"),
         "创意写作专用AI，小说剧本创作/角色开发/故事大纲/章节生成", "写作与文案", 0, 4, 15, I),

        # ==================== 视频制作 ====================
        # ---- 国内 ----
        ("Kling AI (可灵)", "https://klingai.com", favicon("klingai.com"),
         "快手出品，最长120秒AI视频生成，多镜头自动转场，5种语言内置音频，性价比高", "视频制作", 1, 5, 1, D),
        ("Seedance (即梦)", "https://seedance.tv", favicon("seedance.tv"),
         "字节跳动出品，角色锁定跨场景一致，多镜头叙事，免费无水印，支持角色参考视频", "视频制作", 1, 4, 2, D),
        ("Jimeng AI (即梦)", "https://jimeng.jianying.com", favicon("jianying.com"),
         "剪映旗下AI创作平台，文生视频/图生视频，与剪映生态深度融合", "视频制作", 1, 4, 3, D),
        # ---- 国际 ----
        ("Runway", "https://runwayml.com", favicon("runwayml.com"),
         "专业电影级AI视频，Gen-4.5模型领跑排行榜，VFX特效和精确创意控制", "视频制作", 0, 5, 11, I),
        ("Google Veo", "https://deepmind.google/technologies/veo", favicon("deepmind.google"),
         "4K AI视频生成，原生音频同步生成，电影级画质，Google生态深度集成", "视频制作", 0, 5, 12, I),
        ("Pika", "https://pika.art", favicon("pika.art"),
         "15-30秒快速AI视频生成，社交媒体内容首选，操作简洁，生成速度极快", "视频制作", 1, 4, 13, I),
        ("Luma Dream Machine", "https://lumalabs.ai", favicon("lumalabs.ai"),
         "4K HDR专业AI视频，16-bit ACES色彩空间，专业后期工作流集成", "视频制作", 0, 4, 14, I),

        # ==================== 数据分析 ====================
        # ---- 国际 ----
        ("Tableau", "https://tableau.com", favicon("tableau.com"),
         "行业领先数据可视化，Einstein AI驱动洞察，Salesforce生态深度集成", "数据分析", 0, 5, 11, I),
        ("Power BI", "https://powerbi.microsoft.com", favicon("microsoft.com"),
         "微软商业智能平台，Copilot自然语言分析，Microsoft 365无缝集成", "数据分析", 1, 5, 12, I),
        ("Databricks", "https://databricks.com", favicon("databricks.com"),
         "Lakehouse架构AI分析，AI/BI Genie智能查询，大规模数据处理和ML工程", "数据分析", 0, 5, 13, I),
        ("H2O.ai", "https://h2o.ai", favicon("h2o.ai"),
         "开源AutoML平台，预测建模和合规ML流水线，企业级AI部署方案", "数据分析", 1, 4, 14, I),
        ("Julius AI", "https://julius.ai", favicon("julius.ai"),
         "对话式Python数据分析，自然语言生成图表和洞察，快速统计分析", "数据分析", 1, 4, 15, I),
        ("ThoughtSpot", "https://thoughtspot.com", favicon("thoughtspot.com"),
         "搜索驱动分析，自然语言查询和AI自动洞察，自服务BI新模式", "数据分析", 0, 4, 16, I),

        # ==================== 演示文稿 ====================
        # ---- 国际 ----
        ("Gamma", "https://gamma.app", favicon("gamma.app"),
         "70M+用户AI演示工具，45秒生成精美交互式演示，支持文档/网页/演示三种模式", "演示文稿", 1, 5, 11, I),
        ("Beautiful.ai", "https://beautiful.ai", favicon("beautiful.ai"),
         "设计优先AI演示，品牌一致性自动锁定，团队模板协作，设计师友好", "演示文稿", 0, 4, 12, I),
        ("Prezi", "https://prezi.com", favicon("prezi.com"),
         "非线性叙事演示，动态缩放画布效果，AI辅助内容创建和结构设计", "演示文稿", 1, 4, 13, I),
        ("SlidesAI", "https://slidesai.io", favicon("slidesai.io"),
         "Google Slides AI插件，自动从文本生成幻灯片，支持多语言转换", "演示文稿", 1, 3, 14, I),
        ("Decktopus", "https://decktopus.com", favicon("decktopus.com"),
         "初学者友好AI演示工具，内置表单收集和分析，快速创建营销演示", "演示文稿", 1, 3, 15, I),

        # ==================== 语音与音频 ====================
        # ---- 国际 ----
        ("ElevenLabs", "https://elevenlabs.io", favicon("elevenlabs.io"),
         "超真实AI语音合成，29种语言，30秒声音克隆，情绪语调停顿完美呈现", "语音与音频", 1, 5, 11, I),
        ("Suno", "https://suno.com", favicon("suno.com"),
         "100M+用户AI音乐生成，完整歌曲40秒生成，人声+乐器+歌词，日生成700万首", "语音与音频", 1, 5, 12, I),
        ("Udio", "https://udio.com", favicon("udio.com"),
         "专业AI音乐工作室，48kHz高清渲染，分轨编辑下载，最佳混音质量", "语音与音频", 1, 4, 13, I),
        ("Otter.ai", "https://otter.ai", favicon("otter.ai"),
         "智能会议记录转录，实时字幕和自动摘要，Zoom/Teams/Meet深度集成", "语音与音频", 1, 4, 14, I),
        ("Murf AI", "https://murf.ai", favicon("murf.ai"),
         "专业AI配音工作室，120+自然声音，音视频同步编辑，商业授权可用", "语音与音频", 0, 4, 15, I),
    ]


async def seed():
    async with async_session() as db:
        # 获取分类映射
        result = await db.execute(select(AiCategory))
        categories = result.scalars().all()
        cat_map = {c.name: c.id for c in categories}
        print("分类映射:", {k: v for k, v in cat_map.items()})

        # 清空现有工具
        await db.execute(delete(AiTool))
        await db.commit()
        print("已清空现有工具")

        tools = data()
        created = 0
        for name, url, logo_url, desc, cat_key, is_free, rating, sort, region in tools:
            cat_id = cat_map.get(cat_key)
            if not cat_id:
                print(f"⚠️  跳过 {name}: 分类 '{cat_key}' 不存在")
                continue

            tool = AiTool(
                name=name,
                url=url,
                logo_url=logo_url,
                description=desc,
                category_id=cat_id,
                region="domestic" if region == "国内" else "international",
                is_free=is_free,
                rating=rating,
                is_featured=(1 if sort <= 3 else 0),  # 前3名自动精选
                sort_order=sort,
            )
            db.add(tool)
            created += 1
            region_flag = "🇨🇳" if region == "国内" else "🌍"
            print(f"  {region_flag} {name} [{cat_key}] sort={sort}")

        await db.commit()
        print(f"\n🎉 导入完成: {created} 个工具")


if __name__ == "__main__":
    asyncio.run(seed())
