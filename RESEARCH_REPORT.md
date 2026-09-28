# Invoice Quality and Ledger Reconciliation

**Bhargavi Challa — Accounting & Data Analytics**

## Abstract

This synthetic-data study evaluates how record-level controls complement aggregate invoice-to-ledger reconciliation. A reproducible dataset of 612 invoice records produces 63 flagged source records and five ledger-only documents. Twelve duplicate pairs occur on both sides of the reconciliation, illustrating why equal totals are insufficient evidence of transaction quality. Findings describe the constructed case and are not estimates of real-world accounting error rates.

## Research design

The comparison uses two approaches: aggregate reconciliation alone, and aggregate reconciliation combined with document-level controls. The design deliberately introduces known anomalies to verify expected behavior. It is a control demonstration, not a statistical inference exercise.

Six hundred original invoices are allocated across three entities and six months. Twelve copies use modified spacing and capitalization in invoice references. Known vendor gaps, date issues, missing postings, amount mismatches and ledger-only documents are introduced. One legitimate split ledger posting tests join design. Raw data is retained, and calculated keys support comparisons without overwriting evidence.

## Findings

| Category | Events | Review implication |
|---|---:|---|
| Potential duplicate | 24 | Twelve candidate pairs require source-document comparison |
| Vendor master gap | 15 | Validate the supplier and completeness of the reference extract |
| Date sequence | 6 | Review dates and service period before assessing cutoff |
| Missing ledger posting | 8 | Investigate timing or interface completeness |
| Amount mismatch | 10 | Examine coding, tax treatment or entry differences |
| Ledger-only document | 5 | Determine whether an accrual is supported or a source record is missing |

There are 68 events. The invoice population contains 63 flagged records; ledger-only documents are outside that population. In general one invoice can trigger several controls. Duplicate events count both records, not just the extra copy.

The register totals $3,097,272.71 and ledger activity totals $3,056,559.90. The $40,712.81 difference is explained by $50,712.81 missing from the ledger, less $2,500.00 of excess matched ledger amounts and $7,500.00 of ledger-only activity. These values must not be described as savings or confirmed misstatements.

## Accounting interpretation

Aggregate reconciliation identifies the net imbalance but not its underlying causes. Document controls reveal matching duplicate postings, supplier-reference gaps and date-sequence issues that need not affect the net difference. Conversely, a full-period document match can conceal posting-period differences, which the monthly reconciliation can reveal.

Missing postings relate to completeness; mismatches prompt accuracy review; duplicates prompt occurrence and authorization review; unusual dates prompt cutoff investigation. None of the rules independently establishes an audit finding or fraud.

## Validation approach

Independent totals are compared with the source register and ledger. A separately calculated difference bridge must equal the reconciliation result. The joined review must preserve source row count. Baseline assertions verify seeded control counts and a valid split posting. Isolated tests cover normalization, entity boundaries, legitimate split postings, one-cent tolerance, overlapping rules, offsetting errors and period shifts.

## Limitations

- Seeded anomalies make detection predictable; no real-world precision or recall is claimed.
- Matching assumes entity/document IDs are shared by both systems.
- Normalization catches formatting differences but not all near-duplicate references.
- A supplier missing from this extract might still be legitimate.
- Ledger-only documents may be authorized accruals.
- The one-cent tolerance is a documented study assumption, not a universal accounting threshold.
- No ending AP balances, payments, credit memos, foreign exchange or tax compliance determinations are modeled.

## Extension opportunities

Add an independently adjudicated set of legitimate exceptions to measure false positives. Introduce credit notes and purchase-order/receipt matching. Add an approval-backed resolution log without changing raw inputs. A separate Power BI report could reproduce the SQL measures, with its results reconciled to the baseline before publication.

## Conclusion

Transaction-quality analysis and aggregate reconciliation address different questions. The combined approach provides a more informative review queue in this constructed case while retaining the need for supporting evidence and professional judgment.
