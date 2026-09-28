# Invoice Quality & Reconciliation

**Bhargavi Challa**  
Accounting & Data Analytics | Independent graduate portfolio

An applied accounting analytics project examining invoice quality, ledger alignment and exception review. SQL combines invoice records, supplier reference data and ledger postings into a reproducible control process. An offline dashboard presents the findings by entity and month.

## Dashboard

Download the repository and open **dashboard.html** in Chrome, Safari or Edge. No installation is required for viewing. The dashboard includes:

- Entity and reporting-period filters.
- Invoice activity, review population and net reconciliation metrics.
- Exception categories and a monthly register-versus-ledger chart.
- A bridge explaining the selected reconciliation difference.
- A searchable exception register with assigned review owners and recommended actions.
- Export of the filtered worklist as JSON.

GitHub's source viewer does not run the dashboard; download the repository first. The report is a saved analytical snapshot, not a live ERP connection. `src/report.html` is the generation template; **dashboard.html** is the complete report.

## Research objective

Determine whether combining transaction-level checks with aggregate reconciliation reveals accounting issues that agreement of totals alone would miss. The deliberately seeded duplicate records appear in both source and ledger data, so they reconcile while still warranting investigation.

## Dataset and results

All data is synthetic. The sample spans three entities and January–June 2026, with USD amounts stored in integer cents.

| Measure | Result |
|---|---:|
| Invoice records | 612 |
| Vendor master records | 30 |
| Ledger lines | 610 |
| Invoice records requiring review | 63 (10.3%) |
| Exception events, including ledger-only documents | 68 |
| Invoice register activity | $3,097,272.71 |
| Ledger activity | $3,056,559.90 |
| Net source-to-ledger difference | $40,712.81 |

Exception counts are analytical flags, not confirmed errors. Monetary differences are not savings or loss. See [RESEARCH_REPORT.md](RESEARCH_REPORT.md) for the interpretation and limitations.

## Analytical controls

| Control | Method |
|---|---|
| Potential duplicate | Repeated entity + vendor + normalized invoice reference |
| Vendor master gap | Invoice supplier ID has no master-data match |
| Date sequence | Invoice date follows source posting date |
| Missing ledger posting | No ledger match for entity + document ID |
| Amount mismatch | Aggregated matched ledger differs from invoice by more than $0.01 |
| Ledger-only document | Ledger document lacks a source invoice |

Ledger lines are aggregated before joining to avoid multiplying source amounts. Source references remain intact; normalization is calculated separately. Entity/month reconciliation aggregates the two sources independently.

## Reproduce

The analysis requires Python 3.9+ with SQLite support. It has no third-party dependencies.

```sh
python3 refresh.py
python3 test_analysis.py
```

On Windows, use `py` if appropriate. `data/source.json` contains the original synthetic inputs. Refresh preserves that file and overwrites derived reports, the database and dashboard. Copy the folder before experimenting. Tests use isolated in-memory data and do not alter the report.

## Files

| File | Purpose |
|---|---|
| `dashboard.html` | Complete, interactive offline report |
| `analysis.sql` | Document controls and reconciliation logic |
| `refresh.py` | Reproducible data generation, validation and refresh |
| `test_analysis.py` | Independent boundary tests |
| `accounting.sqlite` | Source tables and analytical views |
| `data/` | Synthetic input and derived JSON results |
| `RESEARCH_REPORT.md` | Research design, findings and limitations |
| `DATA_DICTIONARY.md` | Fields, measures and assumptions |
| `QUICK_START.md` | Opening and using the report |
| `src/report.html` | Source template used by refresh |
| `validation.json` | Refresh-check results |

## Scope

This is a reconciliation of invoice-related posting activity, not ending accounts payable. Payments, opening balances, credit notes, currency translation, tax calculations and purchase-order matching are outside scope. Production use would need access controls, source validation, approval workflows and exception resolution tracking.

## Development note

The initial implementation, synthetic dataset and documentation were developed with AI assistance for an independent learning project. The project is not represented as completed university coursework, client work or a production deployment. Personal validation and extensions should be described according to the work actually performed. The dashboard uses HTML/JavaScript; no Power BI report is included.
