# Open and use the report

1. Extract the ZIP archive.
2. Open **dashboard.html** with Chrome, Safari or Edge.
3. Select an entity or reporting period to narrow the results.
4. Use exception category and document search to refine the review register.
5. Export worklist saves the displayed exception records as a JSON file.

The report works offline. No commands, account or software installation are needed to view it. It contains a saved synthetic-data snapshot; filters are interactive but the underlying data is not live.

To refresh after changing inputs, use Python 3.9+ to run `refresh.py` from this folder, then reopen the dashboard. Keep a baseline copy before making changes. `src/report.html` is a developer template, not the finished report.

## GitHub

Suggested repository name: **invoice-quality-reconciliation**.

Suggested description: **SQL-based invoice quality controls, ledger reconciliation and an interactive accounting analytics dashboard.**

Upload the contents of the extracted folder, including data and src, with README.md at the repository root. Upload files rather than the ZIP. No GitHub publishing or website hosting is performed by this package. GitHub previews the README; visitors can download the repository to open the report.
