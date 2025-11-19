"""
数据库会话管理

提供 FastAPI 依赖注入
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.middleware.manager import get_middleware_manager
from app.infrastructure.database.middleware import DatabaseMiddleware


async def get_session() -> AsyncSession:
    """
    获取数据库会话（非依赖注入方式）
    
    Returns:
        数据库会话
        
    Example:
        async with get_session() as session:
            result = await session.execute(...)
    """
    manager = get_middleware_manager()
    db_middleware = manager.get("database")
    
    if not db_middleware:
        raise RuntimeError("Database middleware not registered")
    
    if not isinstance(db_middleware, DatabaseMiddleware):
        raise TypeError("Middleware 'database' is not DatabaseMiddleware")
    
    if not db_middleware.is_connected:
        raise RuntimeError("Database not connected")
    
    return db_middleware.get_session()


async def get_db_dependency() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 依赖注入
    
    自动管理会话生命周期
    
    Example:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db_dependency)):
            result = await db.execute(...)
            return result.scalars().all()
    """
    session = await get_session()
    
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

