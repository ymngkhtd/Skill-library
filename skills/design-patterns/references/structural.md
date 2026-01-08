# Structural Patterns

Patterns that deal with object composition and relationships.

## Table of Contents
- [Adapter](#adapter)
- [Decorator](#decorator)
- [Facade](#facade)
- [Proxy](#proxy)
- [Composite](#composite)
- [Bridge](#bridge)

---

## Adapter

**Intent**: Convert interface of a class into another interface clients expect.

**When to use**:
- Want to use existing class but interface doesn't match
- Need to create reusable class working with unrelated classes
- Integrating third-party libraries with incompatible interfaces

**Structure**:
```
Target (interface client expects)
Adaptee (existing class with incompatible interface)
Adapter (implements Target, wraps Adaptee)
```

### Python Example

```python
from abc import ABC, abstractmethod

# Target interface
class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str) -> str: ...

# Adaptee (third-party library)
class AdvancedMediaLibrary:
    def play_vlc(self, filename: str) -> str:
        return f"Playing VLC: {filename}"

    def play_mp4(self, filename: str) -> str:
        return f"Playing MP4: {filename}"

# Adapter
class MediaAdapter(MediaPlayer):
    def __init__(self):
        self._lib = AdvancedMediaLibrary()

    def play(self, filename: str) -> str:
        if filename.endswith(".vlc"):
            return self._lib.play_vlc(filename)
        elif filename.endswith(".mp4"):
            return self._lib.play_mp4(filename)
        raise ValueError(f"Unsupported format: {filename}")

# Usage
player = MediaAdapter()
print(player.play("video.mp4"))  # "Playing MP4: video.mp4"
```

### TypeScript Example

```typescript
// Target
interface Logger {
  log(message: string): void;
  error(message: string): void;
}

// Adaptee (third-party)
class ThirdPartyLogger {
  writeLog(level: string, msg: string): void {
    console.log(`[${level}] ${msg}`);
  }
}

// Adapter
class LoggerAdapter implements Logger {
  constructor(private adaptee: ThirdPartyLogger) {}

  log(message: string): void {
    this.adaptee.writeLog("INFO", message);
  }

  error(message: string): void {
    this.adaptee.writeLog("ERROR", message);
  }
}

// Usage
const logger: Logger = new LoggerAdapter(new ThirdPartyLogger());
logger.log("Application started");
```

---

## Decorator

**Intent**: Attach additional responsibilities to objects dynamically.

**When to use**:
- Add responsibilities without affecting other objects
- Responsibilities can be withdrawn
- Extension by subclassing is impractical

**Structure**:
```
Component (interface)
ConcreteComponent (implements Component)
Decorator (implements Component, wraps Component)
ConcreteDecoratorA, ConcreteDecoratorB...
```

### Python Example

```python
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def write(self, data: str) -> None: ...
    @abstractmethod
    def read(self) -> str: ...

class FileDataSource(DataSource):
    def __init__(self, filename: str):
        self._filename = filename
        self._data = ""

    def write(self, data: str) -> None:
        self._data = data

    def read(self) -> str:
        return self._data

class DataSourceDecorator(DataSource):
    def __init__(self, source: DataSource):
        self._source = source

    def write(self, data: str) -> None:
        self._source.write(data)

    def read(self) -> str:
        return self._source.read()

class EncryptionDecorator(DataSourceDecorator):
    def write(self, data: str) -> None:
        encrypted = f"[ENCRYPTED]{data}[/ENCRYPTED]"
        super().write(encrypted)

    def read(self) -> str:
        data = super().read()
        return data.replace("[ENCRYPTED]", "").replace("[/ENCRYPTED]", "")

class CompressionDecorator(DataSourceDecorator):
    def write(self, data: str) -> None:
        compressed = f"[COMPRESSED]{data}[/COMPRESSED]"
        super().write(compressed)

    def read(self) -> str:
        data = super().read()
        return data.replace("[COMPRESSED]", "").replace("[/COMPRESSED]", "")

# Usage - Stack decorators
source = CompressionDecorator(
    EncryptionDecorator(
        FileDataSource("data.txt")
    )
)
source.write("Secret Data")
print(source.read())  # "Secret Data"
```

### Python Decorator with `functools`

```python
from functools import wraps
import time

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

def retry(max_attempts: int = 3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Retry {attempt + 1}/{max_attempts}")
        return wrapper
    return decorator

@timing
@retry(max_attempts=3)
def fetch_data(url: str) -> str:
    return f"Data from {url}"
```

---

## Facade

**Intent**: Provide unified interface to a set of interfaces in a subsystem.

**When to use**:
- Need simple interface to complex subsystem
- Many dependencies between clients and implementation classes
- Want to layer subsystems

### Python Example

```python
class VideoFile:
    def __init__(self, filename: str):
        self.filename = filename

class CodecFactory:
    @staticmethod
    def extract(file: VideoFile) -> str:
        return f"codec for {file.filename}"

class AudioMixer:
    def fix(self, result: str) -> str:
        return f"audio_fixed({result})"

class VideoConverter:
    """Facade - simple interface to complex video subsystem"""

    def convert(self, filename: str, format: str) -> str:
        file = VideoFile(filename)
        codec = CodecFactory.extract(file)
        result = f"converted({codec}, {format})"
        result = AudioMixer().fix(result)
        return result

# Usage - Client only knows Facade
converter = VideoConverter()
result = converter.convert("video.ogg", "mp4")
```

### TypeScript Example

```typescript
// Complex subsystem classes
class CPU {
  freeze(): void { console.log("CPU frozen"); }
  jump(address: number): void { console.log(`Jump to ${address}`); }
  execute(): void { console.log("CPU executing"); }
}

class Memory {
  load(address: number, data: string): void {
    console.log(`Loading ${data} at ${address}`);
  }
}

class HardDrive {
  read(sector: number, size: number): string {
    return `data from sector ${sector}`;
  }
}

// Facade
class ComputerFacade {
  private cpu = new CPU();
  private memory = new Memory();
  private hd = new HardDrive();

  start(): void {
    this.cpu.freeze();
    this.memory.load(0, this.hd.read(0, 1024));
    this.cpu.jump(0);
    this.cpu.execute();
  }
}

// Usage
const computer = new ComputerFacade();
computer.start();  // Simple interface to complex startup
```

---

## Proxy

**Intent**: Provide surrogate or placeholder to control access to an object.

**Types**:
- **Virtual Proxy**: Lazy initialization of expensive objects
- **Protection Proxy**: Access control
- **Remote Proxy**: Local representative for remote object
- **Caching Proxy**: Cache results

### Python Example

```python
from abc import ABC, abstractmethod

class Image(ABC):
    @abstractmethod
    def display(self) -> str: ...

class RealImage(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._load_from_disk()  # Expensive operation

    def _load_from_disk(self) -> None:
        print(f"Loading {self._filename} from disk...")

    def display(self) -> str:
        return f"Displaying {self._filename}"

class ImageProxy(Image):
    """Virtual Proxy - lazy loading"""

    def __init__(self, filename: str):
        self._filename = filename
        self._real_image: RealImage | None = None

    def display(self) -> str:
        if self._real_image is None:
            self._real_image = RealImage(self._filename)
        return self._real_image.display()

# Usage
image = ImageProxy("large_photo.jpg")  # No loading yet
# ... later when needed ...
image.display()  # Now loads and displays
```

### Caching Proxy Example

```python
from functools import lru_cache

class DatabaseService:
    def get_user(self, user_id: int) -> dict:
        print(f"Fetching user {user_id} from DB...")
        return {"id": user_id, "name": f"User{user_id}"}

class CachingDatabaseProxy:
    def __init__(self, service: DatabaseService):
        self._service = service
        self._cache: dict[int, dict] = {}

    def get_user(self, user_id: int) -> dict:
        if user_id not in self._cache:
            self._cache[user_id] = self._service.get_user(user_id)
        return self._cache[user_id]

# Or use built-in caching
class CachedService:
    @lru_cache(maxsize=100)
    def get_user(self, user_id: int) -> dict:
        print(f"Fetching user {user_id} from DB...")
        return {"id": user_id, "name": f"User{user_id}"}
```

---

## Composite

**Intent**: Compose objects into tree structures; treat individual objects and compositions uniformly.

**When to use**:
- Represent part-whole hierarchies
- Want clients to ignore difference between compositions and individuals

### Python Example

```python
from abc import ABC, abstractmethod

class FileSystemComponent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_size(self) -> int: ...

    @abstractmethod
    def display(self, indent: int = 0) -> str: ...

class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def get_size(self) -> int:
        return self._size

    def display(self, indent: int = 0) -> str:
        return "  " * indent + f"- {self.name} ({self._size}B)"

class Directory(FileSystemComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: list[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)

    def remove(self, component: FileSystemComponent) -> None:
        self._children.remove(component)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0) -> str:
        lines = ["  " * indent + f"+ {self.name}/"]
        for child in self._children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)

# Usage
root = Directory("root")
docs = Directory("docs")
docs.add(File("readme.txt", 100))
docs.add(File("guide.pdf", 5000))
root.add(docs)
root.add(File("config.yaml", 50))

print(root.display())
print(f"Total size: {root.get_size()}B")
```

---

## Bridge

**Intent**: Decouple abstraction from implementation so both can vary independently.

**When to use**:
- Avoid permanent binding between abstraction and implementation
- Both abstraction and implementation should be extensible
- Changes in implementation shouldn't affect clients

### Python Example

```python
from abc import ABC, abstractmethod

# Implementation hierarchy
class Renderer(ABC):
    @abstractmethod
    def render_circle(self, x: int, y: int, radius: int) -> str: ...

class VectorRenderer(Renderer):
    def render_circle(self, x: int, y: int, radius: int) -> str:
        return f"Drawing circle as vectors at ({x},{y}) r={radius}"

class RasterRenderer(Renderer):
    def render_circle(self, x: int, y: int, radius: int) -> str:
        return f"Drawing circle as pixels at ({x},{y}) r={radius}"

# Abstraction hierarchy
class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self._renderer = renderer

    @abstractmethod
    def draw(self) -> str: ...

class Circle(Shape):
    def __init__(self, renderer: Renderer, x: int, y: int, radius: int):
        super().__init__(renderer)
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self) -> str:
        return self._renderer.render_circle(self.x, self.y, self.radius)

# Usage - Can mix any shape with any renderer
circle_vector = Circle(VectorRenderer(), 10, 10, 5)
circle_raster = Circle(RasterRenderer(), 10, 10, 5)
print(circle_vector.draw())  # "Drawing circle as vectors..."
print(circle_raster.draw())  # "Drawing circle as pixels..."
```
