"""Rebuild the report using Python 3.9+ (standard library only).
Existing source.json is preserved. Outputs are overwritten on refresh.
"""
import json,random,sqlite3
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent

def generate():
    rng=random.Random(20260928)
    vendors=[dict(vendor_id=f'V{i:03}',vendor_name=f'Supplier {i:02}') for i in range(1,31)]
    invoices=[];ledger=[]
    for n in range(1,601):
        entity=['North','Central','West'][(n-1)%3]
        # Known defects are spread across months; no real-world error rate implied.
        month=1+(n-1)%6;day=1+(n-1)//24
        date=f'2026-{month:02}-{day:02}'
        r=dict(document_id=f'AP{n:04}',entity=entity,vendor_id=f'V{1+(n-1)%30:03}',invoice_number=f'INV-{n:05}',invoice_date=date,posting_date=date,amount_cents=rng.randint(10000,950000))
        if 21<=n<=35:r['vendor_id']='V999'
        if 41<=n<=46:r['invoice_date']=f'2026-{month+1:02}-01'
        invoices.append(r)
        if not 61<=n<=68:
            total=r['amount_cents']+(25000 if 81<=n<=90 else 0)
            for amount in ([total//2,total-total//2] if n==100 else [total]):
                ledger.append(dict(line_id=f'GL{len(ledger)+1:04}',entity=entity,document_id=r['document_id'],posting_date=date,amount_cents=amount))
    for n in range(12):
        r=dict(invoices[n]);r['document_id']=f'DUP{n+1:03}';r['invoice_number']=' '+r['invoice_number'].lower().replace('-',' ')+' '
        invoices.append(r)
        ledger.append(dict(line_id=f'GL{len(ledger)+1:04}',entity=r['entity'],document_id=r['document_id'],posting_date=r['posting_date'],amount_cents=r['amount_cents']))
    for n in range(5):
        ledger.append(dict(line_id=f'GL{len(ledger)+1:04}',entity=['North','Central','West'][n%3],document_id=f'MAN{n+1:03}',posting_date='2026-06-28',amount_cents=50000*(n+1)))
    return dict(vendors=vendors,invoices=invoices,ledger=ledger)

def database(raw):
    db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    db.executescript('''
    CREATE TABLE vendors(vendor_id TEXT PRIMARY KEY,vendor_name TEXT NOT NULL);
    CREATE TABLE invoices(document_id TEXT NOT NULL,entity TEXT NOT NULL,vendor_id TEXT NOT NULL,invoice_number TEXT NOT NULL,invoice_date TEXT NOT NULL,posting_date TEXT NOT NULL,amount_cents INTEGER NOT NULL CHECK(amount_cents>0),PRIMARY KEY(entity,document_id));
    CREATE TABLE ledger(line_id TEXT PRIMARY KEY,entity TEXT NOT NULL,document_id TEXT NOT NULL,posting_date TEXT NOT NULL,amount_cents INTEGER NOT NULL);
    ''')
    for table,rows in raw.items():
        if not rows:continue
        keys=list(rows[0])
        db.executemany(f'INSERT INTO {table} ({",".join(keys)}) VALUES ({",".join("?" for _ in keys)})',[[r[k] for k in keys] for r in rows])
    db.executescript((ROOT/'analysis.sql').read_text())
    return db

def main():
    directory=ROOT/'data';directory.mkdir(exist_ok=True)
    source=directory/'source.json'
    if not source.exists():source.write_text(json.dumps(generate(),indent=2))
    raw=json.loads(source.read_text());db=database(raw)
    query=lambda view:[dict(r) for r in db.execute('SELECT * FROM '+view)]
    review=query('invoice_review');exceptions=query('exceptions');recon=query('reconciliation')
    source_total=sum(r['amount_cents'] for r in raw['invoices']);gl_total=sum(r['amount_cents'] for r in raw['ledger'])
    assert sum(r['source_cents'] for r in recon)==source_total
    assert sum(r['ledger_cents'] for r in recon)==gl_total
    assert len(review)==len(raw['invoices'])
    missing=sum(r['amount_cents'] for r in review if r['missing_flag'])
    matched=sum(r['difference_cents'] for r in review if not r['missing_flag'])
    ledger_only=sum(r['amount_cents'] for r in exceptions if r['issue']=='Ledger-only document')
    assert missing+matched-ledger_only==source_total-gl_total
    counts=dict(Counter(r['issue'] for r in exceptions))
    if raw==generate():
        assert sorted(counts.values())==[5,6,8,10,15,24]
        assert next(r for r in review if r['document_id']=='AP0100')['difference_cents']==0
    payload=dict(review=review,exceptions=exceptions,reconciliation=recon)
    for name,rows in payload.items():(directory/(name+'.json')).write_text(json.dumps(rows,indent=2))
    db.commit()
    with sqlite3.connect(ROOT/'accounting.sqlite') as target:db.backup(target)
    template=(ROOT/'src'/'report.html').read_text()
    html=template.replace('__DATA__',json.dumps(payload).replace('</','<\\/'))
    (ROOT/'dashboard.html').write_text(html)
    summary=dict(invoice_records=len(review),exception_events=len(exceptions),flagged_invoices=sum(any(r[k] for k in ['duplicate_flag','vendor_flag','date_flag','missing_flag','amount_flag']) for r in review),source_cents=source_total,ledger_cents=gl_total,difference_cents=source_total-gl_total,missing_cents=missing,matched_difference_cents=matched,ledger_only_cents=ledger_only,counts=counts)
    (directory/'summary.json').write_text(json.dumps(summary,indent=2))
    (ROOT/'validation.json').write_text(json.dumps(dict(status='passed',checks=['source control total','ledger control total','join cardinality','independent difference bridge','baseline controls when applicable']),indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
