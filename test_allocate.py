import unittest
from datetime import date, timedelta
from model import allocate, Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


class TestAllocationService(unittest.TestCase):

    def test_prefers_current_stock_batches_to_shipments(self):
        in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
        shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
        line = OrderLine("oref", "RETRO-CLOCK", 10)

        allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(90, in_stock_batch.available_quantity)
        self.assertEqual(100, shipment_batch.available_quantity)

    def test_prefers_earlier_batches(self):
        earliest = Batch("speed-batch", "MINIMALIST-SPOON", 100, eta=today)
        medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
        latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
        line = OrderLine("order1", "MINIMALIST-SPOON", 10)

        allocate(line, [medium, earliest, latest])

        self.assertEqual(90, earliest.available_quantity)
        self.assertEqual(100, medium.available_quantity)
        self.assertEqual(100, latest.available_quantity)

    def test_returns_allocated_batch_ref(self):
        in_stock_batch = Batch("in-stock-batch", "HIGHBROW-POSTER", 100, eta=None)
        shipment_batch = Batch("shipment-batch", "HIGHBROW-POSTER", 100, eta=tomorrow)
        line = OrderLine("oref", "HIGHBROW-POSTER", 10)

        allocation = allocate(line, [in_stock_batch, shipment_batch])

        self.assertEqual(in_stock_batch.reference, allocation)
