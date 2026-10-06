from datetime import date

from dti import store
from dti.cli import main
from dti.reports.base import REGISTRY, Flag, Report


class FakeSplits(Report):
    name = "_test_splits"
    title = "Stock Splits"

    def fetch(self):
        self.sources.append("https://example.com/splits")
        return [("NVDA", "10-for-1"), ("<b>X</b>", "1-for-20")]

    def normalize(self, raw):
        self.flags.append(Flag("sources disagree on ratio", item="X"))
        return [{"Ticker": t, "Ratio": r} for t, r in raw]


class FakeEmpty(FakeSplits):
    name = "_test_empty"

    def normalize(self, raw):
        return []


def test_registered():
    assert REGISTRY["_test_splits"] is FakeSplits


def test_run_renders_table_and_escapes():
    d = FakeSplits(date(2026, 10, 6)).run()
    assert d.subject == "Stock Splits - Tue 10/06/26"
    assert "<td style=\"padding: 4px 8px;\">NVDA</td>" in d.html
    assert "&lt;b&gt;X&lt;/b&gt;" in d.html  # source text is escaped
    assert d.sources == ["https://example.com/splits"]
    assert d.flags[0].item == "X"
    assert not d.empty


def test_empty_report():
    d = FakeEmpty(date(2026, 10, 6)).run()
    assert d.empty
    assert "Nothing to report today." in d.html


def test_store_roundtrip(tmp_path):
    conn = store.connect(str(tmp_path / "t.sqlite3"))
    draft_id = store.save_draft(conn, FakeSplits(date(2026, 10, 6)).run())
    rows = store.drafts_for_day(conn, "2026-10-06")
    assert [r["id"] for r in rows] == [draft_id]
    assert rows[0]["status"] == "needs_review"


def test_cli_dry_run(tmp_path, capsys):
    assert main(["run", "_test_splits", "--date", "2026-10-06", "--out", str(tmp_path), "--dry-run"]) == 0
    assert (tmp_path / "2026-10-06__test_splits.html").exists()
    assert "1 flag(s)" in capsys.readouterr().out
