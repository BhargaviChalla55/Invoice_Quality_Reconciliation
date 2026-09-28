import unittest
from refresh import database

class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.raw=dict(vendors=[dict(vendor_id='V1',vendor_name='Supplier')],invoices=[],ledger=[])
    def invoice(self,doc='A',entity='North',number='INV-1',vendor='V1'):
        self.raw['invoices'].append(dict(document_id=doc,entity=entity,vendor_id=vendor,invoice_number=number,invoice_date='2026-01-01',posting_date='2026-01-01',amount_cents=10000))
    def ledger(self,line='L1',doc='A',amount=10000):
        self.raw['ledger'].append(dict(line_id=line,document_id=doc,entity='North',posting_date='2026-01-01',amount_cents=amount))
    def scalar(self,sql):
        db=database(self.raw)
        try:return db.execute(sql).fetchone()[0]
        finally:db.close()
    def test_normalization_and_entity_scope(self):
        self.invoice();self.invoice('B',number=' inv 1 ');self.invoice('C',entity='West')
        self.assertEqual(self.scalar('SELECT SUM(duplicate_flag) FROM invoice_review'),2)
    def test_split_posting(self):
        self.invoice();self.ledger(amount=6000);self.ledger('L2',amount=4000)
        self.assertEqual(self.scalar('SELECT COUNT(*) FROM invoice_review'),1)
        self.assertEqual(self.scalar('SELECT difference_cents FROM invoice_review'),0)
    def test_tolerance(self):
        self.invoice();self.ledger(amount=10001)
        self.assertEqual(self.scalar('SELECT amount_flag FROM invoice_review'),0)
        self.raw['ledger'][0]['amount_cents']=10002
        self.assertEqual(self.scalar('SELECT amount_flag FROM invoice_review'),1)
    def test_offsetting_errors(self):
        self.invoice();self.ledger(doc='OTHER')
        self.assertEqual(self.scalar('SELECT SUM(difference_cents) FROM reconciliation'),0)
        self.assertEqual(self.scalar('SELECT COUNT(*) FROM exceptions'),2)
    def test_overlapping_flags(self):
        self.invoice(vendor='UNKNOWN');self.raw['invoices'][0]['invoice_date']='2026-02-01'
        self.assertEqual(self.scalar('SELECT COUNT(*) FROM exceptions'),3)
    def test_period_shift(self):
        self.invoice();self.ledger();self.raw['ledger'][0]['posting_date']='2026-02-01'
        self.assertEqual(self.scalar('SELECT amount_flag FROM invoice_review'),0)
        self.assertEqual(self.scalar('SELECT SUM(ABS(difference_cents)) FROM reconciliation'),20000)
    def test_balanced_duplicate_still_flagged(self):
        self.invoice();self.invoice('B');self.ledger();self.ledger('L2','B')
        self.assertEqual(self.scalar('SELECT SUM(difference_cents) FROM reconciliation'),0)
        self.assertEqual(self.scalar('SELECT SUM(duplicate_flag) FROM invoice_review'),2)

if __name__=='__main__':unittest.main(verbosity=2)
