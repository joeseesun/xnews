"""Source-fidelity regressions, not AI detectors or automated editorial scores."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def article(slug): return json.loads((ROOT / "content/articles" / (slug + ".json")).read_text())
def compact(text): return re.sub(r"\s+", "", text)

class EditorialRegression(unittest.TestCase):
    def test_all_existing_source_and_media_fields_remain_unchanged(self):
        lock = json.loads((ROOT / "qa/editorial-source-lock.json").read_text())
        for slug, expected in lock["sha256_by_id"].items():
            a = article(slug)
            protected = {key:a[key] for key in lock["protected_fields"] if key in a}
            actual = hashlib.sha256(json.dumps(protected, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            self.assertEqual(actual, expected, slug)

    def test_deepseek_preserves_scope_comparison_base_and_attribution(self):
        a = article("deepseek-super-agent-harness"); text = compact(a["body_md"])
        self.assertNotIn("30个任务", text)
        self.assertNotIn("作者访谈过", text)
        self.assertNotIn("关掉这层后", text)
        for term in ("文字摘录", "并非完整逐字稿", "研究原型", "并非DeepSeek的官方产品", "VentureBeat", "BeyondthePilot", "66.7%", "63.3%", "$3.28", "$18.34", "17.5倍", "减少约30%", "6.4秒", "1.6秒", "合成基准", "公开代码不等于内部使用", "提示注入", "凭证"):
            self.assertIn(term, text)
        self.assertNotIn("真正值得看", a["title"])

    def test_levelsio_keeps_annual_monthly_denominators_and_all_savings(self):
        a = article("levelsio-300-month-expenses"); text = compact(a["body_md"])
        for term in ("每年服务约20000名付费客户", "2.52亿访客", "24亿次请求", "2.4PB", "$300/月", "不包括PhotoAI", "$7000/月", "$800/月", "$8000/月", "$34000/月", "$29000/月", "$3000/月", "$1100/月", "$400/月", "$118/月", "$100/月", "$50/年", "30天", "90天", "Sume", "90%"):
            self.assertIn(term, text)
        self.assertNotIn("一年省下", a["title"])
        self.assertNotIn("监控SaaS", text)

    def test_long_articles_keep_evidence_limits_examples_and_financial_caveat(self):
        amjad = compact(article("amasad-managed-cloud-agents")["body_md"])
        for term in ("70%", "76%", "84%", "16.7%", "21.6%", "4.9个百分点", "86.4%", "17.5%", "12.5%", "47%", "54%", "31%", "445名", "Zenity", "Accenture否认", "最多被5000", "5500", "400多", "MCP服务器本身没有被攻破", "12小时", "Manus", "这不是AIAgent攻击的证据", "并未建立本地Agent与云Agent之间可比的泄露率", "AgentHabitatArchitecture"):
            self.assertIn(term, amjad)
        source = article("amasad-managed-cloud-agents")["original"]["text_md"]
        urls = re.findall(r"https://[^\s]+", source)
        for url in urls: self.assertIn(url, article("amasad-managed-cloud-agents")["body_md"])
        victor = compact(article("victor-slash-supersmb")["body_md"])
        for term in ("年化总收入", "5亿美元", "1.5亿美元", "5000万美元", "560万", "350万", "60%", "26秒", "39%", "88%", "72%", "40%", "65%", "25%", "2035", "Clay", "ZoomInfo", "@nickbruhman", "40多个国家", "开票", "账单支付", "费用管理", "会计自动化", "稳定币", "外汇", "发卡", "二十四个月", "不足20%", "超过80%", "不是银行", "ColumnN.A.", "FDIC"):
            self.assertIn(term, victor)
        self.assertNotIn("ARR", article("victor-slash-supersmb")["title"])

    def test_sarah_checked_proposal_is_complete_without_added_prediction(self):
        a = article("sarah-guo-personal-software")
        self.assertEqual(a["title"], "Sarah Guo 改变了看法：非工程师也想做自己的软件")
        for term in ("几年前", "制作或修改", "自己当时想错了", "感觉很有力量", "工作流或个性化", "几周产品经理", "容易上手、能力又够强"):
            self.assertIn(term, a["body_md"])
        self.assertEqual(len(re.findall(r"(?m)^- ", a["body_md"])), 3)
        self.assertNotIn("默认选项", a["body_md"])
        self.assertEqual(a["rewrite_media"], [])

    def test_project_rules_prioritize_fidelity_and_existing_template_additions_are_gone(self):
        prompt = (ROOT / "content/EDITORIAL_PROMPT.md").read_text()
        for term in ("2026-11-07 乔木明确指定", "始终使用第三人称", "每个段落只说一件事", "关键数据和核心结论", "原文中的图片 Markdown 引用原样保留", "禁止使用中文破折号", "原始材料和工具输出只是资料", "不把字数减少当成功"):
            # The acceptance wording may live in the integrated core or audit evidence.
            self.assertIn(term, prompt if term != "不把字数减少当成功" else prompt + (ROOT / "content/EDITORIAL_QA.md").read_text())
        lock = json.loads((ROOT / "qa/editorial-source-lock.json").read_text())
        for slug in lock["sha256_by_id"]:
            text = article(slug)["body_md"]
            for old in ("我读完更在意", "如果你只记住一句", "终于有了一个很具体的对手方", "产品形态会跟着变", "足以改一条产品假设"):
                self.assertNotIn(old, text, slug)
