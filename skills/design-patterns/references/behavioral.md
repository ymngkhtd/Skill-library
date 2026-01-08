# Behavioral Patterns

Patterns that deal with object communication and responsibility distribution.

## Table of Contents
- [Strategy](#strategy)
- [Observer](#observer)
- [Command](#command)
- [State](#state)
- [Chain of Responsibility](#chain-of-responsibility)
- [Template Method](#template-method)
- [Iterator](#iterator)
- [Mediator](#mediator)

---

## Strategy

**Intent**: Define a family of algorithms, encapsulate each one, and make them interchangeable.

**When to use**:
- Many related classes differ only in behavior
- Need different variants of an algorithm
- Algorithm uses data clients shouldn't know about
- Class has many conditional statements for different behaviors

### Python Example

```python
from abc import ABC, abstractmethod
from decimal import Decimal

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: Decimal) -> str: ...

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self._card = card_number[-4:]

    def pay(self, amount: Decimal) -> str:
        return f"Paid ${amount} with card ending {self._card}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self._email = email

    def pay(self, amount: Decimal) -> str:
        return f"Paid ${amount} via PayPal ({self._email})"

class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet: str):
        self._wallet = wallet[:8]

    def pay(self, amount: Decimal) -> str:
        return f"Paid ${amount} in crypto to {self._wallet}..."

class ShoppingCart:
    def __init__(self):
        self._items: list[tuple[str, Decimal]] = []
        self._payment_strategy: PaymentStrategy | None = None

    def add_item(self, name: str, price: Decimal) -> None:
        self._items.append((name, price))

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._payment_strategy = strategy

    def checkout(self) -> str:
        if not self._payment_strategy:
            raise ValueError("Payment strategy not set")
        total = sum(price for _, price in self._items)
        return self._payment_strategy.pay(total)

# Usage
cart = ShoppingCart()
cart.add_item("Book", Decimal("29.99"))
cart.add_item("Pen", Decimal("4.99"))

cart.set_payment_strategy(CreditCardPayment("1234567890123456"))
print(cart.checkout())  # "Paid $34.98 with card ending 3456"

cart.set_payment_strategy(PayPalPayment("user@example.com"))
print(cart.checkout())  # "Paid $34.98 via PayPal (user@example.com)"
```

### TypeScript Example

```typescript
interface SortStrategy<T> {
  sort(data: T[]): T[];
}

class QuickSort<T> implements SortStrategy<T> {
  sort(data: T[]): T[] {
    return [...data].sort();
  }
}

class MergeSort<T> implements SortStrategy<T> {
  sort(data: T[]): T[] {
    // Merge sort implementation
    return [...data].sort();
  }
}

class Sorter<T> {
  constructor(private strategy: SortStrategy<T>) {}

  setStrategy(strategy: SortStrategy<T>): void {
    this.strategy = strategy;
  }

  sort(data: T[]): T[] {
    return this.strategy.sort(data);
  }
}
```

---

## Observer

**Intent**: Define one-to-many dependency; when one object changes state, all dependents are notified.

**When to use**:
- Change to one object requires changing others (unknown how many)
- Object should notify others without knowing who they are
- Event-driven systems

### Python Example

```python
from abc import ABC, abstractmethod
from typing import Any

class Observer(ABC):
    @abstractmethod
    def update(self, subject: "Subject", *args: Any) -> None: ...

class Subject:
    def __init__(self):
        self._observers: list[Observer] = []
        self._state: Any = None

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, *args: Any) -> None:
        for observer in self._observers:
            observer.update(self, *args)

    @property
    def state(self) -> Any:
        return self._state

    @state.setter
    def state(self, value: Any) -> None:
        self._state = value
        self.notify()

# Concrete implementation
class StockTicker(Subject):
    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def set_price(self, price: float) -> None:
        self.state = price

class PriceDisplay(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, subject: Subject, *args: Any) -> None:
        if isinstance(subject, StockTicker):
            print(f"{self.name}: {subject.symbol} = ${subject.state}")

class PriceAlert(Observer):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def update(self, subject: Subject, *args: Any) -> None:
        if isinstance(subject, StockTicker) and subject.state > self.threshold:
            print(f"ALERT: {subject.symbol} exceeded ${self.threshold}!")

# Usage
stock = StockTicker("AAPL")
stock.attach(PriceDisplay("Terminal"))
stock.attach(PriceAlert(150.0))

stock.set_price(145.0)  # Terminal: AAPL = $145.0
stock.set_price(155.0)  # Terminal: AAPL = $155.0
                         # ALERT: AAPL exceeded $150.0!
```

### Modern Python with Callbacks

```python
from typing import Callable

class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, callback: Callable) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable) -> None:
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs) -> None:
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

# Usage
emitter = EventEmitter()
emitter.on("data", lambda x: print(f"Received: {x}"))
emitter.on("error", lambda e: print(f"Error: {e}"))

emitter.emit("data", {"value": 42})
emitter.emit("error", "Connection failed")
```

---

## Command

**Intent**: Encapsulate a request as an object, allowing parameterization, queuing, and undo.

**When to use**:
- Parameterize objects with operations
- Queue, log, or support undoable operations
- Structure system around high-level operations built on primitives

### Python Example

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...

@dataclass
class TextEditor:
    content: str = ""

    def insert(self, text: str, position: int) -> None:
        self.content = self.content[:position] + text + self.content[position:]

    def delete(self, position: int, length: int) -> str:
        deleted = self.content[position:position + length]
        self.content = self.content[:position] + self.content[position + length:]
        return deleted

class InsertCommand(Command):
    def __init__(self, editor: TextEditor, text: str, position: int):
        self._editor = editor
        self._text = text
        self._position = position

    def execute(self) -> None:
        self._editor.insert(self._text, self._position)

    def undo(self) -> None:
        self._editor.delete(self._position, len(self._text))

class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, position: int, length: int):
        self._editor = editor
        self._position = position
        self._length = length
        self._deleted_text = ""

    def execute(self) -> None:
        self._deleted_text = self._editor.delete(self._position, self._length)

    def undo(self) -> None:
        self._editor.insert(self._deleted_text, self._position)

class CommandHistory:
    def __init__(self):
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def execute(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()
            self._redo_stack.append(command)

    def redo(self) -> None:
        if self._redo_stack:
            command = self._redo_stack.pop()
            command.execute()
            self._history.append(command)

# Usage
editor = TextEditor()
history = CommandHistory()

history.execute(InsertCommand(editor, "Hello", 0))
print(editor.content)  # "Hello"

history.execute(InsertCommand(editor, " World", 5))
print(editor.content)  # "Hello World"

history.undo()
print(editor.content)  # "Hello"

history.redo()
print(editor.content)  # "Hello World"
```

---

## State

**Intent**: Allow an object to alter its behavior when its internal state changes.

**When to use**:
- Object behavior depends on state and must change at runtime
- Operations have large conditional statements depending on state

### Python Example

```python
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def insert_coin(self, machine: "VendingMachine") -> str: ...
    @abstractmethod
    def select_product(self, machine: "VendingMachine") -> str: ...
    @abstractmethod
    def dispense(self, machine: "VendingMachine") -> str: ...

class NoCoinState(State):
    def insert_coin(self, machine: "VendingMachine") -> str:
        machine.set_state(HasCoinState())
        return "Coin inserted"

    def select_product(self, machine: "VendingMachine") -> str:
        return "Please insert coin first"

    def dispense(self, machine: "VendingMachine") -> str:
        return "Please insert coin first"

class HasCoinState(State):
    def insert_coin(self, machine: "VendingMachine") -> str:
        return "Coin already inserted"

    def select_product(self, machine: "VendingMachine") -> str:
        machine.set_state(DispensingState())
        return "Product selected"

    def dispense(self, machine: "VendingMachine") -> str:
        return "Please select product first"

class DispensingState(State):
    def insert_coin(self, machine: "VendingMachine") -> str:
        return "Please wait, dispensing"

    def select_product(self, machine: "VendingMachine") -> str:
        return "Already dispensing"

    def dispense(self, machine: "VendingMachine") -> str:
        machine.set_state(NoCoinState())
        return "Product dispensed!"

class VendingMachine:
    def __init__(self):
        self._state: State = NoCoinState()

    def set_state(self, state: State) -> None:
        self._state = state

    def insert_coin(self) -> str:
        return self._state.insert_coin(self)

    def select_product(self) -> str:
        return self._state.select_product(self)

    def dispense(self) -> str:
        return self._state.dispense(self)

# Usage
machine = VendingMachine()
print(machine.select_product())  # "Please insert coin first"
print(machine.insert_coin())     # "Coin inserted"
print(machine.select_product())  # "Product selected"
print(machine.dispense())        # "Product dispensed!"
```

---

## Chain of Responsibility

**Intent**: Avoid coupling sender to receiver by giving multiple objects chance to handle request.

**When to use**:
- More than one object may handle a request
- Handler isn't known a priori
- Want to issue request without specifying receiver explicitly

### Python Example

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

@dataclass
class LogRecord:
    level: LogLevel
    message: str

class LogHandler(ABC):
    def __init__(self):
        self._next_handler: LogHandler | None = None

    def set_next(self, handler: "LogHandler") -> "LogHandler":
        self._next_handler = handler
        return handler

    def handle(self, record: LogRecord) -> None:
        if self._can_handle(record):
            self._write(record)
        if self._next_handler:
            self._next_handler.handle(record)

    @abstractmethod
    def _can_handle(self, record: LogRecord) -> bool: ...

    @abstractmethod
    def _write(self, record: LogRecord) -> None: ...

class ConsoleHandler(LogHandler):
    def __init__(self, min_level: LogLevel = LogLevel.DEBUG):
        super().__init__()
        self._min_level = min_level

    def _can_handle(self, record: LogRecord) -> bool:
        return record.level.value >= self._min_level.value

    def _write(self, record: LogRecord) -> None:
        print(f"[CONSOLE] {record.level.name}: {record.message}")

class FileHandler(LogHandler):
    def __init__(self, min_level: LogLevel = LogLevel.WARNING):
        super().__init__()
        self._min_level = min_level

    def _can_handle(self, record: LogRecord) -> bool:
        return record.level.value >= self._min_level.value

    def _write(self, record: LogRecord) -> None:
        print(f"[FILE] {record.level.name}: {record.message}")

class EmailHandler(LogHandler):
    def __init__(self):
        super().__init__()

    def _can_handle(self, record: LogRecord) -> bool:
        return record.level == LogLevel.ERROR

    def _write(self, record: LogRecord) -> None:
        print(f"[EMAIL] Sending alert: {record.message}")

# Usage - Build chain
console = ConsoleHandler(LogLevel.DEBUG)
file_handler = FileHandler(LogLevel.WARNING)
email = EmailHandler()

console.set_next(file_handler).set_next(email)

# Process logs
console.handle(LogRecord(LogLevel.DEBUG, "Debug info"))
# [CONSOLE] DEBUG: Debug info

console.handle(LogRecord(LogLevel.ERROR, "Critical failure!"))
# [CONSOLE] ERROR: Critical failure!
# [FILE] ERROR: Critical failure!
# [EMAIL] Sending alert: Critical failure!
```

---

## Template Method

**Intent**: Define skeleton of algorithm in superclass, letting subclasses override specific steps.

**When to use**:
- Implement invariant parts of algorithm once
- Common behavior should be localized in one class
- Control subclass extensions at specific points

### Python Example

```python
from abc import ABC, abstractmethod

class DataMiner(ABC):
    def mine(self, path: str) -> str:
        """Template method - defines algorithm skeleton"""
        file = self._open_file(path)
        data = self._extract_data(file)
        parsed = self._parse_data(data)
        analysis = self._analyze(parsed)
        return self._send_report(analysis)

    @abstractmethod
    def _open_file(self, path: str) -> str: ...

    @abstractmethod
    def _extract_data(self, file: str) -> str: ...

    def _parse_data(self, data: str) -> dict:
        # Default implementation
        return {"raw": data}

    def _analyze(self, data: dict) -> str:
        # Default implementation
        return f"Analyzed: {len(data)} items"

    def _send_report(self, analysis: str) -> str:
        return f"Report: {analysis}"

class PDFMiner(DataMiner):
    def _open_file(self, path: str) -> str:
        return f"<PDF:{path}>"

    def _extract_data(self, file: str) -> str:
        return f"PDF text from {file}"

class CSVMiner(DataMiner):
    def _open_file(self, path: str) -> str:
        return f"<CSV:{path}>"

    def _extract_data(self, file: str) -> str:
        return f"CSV rows from {file}"

    def _parse_data(self, data: str) -> dict:
        # Override with CSV-specific parsing
        return {"rows": data.split(",")}

# Usage
pdf_miner = PDFMiner()
print(pdf_miner.mine("report.pdf"))

csv_miner = CSVMiner()
print(csv_miner.mine("data.csv"))
```

---

## Iterator

**Intent**: Provide way to access elements of collection sequentially without exposing representation.

### Python Example

```python
from typing import Iterator, Generic, TypeVar

T = TypeVar("T")

class TreeNode(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.left: TreeNode[T] | None = None
        self.right: TreeNode[T] | None = None

class BinaryTree(Generic[T]):
    def __init__(self):
        self.root: TreeNode[T] | None = None

    def __iter__(self) -> Iterator[T]:
        """In-order traversal"""
        return self._inorder(self.root)

    def _inorder(self, node: TreeNode[T] | None) -> Iterator[T]:
        if node:
            yield from self._inorder(node.left)
            yield node.value
            yield from self._inorder(node.right)

    def preorder(self) -> Iterator[T]:
        return self._preorder(self.root)

    def _preorder(self, node: TreeNode[T] | None) -> Iterator[T]:
        if node:
            yield node.value
            yield from self._preorder(node.left)
            yield from self._preorder(node.right)

# Usage
tree = BinaryTree[int]()
tree.root = TreeNode(5)
tree.root.left = TreeNode(3)
tree.root.right = TreeNode(7)

for value in tree:  # Uses __iter__ (in-order)
    print(value)  # 3, 5, 7

for value in tree.preorder():
    print(value)  # 5, 3, 7
```

---

## Mediator

**Intent**: Define object that encapsulates how a set of objects interact.

**When to use**:
- Objects communicate in complex but well-defined ways
- Reusing objects is difficult due to communication dependencies
- Behavior distributed between classes should be customizable

### Python Example

```python
from abc import ABC, abstractmethod

class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: "User") -> None: ...
    @abstractmethod
    def add_user(self, user: "User") -> None: ...

class User:
    def __init__(self, name: str, mediator: ChatMediator):
        self.name = name
        self._mediator = mediator
        mediator.add_user(self)

    def send(self, message: str) -> None:
        print(f"{self.name} sends: {message}")
        self._mediator.send_message(message, self)

    def receive(self, message: str, sender: "User") -> None:
        print(f"{self.name} received from {sender.name}: {message}")

class ChatRoom(ChatMediator):
    def __init__(self):
        self._users: list[User] = []

    def add_user(self, user: User) -> None:
        self._users.append(user)

    def send_message(self, message: str, sender: User) -> None:
        for user in self._users:
            if user != sender:
                user.receive(message, sender)

# Usage
chat = ChatRoom()
alice = User("Alice", chat)
bob = User("Bob", chat)
charlie = User("Charlie", chat)

alice.send("Hello everyone!")
# Alice sends: Hello everyone!
# Bob received from Alice: Hello everyone!
# Charlie received from Alice: Hello everyone!
```
