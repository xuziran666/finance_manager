from collections import defaultdict
from dao import BudgetDAO, TransactionDAO, LogDAO
from db import connection_scope


class BudgetService:

    @staticmethod
    def get_all(user_id, year=None, month=None):
        return BudgetDAO.get_all(user_id, year, month)

    @staticmethod
    def set(user_id, year, month, category, amount, subcategory=""):
        try:
            amount = float(amount)
            if amount < 0:
                return False, "金额不能为负"
        except:
            return False, "格式错误"
        with connection_scope() as conn:
            BudgetDAO.set(user_id, year, month, category, amount, subcategory, conn=conn)
            LogDAO.add(user_id, "SET_BUDGET", f"{year}/{month} {category}:{amount}", conn=conn)
            return True, "设置成功"

    @staticmethod
    def delete(user_id, year, month, category, subcategory=""):
        BudgetDAO.delete(user_id, year, month, category, subcategory)
        return True

    @staticmethod
    def get_summary(user_id, year, month):
        with connection_scope() as conn:
            budgets = BudgetDAO.get_all(user_id, year, month, conn=conn)
            spend = defaultdict(float)
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year+1}-01-01" if month == 12 else f"{year}-{month+1:02d}-01"
            result = TransactionDAO.get_all(user_id, start_date=start_date, end_date=end_date, page_size=99999, conn=conn)
            for t in result["transactions"]:
                if t["type"] == "expense":
                    spend[t.get("category", "其他")] += float(t["amount"])
            summary = []
            total_budget = total_spent = 0
            warnings = []
            for b in budgets:
                amount = float(b["amount"])
                spent = spend.get(b["category"], 0)
                remaining = amount - spent
                percentage = (spent / amount * 100) if amount > 0 else 0
                summary.append({
                    "category": b["category"], "budget": round(amount, 2),
                    "spent": round(spent, 2), "remaining": round(remaining, 2),
                    "percentage": round(percentage, 1),
                    "status": "overspent" if remaining < 0 else "normal"
                })
                total_budget += amount
                total_spent += spent
                if remaining < 0:
                    warnings.append(f"{b['category']}超预算{abs(remaining):.2f}")
                elif percentage >= 80:
                    warnings.append(f"{b['category']}已用{percentage:.1f}%")
            summary.append({
                "category": "总计", "budget": round(total_budget, 2), "spent": round(total_spent, 2),
                "remaining": round(total_budget - total_spent, 2),
                "percentage": round((total_spent / total_budget * 100) if total_budget > 0 else 0, 1),
                "status": "normal"
            })
            return {"summary": summary, "warnings": warnings}
