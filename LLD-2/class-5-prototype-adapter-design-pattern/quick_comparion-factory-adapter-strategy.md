# UML Diagrams - Different Examples for Each Pattern

## 1. Factory Method Pattern - **Document Creation System**

```
┌─────────────────────────────────────────────────────────┐
│                    Application                          │
│                     (Client)                            │
└────────────────────┬────────────────────────────────────┘
                     │ uses
                     ↓
┌─────────────────────────────────────────────────────────┐
│              DocumentCreatorFactory                            │
│                <<abstract>>                             │
├─────────────────────────────────────────────────────────┤
│ + create_document(): Document  <<abstract>>             │
│ + open_document(): void                                 │
│ + save_document(): void                                 │
└────────────────────┬────────────────────────────────────┘
                     △ inherits
         ┌───────────┼───────────┐
         │           │           │
┌────────┴─────┐ ┌──┴────────┐ ┌┴──────────────┐
│ PDFCreator   │ │WordCreator│ │ ExcelCreator  │
├──────────────┤ ├───────────┤ ├───────────────┤
│ + create_    │ │+ create_  │ │+ create_      │
│   document() │ │ document()│ │  document()   │
│   : PDF      │ │  : Word   │ │  : Excel      │
└────────┬─────┘ └─────┬─────┘ └───────┬───────┘
         │ creates     │ creates       │ creates
         ↓             ↓               ↓
┌────────────────────────────────────────────┐
│           Document                         │
│         <<interface>>                      │
├────────────────────────────────────────────┤
│ + open(): void                             │
│ + save(): void                             │
│ + render(): void                           │
└────────────────┬───────────────────────────┘
                 △ implements
     ┌───────────┼───────────┐
     │           │           │
┌────┴──────┐ ┌──┴────┐ ┌───┴──────┐
│PDFDocument│ │Word    │ │Excel     │
│           │ │Document│ │Document  │
├───────────┤ ├────────┤ ├──────────┤
│+ open()   │ │+ open()│ │+ open()  │
│+ save()   │ │+ save()│ │+ save()  │
│+ render() │ │+ render│ │+ render()│
└───────────┘ └────────┘ └──────────┘
```

### Code Example
```python
# Creator
class DocumentCreator(ABC):
    @abstractmethod
    def create_document(self) -> Document:
        pass
    
    def open_document(self):
        doc = self.create_document()  # Factory method
        doc.open()
        return doc

# Concrete Creators
class PDFCreator(DocumentCreator):
    def create_document(self) -> Document:
        return PDFDocument()  # Creates PDF

class WordCreator(DocumentCreator):
    def create_document(self) -> Document:
        return WordDocument()  # Creates Word

# Usage: Factory decides WHAT to create
def open_file(file_extension: str):
    if file_extension == ".pdf":
        creator = PDFCreator()
    elif file_extension == ".docx":
        creator = WordCreator()
    
    return creator.open_document()  # Factory creates appropriate doc
```

---

## 2. Strategy Pattern - **Compression Algorithm System**

```
┌─────────────────────────────────────────┐
│      FileCompressor                     │
│         (Client)                        │
└──────────────────┬──────────────────────┘
                   │ uses
                   ↓
┌─────────────────────────────────────────┐
│       CompressionContext                │
│          (Context)                      │
├─────────────────────────────────────────┤
│ - strategy: CompressionStrategy         │
├─────────────────────────────────────────┤
│ + __init__(strategy)                    │
│ + set_strategy(strategy)                │
│ + compress_file(file): bytes            │
└──────────────────┬──────────────────────┘
                   │ has-a
                   ↓
┌─────────────────────────────────────────┐
│     CompressionStrategy                 │
│        <<interface>>                    │
├─────────────────────────────────────────┤
│ + compress(data): bytes  <<abstract>>   │
│ + decompress(data): bytes <<abstract>>  │
└──────────────────┬──────────────────────┘
                   △ implements
       ┌───────────┼───────────┐
       │           │           │
┌──────┴─────┐ ┌──┴───────┐ ┌─┴──────────┐
│  ZIP       │ │  RAR     │ │  GZIP      │
│  Strategy  │ │ Strategy │ │  Strategy  │
├────────────┤ ├──────────┤ ├────────────┤
│+compress() │ │+compress()│ │+compress() │
│+decompress│ │+decompress│ │+decompress │
└────────────┘ └──────────┘ └────────────┘
```

