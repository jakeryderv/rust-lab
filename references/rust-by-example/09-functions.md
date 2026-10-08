<a id="section-fn"></a>

<a id="section-fn--functions"></a>

# Functions

[Chapter index](SUMMARY.md)

**In this chapter**

- [Methods](#section-fn-methods)
- [Closures](#section-fn-closures)
  - [Capturing](#section-fn-closures-capture)
  - [As input parameters](#section-fn-closures-input_parameters)
  - [Type anonymity](#section-fn-closures-anonymity)
  - [Input functions](#section-fn-closures-input_functions)
  - [As output parameters](#section-fn-closures-output_parameters)
  - [Examples in `std`](#section-fn-closures-closure_examples)
    - [Iterator::any](#section-fn-closures-closure_examples-iter_any)
    - [Searching through iterators](#section-fn-closures-closure_examples-iter_find)
- [Higher Order Functions](#section-fn-hof)
- [Diverging functions](#section-fn-diverging)


Functions are declared using the `fn` keyword. Its arguments are type
annotated, just like variables, and, if the function returns a value, the
return type must be specified after an arrow `->`.

The final expression in the function will be used as return value.
Alternatively, the `return` statement can be used to return a value earlier
from within the function, even from inside loops or `if` statements.

Let's rewrite FizzBuzz using functions!

```rust
// Unlike C/C++, there's no restriction on the order of function definitions
fn main() {
    // We can use this function here, and define it somewhere later
    fizzbuzz_to(100);
}

// Function that returns a boolean value
fn is_divisible_by(lhs: u32, rhs: u32) -> bool {
    // Corner case, early return
    if rhs == 0 {
        return false;
    }

    // This is an expression, the `return` keyword is not necessary here
    lhs % rhs == 0
}

// Functions that "don't" return a value, actually return the unit type `()`
fn fizzbuzz(n: u32) -> () {
    if is_divisible_by(n, 15) {
        println!("fizzbuzz");
    } else if is_divisible_by(n, 3) {
        println!("fizz");
    } else if is_divisible_by(n, 5) {
        println!("buzz");
    } else {
        println!("{}", n);
    }
}

// When a function returns `()`, the return type can be omitted from the
// signature
fn fizzbuzz_to(n: u32) {
    for n in 1..=n {
        fizzbuzz(n);
    }
}
```

<a id="section-fn-methods"></a>

<a id="section-fn-methods--associated-functions--methods"></a>

## Associated functions & Methods

Some functions are connected to a particular type. These come in two forms:
associated functions, and methods. Associated functions are functions that
are defined on a type generally, while methods are associated functions that are
called on a particular instance of a type.

```rust
struct Point {
    x: f64,
    y: f64,
}

// Implementation block, all `Point` associated functions & methods go in here
impl Point {
    // This is an "associated function" because this function is associated with
    // a particular type, that is, Point.
    //
    // Associated functions don't need to be called with an instance.
    // These functions are generally used like constructors.
    fn origin() -> Point {
        Point { x: 0.0, y: 0.0 }
    }

    // Another associated function, taking two arguments:
    fn new(x: f64, y: f64) -> Point {
        Point { x: x, y: y }
    }
}

struct Rectangle {
    p1: Point,
    p2: Point,
}

impl Rectangle {
    // This is a method
    // `&self` is sugar for `self: &Self`, where `Self` is the type of the
    // caller object. In this case `Self` = `Rectangle`
    fn area(&self) -> f64 {
        // `self` gives access to the struct fields via the dot operator
        let Point { x: x1, y: y1 } = self.p1;
        let Point { x: x2, y: y2 } = self.p2;

        // `abs` is a `f64` method that returns the absolute value of the
        // caller
        ((x1 - x2) * (y1 - y2)).abs()
    }

    fn perimeter(&self) -> f64 {
        let Point { x: x1, y: y1 } = self.p1;
        let Point { x: x2, y: y2 } = self.p2;

        2.0 * ((x1 - x2).abs() + (y1 - y2).abs())
    }

    // This method requires the caller object to be mutable
    // `&mut self` desugars to `self: &mut Self`
    fn translate(&mut self, x: f64, y: f64) {
        self.p1.x += x;
        self.p2.x += x;

        self.p1.y += y;
        self.p2.y += y;
    }
}

// `Pair` owns resources: two heap allocated integers
struct Pair(Box<i32>, Box<i32>);

impl Pair {
    // This method "consumes" the resources of the caller object
    // `self` desugars to `self: Self`
    fn destroy(self) {
        // Destructure `self`
        let Pair(first, second) = self;

        println!("Destroying Pair({}, {})", first, second);

        // `first` and `second` go out of scope and get freed
    }
}

fn main() {
    let rectangle = Rectangle {
        // Associated functions are called using double colons
        p1: Point::origin(),
        p2: Point::new(3.0, 4.0),
    };

    // Methods are called using the dot operator
    // Note that the first argument `&self` is implicitly passed, i.e.
    // `rectangle.perimeter()` === `Rectangle::perimeter(&rectangle)`
    println!("Rectangle perimeter: {}", rectangle.perimeter());
    println!("Rectangle area: {}", rectangle.area());

    let mut square = Rectangle {
        p1: Point::origin(),
        p2: Point::new(1.0, 1.0),
    };

    // Error! `rectangle` is immutable, but this method requires a mutable
    // object
    //rectangle.translate(1.0, 0.0);
    // TODO ^ Try uncommenting this line

    // Okay! Mutable objects can call mutable methods
    square.translate(1.0, 1.0);

    let pair = Pair(Box::new(1), Box::new(2));

    pair.destroy();

    // Error! Previous `destroy` call "consumed" `pair`
    //pair.destroy();
    // TODO ^ Try uncommenting this line
}
```

<a id="section-fn-closures"></a>

<a id="section-fn-closures--closures"></a>

## Closures

Closures are functions that can capture the enclosing environment. For
example, a closure that captures the `x` variable:

```rust
|val| val + x
```

The syntax and capabilities of closures make them very convenient for
on the fly usage. Calling a closure is exactly like calling a function.
However, both input and return types *can* be inferred and input
variable names *must* be specified.

Other characteristics of closures include:

* using `||` instead of `()` around input variables.
* optional body delimitation (`{}`) for a single line expression (mandatory otherwise).
* the ability to capture the outer environment variables.

```rust
fn main() {
    let outer_var = 42;

    // A regular function can't refer to variables in the enclosing environment
    //fn function(i: i32) -> i32 { i + outer_var }
    // TODO: uncomment the line above and see the compiler error. The compiler
    // suggests that we define a closure instead.

    // Closures are anonymous, here we are binding them to references.
    // Annotation is identical to function annotation but is optional
    // as are the `{}` wrapping the body. These nameless functions
    // are assigned to appropriately named variables.
    let closure_annotated = |i: i32| -> i32 { i + outer_var };
    let closure_inferred  = |i     |          i + outer_var  ;

    // Call the closures.
    println!("closure_annotated: {}", closure_annotated(1));
    println!("closure_inferred: {}", closure_inferred(1));
    // Once closure's type has been inferred, it cannot be inferred again with another type.
    //println!("cannot reuse closure_inferred with another type: {}", closure_inferred(42i64));
    // TODO: uncomment the line above and see the compiler error.

    // A closure taking no arguments which returns an `i32`.
    // The return type is inferred.
    let one = || 1;
    println!("closure returning one: {}", one());

}
```

<a id="section-fn-closures-capture"></a>

<a id="section-fn-closures-capture--capturing"></a>

### Capturing

Closures are inherently flexible and will do what the functionality requires
to make the closure work without annotation. This allows capturing to
flexibly adapt to the use case, sometimes moving and sometimes borrowing.
Closures can capture variables:

* by reference: `&T`
* by mutable reference: `&mut T`
* by value: `T`

They preferentially capture variables by reference and only go lower when
required.

```rust
fn main() {
    use std::mem;

    let color = String::from("green");

    // A closure to print `color` which immediately borrows (`&`) `color` and
    // stores the borrow and closure in the `print` variable. It will remain
    // borrowed until `print` is used the last time.
    //
    // `println!` only requires arguments by immutable reference so it doesn't
    // impose anything more restrictive.
    let print = || println!("`color`: {}", color);

    // Call the closure using the borrow.
    print();

    // `color` can be borrowed immutably again, because the closure only holds
    // an immutable reference to `color`.
    let _reborrow = &color;
    print();

    // A move or reborrow is allowed after the final use of `print`
    let _color_moved = color;


    let mut count = 0;
    // A closure to increment `count` could take either `&mut count` or `count`
    // but `&mut count` is less restrictive so it takes that. Immediately
    // borrows `count`.
    //
    // A `mut` is required on `inc` because a `&mut` is stored inside. Thus,
    // calling the closure mutates `count` which requires a `mut`.
    let mut inc = || {
        count += 1;
        println!("`count`: {}", count);
    };

    // Call the closure using a mutable borrow.
    inc();

    // The closure still mutably borrows `count` because it is called later.
    // An attempt to reborrow will lead to an error.
    // let _reborrow = &count;
    // ^ TODO: try uncommenting this line.
    inc();

    // The closure no longer needs to borrow `&mut count`. Therefore, it is
    // possible to reborrow without an error
    let _count_reborrowed = &mut count;


    // A non-copy type.
    let movable = Box::new(3);

    // `mem::drop` requires `T` so this must take by value. A copy type
    // would copy into the closure leaving the original untouched.
    // A non-copy must move and so `movable` immediately moves into
    // the closure.
    let consume = || {
        println!("`movable`: {:?}", movable);
        mem::drop(movable);
    };

    // `consume` consumes the variable so this can only be called once.
    consume();
    // consume();
    // ^ TODO: Try uncommenting this line.
}
```

Using `move` before vertical pipes forces closure
to take ownership of captured variables:

```rust
fn main() {
    // `Vec` has non-copy semantics.
    let haystack = vec![1, 2, 3];

    let contains = move |needle| haystack.contains(needle);

    println!("{}", contains(&1));
    println!("{}", contains(&4));

    // println!("There're {} elements in vec", haystack.len());
    // ^ Uncommenting above line will result in compile-time error
    // because borrow checker doesn't allow re-using variable after it
    // has been moved.

    // Removing `move` from closure's signature will cause closure
    // to borrow _haystack_ variable immutably, hence _haystack_ is still
    // available and uncommenting above line will not cause an error.
}
```

<a id="section-fn-closures-capture--see-also"></a>

##### See also:

[`Box`][section-fn-closures-capture-ref-1] and [`std::mem::drop`][section-fn-closures-capture-ref-2]

[section-fn-closures-capture-ref-1]: 19-std-library-types.md#section-std-box
[section-fn-closures-capture-ref-2]: https://doc.rust-lang.org/std/mem/fn.drop.html

<a id="section-fn-closures-input_parameters"></a>

<a id="section-fn-closures-input_parameters--as-input-parameters"></a>

### As input parameters

While Rust chooses how to capture variables on the fly mostly without type
annotation, this ambiguity is not allowed when writing functions. When
taking a closure as an input parameter, the closure's complete type must be
annotated using one of a few `traits`, and they're determined by what the
closure does with captured value. In order of decreasing restriction,
they are:

* `Fn`: the closure uses the captured value by reference (`&T`)
* `FnMut`: the closure uses the captured value by mutable reference (`&mut T`)
* `FnOnce`: the closure uses the captured value by value (`T`)

On a variable-by-variable basis, the compiler will capture variables in the
least restrictive manner possible.

For instance, consider a parameter annotated as `FnOnce`. This specifies
that the closure *may* capture by `&T`, `&mut T`, or `T`, but the compiler
will ultimately choose based on how the captured variables are used in the
closure.

This is because if a move is possible, then any type of borrow should also
be possible. Note that the reverse is not true. If the parameter is
annotated as `Fn`, then capturing variables by `&mut T` or `T` are not
allowed. However, `&T` is allowed.

In the following example, try swapping the usage of `Fn`, `FnMut`, and
`FnOnce` to see what happens:

```rust
// A function which takes a closure as an argument and calls it.
// <F> denotes that F is a "Generic type parameter"
fn apply<F>(f: F) where
    // The closure takes no input and returns nothing.
    F: FnOnce() {
    // ^ TODO: Try changing this to `Fn` or `FnMut`.

    f();
}

// A function which takes a closure and returns an `i32`.
fn apply_to_3<F>(f: F) -> i32 where
    // The closure takes an `i32` and returns an `i32`.
    F: Fn(i32) -> i32 {

    f(3)
}

fn main() {
    use std::mem;

    let greeting = "hello";
    // A non-copy type.
    // `to_owned` creates owned data from borrowed one
    let mut farewell = "goodbye".to_owned();

    // Capture 2 variables: `greeting` by reference and
    // `farewell` by value.
    let diary = || {
        // `greeting` is by reference: requires `Fn`.
        println!("I said {}.", greeting);

        // Mutation forces `farewell` to be captured by
        // mutable reference. Now requires `FnMut`.
        farewell.push_str("!!!");
        println!("Then I screamed {}.", farewell);
        println!("Now I can sleep. zzzzz");

        // Manually calling drop forces `farewell` to
        // be captured by value. Now requires `FnOnce`.
        mem::drop(farewell);
    };

    // Call the function which applies the closure.
    apply(diary);

    // `double` satisfies `apply_to_3`'s trait bound
    let double = |x| 2 * x;

    println!("3 doubled: {}", apply_to_3(double));
}
```

<a id="section-fn-closures-input_parameters--see-also"></a>

##### See also:

[`std::mem::drop`][section-fn-closures-input_parameters-ref-1], [`Fn`][section-fn-closures-input_parameters-ref-2], [`FnMut`][section-fn-closures-input_parameters-ref-3], [Generics][section-fn-closures-input_parameters-ref-5], [where][section-fn-closures-input_parameters-ref-6] and [`FnOnce`][section-fn-closures-input_parameters-ref-4]

[section-fn-closures-input_parameters-ref-1]: https://doc.rust-lang.org/std/mem/fn.drop.html
[section-fn-closures-input_parameters-ref-2]: https://doc.rust-lang.org/std/ops/trait.Fn.html
[section-fn-closures-input_parameters-ref-3]: https://doc.rust-lang.org/std/ops/trait.FnMut.html
[section-fn-closures-input_parameters-ref-4]: https://doc.rust-lang.org/std/ops/trait.FnOnce.html
[section-fn-closures-input_parameters-ref-5]: 14-generics.md
[section-fn-closures-input_parameters-ref-6]: 14-generics.md#section-generics-where

<a id="section-fn-closures-anonymity"></a>

<a id="section-fn-closures-anonymity--type-anonymity"></a>

### Type anonymity

Closures succinctly capture variables from enclosing scopes. Does this have
any consequences? It surely does. Observe how using a closure as a function
parameter requires [generics][section-fn-closures-anonymity-ref-1], which is necessary because of how they are
defined:

```rust
// `F` must be generic.
fn apply<F>(f: F) where
    F: FnOnce() {
    f();
}
```

When a closure is defined, the compiler implicitly creates a new
anonymous structure to store the captured variables inside, meanwhile
implementing the functionality via one of the `traits`: `Fn`, `FnMut`, or
`FnOnce` for this unknown type. This type is assigned to the variable which
is stored until calling.

Since this new type is of unknown type, any usage in a function will require
generics. However, an unbounded type parameter `<T>` would still be ambiguous
and not be allowed. Thus, bounding by one of the `traits`: `Fn`, `FnMut`, or
`FnOnce` (which it implements) is sufficient to specify its type.

```rust
// `F` must implement `Fn` for a closure which takes no
// inputs and returns nothing - exactly what is required
// for `print`.
fn apply<F>(f: F) where
    F: Fn() {
    f();
}

fn main() {
    let x = 7;

    // Capture `x` into an anonymous type and implement
    // `Fn` for it. Store it in `print`.
    let print = || println!("{}", x);

    apply(print);
}
```

<a id="section-fn-closures-anonymity--see-also"></a>

##### See also:

[A thorough analysis][section-fn-closures-anonymity-ref-5], [`Fn`][section-fn-closures-anonymity-ref-2], [`FnMut`][section-fn-closures-anonymity-ref-3],
and [`FnOnce`][section-fn-closures-anonymity-ref-4]

[section-fn-closures-anonymity-ref-1]: 14-generics.md
[section-fn-closures-anonymity-ref-2]: https://doc.rust-lang.org/std/ops/trait.Fn.html
[section-fn-closures-anonymity-ref-3]: https://doc.rust-lang.org/std/ops/trait.FnMut.html
[section-fn-closures-anonymity-ref-4]: https://doc.rust-lang.org/std/ops/trait.FnOnce.html
[section-fn-closures-anonymity-ref-5]: https://huonw.github.io/blog/2015/05/finding-closure-in-rust/

<a id="section-fn-closures-input_functions"></a>

<a id="section-fn-closures-input_functions--input-functions"></a>

### Input functions

Since closures may be used as arguments, you might wonder if the same can be said
about functions. And indeed they can! If you declare a function that takes a
closure as parameter, then any function that satisfies the trait bound of that
closure can be passed as a parameter.

```rust
// Define a function which takes a generic `F` argument
// bounded by `Fn`, and calls it
fn call_me<F: Fn()>(f: F) {
    f();
}

// Define a wrapper function satisfying the `Fn` bound
fn function() {
    println!("I'm a function!");
}

fn main() {
    // Define a closure satisfying the `Fn` bound
    let closure = || println!("I'm a closure!");

    call_me(closure);
    call_me(function);
}
```

As an additional note, the `Fn`, `FnMut`, and `FnOnce` `traits` dictate how
a closure captures variables from the enclosing scope.

<a id="section-fn-closures-input_functions--see-also"></a>

##### See also:

[`Fn`][section-fn-closures-input_functions-ref-1], [`FnMut`][section-fn-closures-input_functions-ref-2], and [`FnOnce`][section-fn-closures-input_functions-ref-3]

[section-fn-closures-input_functions-ref-1]: https://doc.rust-lang.org/std/ops/trait.Fn.html
[section-fn-closures-input_functions-ref-2]: https://doc.rust-lang.org/std/ops/trait.FnMut.html
[section-fn-closures-input_functions-ref-3]: https://doc.rust-lang.org/std/ops/trait.FnOnce.html

<a id="section-fn-closures-output_parameters"></a>

<a id="section-fn-closures-output_parameters--as-output-parameters"></a>

### As output parameters

Closures as input parameters are possible, so returning closures as
output parameters should also be possible. However, anonymous
closure types are, by definition, unknown, so we have to use
`impl Trait` to return them.

The valid traits for returning a closure are:

* `Fn`
* `FnMut`
* `FnOnce`

Beyond this, the `move` keyword must be used, which signals that all captures
occur by value. This is required because any captures by reference would be
dropped as soon as the function exited, leaving invalid references in the
closure.

```rust
fn create_fn() -> impl Fn() {
    let text = "Fn".to_owned();

    move || println!("This is a: {}", text)
}

fn create_fnmut() -> impl FnMut() {
    let text = "FnMut".to_owned();

    move || println!("This is a: {}", text)
}

fn create_fnonce() -> impl FnOnce() {
    let text = "FnOnce".to_owned();

    move || println!("This is a: {}", text)
}

fn main() {
    let fn_plain = create_fn();
    let mut fn_mut = create_fnmut();
    let fn_once = create_fnonce();

    fn_plain();
    fn_mut();
    fn_once();
}
```

<a id="section-fn-closures-output_parameters--see-also"></a>

##### See also:

[`Fn`][section-fn-closures-output_parameters-ref-1], [`FnMut`][section-fn-closures-output_parameters-ref-2], [Generics][section-fn-closures-output_parameters-ref-3] and [impl Trait][section-fn-closures-output_parameters-ref-4].

[section-fn-closures-output_parameters-ref-1]: https://doc.rust-lang.org/std/ops/trait.Fn.html
[section-fn-closures-output_parameters-ref-2]: https://doc.rust-lang.org/std/ops/trait.FnMut.html
[section-fn-closures-output_parameters-ref-3]: 14-generics.md
[section-fn-closures-output_parameters-ref-4]: 16-traits.md#section-trait-impl_trait

<a id="section-fn-closures-closure_examples"></a>

<a id="section-fn-closures-closure_examples--examples-in-std"></a>

### Examples in `std`

This section contains a few examples of using closures from the `std` library.

<a id="section-fn-closures-closure_examples-iter_any"></a>

<a id="section-fn-closures-closure_examples-iter_any--iteratorany"></a>

#### Iterator::any

`Iterator::any` is a function which when passed an iterator, will return
`true` if any element satisfies the predicate. Otherwise `false`. Its
signature:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
pub trait Iterator {
    // The type being iterated over.
    type Item;

    // `any` takes `&mut self` meaning the caller may be borrowed
    // and modified, but not consumed.
    fn any<F>(&mut self, f: F) -> bool where
        // `FnMut` meaning any captured variable may at most be
        // modified, not consumed. `Self::Item` is the closure parameter type,
        // which is determined by the iterator (e.g., `&T` for `.iter()`,
        // `T` for `.into_iter()`).
        F: FnMut(Self::Item) -> bool;
}
```

```rust
fn main() {
    let vec1 = vec![1, 2, 3];
    let vec2 = vec![4, 5, 6];

    // `iter()` for vecs yields `&i32`. Destructure to `i32`.
    println!("2 in vec1: {}", vec1.iter()     .any(|&x| x == 2));
    // `into_iter()` for vecs yields `i32`. No destructuring required.
    println!("2 in vec2: {}", vec2.into_iter().any(|x| x == 2));

    // `iter()` only borrows `vec1` and its elements, so they can be used again
    println!("vec1 len: {}", vec1.len());
    println!("First element of vec1 is: {}", vec1[0]);
    // `into_iter()` does move `vec2` and its elements, so they cannot be used again
    // println!("First element of vec2 is: {}", vec2[0]);
    // println!("vec2 len: {}", vec2.len());
    // TODO: uncomment two lines above and see compiler errors.

    let array1 = [1, 2, 3];
    let array2 = [4, 5, 6];

    // `iter()` for arrays yields `&i32`.
    println!("2 in array1: {}", array1.iter()     .any(|&x| x == 2));
    // `into_iter()` for arrays yields `i32`.
    println!("2 in array2: {}", array2.into_iter().any(|x| x == 2));
}
```

<a id="section-fn-closures-closure_examples-iter_any--see-also"></a>

###### See also:

[`std::iter::Iterator::any`][section-fn-closures-closure_examples-iter_any-ref-1]

[section-fn-closures-closure_examples-iter_any-ref-1]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.any

<a id="section-fn-closures-closure_examples-iter_find"></a>

<a id="section-fn-closures-closure_examples-iter_find--searching-through-iterators"></a>

#### Searching through iterators

`Iterator::find` is a function which iterates over an iterator and searches for the
first value which satisfies some condition. If none of the values satisfy the
condition, it returns `None`. Its signature:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
pub trait Iterator {
    // The type being iterated over.
    type Item;

    // `find` takes `&mut self` meaning the caller may be borrowed
    // and modified, but not consumed.
    fn find<P>(&mut self, predicate: P) -> Option<Self::Item> where
        // `FnMut` meaning any captured variable may at most be
        // modified, not consumed. `&Self::Item` states it takes
        // arguments to the closure by reference.
        P: FnMut(&Self::Item) -> bool;
}
```

```rust
fn main() {
    let vec1 = vec![1, 2, 3];
    let vec2 = vec![4, 5, 6];

    // `vec1.iter()` yields `&i32`.
    let mut iter = vec1.iter();
    // `vec2.into_iter()` yields `i32`.
    let mut into_iter = vec2.into_iter();

    // `iter()` yields `&i32`, and `find` passes `&Item` to the predicate.
    // Since `Item = &i32`, the closure argument has type `&&i32`,
    // which we pattern-match to dereference down to `i32`.
    println!("Find 2 in vec1: {:?}", iter.find(|&&x| x == 2));
    
    // `into_iter()` yields `i32`, and `find` passes `&Item` to the predicate.
    // Since `Item = i32`, the closure argument has type `&i32`,
    // which we pattern-match to dereference down to `i32`.
    println!("Find 2 in vec2: {:?}", into_iter.find(|&x| x == 2));

    let array1 = [1, 2, 3];
    let array2 = [4, 5, 6];

    // `array1.iter()` yields `&i32`, and `find` passes `&Item` to the
    // predicate. Since `Item = &i32`, the closure argument has type `&&i32`.
    println!("Find 2 in array1: {:?}", array1.iter().find(|&&x| x == 2));
    // `array2.into_iter()` yields `i32` (since Rust 2021 edition), and
    // `find` passes `&Item` to the predicate. Since `Item = i32`, the
    // closure argument has type `&i32`.
    println!("Find 2 in array2: {:?}", array2.into_iter().find(|&x| x == 2));
}
```

`Iterator::find` gives you a reference to the item. But if you want the _index_ of the
item, use `Iterator::position`.

```rust
fn main() {
    let vec = vec![1, 9, 3, 3, 13, 2];

    // `position` passes the iterator’s `Item` by value to the predicate.
    // `vec.iter()` yields `&i32`, so the predicate receives `&i32`,
    // which we pattern-match to dereference to `i32`.
    let index_of_first_even_number = vec.iter().position(|&x| x % 2 == 0);
    assert_eq!(index_of_first_even_number, Some(5));

    // `vec.into_iter()` yields `i32`, so the predicate receives `i32` directly.
    let index_of_first_negative_number = vec.into_iter().position(|x| x < 0);
    assert_eq!(index_of_first_negative_number, None);
}
```

<a id="section-fn-closures-closure_examples-iter_find--see-also"></a>

###### See also:

[`std::iter::Iterator::find`][section-fn-closures-closure_examples-iter_find-ref-1]

[`std::iter::Iterator::find_map`][section-fn-closures-closure_examples-iter_find-ref-2]

[`std::iter::Iterator::position`][section-fn-closures-closure_examples-iter_find-ref-3]

[`std::iter::Iterator::rposition`][section-fn-closures-closure_examples-iter_find-ref-4]

[section-fn-closures-closure_examples-iter_find-ref-1]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.find
[section-fn-closures-closure_examples-iter_find-ref-2]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.find_map
[section-fn-closures-closure_examples-iter_find-ref-3]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.position
[section-fn-closures-closure_examples-iter_find-ref-4]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.rposition

<a id="section-fn-hof"></a>

<a id="section-fn-hof--higher-order-functions"></a>

## Higher Order Functions

Rust provides Higher Order Functions (HOF). These are functions that
take one or more functions and/or produce a more useful function. HOFs
and lazy iterators give Rust its functional flavor.

```rust
fn is_odd(n: u32) -> bool {
    n % 2 == 1
}

fn main() {
    println!("Find the sum of all the numbers with odd squares under 1000");
    let upper = 1000;

    // Imperative approach
    // Declare accumulator variable
    let mut acc = 0;
    // Iterate: 0, 1, 2, ... to infinity
    for n in 0.. {
        // Square the number
        let n_squared = n * n;

        if n_squared >= upper {
            // Break loop if exceeded the upper limit
            break;
        } else if is_odd(n_squared) {
            // Accumulate value, if it's odd
            acc += n;
        }
    }
    println!("imperative style: {}", acc);

    // Functional approach
    let sum: u32 =
        (0..).take_while(|&n| n * n < upper) // Below upper limit
             .filter(|&n| is_odd(n * n))     // That are odd
             .sum();                         // Sum them
    println!("functional style: {}", sum);
}
```

[Option][section-fn-hof-ref-1]
and
[Iterator][section-fn-hof-ref-2]
implement their fair share of HOFs.

[section-fn-hof-ref-1]: https://doc.rust-lang.org/core/option/enum.Option.html
[section-fn-hof-ref-2]: https://doc.rust-lang.org/core/iter/trait.Iterator.html

<a id="section-fn-diverging"></a>

<a id="section-fn-diverging--diverging-functions"></a>

## Diverging functions

Diverging functions never return. They are marked using `!`, which is an empty type.

```rust
fn foo() -> ! {
    panic!("This call never returns.");
}
```

As opposed to all the other types, this one cannot be instantiated, because the
set of all possible values this type can have is empty. Note that, it is
different from the `()` type, which has exactly one possible value.

For example, this function returns as usual, although there is no information
in the return value.

```rust
fn some_fn() {
    ()
}

fn main() {
    let _a: () = some_fn();
    println!("This function returns and you can see this line.");
}
```

As opposed to this function, which will never return the control back to the caller.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
#![feature(never_type)]

fn main() {
    let x: ! = panic!("This call never returns.");
    println!("You will never see this line!");
}
```

Although this might seem like an abstract concept, it is actually very useful and
often handy. The main advantage of this type is that it can be cast to any other
type, making it versatile in situations where an exact type is required, such as
in match branches. This flexibility allows us to write code like this:

```rust
fn main() {
    fn sum_odd_numbers(up_to: u32) -> u32 {
        let mut acc = 0;
        for i in 0..up_to {
            // Notice that the return type of this match expression must be u32
            // because of the type of the "addition" variable.
            let addition: u32 = match i%2 == 1 {
                // The "i" variable is of type u32, which is perfectly fine.
                true => i,
                // On the other hand, the "continue" expression does not return
                // u32, but it is still fine, because it never returns and therefore
                // does not violate the type requirements of the match expression.
                false => continue,
            };
            acc += addition;
        }
        acc
    }
    println!("Sum of odd numbers up to 9 (excluding): {}", sum_odd_numbers(9));
}
```

It is also the return type of functions that loop forever (e.g. `loop {}`) like
network servers or functions that terminate the process (e.g. `exit()`).
