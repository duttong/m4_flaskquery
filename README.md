# M4 Flask Query

A small PyQt desktop tool for looking up flask fill metadata by flask number. Given a flask number and an analysis date, it finds the most recent matching flask event in the HATS database and displays the site code, fill date, and pair ID — along with a combined string formatted for quick copy/paste into other tools.

## Files

- **flaskquery.py** — main application, built with PyQt5.
- **flaskquery_pyqt6.py** — equivalent application built with PyQt6, for environments where PyQt6 is preferred/available instead of PyQt5.

## Requirements

- Python 3
- PyQt5 (for `flaskquery.py`) or PyQt6 (for `flaskquery_pyqt6.py`)
- Access to the `db_utils` package at `/Volumes/ccg/src/db/` and read access to the `hats` database (via `db_conn.HATS_ng()`)

## Usage

```bash
python3 flaskquery.py
```

Enter a flask number and an analysis date, then click **Query** (or press Enter in the flask number field). The tool queries `hats.hatsflask_event_view` for the most recent event prior to the analysis date matching that flask ID, and populates:

- **Site Code**
- **Fill Date**
- **Pair ID**
- **Combined** — a lowercased `site filldate #flasknumber-pairid` string, auto-selected for easy copying.

## Data source

Queries run against the `hats.hatsflask_event_view` view (columns include `site`, `pair_id`, `flask_id`, `ev_datetime`), which replaced the deprecated `hats.Status_MetData` table.
