"""
国际化（i18n）支持

使用 YAML 配置文件管理多语言消息（类似 Java 的 ResourceBundle）
"""

from typing import Dict, Optional
from enum import Enum
from pathlib import Path
import yaml
import threading
from app.core.exceptions.error_codes import ErrorCode


class Language(str, Enum):
    """支持的语言"""
    ZH_CN = "zh-CN"  # 简体中文
    ZH_TW = "zh-TW"  # 繁体中文
    EN_US = "en-US"  # 英语
    JA_JP = "ja-JP"  # 日语
    KO_KR = "ko-KR"  # 韩语


class I18nManager:
    """
    国际化管理器（单例模式）
    
    类似 Java 的 ResourceBundle，从 YAML 文件加载多语言消息
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._messages: Dict[Language, Dict[str, str]] = {}
        self._locales_dir = Path(__file__).parent.parent.parent / "locales"
        self._load_all_locales()
        self._initialized = True
    
    def _load_all_locales(self) -> None:
        """加载所有语言的消息文件"""
        if not self._locales_dir.exists():
            # 静默处理，不打印警告（开发环境可能没有所有语言文件）
            return
        
        for language in Language:
            locale_file = self._locales_dir / language.value / "errors.yaml"
            if locale_file.exists():
                try:
                    with open(locale_file, 'r', encoding='utf-8') as f:
                        messages = yaml.safe_load(f) or {}
                    # 将 int key 转换为 str
                    self._messages[language] = {str(k): v for k, v in messages.items()}
                except Exception as e:
                    # 静默处理加载错误
                    pass
            # 如果文件不存在，静默跳过（不是所有语言都需要实现）
    
    def get_message(
        self,
        error_code: ErrorCode,
        language: Language = Language.ZH_CN,
        default: Optional[str] = None
    ) -> str:
        """
        获取错误消息
        
        Args:
            error_code: 错误码
            language: 语言
            default: 默认消息
            
        Returns:
            错误消息
        """
        code_str = str(int(error_code))
        
        # 尝试获取指定语言的消息
        if language in self._messages:
            if code_str in self._messages[language]:
                return self._messages[language][code_str]
        
        # 降级到英语
        if Language.EN_US in self._messages:
            if code_str in self._messages[Language.EN_US]:
                return self._messages[Language.EN_US][code_str]
        
        # 降级到中文
        if Language.ZH_CN in self._messages:
            if code_str in self._messages[Language.ZH_CN]:
                return self._messages[Language.ZH_CN][code_str]
        
        # 使用默认消息
        if default:
            return default
        
        # 最后的降级
        return f"Error {error_code}"
    
    def reload(self) -> None:
        """重新加载所有语言文件（支持热更新）"""
        self._messages.clear()
        self._load_all_locales()


# 全局 i18n 管理器实例
_i18n_manager = I18nManager()


def get_error_message(
    error_code: ErrorCode,
    language: Language = Language.ZH_CN,
    custom_message: Optional[str] = None
) -> str:
    """
    获取错误消息
    
    Args:
        error_code: 错误码
        language: 语言
        custom_message: 自定义消息（优先级最高）
        
    Returns:
        错误消息
    """
    # 如果有自定义消息，直接返回
    if custom_message:
        return custom_message
    
    # 从 i18n 管理器获取
    return _i18n_manager.get_message(error_code, language)


def detect_language(accept_language: Optional[str] = None) -> Language:
    """
    检测语言
    
    Args:
        accept_language: HTTP Accept-Language 头
        
    Returns:
        语言
    """
    if not accept_language:
        return Language.ZH_CN
    
    # 简单解析 Accept-Language
    accept_language = accept_language.lower()
    
    if "zh-cn" in accept_language or "zh" in accept_language:
        return Language.ZH_CN
    elif "zh-tw" in accept_language:
        return Language.ZH_TW
    elif "en" in accept_language:
        return Language.EN_US
    elif "ja" in accept_language:
        return Language.JA_JP
    elif "ko" in accept_language:
        return Language.KO_KR
    
    # 默认中文
    return Language.ZH_CN


def reload_locales() -> None:
    """重新加载所有语言文件"""
    _i18n_manager.reload()


# 废弃的硬编码字典（保留用于向后兼容，但不推荐使用）
# 建议使用 YAML 配置文件
_DEPRECATED_ERROR_MESSAGES: Dict[ErrorCode, Dict[Language, str]] = {
    # 通用错误
    ErrorCode.SUCCESS: {
        Language.ZH_CN: "成功",
        Language.EN_US: "Success",
        Language.JA_JP: "成功",
    },
    ErrorCode.UNKNOWN_ERROR: {
        Language.ZH_CN: "未知错误",
        Language.EN_US: "Unknown error",
        Language.JA_JP: "不明なエラー",
    },
    ErrorCode.INVALID_REQUEST: {
        Language.ZH_CN: "无效的请求",
        Language.EN_US: "Invalid request",
        Language.JA_JP: "無効なリクエスト",
    },
    ErrorCode.MISSING_PARAMETER: {
        Language.ZH_CN: "缺少必需参数",
        Language.EN_US: "Missing required parameter",
        Language.JA_JP: "必須パラメータが不足しています",
    },
    ErrorCode.INVALID_PARAMETER: {
        Language.ZH_CN: "参数无效",
        Language.EN_US: "Invalid parameter",
        Language.JA_JP: "無効なパラメータ",
    },
    
    # 认证授权错误
    ErrorCode.UNAUTHORIZED: {
        Language.ZH_CN: "未授权，请先登录",
        Language.EN_US: "Unauthorized, please login first",
        Language.JA_JP: "未承認、先にログインしてください",
    },
    ErrorCode.INVALID_TOKEN: {
        Language.ZH_CN: "无效的访问令牌",
        Language.EN_US: "Invalid access token",
        Language.JA_JP: "無効なアクセストークン",
    },
    ErrorCode.TOKEN_EXPIRED: {
        Language.ZH_CN: "访问令牌已过期",
        Language.EN_US: "Access token expired",
        Language.JA_JP: "アクセストークンの有効期限が切れました",
    },
    ErrorCode.INSUFFICIENT_PERMISSIONS: {
        Language.ZH_CN: "权限不足",
        Language.EN_US: "Insufficient permissions",
        Language.JA_JP: "権限が不足しています",
    },
    
    # 资源错误
    ErrorCode.RESOURCE_NOT_FOUND: {
        Language.ZH_CN: "资源不存在",
        Language.EN_US: "Resource not found",
        Language.JA_JP: "リソースが見つかりません",
    },
    ErrorCode.RESOURCE_ALREADY_EXISTS: {
        Language.ZH_CN: "资源已存在",
        Language.EN_US: "Resource already exists",
        Language.JA_JP: "リソースはすでに存在します",
    },
    
    # 限流错误
    ErrorCode.RATE_LIMIT_EXCEEDED: {
        Language.ZH_CN: "请求频率超过限制",
        Language.EN_US: "Rate limit exceeded",
        Language.JA_JP: "リクエスト頻度が制限を超えました",
    },
    ErrorCode.TOO_MANY_REQUESTS: {
        Language.ZH_CN: "请求过于频繁，请稍后再试",
        Language.EN_US: "Too many requests, please try again later",
        Language.JA_JP: "リクエストが多すぎます、後でもう一度お試しください",
    },
    
    # 验证错误
    ErrorCode.VALIDATION_ERROR: {
        Language.ZH_CN: "数据验证失败",
        Language.EN_US: "Validation error",
        Language.JA_JP: "検証エラー",
    },
    
    # 系统错误
    ErrorCode.INTERNAL_SERVER_ERROR: {
        Language.ZH_CN: "服务器内部错误",
        Language.EN_US: "Internal server error",
        Language.JA_JP: "サーバー内部エラー",
    },
    ErrorCode.SERVICE_UNAVAILABLE: {
        Language.ZH_CN: "服务暂时不可用",
        Language.EN_US: "Service temporarily unavailable",
        Language.JA_JP: "サービスは一時的に利用できません",
    },
    ErrorCode.SERVICE_TIMEOUT: {
        Language.ZH_CN: "服务超时",
        Language.EN_US: "Service timeout",
        Language.JA_JP: "サービスタイムアウト",
    },
    
    # 数据库错误
    ErrorCode.DATABASE_ERROR: {
        Language.ZH_CN: "数据库错误",
        Language.EN_US: "Database error",
        Language.JA_JP: "データベースエラー",
    },
    
    # Agent 错误
    ErrorCode.AGENT_ERROR: {
        Language.ZH_CN: "智能体执行错误",
        Language.EN_US: "Agent execution error",
        Language.JA_JP: "エージェント実行エラー",
    },
    ErrorCode.AGENT_NOT_FOUND: {
        Language.ZH_CN: "智能体不存在",
        Language.EN_US: "Agent not found",
        Language.JA_JP: "エージェントが見つかりません",
    },
    ErrorCode.AGENT_TIMEOUT: {
        Language.ZH_CN: "智能体执行超时",
        Language.EN_US: "Agent execution timeout",
        Language.JA_JP: "エージェント実行タイムアウト",
    },
    
    # Workflow 错误
    ErrorCode.WORKFLOW_ERROR: {
        Language.ZH_CN: "工作流执行错误",
        Language.EN_US: "Workflow execution error",
        Language.JA_JP: "ワークフロー実行エラー",
    },
    
    # Tool 错误
    ErrorCode.TOOL_ERROR: {
        Language.ZH_CN: "工具执行错误",
        Language.EN_US: "Tool execution error",
        Language.JA_JP: "ツール実行エラー",
    },
    ErrorCode.TOOL_PERMISSION_DENIED: {
        Language.ZH_CN: "工具权限不足",
        Language.EN_US: "Tool permission denied",
        Language.JA_JP: "ツールの権限が拒否されました",
    },
    
    # RAG 错误
    ErrorCode.DOCUMENT_NOT_FOUND: {
        Language.ZH_CN: "文档不存在",
        Language.EN_US: "Document not found",
        Language.JA_JP: "ドキュメントが見つかりません",
    },
    ErrorCode.RETRIEVAL_ERROR: {
        Language.ZH_CN: "检索失败",
        Language.EN_US: "Retrieval error",
        Language.JA_JP: "検索エラー",
    },
    
    # 模型错误
    ErrorCode.MODEL_ERROR: {
        Language.ZH_CN: "模型调用错误",
        Language.EN_US: "Model invocation error",
        Language.JA_JP: "モデル呼び出しエラー",
    },
    ErrorCode.MODEL_TIMEOUT: {
        Language.ZH_CN: "模型调用超时",
        Language.EN_US: "Model invocation timeout",
        Language.JA_JP: "モデル呼び出しタイムアウト",
    },
    ErrorCode.MODEL_RATE_LIMIT: {
        Language.ZH_CN: "模型调用频率超限",
        Language.EN_US: "Model rate limit exceeded",
        Language.JA_JP: "モデル呼び出し頻度制限超過",
    },
    
    # 插件错误
    ErrorCode.PLUGIN_ERROR: {
        Language.ZH_CN: "插件错误",
        Language.EN_US: "Plugin error",
        Language.JA_JP: "プラグインエラー",
    },
    ErrorCode.PLUGIN_NOT_FOUND: {
        Language.ZH_CN: "插件不存在",
        Language.EN_US: "Plugin not found",
        Language.JA_JP: "プラグインが見つかりません",
    },
}

