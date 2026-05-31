"""交易记录路由：定义收支记录的查询、添加、转账和 CSV 导出接口"""
import csv
import io
from flask import request
from service import TransactionService
from route.result import Result


def init_transaction_routes(api):
    """注册交易记录相关路由到指定的 Blueprint 对象"""

    @api.route("/transactions", methods=["POST"])
    def add_transaction():
        """POST /api/transactions — 添加一条交易记录（自动更新账户余额）"""
        data = request.json
        ok, result = TransactionService.add(
            data.get("account_id"), data.get("type"), data.get("category"),
            data.get("amount"), data.get("note", ""), data.get("date", ""),
            data.get("subcategory", "")
        )
        return Result.success(result) if ok else Result.fail(result)

    @api.route("/transactions/transfer", methods=["POST"])
    def transfer_money():
        """POST /api/transactions/transfer — 账户间转账（生成两条对应记录）"""
        data = request.json
        ok, msg = TransactionService.transfer(
            data.get("from_account"), data.get("to_account"),
            data.get("amount"), data.get("note", "")
        )
        return Result.success(msg=msg) if ok else Result.fail(msg)

    @api.route("/transactions", methods=["GET"])
    def get_transactions():
        """GET /api/transactions — 分页查询交易记录，支持按账户/日期/分类筛选"""
        return Result.success(TransactionService.get_all(
            request.args.get("account_id", type=int),
            request.args.get("start_date"),
            request.args.get("end_date"),
            request.args.get("category"),
            request.args.get("page", 1, type=int),
            request.args.get("page_size", 20, type=int)
        ))

    @api.route("/transactions/export", methods=["GET"])
    def export_csv():
        """GET /api/transactions/export — 导出筛选后的交易记录为 CSV 文件"""
        data = TransactionService.get_all(
            request.args.get("account_id", type=int),
            request.args.get("start_date"),
            request.args.get("end_date"),
            page_size=99999
        )
        transactions = data.get("transactions", [])
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["日期", "类型", "分类", "二级分类", "金额", "账户", "备注"])
        for txn in transactions:
            writer.writerow([
                txn.get("date", ""),
                "收入" if txn["type"] == "income" else "支出",
                txn.get("category", ""),
                txn.get("subcategory", ""),
                txn.get("amount", ""),
                txn.get("account_name", ""),
                txn.get("note", "")
            ])
        # 返回 CSV 格式的响应，设置 Content-Type 和文件下载头
        return output.getvalue(), 200, {
            "Content-Type": "text/csv;charset=utf-8",
            "Content-Disposition": "attachment;filename=export.csv"
        }