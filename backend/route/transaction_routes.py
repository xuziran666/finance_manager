from fastapi import APIRouter, Query
from fastapi.responses import Response
from typing import Optional
import csv
import io
from dto import TransactionCreate, TransferCreate
from vo import ApiResponse
from service import TransactionService

router = APIRouter(tags=["交易记录"])


@router.post("/transactions", summary="添加交易")
def add_transaction(data: TransactionCreate):
    ok, result = TransactionService.add(
        data.account_id, data.type, data.category,
        data.amount, data.note, data.date, data.subcategory,
    )
    return ApiResponse(data=result) if ok else ApiResponse(code=400, msg=result)


@router.post("/transactions/transfer", summary="账户转账")
def transfer_money(data: TransferCreate):
    ok, msg = TransactionService.transfer(
        data.from_account, data.to_account, data.amount, data.note,
    )
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.get("/transactions", summary="查询交易记录")
def get_transactions(
    account_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1),
    page_size: int = Query(20),
):
    return ApiResponse(data=TransactionService.get_all(
        account_id, start_date, end_date, category, page, page_size,
    ))


@router.delete("/transactions/{id}", summary="删除交易")
def delete_transaction(id: int):
    ok, msg = TransactionService.delete(id)
    return ApiResponse(msg=msg) if ok else ApiResponse(code=400, msg=msg)


@router.get("/transactions/export", summary="导出交易 CSV")
def export_csv(
    account_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    data = TransactionService.get_all(account_id, start_date, end_date, page_size=99999)
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
            txn.get("note", ""),
        ])
    return Response(
        content=output.getvalue(),
        media_type="text/csv;charset=utf-8",
        headers={"Content-Disposition": "attachment;filename=export.csv"},
    )
