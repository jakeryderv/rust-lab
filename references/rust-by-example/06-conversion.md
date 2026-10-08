<a id="section-conversion"></a>

<a id="section-conversion--conversion"></a>

# Conversion

[Chapter index](SUMMARY.md)

**In this chapter**

- [`From` and `Into`](#section-conversion-from_into)
- [`TryFrom` and `TryInto`](#section-conversion-try_from_try_into)
- [To and from `String`s](#section-conversion-string)


Primitive types can be converted to each other through [casting][section-conversion-ref-1].

Rust addresses conversion between custom types (i.e., `struct` and `enum`)
by the use of [traits][section-conversion-ref-2]. The generic
conversions will use the [`From`][section-conversion-ref-3] and [`Into`][section-conversion-ref-4] traits. However there are more
specific ones for the more common cases, in particular when converting to and
from `String`s.

[section-conversion-ref-1]: 05-types.md#section-types-cast
[section-conversion-ref-2]: 16-traits.md
[section-conversion-ref-3]: https://doc.rust-lang.org/std/convert/trait.From.html
[section-conversion-ref-4]: https://doc.rust-lang.org/std/convert/trait.Into.html

<a id="section-conversion-from_into"></a>

<a id="section-conversion-from_into--from-and-into"></a>

## `From` and `Into`

The [`From`][section-conversion-from_into-ref-1] and [`Into`][section-conversion-from_into-ref-2] traits are inherently linked, and this is actually part of
its implementation. If you are able to convert type A from type B, then it
should be easy to believe that we should be able to convert type B to type A.

<a id="section-conversion-from_into--from"></a>

### `From`

The [`From`][section-conversion-from_into-ref-1] trait allows for a type to define how to create itself from another
type, hence providing a very simple mechanism for converting between several
types. There are numerous implementations of this trait within the standard
library for conversion of primitive and common types.

For example we can easily convert a `str` into a `String`

```rust
let my_str = "hello";
let my_string = String::from(my_str);
```

We can do something similar for defining a conversion for our own type.

```rust
use std::convert::From;

#[derive(Debug)]
struct Number {
    value: i32,
}

impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}

fn main() {
    let num = Number::from(30);
    println!("My number is {:?}", num);
}
```

<a id="section-conversion-from_into--into"></a>

### `Into`

The [`Into`][section-conversion-from_into-ref-2] trait is simply the reciprocal of the `From` trait. It
defines how to convert a type into another type.

Calling `into()` typically requires us to specify the result type as the compiler is unable to determine this most of the time.

```rust
use std::convert::Into;

#[derive(Debug)]
struct Number {
    value: i32,
}

impl Into<Number> for i32 {
    fn into(self) -> Number {
        Number { value: self }
    }
}

fn main() {
    let int = 5;
    // Try removing the type annotation
    let num: Number = int.into();
    println!("My number is {:?}", num);
}
```

<a id="section-conversion-from_into--from-and-into-are-interchangeable"></a>

### `From` and `Into` are interchangeable

`From` and `Into` are designed to be complementary.
We do not need to provide an implementation for both traits.
If you have implemented the `From` trait for your type, `Into` will call it
when necessary. Note, however, that the converse is not true: implementing `Into` for your type will not automatically provide it with an implementation of `From`.

```rust
use std::convert::From;

#[derive(Debug)]
struct Number {
    value: i32,
}

// Define `From`
impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}

fn main() {
    let int = 5;
    // use `Into`
    let num: Number = int.into();
    println!("My number is {:?}", num);
}
```

[section-conversion-from_into-ref-1]: https://doc.rust-lang.org/std/convert/trait.From.html
[section-conversion-from_into-ref-2]: https://doc.rust-lang.org/std/convert/trait.Into.html

<a id="section-conversion-try_from_try_into"></a>

<a id="section-conversion-try_from_try_into--tryfrom-and-tryinto"></a>

## `TryFrom` and `TryInto`

Similar to [`From` and `Into`][section-conversion-try_from_try_into-ref-1], [`TryFrom`][section-conversion-try_from_try_into-ref-2] and [`TryInto`][section-conversion-try_from_try_into-ref-3] are
generic traits for converting between types. Unlike `From`/`Into`, the
`TryFrom`/`TryInto` traits are used for fallible conversions, and as such,
return [`Result`][section-conversion-try_from_try_into-ref-4]s.

[section-conversion-try_from_try_into-ref-1]: #section-conversion-from_into
[section-conversion-try_from_try_into-ref-2]: https://doc.rust-lang.org/std/convert/trait.TryFrom.html
[section-conversion-try_from_try_into-ref-3]: https://doc.rust-lang.org/std/convert/trait.TryInto.html
[section-conversion-try_from_try_into-ref-4]: https://doc.rust-lang.org/std/result/enum.Result.html

```rust
use std::convert::TryFrom;
use std::convert::TryInto;

#[derive(Debug, PartialEq)]
struct EvenNumber(i32);

impl TryFrom<i32> for EvenNumber {
    type Error = ();

    fn try_from(value: i32) -> Result<Self, Self::Error> {
        if value % 2 == 0 {
            Ok(EvenNumber(value))
        } else {
            Err(())
        }
    }
}

fn main() {
    // TryFrom

    assert_eq!(EvenNumber::try_from(8), Ok(EvenNumber(8)));
    assert_eq!(EvenNumber::try_from(5), Err(()));

    // TryInto

    let result: Result<EvenNumber, ()> = 8i32.try_into();
    assert_eq!(result, Ok(EvenNumber(8)));
    let result: Result<EvenNumber, ()> = 5i32.try_into();
    assert_eq!(result, Err(()));
}
```

<a id="section-conversion-string"></a>

<a id="section-conversion-string--to-and-from-strings"></a>

## To and from Strings

<a id="section-conversion-string--converting-to-string"></a>

### Converting to String

To convert any type to a `String` is as simple as implementing the [`ToString`][section-conversion-string-ref-1]
trait for the type. Rather than doing so directly, you should implement the
[`fmt::Display`][section-conversion-string-ref-2] trait which automatically provides [`ToString`][section-conversion-string-ref-1] and
also allows printing the type as discussed in the section on [`print!`][section-conversion-string-ref-3].

```rust
use std::fmt;

struct Circle {
    radius: i32
}

impl fmt::Display for Circle {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Circle of radius {}", self.radius)
    }
}

fn main() {
    let circle = Circle { radius: 6 };
    println!("{}", circle.to_string());
}
```

<a id="section-conversion-string--parsing-a-string"></a>

### Parsing a String

It's useful to convert strings into many types, but one of the more common string
operations is to convert them from string to number. The idiomatic approach to
this is to use the [`parse`][section-conversion-string-ref-4] function and either to arrange for type inference or
to specify the type to parse using the 'turbofish' syntax. Both alternatives are
shown in the following example.

This will convert the string into the type specified as long as the [`FromStr`][section-conversion-string-ref-5]
trait is implemented for that type. This is implemented for numerous types
within the standard library.

```rust
fn main() {
    let parsed: i32 = "5".parse().unwrap();
    let turbo_parsed = "10".parse::<i32>().unwrap();

    let sum = parsed + turbo_parsed;
    println!("Sum: {:?}", sum);
}
```

To obtain this functionality on a user defined type simply implement the
[`FromStr`][section-conversion-string-ref-5] trait for that type.

```rust
use std::num::ParseIntError;
use std::str::FromStr;

#[derive(Debug)]
struct Circle {
    radius: i32,
}

impl FromStr for Circle {
    type Err = ParseIntError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.trim().parse() {
            Ok(num) => Ok(Circle{ radius: num }),
            Err(e) => Err(e),
        }
    }
}

fn main() {
    let radius = "    3 ";
    let circle: Circle = radius.parse().unwrap();
    println!("{:?}", circle);
}
```

[section-conversion-string-ref-1]: https://doc.rust-lang.org/std/string/trait.ToString.html
[section-conversion-string-ref-2]: https://doc.rust-lang.org/std/fmt/trait.Display.html
[section-conversion-string-ref-3]: 01-hello-world.md#section-hello-print
[section-conversion-string-ref-4]: https://doc.rust-lang.org/std/primitive.str.html#method.parse
[section-conversion-string-ref-5]: https://doc.rust-lang.org/std/str/trait.FromStr.html
