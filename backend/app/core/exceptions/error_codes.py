"""
统一错误码定义

错误码规范：
- 5 位数字
- 第一位：错误类别（1=客户端错误，2=服务端错误，3=业务错误，4=外部服务错误）
- 后四位：具体错误编号

分段规则：
- 10000-19999: 客户端错误（请求参数、认证授权等）
- 20000-29999: 服务端错误（系统错误、数据库错误等）
- 30000-39999: 业务逻辑错误（Agent、Workflow 等）
- 40000-49999: 外部服务错误（模型调用、第三方 API 等）
"""

from enum import IntEnum


class ErrorCode(IntEnum):
    """错误码枚举"""
    
    # ========================================
    # 通用错误 (10000-10099)
    # ========================================
    SUCCESS = 0
    UNKNOWN_ERROR = 10000
    INVALID_REQUEST = 10001
    MISSING_PARAMETER = 10002
    INVALID_PARAMETER = 10003
    
    # ========================================
    # 认证授权错误 (10100-10199)
    # ========================================
    UNAUTHORIZED = 10100
    INVALID_TOKEN = 10101
    TOKEN_EXPIRED = 10102
    INSUFFICIENT_PERMISSIONS = 10103
    INVALID_CREDENTIALS = 10104
    ACCOUNT_DISABLED = 10105
    ACCOUNT_LOCKED = 10106
    
    # ========================================
    # 资源错误 (10200-10299)
    # ========================================
    RESOURCE_NOT_FOUND = 10200
    RESOURCE_ALREADY_EXISTS = 10201
    RESOURCE_DELETED = 10202
    RESOURCE_LOCKED = 10203
    
    # ========================================
    # 请求限制错误 (10300-10399)
    # ========================================
    RATE_LIMIT_EXCEEDED = 10300
    QUOTA_EXCEEDED = 10301
    REQUEST_TOO_LARGE = 10302
    TOO_MANY_REQUESTS = 10303
    
    # ========================================
    # 数据验证错误 (10400-10499)
    # ========================================
    VALIDATION_ERROR = 10400
    INVALID_FORMAT = 10401
    INVALID_VALUE = 10402
    DUPLICATE_VALUE = 10403
    CONSTRAINT_VIOLATION = 10404
    
    # ========================================
    # 系统错误 (20000-20099)
    # ========================================
    INTERNAL_SERVER_ERROR = 20000
    SERVICE_UNAVAILABLE = 20001
    SERVICE_TIMEOUT = 20002
    CONFIGURATION_ERROR = 20003
    
    # ========================================
    # 数据库错误 (20100-20199)
    # ========================================
    DATABASE_ERROR = 20100
    DATABASE_CONNECTION_ERROR = 20101
    DATABASE_QUERY_ERROR = 20102
    DATABASE_CONSTRAINT_ERROR = 20103
    DATABASE_DEADLOCK = 20104
    
    # ========================================
    # 缓存错误 (20200-20299)
    # ========================================
    CACHE_ERROR = 20200
    CACHE_CONNECTION_ERROR = 20201
    CACHE_OPERATION_ERROR = 20202
    
    # ========================================
    # 消息队列错误 (20300-20399)
    # ========================================
    MESSAGE_QUEUE_ERROR = 20300
    MESSAGE_PUBLISH_ERROR = 20301
    MESSAGE_CONSUME_ERROR = 20302
    
    # ========================================
    # Agent 错误 (30000-30099)
    # ========================================
    AGENT_ERROR = 30000
    AGENT_NOT_FOUND = 30001
    AGENT_EXECUTION_ERROR = 30002
    AGENT_TIMEOUT = 30003
    AGENT_INITIALIZATION_ERROR = 30004
    AGENT_INVALID_STATE = 30005
    
    # ========================================
    # Workflow 错误 (30100-30199)
    # ========================================
    WORKFLOW_ERROR = 30100
    WORKFLOW_NOT_FOUND = 30101
    WORKFLOW_EXECUTION_ERROR = 30102
    WORKFLOW_TIMEOUT = 30103
    WORKFLOW_INVALID_STATE = 30104
    
    # ========================================
    # Tool 错误 (30200-30299)
    # ========================================
    TOOL_ERROR = 30200
    TOOL_NOT_FOUND = 30201
    TOOL_EXECUTION_ERROR = 30202
    TOOL_PERMISSION_DENIED = 30203
    TOOL_INVALID_INPUT = 30204
    
    # ========================================
    # RAG 错误 (30300-30399)
    # ========================================
    RAG_ERROR = 30300
    DOCUMENT_NOT_FOUND = 30301
    DOCUMENT_PARSE_ERROR = 30302
    EMBEDDING_ERROR = 30303
    RETRIEVAL_ERROR = 30304
    VECTOR_STORE_ERROR = 30305
    
    # ========================================
    # 模型调用错误 (40000-40099)
    # ========================================
    MODEL_ERROR = 40000
    MODEL_NOT_FOUND = 40001
    MODEL_TIMEOUT = 40002
    MODEL_RATE_LIMIT = 40003
    MODEL_INVALID_RESPONSE = 40004
    MODEL_API_ERROR = 40005
    MODEL_QUOTA_EXCEEDED = 40006
    
    # ========================================
    # 外部服务错误 (40100-40199)
    # ========================================
    EXTERNAL_SERVICE_ERROR = 40100
    EXTERNAL_SERVICE_TIMEOUT = 40101
    EXTERNAL_SERVICE_UNAVAILABLE = 40102
    EXTERNAL_API_ERROR = 40103
    
    # ========================================
    # 插件错误 (40200-40299)
    # ========================================
    PLUGIN_ERROR = 40200
    PLUGIN_NOT_FOUND = 40201
    PLUGIN_LOAD_ERROR = 40202
    PLUGIN_INITIALIZATION_ERROR = 40203
    PLUGIN_EXECUTION_ERROR = 40204


