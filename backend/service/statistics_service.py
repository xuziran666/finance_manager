from collections import defaultdict
from datetime import datetime, date, timedelta
from dao import TransactionDAO


class StatisticsService:

    @staticmethod
    def get(user_id, account_id=None, start_date=None, end_date=None, group_by="month"):
        result = TransactionDAO.get_all(user_id, account_id=account_id, start_date=start_date, end_date=end_date, page_size=99999)
        transactions = result["transactions"]
        total_income = sum(float(t["amount"]) for t in transactions if t["type"] == "income")
        total_expense = sum(float(t["amount"]) for t in transactions if t["type"] == "expense")
        income_grouped = defaultdict(float)
        expense_grouped = defaultdict(float)
        for t in transactions:
            group_key = StatisticsService._get_group_key(t.get("date", ""), group_by)
            amount = float(t["amount"])
            if t["type"] == "income":
                income_grouped[group_key] += amount
            else:
                expense_grouped[group_key] += amount
        all_groups = sorted(set(list(income_grouped.keys()) + list(expense_grouped.keys())))
        trend = [{
            "period": g, "income": round(income_grouped.get(g, 0), 2),
            "expense": round(expense_grouped.get(g, 0), 2),
            "balance": round(income_grouped.get(g, 0) - expense_grouped.get(g, 0), 2)
        } for g in all_groups]
        expense_by_category = defaultdict(float)
        income_by_category = defaultdict(float)
        expense_by_account = defaultdict(float)
        income_by_account = defaultdict(float)
        for t in transactions:
            amount = float(t["amount"])
            if t["type"] == "expense":
                expense_by_category[t.get("category", "其他")] += amount
                expense_by_account[t.get("account_name", "未知")] += amount
            else:
                income_by_category[t.get("category", "其他")] += amount
                income_by_account[t.get("account_name", "未知")] += amount
        return {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "balance": round(total_income - total_expense, 2),
            "trend": trend,
            "expense_by_category": [
                {"name": k, "amount": round(v, 2)}
                for k, v in sorted(expense_by_category.items(), key=lambda x: x[1], reverse=True)
            ],
            "income_by_category": [
                {"name": k, "amount": round(v, 2)}
                for k, v in sorted(income_by_category.items(), key=lambda x: x[1], reverse=True)
            ],
            "pie_chart": "",
            "line_chart": ""
        }

    @staticmethod
    def _get_group_key(date_str, group_by):
        if not date_str:
            return "未知"
        if isinstance(date_str, (datetime, date)):
            date_str = date_str.strftime("%Y-%m-%d")
        parts = date_str.split("-")
        if group_by == "year":
            return parts[0]
        if group_by == "month":
            return f"{parts[0]}-{parts[1]}"
        if group_by == "day":
            return date_str
        if group_by == "week":
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                return (dt - timedelta(days=dt.weekday())).strftime("%Y-%m-%d")
            except:
                return date_str
        return date_str
