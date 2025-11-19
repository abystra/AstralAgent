from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as v1_router

app = FastAPI(
    title="AstralAgent API",
    description="FastAPI application with uv dependency management",
    version="0.1.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(v1_router.router)


@app.get("/")
async def root():
    """根路径"""
    return {"message": "Welcome to AstralAgent API"}


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}

