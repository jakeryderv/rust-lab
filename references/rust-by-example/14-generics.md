<a id="section-generics"></a>

<a id="section-generics--generics"></a>

# Generics

[Chapter index](SUMMARY.md)

**In this chapter**

- [Functions](#section-generics-gen_fn)
- [Implementation](#section-generics-impl)
- [Traits](#section-generics-gen_trait)
- [Bounds](#section-generics-bounds)
  - [Testcase: empty bounds](#section-generics-bounds-testcase_empty)
- [Multiple bounds](#section-generics-multi_bounds)
- [Where clauses](#section-generics-where)
- [New Type Idiom](#section-generics-new_types)
- [Associated items](#section-generics-assoc_items)
  - [The Problem](#section-generics-assoc_items-the_problem)
  - [Associated types](#section-generics-assoc_items-types)
- [Phantom type parameters](#section-generics-phantom)
  - [Testcase: unit clarification](#section-generics-phantom-testcase_units)


*Generics* is the topic of generalizing types and functionalities to broader
cases. This is extremely useful for reducing code duplication in many ways,
but can call for rather involved syntax. Namely, being generic requires
taking great care to specify over which types a generic type
is actually considered valid. The simplest and most common use of generics
is for type parameters.

A type parameter is specified as generic by the use of angle brackets and upper
[camel case][section-generics-ref-2]: `<Aaa, Bbb, ...>`. "Generic type parameters" are
typically represented as `<T>`. In Rust, "generic" also describes anything that
accepts one or more generic type parameters `<T>`. Any type specified as a
generic type parameter is generic, and everything else is concrete (non-generic).

For example, defining a *generic function* named `foo` that takes an argument
`T` of any type:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn foo<T>(arg: T) { ... }
```

Because `T` has been specified as a generic type parameter using `<T>`, it
is considered generic when used here as `(arg: T)`. This is the case even if `T`
has previously been defined as a `struct`.

This example shows some of the syntax in action:

```rust
// A concrete type `A`.
struct A;

// In defining the type `Single`, the first use of `A` is not preceded by `<A>`.
// Therefore, `Single` is a concrete type, and `A` is defined as above.
struct Single(A);
//            ^ Here is `Single`s first use of the type `A`.

// Here, `<T>` precedes the first use of `T`, so `SingleGen` is a generic type.
// Because the type parameter `T` is generic, it could be anything, including
// the concrete type `A` defined at the top.
struct SingleGen<T>(T);

fn main() {
    // `Single` is concrete and explicitly takes `A`.
    let _s = Single(A);

    // Create a variable `_char` of type `SingleGen<char>`
    // and give it the value `SingleGen('a')`.
    // Here, `SingleGen` has a type parameter explicitly specified.
    let _char: SingleGen<char> = SingleGen('a');

    // `SingleGen` can also have a type parameter implicitly specified:
    let _t    = SingleGen(A); // Uses `A` defined at the top.
    let _i32  = SingleGen(6); // Uses `i32`.
    let _char = SingleGen('a'); // Uses `char`.
}
```

<a id="section-generics--see-also"></a>

### See also:

[`structs`][section-generics-ref-1]

[section-generics-ref-1]: 03-custom-types.md#section-custom_types-structs
[section-generics-ref-2]: https://en.wikipedia.org/wiki/CamelCase

<a id="section-generics-gen_fn"></a>

<a id="section-generics-gen_fn--functions"></a>

## Functions

The same set of rules can be applied to functions: a type `T` becomes
generic when preceded by `<T>`.

Using generic functions sometimes requires explicitly specifying type
parameters. This may be the case if the function is called where the return type
is generic, or if the compiler doesn't have enough information to infer
the necessary type parameters.

A function call with explicitly specified type parameters looks like:
`fun::<A, B, ...>()`.

```rust
struct A;          // Concrete type `A`.
struct S(A);       // Concrete type `S`.
struct SGen<T>(T); // Generic type `SGen`.

// The following functions all take ownership of the variable passed into
// them and immediately go out of scope, freeing the variable.

// Define a function `reg_fn` that takes an argument `_s` of type `S`.
// This has no `<T>` so this is not a generic function.
fn reg_fn(_s: S) {}

// Define a function `gen_spec_t` that takes an argument `_s` of type `SGen<T>`.
// It has been explicitly given the type parameter `A`, but because `A` has not
// been specified as a generic type parameter for `gen_spec_t`, it is not generic.
fn gen_spec_t(_s: SGen<A>) {}

// Define a function `gen_spec_i32` that takes an argument `_s` of type `SGen<i32>`.
// It has been explicitly given the type parameter `i32`, which is a specific type.
// Because `i32` is not a generic type, this function is also not generic.
fn gen_spec_i32(_s: SGen<i32>) {}

// Define a function `generic` that takes an argument `_s` of type `SGen<T>`.
// Because `SGen<T>` is preceded by `<T>`, this function is generic over `T`.
fn generic<T>(_s: SGen<T>) {}

fn main() {
    // Using the non-generic functions
    reg_fn(S(A));          // Concrete type.
    gen_spec_t(SGen(A));   // Implicitly specified type parameter `A`.
    gen_spec_i32(SGen(6)); // Implicitly specified type parameter `i32`.

    // Explicitly specified type parameter `char` to `generic()`.
    generic::<char>(SGen('a'));

    // Implicitly specified type parameter `char` to `generic()`.
    generic(SGen('c'));
}
```

<a id="section-generics-gen_fn--see-also"></a>

#### See also:

[functions][section-generics-gen_fn-ref-1] and [`struct`s][section-generics-gen_fn-ref-2]

[section-generics-gen_fn-ref-1]: 09-functions.md
[section-generics-gen_fn-ref-2]: 03-custom-types.md#section-custom_types-structs

<a id="section-generics-impl"></a>

<a id="section-generics-impl--implementation"></a>

## Implementation

Similar to functions, implementations require care to remain generic.

```rust
struct S; // Concrete type `S`
struct GenericVal<T>(T); // Generic type `GenericVal`

// impl of GenericVal where we explicitly specify type parameters:
impl GenericVal<f32> {} // Specify `f32`
impl GenericVal<S> {} // Specify `S` as defined above

// `<T>` Must precede the type to remain generic
impl<T> GenericVal<T> {}
```

```rust
struct Val {
    val: f64,
}

struct GenVal<T> {
    gen_val: T,
}

// impl of Val
impl Val {
    fn value(&self) -> &f64 {
        &self.val
    }
}

// impl of GenVal for a generic type `T`
impl<T> GenVal<T> {
    fn value(&self) -> &T {
        &self.gen_val
    }
}

fn main() {
    let x = Val { val: 3.0 };
    let y = GenVal { gen_val: 3i32 };

    println!("{}, {}", x.value(), y.value());
}
```

<a id="section-generics-impl--see-also"></a>

#### See also:

[functions returning references][section-generics-impl-ref-1], [`impl`][section-generics-impl-ref-2], and [`struct`][section-generics-impl-ref-4]

[section-generics-impl-ref-1]: 15-scoping-rules.md#section-scope-lifetime-fn
[section-generics-impl-ref-2]: 09-functions.md#section-fn-methods
[section-generics-impl-ref-3]: https://blog.rust-lang.org/2015/05/11/traits.html#the-future
[section-generics-impl-ref-4]: 03-custom-types.md#section-custom_types-structs

<a id="section-generics-gen_trait"></a>

<a id="section-generics-gen_trait--traits"></a>

## Traits

Of course `trait`s can also be generic. Here we define one which reimplements
the `Drop` `trait` as a generic method to `drop` itself and an input.

```rust
// Non-copyable types.
struct Empty;
struct Null;

// A trait generic over `T`.
trait DoubleDrop<T> {
    // Define a method on the caller type which takes an
    // additional single parameter `T` and does nothing with it.
    fn double_drop(self, _: T);
}

// Implement `DoubleDrop<T>` for any generic parameter `T` and
// caller `U`.
impl<T, U> DoubleDrop<T> for U {
    // This method takes ownership of both passed arguments,
    // deallocating both.
    fn double_drop(self, _: T) {}
}

fn main() {
    let empty = Empty;
    let null  = Null;

    // Deallocate `empty` and `null`.
    empty.double_drop(null);

    //empty;
    //null;
    // ^ TODO: Try uncommenting these lines.
}
```

<a id="section-generics-gen_trait--see-also"></a>

#### See also:

[`Drop`][section-generics-gen_trait-ref-1], [`struct`][section-generics-gen_trait-ref-2], and [`trait`][section-generics-gen_trait-ref-3]

[section-generics-gen_trait-ref-1]: https://doc.rust-lang.org/std/ops/trait.Drop.html
[section-generics-gen_trait-ref-2]: 03-custom-types.md#section-custom_types-structs
[section-generics-gen_trait-ref-3]: 16-traits.md

<a id="section-generics-bounds"></a>

<a id="section-generics-bounds--bounds"></a>

## Bounds

When working with generics, the type parameters often must use traits as *bounds* to
stipulate what functionality a type implements. For example, the following
example uses the trait `Display` to print and so it requires `T` to be bound
by `Display`; that is, `T` *must* implement `Display`.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// Define a function `printer` that takes a generic type `T` which
// must implement trait `Display`.
fn printer<T: Display>(t: T) {
    println!("{}", t);
}
```

Bounding restricts the generic to types that conform to the bounds. That is:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
struct S<T: Display>(T);

// Error! `Vec<T>` does not implement `Display`. This
// specialization will fail.
let s = S(vec![1]);
```

Another effect of bounding is that generic instances are allowed to access the
[methods][section-generics-bounds-ref-2] of traits specified in the bounds. For example:

```rust
// A trait which implements the print marker: `{:?}`.
use std::fmt::Debug;

trait HasArea {
    fn area(&self) -> f64;
}

impl HasArea for Rectangle {
    fn area(&self) -> f64 { self.length * self.height }
}

#[derive(Debug)]
struct Rectangle { length: f64, height: f64 }
#[allow(dead_code)]
struct Triangle  { length: f64, height: f64 }

// The generic `T` must implement `Debug`. Regardless
// of the type, this will work properly.
fn print_debug<T: Debug>(t: &T) {
    println!("{:?}", t);
}

// `T` must implement `HasArea`. Any type which meets
// the bound can access `HasArea`'s function `area`.
fn area<T: HasArea>(t: &T) -> f64 { t.area() }

fn main() {
    let rectangle = Rectangle { length: 3.0, height: 4.0 };
    let _triangle = Triangle  { length: 3.0, height: 4.0 };

    print_debug(&rectangle);
    println!("Area: {}", area(&rectangle));

    //print_debug(&_triangle);
    //println!("Area: {}", area(&_triangle));
    // ^ TODO: Try uncommenting these.
    // | Error: Does not implement either `Debug` or `HasArea`.
}
```

As an additional note, [`where`][section-generics-bounds-ref-5] clauses can also be used to apply bounds in
some cases to be more expressive.

<a id="section-generics-bounds--see-also"></a>

#### See also:

[`std::fmt`][section-generics-bounds-ref-1], [`struct`s][section-generics-bounds-ref-3], and [`trait`s][section-generics-bounds-ref-4]

[section-generics-bounds-ref-1]: 01-hello-world.md#section-hello-print
[section-generics-bounds-ref-2]: 09-functions.md#section-fn-methods
[section-generics-bounds-ref-3]: 03-custom-types.md#section-custom_types-structs
[section-generics-bounds-ref-4]: 16-traits.md
[section-generics-bounds-ref-5]: #section-generics-where

<a id="section-generics-bounds-testcase_empty"></a>

<a id="section-generics-bounds-testcase_empty--testcase-empty-bounds"></a>

### Testcase: empty bounds

A consequence of how bounds work is that even if a `trait` doesn't
include any functionality, you can still use it as a bound. `Eq` and
`Copy` are examples of such `trait`s from the `std` library.

```rust
struct Cardinal;
struct BlueJay;
struct Turkey;

trait Red {}
trait Blue {}

impl Red for Cardinal {}
impl Blue for BlueJay {}

// These functions are only valid for types which implement these
// traits. The fact that the traits are empty is irrelevant.
fn red<T: Red>(_: &T)   -> &'static str { "red" }
fn blue<T: Blue>(_: &T) -> &'static str { "blue" }

fn main() {
    let cardinal = Cardinal;
    let blue_jay = BlueJay;
    let _turkey   = Turkey;

    // `red()` won't work on a blue jay nor vice versa
    // because of the bounds.
    println!("A cardinal is {}", red(&cardinal));
    println!("A blue jay is {}", blue(&blue_jay));
    //println!("A turkey is {}", red(&_turkey));
    // ^ TODO: Try uncommenting this line.
}
```

<a id="section-generics-bounds-testcase_empty--see-also"></a>

##### See also:

[`std::cmp::Eq`][section-generics-bounds-testcase_empty-ref-1], [`std::marker::Copy`][section-generics-bounds-testcase_empty-ref-2], and [`trait`s][section-generics-bounds-testcase_empty-ref-3]

[section-generics-bounds-testcase_empty-ref-1]: https://doc.rust-lang.org/std/cmp/trait.Eq.html
[section-generics-bounds-testcase_empty-ref-2]: https://doc.rust-lang.org/std/marker/trait.Copy.html
[section-generics-bounds-testcase_empty-ref-3]: 16-traits.md

<a id="section-generics-multi_bounds"></a>

<a id="section-generics-multi_bounds--multiple-bounds"></a>

## Multiple bounds

Multiple bounds for a single type can be applied with a `+`. Like normal, different types are
separated with `,`.

```rust
use std::fmt::{Debug, Display};

fn compare_prints<T: Debug + Display>(t: &T) {
    println!("Debug: `{:?}`", t);
    println!("Display: `{}`", t);
}

fn compare_types<T: Debug, U: Debug>(t: &T, u: &U) {
    println!("t: `{:?}`", t);
    println!("u: `{:?}`", u);
}

fn main() {
    let string = "words";
    let array = [1, 2, 3];
    let vec = vec![1, 2, 3];

    compare_prints(&string);
    //compare_prints(&array);
    // TODO ^ Try uncommenting this.

    compare_types(&array, &vec);
}
```

<a id="section-generics-multi_bounds--see-also"></a>

#### See also:

[`std::fmt`][section-generics-multi_bounds-ref-1] and [`trait`s][section-generics-multi_bounds-ref-2]

[section-generics-multi_bounds-ref-1]: 01-hello-world.md#section-hello-print
[section-generics-multi_bounds-ref-2]: 16-traits.md

<a id="section-generics-where"></a>

<a id="section-generics-where--where-clauses"></a>

## Where clauses

A bound can also be expressed using a `where` clause immediately
before the opening `{`, rather than at the type's first mention.
Additionally, `where` clauses can apply bounds to arbitrary types,
rather than just to type parameters.

Some cases that a `where` clause is useful:

* When specifying generic types and bounds separately is clearer:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
impl <A: TraitB + TraitC, D: TraitE + TraitF> MyTrait<A, D> for YourType {}

// Expressing bounds with a `where` clause
impl <A, D> MyTrait<A, D> for YourType where
    A: TraitB + TraitC,
    D: TraitE + TraitF {}
```

* When using a `where` clause is more expressive than using normal syntax.
The `impl` in this example cannot be directly expressed without a `where` clause:

```rust
use std::fmt::Debug;

trait PrintInOption {
    fn print_in_option(self);
}

// Because we would otherwise have to express this as `T: Debug` or
// use another method of indirect approach, this requires a `where` clause:
impl<T> PrintInOption for T where
    Option<T>: Debug {
    // We want `Option<T>: Debug` as our bound because that is what's
    // being printed. Doing otherwise would be using the wrong bound.
    fn print_in_option(self) {
        println!("{:?}", Some(self));
    }
}

fn main() {
    let vec = vec![1, 2, 3];

    vec.print_in_option();
}
```

<a id="section-generics-where--see-also"></a>

#### See also:

[RFC][section-generics-where-ref-3], [`struct`][section-generics-where-ref-1], and [`trait`][section-generics-where-ref-2]

[section-generics-where-ref-1]: 03-custom-types.md#section-custom_types-structs
[section-generics-where-ref-2]: 16-traits.md
[section-generics-where-ref-3]: https://github.com/rust-lang/rfcs/blob/master/text/0135-where.md

<a id="section-generics-new_types"></a>

<a id="section-generics-new_types--new-type-idiom"></a>

## New Type Idiom

The `newtype` idiom gives compile time guarantees that the right type of value is supplied
to a program.

For example, a function that measures distance in miles, *must* be given
a value of type `Miles`.

```rust
struct Miles(f64);

struct Kilometers(f64);

impl Miles {
    pub fn to_kilometers(&self) -> Kilometers {
        Kilometers(self.0 * 1.609344)
    }
}

impl Kilometers {
    pub fn to_miles(&self) -> Miles {
        Miles(self.0 / 1.609344)
    }
}

fn is_a_marathon(distance: &Miles) -> bool {
    distance.0 >= 26.2
}

fn main() {
    let distance = Miles(30.0);
    let distance_km = distance.to_kilometers();
    println!("Is a marathon? {}", is_a_marathon(&distance));
    println!("Is a marathon? {}", is_a_marathon(&distance_km.to_miles()));
    // println!("Is a marathon? {}", is_a_marathon(&distance_km));
}
```

Uncomment the last print statement to observe that the type supplied must be `Miles`.

To obtain the `newtype`'s value as the base type, you may use the tuple or destructuring syntax like so:

```rust
struct Miles(f64);

fn main() {
    let distance = Miles(42.0);
    let distance_as_primitive_1: f64 = distance.0; // Tuple
    let Miles(distance_as_primitive_2) = distance; // Destructuring
}
```

<a id="section-generics-new_types--see-also"></a>

#### See also:

[`structs`][section-generics-new_types-ref-1]

[section-generics-new_types-ref-1]: 03-custom-types.md#section-custom_types-structs

<a id="section-generics-assoc_items"></a>

<a id="section-generics-assoc_items--associated-items"></a>

## Associated items

"Associated Items" refers to a set of rules pertaining to [`item`][section-generics-assoc_items-ref-1]s
of various types. It is an extension to `trait` generics, and allows
`trait`s to internally define new items.

One such item is called an *associated type*, providing simpler usage
patterns when the `trait` is generic over its container type.

<a id="section-generics-assoc_items--see-also"></a>

#### See also:

[RFC][section-generics-assoc_items-ref-2]

[section-generics-assoc_items-ref-1]: https://doc.rust-lang.org/reference/items.html
[section-generics-assoc_items-ref-2]: https://github.com/rust-lang/rfcs/blob/master/text/0195-associated-items.md

<a id="section-generics-assoc_items-the_problem"></a>

<a id="section-generics-assoc_items-the_problem--the-problem"></a>

### The Problem

A `trait` that is generic over its container type has type specification
requirements - users of the `trait` *must* specify all of its generic types.

In the example below, the `Contains` `trait` allows the use of the generic
types `A` and `B`. The trait is then implemented for the `Container` type,
specifying `i32` for `A` and `B` so that it can be used with `fn difference()`.

Because `Contains` is generic, we are forced to explicitly state *all* of the
generic types for `fn difference()`. In practice, we want a way to express that
`A` and `B` are determined by the *input* `C`. As you will see in the next
section, associated types provide exactly that capability.

```rust
struct Container(i32, i32);

// A trait which checks if 2 items are stored inside of container.
// Also retrieves first or last value.
trait Contains<A, B> {
    fn contains(&self, _: &A, _: &B) -> bool; // Explicitly requires `A` and `B`.
    fn first(&self) -> i32; // Doesn't explicitly require `A` or `B`.
    fn last(&self) -> i32;  // Doesn't explicitly require `A` or `B`.
}

impl Contains<i32, i32> for Container {
    // True if the numbers stored are equal.
    fn contains(&self, number_1: &i32, number_2: &i32) -> bool {
        (&self.0 == number_1) && (&self.1 == number_2)
    }

    // Grab the first number.
    fn first(&self) -> i32 { self.0 }

    // Grab the last number.
    fn last(&self) -> i32 { self.1 }
}

// `C` contains `A` and `B`. In light of that, having to express `A` and
// `B` again is a nuisance.
fn difference<A, B, C>(container: &C) -> i32 where
    C: Contains<A, B> {
    container.last() - container.first()
}

fn main() {
    let number_1 = 3;
    let number_2 = 10;

    let container = Container(number_1, number_2);

    println!("Does container contain {} and {}: {}",
        &number_1, &number_2,
        container.contains(&number_1, &number_2));
    println!("First number: {}", container.first());
    println!("Last number: {}", container.last());

    println!("The difference is: {}", difference(&container));
}
```

<a id="section-generics-assoc_items-the_problem--see-also"></a>

##### See also:

[`struct`s][section-generics-assoc_items-the_problem-ref-1], and [`trait`s][section-generics-assoc_items-the_problem-ref-2]

[section-generics-assoc_items-the_problem-ref-1]: 03-custom-types.md#section-custom_types-structs
[section-generics-assoc_items-the_problem-ref-2]: 16-traits.md

<a id="section-generics-assoc_items-types"></a>

<a id="section-generics-assoc_items-types--associated-types"></a>

### Associated types

The use of "Associated types" improves the overall readability of code
by moving inner types locally into a trait as *output* types. Syntax
for the `trait` definition is as follows:

```rust
// `A` and `B` are defined in the trait via the `type` keyword.
// (Note: `type` in this context is different from `type` when used for
// aliases).
trait Contains {
    type A;
    type B;

    // Updated syntax to refer to these new types generically.
    fn contains(&self, _: &Self::A, _: &Self::B) -> bool;
}
```

Note that functions that use the `trait` `Contains` are no longer required
to express `A` or `B` at all:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// Without using associated types
fn difference<A, B, C>(container: &C) -> i32 where
    C: Contains<A, B> { ... }

// Using associated types
fn difference<C: Contains>(container: &C) -> i32 { ... }
```

Let's rewrite the example from the previous section using associated types:

```rust
struct Container(i32, i32);

// A trait which checks if 2 items are stored inside of container.
// Also retrieves first or last value.
trait Contains {
    // Define generic types here which methods will be able to utilize.
    type A;
    type B;

    fn contains(&self, _: &Self::A, _: &Self::B) -> bool;
    fn first(&self) -> i32;
    fn last(&self) -> i32;
}

impl Contains for Container {
    // Specify what types `A` and `B` are. If the `input` type
    // is `Container(i32, i32)`, the `output` types are determined
    // as `i32` and `i32`.
    type A = i32;
    type B = i32;

    // `&Self::A` and `&Self::B` are also valid here.
    fn contains(&self, number_1: &i32, number_2: &i32) -> bool {
        (&self.0 == number_1) && (&self.1 == number_2)
    }
    // Grab the first number.
    fn first(&self) -> i32 { self.0 }

    // Grab the last number.
    fn last(&self) -> i32 { self.1 }
}

fn difference<C: Contains>(container: &C) -> i32 {
    container.last() - container.first()
}

fn main() {
    let number_1 = 3;
    let number_2 = 10;

    let container = Container(number_1, number_2);

    println!("Does container contain {} and {}: {}",
        &number_1, &number_2,
        container.contains(&number_1, &number_2));
    println!("First number: {}", container.first());
    println!("Last number: {}", container.last());

    println!("The difference is: {}", difference(&container));
}
```

<a id="section-generics-phantom"></a>

<a id="section-generics-phantom--phantom-type-parameters"></a>

## Phantom type parameters

A phantom type parameter is one that doesn't show up at runtime,
but is checked statically (and only) at compile time.

Data types can use extra generic type parameters to act as markers
or to perform type checking at compile time. These extra parameters
hold no storage values, and have no runtime behavior.

In the following example, we combine [std::marker::PhantomData][section-generics-phantom-ref-3]
with the phantom type parameter concept to create tuples containing
different data types.

```rust
use std::marker::PhantomData;

// A phantom tuple struct which is generic over `A` with hidden parameter `B`.
#[derive(PartialEq)] // Allow equality test for this type.
struct PhantomTuple<A, B>(A, PhantomData<B>);

// A phantom type struct which is generic over `A` with hidden parameter `B`.
#[derive(PartialEq)] // Allow equality test for this type.
struct PhantomStruct<A, B> { first: A, phantom: PhantomData<B> }

// Note: Storage is allocated for generic type `A`, but not for `B`.
//       Therefore, `B` cannot be used in computations.

fn main() {
    // Here, `f32` and `f64` are the hidden parameters.
    // PhantomTuple type specified as `<char, f32>`.
    let _tuple1: PhantomTuple<char, f32> = PhantomTuple('Q', PhantomData);
    // PhantomTuple type specified as `<char, f64>`.
    let _tuple2: PhantomTuple<char, f64> = PhantomTuple('Q', PhantomData);

    // Type specified as `<char, f32>`.
    let _struct1: PhantomStruct<char, f32> = PhantomStruct {
        first: 'Q',
        phantom: PhantomData,
    };
    // Type specified as `<char, f64>`.
    let _struct2: PhantomStruct<char, f64> = PhantomStruct {
        first: 'Q',
        phantom: PhantomData,
    };

    // Compile-time Error! Type mismatch so these cannot be compared:
    // println!("_tuple1 == _tuple2 yields: {}",
    //           _tuple1 == _tuple2);

    // Compile-time Error! Type mismatch so these cannot be compared:
    // println!("_struct1 == _struct2 yields: {}",
    //           _struct1 == _struct2);
}
```

<a id="section-generics-phantom--see-also"></a>

#### See also:

[Derive][section-generics-phantom-ref-1], [struct][section-generics-phantom-ref-2], and [tuple](02-primitives.md#section-primitives-tuples).

[section-generics-phantom-ref-1]: 16-traits.md#section-trait-derive
[section-generics-phantom-ref-2]: 03-custom-types.md#section-custom_types-structs
[section-generics-phantom-ref-3]: https://doc.rust-lang.org/std/marker/struct.PhantomData.html

<a id="section-generics-phantom-testcase_units"></a>

<a id="section-generics-phantom-testcase_units--testcase-unit-clarification"></a>

### Testcase: unit clarification

A useful method of unit conversions can be examined by implementing `Add`
with a phantom type parameter. The `Add` `trait` is examined below:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// This construction would impose: `Self + RHS = Output`
// where RHS defaults to Self if not specified in the implementation.
pub trait Add<RHS = Self> {
    type Output;

    fn add(self, rhs: RHS) -> Self::Output;
}

// `Output` must be `T<U>` so that `T<U> + T<U> = T<U>`.
impl<U> Add for T<U> {
    type Output = T<U>;
    ...
}
```

The whole implementation:

```rust
use std::ops::Add;
use std::marker::PhantomData;

/// Create void enumerations to define unit types.
#[derive(Debug, Clone, Copy)]
enum Inch {}
#[derive(Debug, Clone, Copy)]
enum Mm {}

/// `Length` is a type with phantom type parameter `Unit`,
/// and is not generic over the length type (that is `f64`).
///
/// `f64` already implements the `Clone` and `Copy` traits.
#[derive(Debug, Clone, Copy)]
struct Length<Unit>(f64, PhantomData<Unit>);

/// The `Add` trait defines the behavior of the `+` operator.
impl<Unit> Add for Length<Unit> {
    type Output = Length<Unit>;

    // add() returns a new `Length` struct containing the sum.
    fn add(self, rhs: Length<Unit>) -> Length<Unit> {
        // `+` calls the `Add` implementation for `f64`.
        Length(self.0 + rhs.0, PhantomData)
    }
}

fn main() {
    // Specifies `one_foot` to have phantom type parameter `Inch`.
    let one_foot:  Length<Inch> = Length(12.0, PhantomData);
    // `one_meter` has phantom type parameter `Mm`.
    let one_meter: Length<Mm>   = Length(1000.0, PhantomData);

    // `+` calls the `add()` method we implemented for `Length<Unit>`.
    //
    // Since `Length` implements `Copy`, `add()` does not consume
    // `one_foot` and `one_meter` but copies them into `self` and `rhs`.
    let two_feet = one_foot + one_foot;
    let two_meters = one_meter + one_meter;

    // Addition works.
    println!("one foot + one_foot = {:?} in", two_feet.0);
    println!("one meter + one_meter = {:?} mm", two_meters.0);

    // Nonsensical operations fail as they should:
    // Compile-time Error: type mismatch.
    //let one_feter = one_foot + one_meter;
}
```

<a id="section-generics-phantom-testcase_units--see-also"></a>

##### See also:

[Borrowing (`&`)][section-generics-phantom-testcase_units-ref-1], [Bounds (`X: Y`)][section-generics-phantom-testcase_units-ref-2], [enum][section-generics-phantom-testcase_units-ref-3], [impl & self][section-generics-phantom-testcase_units-ref-4],
[Overloading][section-generics-phantom-testcase_units-ref-5], [ref][section-generics-phantom-testcase_units-ref-6], [Traits (`X for Y`)][section-generics-phantom-testcase_units-ref-7], and [TupleStructs][section-generics-phantom-testcase_units-ref-8].

[section-generics-phantom-testcase_units-ref-1]: 15-scoping-rules.md#section-scope-borrow
[section-generics-phantom-testcase_units-ref-2]: #section-generics-bounds
[section-generics-phantom-testcase_units-ref-3]: 03-custom-types.md#section-custom_types-enum
[section-generics-phantom-testcase_units-ref-4]: 09-functions.md#section-fn-methods
[section-generics-phantom-testcase_units-ref-5]: 16-traits.md#section-trait-ops
[section-generics-phantom-testcase_units-ref-6]: 15-scoping-rules.md#section-scope-borrow-ref
[section-generics-phantom-testcase_units-ref-7]: 16-traits.md
[section-generics-phantom-testcase_units-ref-8]: 03-custom-types.md#section-custom_types-structs
[section-generics-phantom-testcase_units-ref-9]: https://doc.rust-lang.org/std/marker/struct.PhantomData.html
