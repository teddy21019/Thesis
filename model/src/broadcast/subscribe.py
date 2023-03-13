from typing import Callable, Any, Hashable


__subscribers = dict()

def subscribe(event_code:Hashable, callback_fn:Callable) -> None :
    """
    Subscribes some callback function to the given `event_code`.

    Ex:

    If a bank object needs to listen to payments conducted in the form of its
    own deposit, then the bank can subscribe the reaction function to the code,
    say, 'using deposit'.

    >>> def bank_handle_deposit_payment(payment):
            payment.sender_bank.transfer(payment.price, payment.target_bank)
    >>> subscribe('using deposit', bank_handle_deposit_payment)
    >>> ## after some payment
    >>> announce('using deposit',
                {'price': 10, 'target_bank':'First', 'sender_bank':'BOT'}
            )

    This will then let every function subscribed to the event run the code, given a data.

    """
    if event_code not in __subscribers:
        __subscribers[event_code] = []

    __subscribers[event_code].append(callback_fn)


def announce(event_code:Hashable, data:Any) -> None:
    if event_code not in __subscribers:
        raise EventNotExistsError(event_code)
    for fn in __subscribers[event_code]:
        fn(data)


class EventNotExistsError(Exception):
    def __init__(self, event_code:Hashable):
        super().__init__(f"Event 'f{event_code}' is not registered. Please check the code!")
        print(__subscribers)