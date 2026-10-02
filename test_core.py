import unittest, tempfile, json, sqlite3, copy
from pathlib import Path
import app as c

class CoreTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test.sqlite'
        self.config = json.loads((Path(__file__).resolve().parent / 'scenario.json').read_text(encoding='utf-8'))

    def test_no_retry(self):
        r = c.simulate([{'id': 'A', 'at': 0, 'service': 1}], 'none', outage=(0, 10))
        self.assertEqual(r['calls'], 1)

    def test_reproducible(self):
        self.assertEqual(c.run({'requests': 15, 'seed': 3}), c.run({'requests': 15, 'seed': 3}))

    def test_deadline(self):
        r = c.simulate([{'id': 'A', 'at': 0, 'service': 10}], 'fixed', deadline=2)
        self.assertEqual(r['calls'], 0)

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            c.simulate([{'id': 'A', 'at': 0, 'service': 1}] * 2, 'fixed')

    def test_capacity(self):
        with self.assertRaises(ValueError):
            c.simulate([], 'fixed', workers=0)

    def test_policy(self):
        with self.assertRaises(ValueError):
            c.simulate([], 'unknown')

    def test_attempt_bound(self):
        r = c.simulate([{'id': 'A', 'at': 0, 'service': 0.1}], 'fixed', outage=(0, 100), max_attempts=3)
        self.assertEqual(r['calls'], 3)

    def test_empty(self):
        self.assertEqual(c.simulate([], 'none')['calls'], 0)
if __name__ == '__main__':
    unittest.main()
