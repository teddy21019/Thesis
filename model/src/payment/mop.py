"""Means of payments as a dataclass"""

from dataclasses import dataclass, field

@dataclass(eq=True, frozen=True)
class MeansOfPaymentType:
    """
        Means of payment dataclass that is hashable.

        - Hashable: Can be used in dict/set...
        - Exchange rate: Relative to real goods.
    """
    name: str
    exchange_rate_to_real: float = field(compare=False, default=1)

    def __str__(self) -> str:
        return self.name