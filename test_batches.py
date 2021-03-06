import unittest
from datetime import date
from model import Batch, OrderLine


def make_batch_and_line(sku, batch_qty, line_qty):
    return(
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty),
    )


class TestBatchesAndOrderLines(unittest.TestCase):

    def test_allocating_to_a_batch_reduces_the_available_quantity(self):
        batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
        line = OrderLine("order-ref", "SMALL-TABLE", 2)
        batch.allocate(line)
        self.assertEqual(18, batch.available_quantity)

    def test_does_not_allocate_if_line_bigger_than_batch(self):
        small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
        small_batch.allocate(large_line)
        self.assertEqual(2, small_batch.available_quantity)

    def test_can_allocate_if_available_greater_than_required(self):
        large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
        self.assertTrue(large_batch.can_allocate(small_line))

    def test_cannot_allocate_if_available_smaller_than_required(self):
        small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
        self.assertFalse(small_batch.can_allocate(large_line))

    def test_can_allocate_if_available_equal_to_required(self):
        batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
        self.assertTrue(batch.can_allocate(line))

    def test_cannot_allocate_if_skus_do_not_match(self):
        batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
        different_sku_line = OrderLine("order-123", "EXPENSIVE_TOASTER", 10)
        self.assertFalse(batch.can_allocate(different_sku_line))

    def test_can_only_deallocate_allocated_lines(self):
        batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
        batch.deallocate(unallocated_line)
        self.assertEqual(20, batch.available_quantity)

    def test_can_deallocate_allocated_lines(self):
        batch, line = make_batch_and_line("DECORATIVE-TRINKET", 2, 2)
        batch.allocate(line)
        self.assertEqual(0, batch.available_quantity)
        batch.deallocate(line)
        self.assertEqual(2, batch.available_quantity)

    def test_allocation_is_idempotent(self):
        batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
        batch.allocate(line)
        batch.allocate(line)
        self.assertEqual(18, batch.available_quantity)


if __name__ == '__main__':
    unittest.main()
