# Data dictionary

## Source tables

| Table | Grain / key | Fields |
|---|---|---|
| invoices | One source invoice; entity + document_id | vendor_id, invoice_number, invoice_date, posting_date, amount_cents |
| vendors | One supplier; vendor_id | vendor_name |
| ledger | One posting line; line_id | entity, document_id, posting_date, amount_cents |

Dates use ISO YYYY-MM-DD. Amounts are integer USD cents. Source invoice amounts must be positive. Ledger lines are summed by entity/document before matching; multiple lines per document are supported. Vendor relationships are deliberately not enforced as foreign keys, preserving unmatched records for review.

## Derived measures

| Measure | Definition |
|---|---|
| invoice_key | Uppercase supplier reference with spaces and hyphens removed |
| ledger_cents | Sum of ledger lines matching entity/document |
| difference_cents | Invoice amount less ledger amount; absent ledger treated as zero |
| duplicate_flag | Repeated entity/vendor/invoice_key |
| vendor_flag | No matching vendor master record |
| date_flag | Invoice date later than source posting date |
| missing_flag | No matching entity/document ledger record |
| amount_flag | Existing matched ledger differs by more than one cent |
| Flagged invoices | Source records satisfying at least one flag |
| Exception events | One row per document/control, plus ledger-only documents |
| Reconciliation | Independently aggregated source and ledger by posting month/entity |

## Dashboard behavior

Entity and reporting-period selections filter all panels. Exception category and document search affect only the exception register and its exported worklist. A blank search includes all document IDs. Reset restores all filters. No date controls imply live refresh.

The bridge shows missing postings, matched/timing variance, negative ledger-only activity and the resulting net difference. Matched/timing variance is the residual needed to reconcile the selected posting periods; across all periods it equals the sum of matched-document differences. A monthly shift can change this component even if full-period document amounts match.

Balanced status means a zero aggregate difference only, not absence of record-quality flags. Worklist document amounts must not be summed as exposure or savings, because overlapping controls may repeat amounts.
