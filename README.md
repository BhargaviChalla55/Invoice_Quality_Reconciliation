# Invoice Quality & Reconciliation

**Bhargavi Challa**  
Accounting & Data Analytics Portfolio

## Project Overview

I created this project to explore how accounting knowledge, SQL, and data analytics can be combined to review invoice activity and reconcile transactions to the general ledger.

The analysis brings together invoice records, vendor master data, and ledger postings to identify transactions that may require additional review. The project focuses on common accounting issues such as duplicate invoices, missing vendor records, posting-date exceptions, missing ledger entries, and amount differences.

I also built an interactive dashboard to make the results easier to review across entities and reporting periods.

## Dashboard

The interactive report is available in **`dashboard.html`**.

Download the repository and open `dashboard.html` in Chrome, Safari, or Edge. No additional installation is required to view the dashboard.

The dashboard allows users to:

- Filter results by entity and reporting period
- Review invoice register and general ledger activity
- Identify invoices requiring additional review
- Analyze exceptions by category
- Compare monthly invoice and ledger activity
- Review the components driving reconciliation differences
- Search individual exception records
- Export a filtered exception worklist

> **Note:** GitHub's file viewer does not run the interactive dashboard directly. Download the repository and open `dashboard.html` locally to use the dashboard.

## Why I Built This Project

One of the ideas I wanted to demonstrate is that a reconciliation can balance while individual transactions may still require investigation.

For example, if a duplicate invoice appears in both the invoice register and the general ledger, the two sources may still reconcile. Looking only at the final reconciliation difference would not necessarily identify that issue.

For this reason, I combined two approaches:

1. **Transaction-level exception testing**
2. **Invoice-to-ledger reconciliation**

This provides both a high-level view of the reconciliation and a more detailed review of the transactions behind it.

## Dataset

The project uses a fully synthetic dataset created for analysis and portfolio demonstration.

The sample covers three entities from **January through June 2026**.

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

The exception results represent records requiring additional review. They should not automatically be interpreted as accounting errors, financial losses, or audit findings.

For a more detailed explanation of the results and limitations, see [RESEARCH_REPORT.md](RESEARCH_REPORT.md).

## Accounting & Data Controls

I used the following controls to identify transactions requiring review:

| Control | Logic |
|---|---|
| Potential duplicate | Repeated entity + vendor + normalized invoice reference |
| Vendor master gap | Invoice vendor ID does not have a matching vendor master record |
| Date sequence | Invoice date occurs after the source posting date |
| Missing ledger posting | Invoice does not have a matching ledger record |
| Amount mismatch | Matched ledger amount differs from the invoice amount by more than $0.01 |
| Ledger-only document | Ledger document does not have a corresponding source invoice |

Ledger lines are aggregated before matching them to invoices. This prevents invoice amounts from being duplicated when multiple ledger lines relate to the same document.

## Reconciliation Approach

The reconciliation compares invoice register activity with general ledger activity by entity and reporting period.

Instead of looking only at the final difference, I separated the reconciliation into components that help explain what is driving the variance.

These include:

- Missing ledger postings
- Matched amount differences
- Ledger-only activity
- Posting-period differences

This makes it easier to move from the overall reconciliation balance to the individual transactions that may require follow-up.

## Key Results

The analysis identified **63 invoice records requiring review**, representing **10.3% of the invoice population**.

Across the analysis, there were **68 exception events**, including ledger-only documents.

The invoice register contained **$3,097,272.71** of activity compared with **$3,056,559.90** in ledger activity, resulting in a net source-to-ledger difference of **$40,712.81**.

The exception categories include:

| Exception | Events |
|---|---:|
| Potential duplicate | 24 |
| Vendor master gap | 15 |
| Date sequence | 6 |
| Missing ledger posting | 8 |
| Amount mismatch | 10 |
| Ledger-only document | 5 |

These results are based on intentionally constructed synthetic data and are designed to demonstrate the control and reconciliation process rather than estimate real-world accounting error rates.

## Tools & Skills Demonstrated

### SQL / SQLite

Used for:

- Data joins
- Aggregations
- Invoice-to-ledger matching
- Duplicate identification
- Exception testing
- Reconciliation logic
- Analytical views

### Python

Used for:

- Data processing
- Refreshing analytical outputs
- Validation
- Testing reconciliation logic

### Accounting Analysis

Applied concepts including:

- Accounts payable
- General ledger reconciliation
- Transaction completeness
- Transaction accuracy
- Duplicate invoice review
- Vendor master review
- Cutoff and posting-date analysis
- Exception investigation

### HTML / JavaScript

Used to present the results through an interactive accounting analytics dashboard with filters, reconciliation views, exception details, and worklist export.

## Running the Analysis

Python 3.9+ with SQLite support is required to reproduce the analysis.

Run:

```bash
python3 refresh.py
python3 test_analysis.py
```

On Windows, `py` can be used instead of `python3` where appropriate.

The refresh process rebuilds the analytical outputs, database, validation results, and dashboard from the synthetic source data.

## Project Structure

```text
Invoice_Quality_Reconciliation/
│
├── README.md
├── dashboard.html
├── analysis.sql
├── refresh.py
├── test_analysis.py
├── accounting.sqlite
├── validation.json
│
├── DATA_DICTIONARY.md
├── RESEARCH_REPORT.md
├── QUICK_START.md
│
├── data/
│   └── Synthetic source and derived data
│
└── src/
    └── report.html
```

## Project Files

| File | Purpose |
|---|---|
| `dashboard.html` | Complete interactive accounting analytics dashboard |
| `analysis.sql` | SQL controls and reconciliation logic |
| `refresh.py` | Data refresh and validation process |
| `test_analysis.py` | Tests for analytical logic |
| `accounting.sqlite` | SQLite database containing source tables and analytical views |
| `data/` | Synthetic source and derived data |
| `RESEARCH_REPORT.md` | Detailed analysis, findings, and limitations |
| `DATA_DICTIONARY.md` | Data fields, calculated measures, and assumptions |
| `QUICK_START.md` | Instructions for opening and using the project |
| `src/report.html` | Dashboard generation template |
| `validation.json` | Validation results |

## Validation

I included validation checks to confirm that the analytical process remains consistent.

The validation covers:

- Source control totals
- Ledger control totals
- Join cardinality
- Independent reconciliation difference
- Baseline control results

This helps verify that the reconciliation and exception logic continue to produce the expected results when the analysis is refreshed.

## Key Takeaway

The main takeaway from this project is that **a balanced reconciliation does not necessarily mean every underlying transaction is correct**.

Aggregate reconciliation is useful for identifying differences between accounting sources, while transaction-level testing can identify issues that may not affect the overall balance.

Combining both approaches provides a more complete review of invoice quality and helps identify transactions that require additional investigation.

## Scope & Limitations

This project focuses on invoice-related posting activity rather than the complete accounts payable cycle.

The following areas are outside the current scope:

- AP payments
- Opening balances
- Credit memos
- Foreign currency translation
- Tax calculations
- Purchase-order matching
- Three-way matching
- Production approval workflows

The dataset is fully synthetic and the project is intended for learning, accounting analytics practice, and portfolio demonstration.

---

**Bhargavi Challa**  
Accounting & Data Analytics
