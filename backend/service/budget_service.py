"""预算业务层：封装预算设置、查询与超支预警的核心逻辑"""
from collections import defaultdict
from dao import BudgetDAO, TransactionDAO, LogDAO
from db import connection_scope


class BudgetService:
    """预算服务类，提供预算管理的核心业务方法"""

    @staticmethod
    def get_all(year=None, month=None):
        """获取预算列表，可按年月筛选"""
        return BudgetDAO.get_all(year, month)

    @staticmethod
    def set(year, month, category, amount, subcategory=""):
        """
        设置预算（upsert 语义：已存在则覆盖，否则新增）
        校验：金额不能为负
        """
        try:
            amount = float(amount)
            if amount < 0:
                return False, "金额不能为负"
        except:
            return False, "格式错误"
        with connection_scope() as conn:
            BudgetDAO.set(year, month, category, amount, subcategory, conn=conn)
            LogDAO.add("SET_BUDGET", f"{year}/{month} {category}:{amount}", conn=conn)
            return True, "设置成功"

    @staticmethod
    def delete(year, month, category, subcategory=""):
        """删除指定预算"""
        BudgetDAO.delete(year, month, category, subcategory)
        return True

    @staticmethod
    def get_summary(year, month):
        """
        获取预算汇总
        包含：预算金额、实际花费、剩余金额、使用百分比
        预警规则：
        - 花费 ≥ 预算 → overspent（超支）
        - 使用率 ≥ 80% → 黄色预警
        - 使用率 < 80% → normal
        """
        with connection_scope() as conn:
            budgets = BudgetDAO.get_all(year, month, conn=conn)
            spend = defaultdict(float)
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year+1}-01-01" if month == 12 else f"{year}-{month+1:02d}-01"
            result = TransactionDAO.get_all(start_date=start_date, end_date=end_date, page_size=99999, conn=conn)
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
