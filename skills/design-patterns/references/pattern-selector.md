# Pattern Selection Guide

Decision trees and guidance for choosing the right pattern.

## Table of Contents
- [Decision Tree by Problem Type](#decision-tree-by-problem-type)
- [Pattern Comparison Tables](#pattern-comparison-tables)
- [Anti-Patterns and Smells](#anti-patterns-and-smells)
- [Pattern Combinations](#pattern-combinations)
- [Refactoring to Patterns](#refactoring-to-patterns)

---

## Decision Tree by Problem Type

### Object Creation Problems

```
Need to create objects?
├── Single type, but want subclasses to decide?
│   └── Factory Method
├── Families of related objects?
│   └── Abstract Factory
├── Complex object with many parts/options?
│   └── Builder
├── Only one instance allowed?
│   └── Singleton (or module-level instance)
└── Creating from existing object is easier?
    └── Prototype
```

### Structural Problems

```
Need to compose objects?
├── Incompatible interface?
│   └── Adapter
├── Add behavior dynamically?
│   └── Decorator
├── Simplify complex subsystem?
│   └── Facade
├── Control access to object?
│   └── Proxy
├── Tree/hierarchy of objects?
│   └── Composite
└── Vary abstraction and implementation independently?
    └── Bridge
```

### Behavioral Problems

```
Need to manage behavior/communication?
├── Swap algorithms at runtime?
│   └── Strategy
├── Notify multiple objects of changes?
│   └── Observer
├── Encapsulate request as object (undo/queue)?
│   └── Command
├── Object behavior changes with state?
│   └── State
├── Pass request along chain of handlers?
│   └── Chain of Responsibility
├── Define algorithm skeleton, vary steps?
│   └── Template Method
├── Traverse collection without exposing internals?
│   └── Iterator
└── Reduce direct communication between objects?
    └── Mediator
```

---

## Pattern Comparison Tables

### Strategy vs State vs Command

| Aspect | Strategy | State | Command |
|--------|----------|-------|---------|
| **Purpose** | Swap algorithms | Change behavior with state | Encapsulate requests |
| **Trigger** | Client decision | Internal state change | User action |
| **Undo support** | No | No | Yes |
| **Context awareness** | Stateless | Knows context | Knows receiver |
| **Example** | Payment methods | Order status | Text editor actions |

### Factory Method vs Abstract Factory vs Builder

| Aspect | Factory Method | Abstract Factory | Builder |
|--------|----------------|------------------|---------|
| **Creates** | Single product | Product families | Complex product |
| **Variation** | Subclass decides | Factory decides | Steps decide |
| **Returns** | New instance | Related instances | Configured instance |
| **Example** | Document creator | GUI toolkit | Query builder |

### Adapter vs Decorator vs Proxy vs Facade

| Aspect | Adapter | Decorator | Proxy | Facade |
|--------|---------|-----------|-------|--------|
| **Purpose** | Convert interface | Add behavior | Control access | Simplify interface |
| **Wraps** | Different interface | Same interface | Same interface | Multiple classes |
| **Changes interface** | Yes | No | No | Yes |
| **Multiple layers** | No | Yes | No | No |

---

## Anti-Patterns and Smells

### Singleton Overuse

**Smell**: Global state, hidden dependencies, hard to test.

```python
# Bad - hidden dependency
class OrderService:
    def process(self, order):
        db = Database.get_instance()  # Hidden!
        db.save(order)

# Good - explicit dependency
class OrderService:
    def __init__(self, db: Database):
        self._db = db

    def process(self, order):
        self._db.save(order)
```

### God Factory

**Smell**: Factory creating many unrelated types.

```python
# Bad - creates unrelated objects
class Factory:
    def create(self, type_name):
        if type_name == "user": return User()
        if type_name == "order": return Order()
        if type_name == "report": return Report()
        if type_name == "email": return Email()  # Unrelated!

# Good - separate factories or simple constructors
class UserFactory:
    def create(self, data) -> User: ...

class ReportFactory:
    def create(self, data) -> Report: ...
```

### Pattern Fever

**Smell**: Applying patterns where simple code suffices.

```python
# Over-engineered for simple case
class GreetingStrategy(ABC):
    @abstractmethod
    def greet(self, name): ...

class EnglishGreeting(GreetingStrategy):
    def greet(self, name):
        return f"Hello, {name}"

class GreetingContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def greet(self, name):
        return self._strategy.greet(name)

# Just use a function!
def greet(name: str, language: str = "en") -> str:
    greetings = {"en": "Hello", "es": "Hola", "fr": "Bonjour"}
    return f"{greetings.get(language, 'Hello')}, {name}"
```

### When NOT to Use Patterns

- **Simple CRUD**: Don't add patterns for basic create/read/update/delete
- **One-time code**: Scripts or one-off tasks don't need patterns
- **Premature optimization**: Don't add patterns for hypothetical future needs
- **Small codebases**: Patterns add complexity; weigh benefits vs overhead

---

## Pattern Combinations

### Common Combinations

**Factory + Singleton**
```python
class ConnectionPool:
    _instance = None

    @classmethod
    def get_instance(cls) -> "ConnectionPool":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_connection(self) -> Connection:
        # Factory method within singleton
        return Connection(self._config)
```

**Strategy + Factory**
```python
class PaymentFactory:
    _strategies = {
        "credit": CreditCardPayment,
        "paypal": PayPalPayment,
        "crypto": CryptoPayment,
    }

    @classmethod
    def create(cls, payment_type: str) -> PaymentStrategy:
        strategy_class = cls._strategies.get(payment_type)
        if not strategy_class:
            raise ValueError(f"Unknown payment: {payment_type}")
        return strategy_class()
```

**Decorator + Factory**
```python
def create_data_source(encrypted: bool, compressed: bool) -> DataSource:
    source = FileDataSource("data.txt")
    if encrypted:
        source = EncryptionDecorator(source)
    if compressed:
        source = CompressionDecorator(source)
    return source
```

**Command + Composite (Macro Commands)**
```python
class MacroCommand(Command):
    def __init__(self):
        self._commands: list[Command] = []

    def add(self, command: Command) -> None:
        self._commands.append(command)

    def execute(self) -> None:
        for cmd in self._commands:
            cmd.execute()

    def undo(self) -> None:
        for cmd in reversed(self._commands):
            cmd.undo()
```

---

## Refactoring to Patterns

### Conditionals to Strategy

**Before:**
```python
def calculate_shipping(order, method):
    if method == "ground":
        return order.weight * 1.5
    elif method == "air":
        return order.weight * 3.0
    elif method == "express":
        return order.weight * 5.0 + 10
```

**After:**
```python
class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, order) -> float: ...

class GroundShipping(ShippingStrategy):
    def calculate(self, order) -> float:
        return order.weight * 1.5

class AirShipping(ShippingStrategy):
    def calculate(self, order) -> float:
        return order.weight * 3.0

class ExpressShipping(ShippingStrategy):
    def calculate(self, order) -> float:
        return order.weight * 5.0 + 10
```

### State Machine to State Pattern

**Before:**
```python
class Order:
    def __init__(self):
        self.status = "pending"

    def ship(self):
        if self.status == "pending":
            self.status = "shipped"
        elif self.status == "shipped":
            raise Error("Already shipped")
        elif self.status == "delivered":
            raise Error("Already delivered")
```

**After:**
```python
class OrderState(ABC):
    @abstractmethod
    def ship(self, order: "Order") -> None: ...

class PendingState(OrderState):
    def ship(self, order: "Order") -> None:
        order.set_state(ShippedState())

class ShippedState(OrderState):
    def ship(self, order: "Order") -> None:
        raise Error("Already shipped")
```

### Inheritance to Decorator

**Before:**
```python
class Coffee: pass
class CoffeeWithMilk(Coffee): pass
class CoffeeWithSugar(Coffee): pass
class CoffeeWithMilkAndSugar(Coffee): pass  # Explosion!
```

**After:**
```python
class Coffee:
    def cost(self) -> float:
        return 2.0

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5

class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.2

# Usage: MilkDecorator(SugarDecorator(Coffee()))
```

---

## Quick Reference: Problem to Pattern

| Problem | Consider |
|---------|----------|
| "I need to support multiple algorithms" | Strategy |
| "I need undo/redo functionality" | Command |
| "I need to react to state changes" | Observer |
| "I have complex conditional state logic" | State |
| "I need to build complex objects" | Builder |
| "I need to create families of objects" | Abstract Factory |
| "I need to adapt third-party code" | Adapter |
| "I need to add features without subclassing" | Decorator |
| "I need to simplify a complex API" | Facade |
| "I need lazy loading or access control" | Proxy |
| "I need to process requests through handlers" | Chain of Responsibility |
| "I need uniform tree/hierarchy handling" | Composite |
