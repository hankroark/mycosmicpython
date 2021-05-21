from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        return self.available_quantity >= line.qty and self.sku == line.sku
