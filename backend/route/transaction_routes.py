"""交易记录路由：定义收支记录的查询、添加、转账和 CSV 导出接口"""
import csv
import io
from flask import request
from service import TransactionService
from route.result import Result


def init_transaction_routes(api):
    """注册交易记录相关路由到指定的 Blueprint 对象"""

    @api.route("/transactions", methods=["GET"])
    def gt():
        """GET /api/transactions — 分页查询交易记录，支持按账户/日期/分类筛选"""
        return Result.success(TransactionService.get_all(
            request.args.get("account_id", type=int),
            request.args.get("start_date"),
            request.args.get("end_date"),
            request.args.get("category"),
            request.args.get("page", 1, type=int),
            request.args.get("page_size", 20, type=int)
        ))

    @api.route("/transactions", methods=["POST"])
    def at():
        """POST /api/transactions — 添加一条交易记录（自动更新账户余额）"""
        d = request.json
        succ, r = TransactionService.add(
            d.get("account_id"), d.get("type"), d.get("category"),
            d.get("amount"), d.get("note", ""), d.get("date", ""),
            d.get("subcategory", "")
        )
        return Result.success(r) if succ else Result.fail(r)

    @api.route("/transactions/transfer", methods=["POST"])
    def tr():
        """POST /api/transactions/transfer — 账户间转账（生成两条对应记录）"""
        d = request.json
        succ, r = TransactionService.transfer(
            d.get("from_account"), d.get("to_account"),
            d.get("amount"), d.get("note", "")
        )
        return Result.success(msg=r) if succ else Result.fail(r)

    @api.route("/transactions/export", methods=["GET"])
    def ex():
        """GET /api/transactions/export — 导出筛选后的交易记录为 CSV 文件"""
        r = TransactionService.get_all(
            request.args.get("account_id", type=int),
            request.args.get("start_date"),
            request.args.get("end_date"),
            page_size=99999
        )
        txns = r.get("transactions", [])
        out = io.StringIO()
        w = csv.writer(out)
        w.writerow(["日期", "类型", "分类", "二级分类", "金额", "账户", "备注"])
        for t in txns:
            w.writerow([
                t.get("date", ""),
                "收入" if t["type"] == "income" else "支出",
                t.get("category", ""),
                t.get("subcategory", ""),
                t.get("amount", ""),
                t.get("account_name", ""),
                t.get("note", "")
            ])
        # 返回 CSV 格式的响应，设置 Content-Type 和文件下载头
        return out.getvalue(), 200, {
            "Content-Type": "text/csv;charset=utf-8",
            "Content-Disposition": "attachment;filename=export.csv"
        }