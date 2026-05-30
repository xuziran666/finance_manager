"""统一响应结果封装：所有 API 接口返回标准的 JSON 格式"""
from flask import jsonify


class Result:
    """
    统一响应结果类
    所有接口返回值格式统一为 { code: 200/400, data: ..., msg: "..." }
    """

    @staticmethod
    def success(data=None, msg="成功"):
        """构造成功响应，data 为返回数据，msg 为提示信息"""
        return jsonify({"code": 200, "data": data, "msg": msg})

    @staticmethod
    def fail(msg, code=400):
        """构造失败响应，msg 为错误描述，code 为错误码（默认 400）"""
        return jsonify({"code": code, "msg": msg})