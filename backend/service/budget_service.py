"""预算业务层：封装预算设置、查询与超支预警的核心逻辑"""
from collections import defaultdict
from dao import BudgetDAO, TransactionDAO, LogDAO
from db import connection_scope


class BudgetService:
    """预算服务类，提供预算管理的核心业务方法"""

    @staticmethod
    def get_all(y=None, m=None):
        """获取预算列表，可按年月筛选"""
        return BudgetDAO.get_all(y, m)

    @staticmethod
    def set(y, m, cat, amt, sub=""):
        """
        设置预算（upsert 语义：已存在则覆盖，否则新增）
        校验：金额不能为负
        """
        try:
            amt = float(amt)
            if amt < 0:
                return False, "金额不能为负"
        except:
            return False, "格式错误"
        with connection_scope() as conn:
            BudgetDAO.set(y, m, cat, amt, sub, conn=conn)
            LogDAO.add("SET_BUDGET", f"{y}/{m} {cat}:{amt}", conn=conn)
            return True, "设置成功"

    @staticmethod
    def delete(y, m, cat, sub=""):
        """删除指定预算"""
        BudgetDAO.delete(y, m, cat, sub)
        return True

    @staticmethod
    def get_summary(y, m):
        """
        获取预算汇总
        包含：预算金额、实际花费、剩余金额、使用百分比
        预警规则：
        - 花费 ≥ 预算 → overspent（超支）
        - 使用率 ≥ 80% → 黄色预警
        - 使用率 < 80% → normal
        """
        with connection_scope() as conn:
            budgets = BudgetDAO.get_all(y, m, conn=conn)
            spend = defaultdict(float)
            sd = f"{y}-{m:02d}-01"
            # 计算该月的日期范围
            ed = f"{y+1}-01-01" if m == 12 else f"{y}-{m+1:02d}-01"
            result = TransactionDAO.get_all(start_date=sd, end_date=ed, page_size=99999, conn=conn)
            for t in result["transactions"]:
                if t["type"] == "expense":
                    spend[t.get("category", "其他")] += float(t["amount"])
            summary = []
            tb = ts = 0
            warns = []
            for b in budgets:
                amt = float(b["amount"])
                sp = spend.get(b["category"], 0)
                rm = amt - sp
                pct = (sp / amt * 100) if amt > 0 else 0
                summary.append({
                    "category": b["category"], "budget": round(amt, 2),
                    "spent": round(sp, 2), "remaining": round(rm, 2),
                    "percentage": round(pct, 1),
                    "status": "overspent" if rm < 0 else "normal"
                })
                tb += amt
                ts += sp
                if rm < 0:
                    warns.append(f"{b['category']}超预算{abs(rm):.2f}")
                elif pct >= 80:
                    warns.append(f"{b['category']}已用{pct:.1f}%")
            # 添加总计行
            summary.append({
                "category": "总计", "budget": round(tb, 2), "spent": round(ts, 2),
                "remaining": round(tb - ts, 2),
                "percentage": round((ts / tb * 100) if tb > 0 else 0, 1),
                "status": "normal"
            })
            return {"summary": summary, "warnings": warns}