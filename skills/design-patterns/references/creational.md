# Creational Patterns

Patterns that deal with object creation mechanisms.

## Table of Contents
- [Factory Method](#factory-method)
- [Abstract Factory](#abstract-factory)
- [Builder](#builder)
- [Singleton](#singleton)
- [Prototype](#prototype)

---

## Factory Method

**Intent**: Define an interface for creating objects, letting subclasses decide which class to instantiate.

**When to use**:
- Don't know exact types upfront
- Want subclasses to specify created objects
- Need to delegate creation to helper subclasses

**Structure**:
```
Creator (abstract)
  └── create_product() -> Product
ConcreteCreatorA
  └── create_product() -> ConcreteProductA
ConcreteCreatorB
  └── create_product() -> ConcreteProductB
```

### Python Example

```python
from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def render(self) -> str: ...

class PDFDocument(Document):
    def render(self) -> str:
        return "Rendering PDF"

class HTMLDocument(Document):
    def render(self) -> str:
        return "Rendering HTML"

class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self) -> Document: ...

    def process(self) -> str:
        doc = self.create_document()
        return doc.render()

class PDFFactory(DocumentFactory):
    def create_document(self) -> Document:
        return PDFDocument()

class HTMLFactory(DocumentFactory):
    def create_document(self) -> Document:
        return HTMLDocument()

# Usage
factory = PDFFactory()
result = factory.process()  # "Rendering PDF"
```

### TypeScript Example

```typescript
interface Product {
  operation(): string;
}

abstract class Creator {
  abstract createProduct(): Product;

  doSomething(): string {
    const product = this.createProduct();
    return product.operation();
  }
}

class ConcreteProductA implements Product {
  operation(): string { return "ProductA"; }
}

class ConcreteCreatorA extends Creator {
  createProduct(): Product { return new ConcreteProductA(); }
}
```

---

## Abstract Factory

**Intent**: Create families of related objects without specifying concrete classes.

**When to use**:
- System should be independent of product creation
- Need to configure with one of multiple product families
- Related products must be used together

**Structure**:
```
AbstractFactory
  └── create_product_a() -> AbstractProductA
  └── create_product_b() -> AbstractProductB
ConcreteFactory1, ConcreteFactory2...
```

### Python Example

```python
from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...

class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: ...

class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...
    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...

# Windows family
class WindowsButton(Button):
    def render(self) -> str: return "Windows Button"

class WindowsCheckbox(Checkbox):
    def render(self) -> str: return "Windows Checkbox"

class WindowsFactory(GUIFactory):
    def create_button(self) -> Button: return WindowsButton()
    def create_checkbox(self) -> Checkbox: return WindowsCheckbox()

# Mac family
class MacButton(Button):
    def render(self) -> str: return "Mac Button"

class MacCheckbox(Checkbox):
    def render(self) -> str: return "Mac Checkbox"

class MacFactory(GUIFactory):
    def create_button(self) -> Button: return MacButton()
    def create_checkbox(self) -> Checkbox: return MacCheckbox()

# Usage
def create_ui(factory: GUIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    return f"{button.render()}, {checkbox.render()}"

ui = create_ui(MacFactory())  # "Mac Button, Mac Checkbox"
```

---

## Builder

**Intent**: Construct complex objects step by step, allowing different representations.

**When to use**:
- Object has many optional parameters
- Construction involves multiple steps
- Same construction process should create different representations

**Structure**:
```
Builder (interface)
  └── build_part_a()
  └── build_part_b()
  └── get_result() -> Product
Director
  └── construct(builder)
```

### Python Example

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class House:
    walls: int = 0
    doors: int = 0
    windows: int = 0
    roof: Optional[str] = None
    garage: bool = False
    pool: bool = False

class HouseBuilder:
    def __init__(self):
        self._house = House()

    def set_walls(self, count: int) -> "HouseBuilder":
        self._house.walls = count
        return self

    def set_doors(self, count: int) -> "HouseBuilder":
        self._house.doors = count
        return self

    def set_windows(self, count: int) -> "HouseBuilder":
        self._house.windows = count
        return self

    def set_roof(self, roof_type: str) -> "HouseBuilder":
        self._house.roof = roof_type
        return self

    def add_garage(self) -> "HouseBuilder":
        self._house.garage = True
        return self

    def add_pool(self) -> "HouseBuilder":
        self._house.pool = True
        return self

    def build(self) -> House:
        result = self._house
        self._house = House()  # Reset for next build
        return result

# Usage (fluent interface)
house = (HouseBuilder()
    .set_walls(4)
    .set_doors(2)
    .set_windows(6)
    .set_roof("gable")
    .add_garage()
    .build())
```

### TypeScript Example

```typescript
interface Builder<T> {
  build(): T;
}

class QueryBuilder implements Builder<string> {
  private table = "";
  private conditions: string[] = [];
  private columns = "*";

  from(table: string): this {
    this.table = table;
    return this;
  }

  select(...cols: string[]): this {
    this.columns = cols.join(", ");
    return this;
  }

  where(condition: string): this {
    this.conditions.push(condition);
    return this;
  }

  build(): string {
    let query = `SELECT ${this.columns} FROM ${this.table}`;
    if (this.conditions.length > 0) {
      query += ` WHERE ${this.conditions.join(" AND ")}`;
    }
    return query;
  }
}

// Usage
const query = new QueryBuilder()
  .from("users")
  .select("id", "name")
  .where("active = true")
  .where("age > 18")
  .build();
// "SELECT id, name FROM users WHERE active = true AND age > 18"
```

---

## Singleton

**Intent**: Ensure a class has only one instance with global access point.

**When to use**:
- Exactly one instance needed (config, connection pool, logger)
- Need stricter access control than global variable

**Warning**: Often an anti-pattern. Consider dependency injection instead.

### Python Example

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Better: Module-level singleton
# config.py
class _Config:
    def __init__(self):
        self.debug = False
        self.api_key = ""

config = _Config()  # Single instance at module level

# Usage elsewhere
from config import config
config.debug = True
```

### Thread-Safe Python Singleton

```python
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-check
                    cls._instance = super().__new__(cls)
        return cls._instance
```

### TypeScript Example

```typescript
class Database {
  private static instance: Database;
  private constructor() {}

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  query(sql: string): void {
    console.log(`Executing: ${sql}`);
  }
}

// Usage
const db = Database.getInstance();
db.query("SELECT * FROM users");
```

---

## Prototype

**Intent**: Create objects by cloning existing instances.

**When to use**:
- Creating object is expensive (complex initialization, DB reads)
- Need copies with slight modifications
- Avoid subclasses of factories

### Python Example

```python
import copy
from dataclasses import dataclass, field
from typing import List

@dataclass
class Document:
    title: str
    content: str
    authors: List[str] = field(default_factory=list)

    def clone(self) -> "Document":
        return copy.deepcopy(self)

# Usage
template = Document(
    title="Report Template",
    content="Introduction...",
    authors=["Admin"]
)

report1 = template.clone()
report1.title = "Q1 Report"
report1.authors.append("Alice")

report2 = template.clone()
report2.title = "Q2 Report"
report2.authors.append("Bob")

# template.authors still ["Admin"]
# report1.authors is ["Admin", "Alice"]
# report2.authors is ["Admin", "Bob"]
```

### TypeScript Example

```typescript
interface Prototype<T> {
  clone(): T;
}

class Shape implements Prototype<Shape> {
  constructor(
    public x: number,
    public y: number,
    public color: string
  ) {}

  clone(): Shape {
    return new Shape(this.x, this.y, this.color);
  }
}

class Circle extends Shape {
  constructor(x: number, y: number, color: string, public radius: number) {
    super(x, y, color);
  }

  clone(): Circle {
    return new Circle(this.x, this.y, this.color, this.radius);
  }
}

// Usage
const original = new Circle(10, 20, "red", 5);
const copy = original.clone();
copy.color = "blue";
```