class HTTPStatusCode(IntEnum):
    """HTTP 状态码枚举"""
    
    # 2xx 成功
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    # 3xx 重定向
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304
    
    # 4xx 客户端错误
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    
    # 5xx 服务端错误
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


# 错误码到 HTTP 状态码的映射
ERROR_CODE_TO_HTTP_STATUS = {
    # 客户端错误 -> 4xx
    ErrorCode.INVALID_REQUEST: HTTPStatusCode.BAD_REQUEST,
    ErrorCode.MISSING_PARAMETER: HTTPStatusCode.BAD_REQUEST,
    ErrorCode.INVALID_PARAMETER: HTTPStatusCode.BAD_REQUEST,
    ErrorCode.UNAUTHORIZED: HTTPStatusCode.UNAUTHORIZED,
    ErrorCode.INVALID_TOKEN: HTTPStatusCode.UNAUTHORIZED,
    ErrorCode.TOKEN_EXPIRED: HTTPStatusCode.UNAUTHORIZED,
    ErrorCode.INSUFFICIENT_PERMISSIONS: HTTPStatusCode.FORBIDDEN,
    ErrorCode.RESOURCE_NOT_FOUND: HTTPStatusCode.NOT_FOUND,
    ErrorCode.RATE_LIMIT_EXCEEDED: HTTPStatusCode.TOO_MANY_REQUESTS,
    ErrorCode.VALIDATION_ERROR: HTTPStatusCode.UNPROCESSABLE_ENTITY,
    
    # 服务端错误 -> 5xx
    ErrorCode.INTERNAL_SERVER_ERROR: HTTPStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.SERVICE_UNAVAILABLE: HTTPStatusCode.SERVICE_UNAVAILABLE,
    ErrorCode.SERVICE_TIMEOUT: HTTPStatusCode.GATEWAY_TIMEOUT,
    ErrorCode.DATABASE_ERROR: HTTPStatusCode.INTERNAL_SERVER_ERROR,
    
    # 业务错误 -> 400 or 500
    ErrorCode.AGENT_ERROR: HTTPStatusCode.INTERNAL_SERVER_ERROR,
    ErrorCode.AGENT_TIMEOUT: HTTPStatusCode.GATEWAY_TIMEOUT,
    ErrorCode.MODEL_TIMEOUT: HTTPStatusCode.GATEWAY_TIMEOUT,
    ErrorCode.MODEL_RATE_LIMIT: HTTPStatusCode.TOO_MANY_REQUESTS,
}


def get_http_status(error_code: ErrorCode) -> int:
    """
    获取错误码对应的 HTTP 状态码
    
    Args:
        error_code: 错误码
        
    Returns:
        HTTP 状态码
    """
    return ERROR_CODE_TO_HTTP_STATUS.get(
        error_code,
        HTTPStatusCode.INTERNAL_SERVER_ERROR
    )

