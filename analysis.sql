-- Monetary values are integer USD cents. Raw records remain unchanged.
CREATE VIEW invoice_review AS
WITH normalized AS (
 SELECT *, UPPER(REPLACE(REPLACE(TRIM(invoice_number),'-',''),' ','')) AS invoice_key FROM invoices
), duplicate_groups AS (
 SELECT entity,vendor_id,invoice_key,COUNT(*) AS n FROM normalized
 GROUP BY entity,vendor_id,invoice_key HAVING COUNT(*)>1
), gl AS (
 SELECT entity,document_id,SUM(amount_cents) AS amount_cents FROM ledger GROUP BY entity,document_id
)
SELECT i.*,v.vendor_name,COALESCE(g.amount_cents,0) AS ledger_cents,
 i.amount_cents-COALESCE(g.amount_cents,0) AS difference_cents,
 CASE WHEN d.n IS NOT NULL THEN 1 ELSE 0 END AS duplicate_flag,
 CASE WHEN v.vendor_id IS NULL THEN 1 ELSE 0 END AS vendor_flag,
 CASE WHEN i.invoice_date>i.posting_date THEN 1 ELSE 0 END AS date_flag,
 CASE WHEN g.document_id IS NULL THEN 1 ELSE 0 END AS missing_flag,
 CASE WHEN g.document_id IS NOT NULL AND ABS(i.amount_cents-g.amount_cents)>1 THEN 1 ELSE 0 END AS amount_flag
FROM normalized i
LEFT JOIN vendors v ON i.vendor_id=v.vendor_id
LEFT JOIN duplicate_groups d ON i.entity=d.entity AND i.vendor_id=d.vendor_id AND i.invoice_key=d.invoice_key
LEFT JOIN gl g ON i.entity=g.entity AND i.document_id=g.document_id;

CREATE VIEW exceptions AS
SELECT entity,document_id,posting_date,amount_cents,'Potential duplicate' AS issue,'AP lead' AS owner,
 'Compare the original supplier invoice and purchase order before determining which record to retain.' AS action
FROM invoice_review WHERE duplicate_flag=1
UNION ALL SELECT entity,document_id,posting_date,amount_cents,'Vendor master gap','Vendor master team',
 'Verify supplier identity and the authorized master record.' FROM invoice_review WHERE vendor_flag=1
UNION ALL SELECT entity,document_id,posting_date,amount_cents,'Date sequence','AP accountant',
 'Check document dates and service period; assess cutoff with the controller.' FROM invoice_review WHERE date_flag=1
UNION ALL SELECT entity,document_id,posting_date,amount_cents,'Missing ledger posting','GL accountant',
 'Investigate timing or interface failure; obtain approval before posting.' FROM invoice_review WHERE missing_flag=1
UNION ALL SELECT entity,document_id,posting_date,amount_cents,'Amount mismatch','GL accountant',
 'Compare source and ledger details; investigate coding, tax or entry differences.' FROM invoice_review WHERE amount_flag=1
UNION ALL SELECT l.entity,l.document_id,MIN(l.posting_date),SUM(l.amount_cents),'Ledger-only document','Controller',
 'Determine whether the document is an authorized accrual or has missing source support.'
FROM ledger l LEFT JOIN invoices i ON l.entity=i.entity AND l.document_id=i.document_id
WHERE i.document_id IS NULL GROUP BY l.entity,l.document_id;

-- Posting activity only: not an ending AP balance reconciliation.
CREATE VIEW reconciliation AS
WITH movements AS (
 SELECT entity,SUBSTR(posting_date,1,7) AS period,amount_cents AS source_cents,0 AS ledger_cents FROM invoices
 UNION ALL
 SELECT entity,SUBSTR(posting_date,1,7),0,amount_cents FROM ledger
)
SELECT entity,period,SUM(source_cents) AS source_cents,SUM(ledger_cents) AS ledger_cents,
 SUM(source_cents)-SUM(ledger_cents) AS difference_cents
FROM movements GROUP BY entity,period;
