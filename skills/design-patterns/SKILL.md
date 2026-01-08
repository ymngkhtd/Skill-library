---
name: design-patterns
description: |
  Help agents retrieve, filter, and apply software design patterns (GoF and beyond).
  Use this skill when:
  - User describes a problem and needs pattern recommendations (e.g., "how to decouple...", "need flexible object creation")
  - User asks about specific patterns (e.g., "explain Factory pattern", "when to use Strategy")
  - User wants code examples in specific languages (Python, TypeScript, Java, Go, etc.)
  - User needs help identifying patterns in existing code
  - User is refactoring and considering pattern application
  - Questions involve: object creation, structural composition, behavioral communication, SOLID principles
---

# Design Patterns Skill

Quick reference for applying Gang of Four (GoF) and modern design patterns.

## Pattern Categories

| Category | Purpose | Common Patterns |
|----------|---------|-----------------|
| **Creational** | Object creation mechanisms | Factory, Builder, Singleton, Prototype |
| **Structural** | Object composition | Adapter, Decorator, Facade, Proxy, Composite |
| **Behavioral** | Object communication | Strategy, Observer, Command, State, Chain of Responsibility |

## Quick Pattern Selection

### "I need flexible object creation"
-> **Factory Method** (single product) or **Abstract Factory** (product families)

### "I need to build complex objects step by step"
-> **Builder**

### "I need to add behavior without modifying classes"
-> **Decorator** (wrapping) or **Strategy** (injection)

### "I need to decouple components"
-> **Observer** (events), **Mediator** (central hub), or **Command** (requests as objects)

### "I need to adapt incompatible interfaces"
-> **Adapter**

### "I need to simplify a complex subsystem"
-> **Facade**

### "I need state-dependent behavior"
-> **State**

### "I need to process requests through multiple handlers"
-> **Chain of Responsibility**

## Detailed References

For implementation details and code examples, read the appropriate reference file:
- [references/creational.md](references/creational.md) - Factory, Builder, Singleton, Prototype
- [references/structural.md](references/structural.md) - Adapter, Decorator, Facade, Proxy, Composite
- [references/behavioral.md](references/behavioral.md) - Strategy, Observer, Command, State, Chain of Responsibility
- [references/pattern-selector.md](references/pattern-selector.md) - Decision trees and anti-pattern warnings

## Identifying Patterns in Code

Look for these signatures:

| Code Signature | Likely Pattern |
|----------------|----------------|
| `create_xxx()` returning interface types | Factory |
| `.set_xxx().set_yyy().build()` chains | Builder |
| Class wrapping another of same interface | Decorator |
| `execute()` / `undo()` methods with command objects | Command |
| `notify()` / `update()` / `subscribe()` | Observer |
| `handle()` passing to `next_handler` | Chain of Responsibility |
| State classes with `handle()` methods | State |
| `algorithm` injected/swapped at runtime | Strategy |

## Anti-Pattern Warnings

- **Singleton overuse**: Often hides dependencies; prefer DI
- **God Factory**: Factory creating too many unrelated types
- **Pattern fever**: Applying patterns where simple code suffices
- **Premature abstraction**: Adding patterns before actual need

## Usage Examples

**Recommend a pattern:**
> "I have multiple payment methods (credit card, PayPal, crypto) and need to process payments differently for each"
-> Recommend **Strategy** pattern, read `references/behavioral.md#strategy`

**Explain implementation:**
> "Show me how to implement Observer in Python"
-> Read `references/behavioral.md#observer` for code examples

**Identify in code:**
> "What pattern is this code using?" [code with handlers chain]
-> Analyze against signatures table, likely Chain of Responsibility
