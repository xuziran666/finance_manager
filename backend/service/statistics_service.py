"""统计业务层：提供收支数据的多维度聚合统计分析"""
from collections import defaultdict
from datetime import datetime, date, timedelta
from dao import TransactionDAO


class StatisticsService:
    """统计服务类，提供各类财务数据统计分析"""

    @staticmethod
    def get(aid=None, sd=None, ed=None, gb="month"):
        """
        获取统计数据
        参数：
            aid — 账户 ID（可选）
            sd  — 开始日期（可选）
            ed  — 结束日期（可选）
            gb  — 时间分组方式（year/month/day/week）
        返回：
            total_income / total_expense / balance — 汇总数据
            trend — 按时间维度的趋势数据
            expense_by_category / income_by_category — 分类汇总（降序）
        """
        r = TransactionDAO.get_all(account_id=aid, page_size=99999)
        txns = r["transactions"]
        # 应用日期筛选
        if sd:
            txns = [t for t in txns if str(t.get("date", "")) >= sd]
        if ed:
            txns = [t for t in txns if str(t.get("date", "")) <= ed]
        ti = sum(float(t["amount"]) for t in txns if t["type"] == "income")
        te = sum(float(t["amount"]) for t in txns if t["type"] == "expense")
        # 按时间分组统计趋势
        ig = defaultdict(float)
        eg = defaultdict(float)
        for t in txns:
            gk = StatisticsService._gk(t.get("date", ""), gb)
            am = float(t["amount"])
            if t["type"] == "income":
                ig[gk] += am
            else:
                eg[gk] += am
        ag = sorted(set(list(ig.keys()) + list(eg.keys())))
        trend = [{
            "period": g, "income": round(ig.get(g, 0), 2),
            "expense": round(eg.get(g, 0), 2),
            "balance": round(ig.get(g, 0) - eg.get(g, 0), 2)
        } for g in ag]
        # 按分类和账户汇总
        ec = defaultdict(float)
        ic = defaultdict(float)
        ea = defaultdict(float)
        ia = defaultdict(float)
        for t in txns:
            am = float(t["amount"])
            if t["type"] == "expense":
                ec[t.get("category", "其他")] += am
                ea[t.get("account_name", "未知")] += am
            else:
                ic[t.get("category", "其他")] += am
                ia[t.get("account_name", "未知")] += am
        return {
            "total_income": round(ti, 2),
            "total_expense": round(te, 2),
            "balance": round(ti - te, 2),
            "trend": trend,
            "expense_by_category": [
                {"name": k, "amount": round(v, 2)}
                for k, v in sorted(ec.items(), key=lambda x: x[1], reverse=True)
            ],
            "income_by_category": [
                {"name": k, "amount": round(v, 2)}
                for k, v in sorted(ic.items(), key=lambda x: x[1], reverse=True)
            ],
            "pie_chart": "",
            "line_chart": ""
        }

    @staticmethod
    def _gk(ds, gb):
        """
        根据日期字符串和分组方式生成时间分组键
        如：2026-05-21, month → "2026-05"
        """
        if not ds:
            return "未知"
        if isinstance(ds, (datetime, date)):
            ds = ds.strftime("%Y-%m-%d")
        p = ds.split("-")
        if gb == "year":
            return p[0]
        if gb == "month":
            return f"{p[0]}-{p[1]}"
        if gb == "day":
            return ds
        if gb == "week":
            try:
                d = datetime.strptime(ds, "%Y-%m-%d")
                return (d - timedelta(days=d.weekday())).strftime("%Y-%m-%d")
            except:
                return ds
        return ds
