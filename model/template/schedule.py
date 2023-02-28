from __future__ import annotations
from mesa.time import BaseScheduler
from typing import TYPE_CHECKING, Callable, Iterator
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from template.agent import TemplateAgent

class TemplateScheduler(BaseScheduler, ABC):

    def step(self) -> None:

        procedure_list = [
            self._consumption_decision_step,
            self._consumption_bundling_step,
            self._seller_summarize_step,
            self._seller_buyer_toggle_step
        ]

        for func in procedure_list:
            add_separate_line(func)()



    def _consumption_decision_step(self) -> None:
        buyer_consumption_decision_order : Iterator[TemplateAgent] = self._buyer_activation_order()

        for buyer in buyer_consumption_decision_order:
            buyer.decide_consumption()
        return

    def _consumption_bundling_step(self) -> None:
        buyer_shopping_order : Iterator[TemplateAgent] = self._buyer_activation_order()

        for buyer in buyer_shopping_order:
            seller_candidate : Iterator[TemplateAgent] = buyer.seller_candidate
            buyer.shop(seller_candidate)
        return

    def _seller_summarize_step(self) -> None:
        seller_order : Iterator[TemplateAgent] = self._seller_activation_order()

        for seller in seller_order:
            seller.respond_selling_strategy()



    def _seller_buyer_toggle_step(self) -> None:
        ...

    @abstractmethod
    def _buyer_activation_order(self) -> Iterator[TemplateAgent]:
        ...

    @abstractmethod
    def _seller_activation_order(self) -> Iterator[TemplateAgent]:
        ...



def add_separate_line(func: Callable, *args, **kargs) -> Callable:
    def print_sep_after_func(*args, **kargs):
        func(*args, **kargs)
        print("====================")

    return print_sep_after_func