### Code Example
```python
# Strategy Interface
class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        pass

# Concrete Strategies (Different algorithms)
class ZipStrategy(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        return zlib.compress(data)  # ZIP algorithm

class RarStrategy(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        return rarfile.compress(data)  # RAR algorithm

class GzipStrategy(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        return gzip.compress(data)  # GZIP algorithm

# Context
class CompressionContext:
    def __init__(self, strategy: CompressionStrategy):
        self.strategy = strategy
    
    def compress_file(self, file_data: bytes) -> bytes:
        return self.strategy.compress(file_data)

# Usage: Strategy decides HOW to compress
compressor = CompressionContext(ZipStrategy())
result = compressor.compress_file(data)

# SWITCH algorithm at runtime
compressor.set_strategy(GzipStrategy())  # Change behavior
result = compressor.compress_file(data)
```

---

## 3. Adapter Pattern - **Payment SDK Integration** (same as before)

```
┌─────────────────────────────────────────┐
│           Client                        │
└──────────────────┬──────────────────────┘
                   │ expects
                   ↓
┌─────────────────────────────────────────┐
│       PaymentGateway                    │
│        <<interface>>                    │
│          (Target)                       │
├─────────────────────────────────────────┤
│ + process_payment(amount): dict         │
└──────────────────┬──────────────────────┘
                   △ implements
       ┌───────────┴───────────┐
       │                       │
┌──────┴─────────┐   ┌─────────┴────────┐
│ StripeAdapter  │   │  PayPalAdapter   │
├────────────────┤   ├──────────────────┤
│- stripe_sdk    │   │- paypal_sdk      │
├────────────────┤   ├──────────────────┤
│+ process_      │   │+ process_        │
│  payment()     │   │  payment()       │
└────────┬───────┘   └────────┬─────────┘
         │ wraps              │ wraps
         ↓                    ↓
┌────────────────┐   ┌────────────────┐
│   StripeSDK    │   │   PayPalSDK    │
│   (Adaptee)    │   │   (Adaptee)    │
├────────────────┤   ├────────────────┤
│+ create_charge │   │+ execute_      │
│  (cents)       │   │  payment(dict) │
└────────────────┘   └────────────────┘
     ↑ Third-party          ↑ Third-party
     (Can't modify)         (Can't modify)
```

---

## Complete Comparison Table

| Aspect | Factory Method (Documents) | Strategy (Compression) | Adapter (Payment) |
|--------|---------------------------|------------------------|-------------------|
| **Purpose** | Create different document types | Switch compression algorithms | Integrate incompatible payment SDKs |
| **Example** | `PDFCreator` creates `PDFDocument` | `ZipStrategy` vs `GzipStrategy` | `StripeAdapter` wraps `StripeSDK` |
| **Problem Solved** | Don't know document type until runtime | Need different compression for different files | Stripe SDK has `create_charge()`, we need `process_payment()` |
| **Key Question** | **WHAT** to create? | **HOW** to do it? | **HOW** to make it compatible? |
| **Flexibility** | Add new document types easily | Switch algorithms at runtime | Integrate new SDKs without changing code |
| **Client Code** | `creator.open_document()` | `compressor.compress_file(data)` | `gateway.process_payment(100)` |
| **Changes When** | Adding PDF/Word/Excel support | Adding ZIP/RAR/GZIP support | Adding Stripe/PayPal/Square support |
| **Pattern Type** | Creational | Behavioral | Structural |
| **Relationship** | Creator creates Product | Context uses Strategy | Adapter wraps Adaptee |

---

## Real-World Scenario Comparison

| Scenario | Factory | Strategy | Adapter |
|----------|---------|----------|---------|
| **File Export** | User clicks "Export" → Factory creates PDF/Excel/CSV based on choice | User chooses quality → Strategy uses High/Medium/Low compression | PDF library expects inches, you use pixels → Adapter converts |
| **Sorting** | Create different sorters for arrays/linked lists | Choose QuickSort/MergeSort/BubbleSort based on data size | Old sorting API uses callbacks, new uses comparators → Adapter translates |
| **Logging** | Create FileLogger/DatabaseLogger/CloudLogger | Choose log format: JSON/XML/Plain text | Third-party logger uses `log()`, you need `write()` → Adapter wraps |
| **Navigation** | Create CarNavigator/BikeNavigator/WalkingNavigator | Choose route algorithm: Fastest/Shortest/Scenic | Google Maps API incompatible with your Map interface → Adapter translates |

---

## Key Takeaway

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│    FACTORY     │     │   STRATEGY     │     │    ADAPTER     │
│                │     │                │     │                │
│  "Which one    │     │  "How to do    │     │  "Make it fit" │
│   to create?"  │     │   this task?"  │     │                │
│                │     │                │     │                │
│  PDF or Word?  │     │  ZIP or GZIP?  │     │  Stripe SDK    │
│                │     │                │     │  → Your API    │
└────────────────┘     └────────────────┘     └────────────────┘
     CREATION              BEHAVIOR              STRUCTURE
```