"""
FastAPI 应用主入口

职责：
1. 作为应用的唯一入口点
2. 通过 App Factory 创建应用实例
3. 保持简洁，所有逻辑在 factory 中

遵循最佳实践：
- Flask App Factory 模式
- 关注点分离
- 易于测试
"""

from app.factory import create_app

# 创建应用实例
# 所有配置、中间件、路由注册都在 factory 中完成
app = create_app()

