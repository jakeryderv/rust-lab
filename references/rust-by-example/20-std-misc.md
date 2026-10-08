<a id="section-std_misc"></a>

<a id="section-std_misc--std-misc"></a>

# Std misc

[Chapter index](SUMMARY.md)

**In this chapter**

- [Threads](#section-std_misc-threads)
  - [Testcase: map-reduce](#section-std_misc-threads-testcase_mapreduce)
- [Channels](#section-std_misc-channels)
- [Path](#section-std_misc-path)
- [File I/O](#section-std_misc-file)
  - [`open`](#section-std_misc-file-open)
  - [`create`](#section-std_misc-file-create)
  - [`read_lines`](#section-std_misc-file-read_lines)
- [Child processes](#section-std_misc-process)
  - [Pipes](#section-std_misc-process-pipe)
  - [Wait](#section-std_misc-process-wait)
- [Filesystem Operations](#section-std_misc-fs)
- [Program arguments](#section-std_misc-arg)
  - [Argument parsing](#section-std_misc-arg-matching)
- [Foreign Function Interface](#section-std_misc-ffi)


Many other types are provided by the std library to support
things such as:

* Threads
* Channels
* File I/O

These expand beyond what the [primitives][section-std_misc-ref-1] provide.

<a id="section-std_misc--see-also"></a>

### See also:

[primitives][section-std_misc-ref-1] and [the std library][section-std_misc-ref-2]

[section-std_misc-ref-1]: 02-primitives.md
[section-std_misc-ref-2]: https://doc.rust-lang.org/std/

<a id="section-std_misc-threads"></a>

<a id="section-std_misc-threads--threads"></a>

## Threads

Rust provides a mechanism for spawning native OS threads via the `spawn`
function, the argument of this function is a moving closure.

```rust
use std::thread;

const NTHREADS: u32 = 10;

// This is the `main` thread
fn main() {
    // Make a vector to hold the children which are spawned.
    let mut children = vec![];

    for i in 0..NTHREADS {
        // Spin up another thread
        children.push(thread::spawn(move || {
            println!("this is thread number {}", i);
        }));
    }

    for child in children {
        // Wait for the thread to finish. Returns a result.
        let _ = child.join();
    }
}
```

These threads will be scheduled by the OS.

<a id="section-std_misc-threads-testcase_mapreduce"></a>

<a id="section-std_misc-threads-testcase_mapreduce--testcase-map-reduce"></a>

### Testcase: map-reduce

Rust makes it very easy to parallelize data processing, without many of the headaches traditionally associated with such an attempt.

The standard library provides great threading primitives out of the box.
These, combined with Rust's concept of Ownership and aliasing rules, automatically prevent
data races.

The aliasing rules (one writable reference XOR many readable references) automatically prevent
you from manipulating state that is visible to other threads. (Where synchronization is needed,
there are synchronization
primitives like `Mutex`es or `Channel`s.)

In this example, we will calculate the sum of all digits in a block of numbers.
We will do this by parcelling out chunks of the block into different threads. Each thread will sum
its tiny block of digits, and subsequently we will sum the intermediate sums produced by each
thread.

Note that, although we're passing references across thread boundaries, Rust understands that we're
only passing read-only references, and that thus no unsafety or data races can occur. Also because
the references we're passing have `'static` lifetimes, Rust understands that our data won't be
destroyed while these threads are still running. (When you need to share non-`static` data between
threads, you can use a smart pointer like `Arc` to keep the data alive and avoid non-`static`
lifetimes.)

```rust
use std::thread;

// This is the `main` thread
fn main() {

    // This is our data to process.
    // We will calculate the sum of all digits via a threaded map-reduce algorithm.
    // Each whitespace separated chunk will be handled in a different thread.
    //
    // TODO: see what happens to the output if you insert spaces!
    let data = "86967897737416471853297327050364959
11861322575564723963297542624962850
70856234701860851907960690014725639
38397966707106094172783238747669219
52380795257888236525459303330302837
58495327135744041048897885734297812
69920216438980873548808413720956532
16278424637452589860345374828574668";

    // Make a vector to hold the child-threads which we will spawn.
    let mut children = vec![];

    /*************************************************************************
     * "Map" phase
     *
     * Divide our data into segments, and apply initial processing
     ************************************************************************/

    // split our data into segments for individual calculation
    // each chunk will be a reference (&str) into the actual data
    let chunked_data = data.split_whitespace();

    // Iterate over the data segments.
    // .enumerate() adds the current loop index to whatever is iterated
    // the resulting tuple "(index, element)" is then immediately
    // "destructured" into two variables, "i" and "data_segment" with a
    // "destructuring assignment"
    for (i, data_segment) in chunked_data.enumerate() {
        println!("data segment {} is \"{}\"", i, data_segment);

        // Process each data segment in a separate thread
        //
        // spawn() returns a handle to the new thread,
        // which we MUST keep to access the returned value
        //
        // 'move || -> u32' is syntax for a closure that:
        // * takes no arguments ('||')
        // * takes ownership of its captured variables ('move') and
        // * returns an unsigned 32-bit integer ('-> u32')
        //
        // Rust is smart enough to infer the '-> u32' from
        // the closure itself so we could have left that out.
        //
        // TODO: try removing the 'move' and see what happens
        children.push(thread::spawn(move || -> u32 {
            // Calculate the intermediate sum of this segment:
            let result = data_segment
                        // iterate over the characters of our segment..
                        .chars()
                        // .. convert text-characters to their number value..
                        .map(|c| c.to_digit(10).expect("should be a digit"))
                        // .. and sum the resulting iterator of numbers
                        .sum();

            // println! locks stdout, so no text-interleaving occurs
            println!("processed segment {}, result={}", i, result);

            // "return" not needed, because Rust is an "expression language", the
            // last evaluated expression in each block is automatically its value.
            result

        }));
    }


    /*************************************************************************
     * "Reduce" phase
     *
     * Collect our intermediate results, and combine them into a final result
     ************************************************************************/

    // combine each thread's intermediate results into a single final sum.
    //
    // we use the "turbofish" ::<> to provide sum() with a type hint.
    //
    // TODO: try without the turbofish, by instead explicitly
    // specifying the type of final_result
    let final_result = children.into_iter().map(|c| c.join().unwrap()).sum::<u32>();

    println!("Final sum result: {}", final_result);
}
```

<a id="section-std_misc-threads-testcase_mapreduce--assignments"></a>

##### Assignments

It is not wise to let our number of threads depend on user inputted data.
What if the user decides to insert a lot of spaces? Do we _really_ want to spawn 2,000 threads?
Modify the program so that the data is always chunked into a limited number of chunks,
defined by a static constant at the beginning of the program.

<a id="section-std_misc-threads-testcase_mapreduce--see-also"></a>

##### See also:

* [Threads][section-std_misc-threads-testcase_mapreduce-ref-1]
* [vectors][section-std_misc-threads-testcase_mapreduce-ref-2] and [iterators][section-std_misc-threads-testcase_mapreduce-ref-3]
* [closures][section-std_misc-threads-testcase_mapreduce-ref-5], [move][section-std_misc-threads-testcase_mapreduce-ref-6] semantics and [`move` closures][section-std_misc-threads-testcase_mapreduce-ref-7]
* [destructuring][section-std_misc-threads-testcase_mapreduce-ref-4] assignments
* [turbofish notation][section-std_misc-threads-testcase_mapreduce-ref-8] to help type inference
* [unwrap vs. expect][section-std_misc-threads-testcase_mapreduce-ref-9]
* [enumerate][section-std_misc-threads-testcase_mapreduce-ref-10]

[section-std_misc-threads-testcase_mapreduce-ref-1]: #section-std_misc-threads
[section-std_misc-threads-testcase_mapreduce-ref-2]: 19-std-library-types.md#section-std-vec
[section-std_misc-threads-testcase_mapreduce-ref-3]: 16-traits.md#section-trait-iter
[section-std_misc-threads-testcase_mapreduce-ref-4]: https://doc.rust-lang.org/book/ch18-03-pattern-syntax.html#destructuring-to-break-apart-values
[section-std_misc-threads-testcase_mapreduce-ref-5]: 09-functions.md#section-fn-closures
[section-std_misc-threads-testcase_mapreduce-ref-6]: 15-scoping-rules.md#section-scope-move
[section-std_misc-threads-testcase_mapreduce-ref-7]: https://doc.rust-lang.org/book/ch13-01-closures.html#closures-can-capture-their-environment
[section-std_misc-threads-testcase_mapreduce-ref-8]: https://doc.rust-lang.org/book/appendix-02-operators.html?highlight=turbofish
[section-std_misc-threads-testcase_mapreduce-ref-9]: 18-error-handling.md#section-error-option_unwrap
[section-std_misc-threads-testcase_mapreduce-ref-10]: https://doc.rust-lang.org/book/loops.html#enumerate

<a id="section-std_misc-channels"></a>

<a id="section-std_misc-channels--channels"></a>

## Channels

Rust provides asynchronous `channels` for communication between threads. Channels
allow a unidirectional flow of information between two end-points: the
`Sender` and the `Receiver`.

```rust
use std::sync::mpsc::{Sender, Receiver};
use std::sync::mpsc;
use std::thread;

static NTHREADS: i32 = 3;

fn main() {
    // Channels have two endpoints: the `Sender<T>` and the `Receiver<T>`,
    // where `T` is the type of the message to be transferred
    // (type annotation is superfluous)
    let (tx, rx): (Sender<i32>, Receiver<i32>) = mpsc::channel();
    let mut children = Vec::new();

    for id in 0..NTHREADS {
        // The sender endpoint can be copied
        let thread_tx = tx.clone();

        // Each thread will send its id via the channel
        let child = thread::spawn(move || {
            // The thread takes ownership over `thread_tx`
            // Each thread queues a message in the channel
            thread_tx.send(id).unwrap();

            // Sending is a non-blocking operation, the thread will continue
            // immediately after sending its message
            println!("thread {} finished", id);
        });

        children.push(child);
    }

    // Here, all the messages are collected
    let mut ids = Vec::with_capacity(NTHREADS as usize);
    for _ in 0..NTHREADS {
        // The `recv` method picks a message from the channel
        // `recv` will block the current thread if there are no messages available
        ids.push(rx.recv());
    }

    // Wait for the threads to complete any remaining work
    for child in children {
        child.join().expect("oops! the child thread panicked");
    }

    // Show the order in which the messages were sent
    println!("{:?}", ids);
}
```

<a id="section-std_misc-path"></a>

<a id="section-std_misc-path--path"></a>

## Path

The `Path` type represents file paths in the underlying filesystem. Across all
platforms there is a single `std::path::Path` that abstracts over
platform-specific path semantics and separators. Bring it into scope with
`use std::path::Path;` when needed.

A `Path` can be created from an `OsStr`, and provides several methods to get
information from the file/directory the path points to.

A `Path` is immutable. The owned version of `Path` is `PathBuf`. The relation
between `Path` and `PathBuf` is similar to that of `str` and `String`:
a `PathBuf` can be mutated in-place, and can be dereferenced to a `Path`.

Note that a `Path` is *not* internally represented as an UTF-8 string, but
instead is stored as an `OsString`. Therefore, converting a `Path` to a `&str`
is *not* free and may fail (an `Option` is returned). However, a `Path` can be
freely converted to an `OsString` or `&OsStr` using `into_os_string` and
`as_os_str`, respectively.

```rust
use std::path::Path;

fn main() {
    // Create a `Path` from an `&'static str`
    let path = Path::new(".");

    // The `display` method returns a `Display`able structure
    let _display = path.display();

    // `join` merges a path with a byte container using the OS specific
    // separator, and returns a `PathBuf`
    let mut new_path = path.join("a").join("b");

    // `push` extends the `PathBuf` with a `&Path`
    new_path.push("c");
    new_path.push("myfile.tar.gz");

    // `set_file_name` updates the file name of the `PathBuf`
    new_path.set_file_name("package.tgz");

    // Convert the `PathBuf` into a string slice
    match new_path.to_str() {
        None => panic!("new path is not a valid UTF-8 sequence"),
        Some(s) => println!("new path is {}", s),
    }
}
```

Be sure to check other `Path` methods and the `Metadata` struct.

<a id="section-std_misc-path--see-also"></a>

#### See also:

[OsStr][section-std_misc-path-ref-1] and [Metadata][section-std_misc-path-ref-2].

[section-std_misc-path-ref-1]: https://doc.rust-lang.org/std/ffi/struct.OsStr.html
[section-std_misc-path-ref-2]: https://doc.rust-lang.org/std/fs/struct.Metadata.html

<a id="section-std_misc-file"></a>

<a id="section-std_misc-file--file-io"></a>

## File I/O

The `File` struct represents a file that has been opened (it wraps a file
descriptor), and gives read and/or write access to the underlying file.

Since many things can go wrong when doing file I/O, all the `File` methods
return the `io::Result<T>` type, which is an alias for `Result<T, io::Error>`.

This makes the failure of all I/O operations *explicit*. Thanks to this, the
programmer can see all the failure paths, and is encouraged to handle them in
a proactive manner.

<a id="section-std_misc-file-open"></a>

<a id="section-std_misc-file-open--open"></a>

### `open`

The `open` function can be used to open a file in read-only mode.

A `File` owns a resource, the file descriptor and takes care of closing the
file when it is `drop`ed.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

fn main() {
    // Create a path to the desired file
    let path = Path::new("hello.txt");
    let display = path.display();

    // Open the path in read-only mode, returns `io::Result<File>`
    let mut file = match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", display, why),
        Ok(file) => file,
    };

    // Read the file contents into a string, returns `io::Result<usize>`
    let mut s = String::new();
    match file.read_to_string(&mut s) {
        Err(why) => panic!("couldn't read {}: {}", display, why),
        Ok(_) => print!("{} contains:\n{}", display, s),
    }

    // `file` goes out of scope, and the "hello.txt" file gets closed
}
```

Here's the expected successful output:

```shell
$ echo "Hello World!" > hello.txt
$ rustc open.rs && ./open
hello.txt contains:
Hello World!
```

(You are encouraged to test the previous example under different failure
conditions: `hello.txt` doesn't exist, or `hello.txt` is not readable,
etc.)

<a id="section-std_misc-file-create"></a>

<a id="section-std_misc-file-create--create"></a>

### `create`

The `create` function opens a file in write-only mode. If the file
already existed, the old content is destroyed. Otherwise, a new file is
created.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
static LOREM_IPSUM: &str =
    "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
";

use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

fn main() {
    let path = Path::new("lorem_ipsum.txt");
    let display = path.display();

    // Open a file in write-only mode, returns `io::Result<File>`
    let mut file = match File::create(&path) {
        Err(why) => panic!("couldn't create {}: {}", display, why),
        Ok(file) => file,
    };

    // Write the `LOREM_IPSUM` string to `file`, returns `io::Result<()>`
    match file.write_all(LOREM_IPSUM.as_bytes()) {
        Err(why) => panic!("couldn't write to {}: {}", display, why),
        Ok(_) => println!("successfully wrote to {}", display),
    }
}
```

Here's the expected successful output:

```shell
$ rustc create.rs && ./create
successfully wrote to lorem_ipsum.txt

$ cat lorem_ipsum.txt
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```

(As in the previous example, you are encouraged to test this example under
failure conditions.)

The [`OpenOptions`][section-std_misc-file-create-ref-1] struct can be used to configure how a file is opened.

[section-std_misc-file-create-ref-1]: https://doc.rust-lang.org/std/fs/struct.OpenOptions.html

<a id="section-std_misc-file-read_lines"></a>

<a id="section-std_misc-file-read_lines--read_lines"></a>

### `read_lines`

<a id="section-std_misc-file-read_lines--a-naive-approach"></a>

#### A naive approach

This might be a reasonable first attempt for a beginner's first
implementation for reading lines from a file.

> **Example note:** Upstream compiles this example without running it.

```rust
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(line.to_string())
    }

    result
}
```

Since the method `lines()` returns an iterator over the lines in the file,
we can also perform a map inline and collect the results, yielding a more
concise and fluent expression.

> **Example note:** Upstream compiles this example without running it.

```rust
use std::fs::read_to_string;

fn read_lines(filename: &str) -> Vec<String> {
    read_to_string(filename)
        .unwrap()  // panic on possible file-reading errors
        .lines()  // split the string into an iterator of string slices
        .map(String::from)  // make each slice into a string
        .collect()  // gather them together into a vector
}
```

Note that in both examples above, we must convert the `&str` reference
returned from `lines()` to the owned type `String`, using `.to_string()`
and `String::from` respectively.

<a id="section-std_misc-file-read_lines--a-more-efficient-approach"></a>

#### A more efficient approach

Here we pass ownership of the open `File` to a `BufReader` struct. `BufReader` uses an internal
buffer to reduce intermediate allocations.

We also update `read_lines` to return an iterator instead of allocating new
`String` objects in memory for each line.

> **Example note:** Upstream compiles this example without running it.

```rust
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    // File hosts.txt must exist in the current path
    if let Ok(lines) = read_lines("./hosts.txt") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines.map_while(Result::ok) {
            println!("{}", line);
        }
    }
}

// The output is wrapped in a Result to allow matching on errors.
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
```

Running this program simply prints the lines individually.

```shell
$ echo -e "127.0.0.1\n192.168.0.1\n" > hosts.txt
$ rustc read_lines.rs && ./read_lines
127.0.0.1
192.168.0.1
```

(Note that since `File::open` expects a generic `AsRef<Path>` as argument, we define our
generic `read_lines()` method with the same generic constraint, using the `where` keyword.)

This process is more efficient than creating a `String` in memory with all of the file's
contents. This can especially cause performance issues when working with larger files.

<a id="section-std_misc-process"></a>

<a id="section-std_misc-process--child-processes"></a>

## Child processes

The `process::Output` struct represents the output of a finished child process,
and the `process::Command` struct is a process builder.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
use std::process::Command;

fn main() {
    let output = Command::new("rustc")
        .arg("--version")
        .output().unwrap_or_else(|e| {
            panic!("failed to execute process: {}", e)
    });

    if output.status.success() {
        let s = String::from_utf8_lossy(&output.stdout);

        print!("rustc succeeded and stdout was:\n{}", s);
    } else {
        let s = String::from_utf8_lossy(&output.stderr);

        print!("rustc failed and stderr was:\n{}", s);
    }
}
```

(You are encouraged to try the previous example with an incorrect flag passed
to `rustc`)

<a id="section-std_misc-process-pipe"></a>

<a id="section-std_misc-process-pipe--pipes"></a>

### Pipes

The `std::process::Child` struct represents a child process, and exposes the
`stdin`, `stdout` and `stderr` handles for interaction with the underlying
process via pipes.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
use std::io::prelude::*;
use std::process::{Command, Stdio};

static PANGRAM: &'static str =
"the quick brown fox jumps over the lazy dog\n";

fn main() {
    // Spawn the `wc` command
    let mut cmd = if cfg!(target_family = "windows") {
        let mut cmd = Command::new("powershell");
        cmd.arg("-Command").arg("$input | Measure-Object -Line -Word -Character");
        cmd
    } else {
        Command::new("wc")
    };
    let process = match cmd
                                .stdin(Stdio::piped())
                                .stdout(Stdio::piped())
                                .spawn() {
        Err(why) => panic!("couldn't spawn wc: {}", why),
        Ok(process) => process,
    };

    // Write a string to the `stdin` of `wc`.
    //
    // `stdin` has type `Option<ChildStdin>`, but since we know this instance
    // must have one, we can directly `unwrap` it.
    match process.stdin.unwrap().write_all(PANGRAM.as_bytes()) {
        Err(why) => panic!("couldn't write to wc stdin: {}", why),
        Ok(_) => println!("sent pangram to wc"),
    }

    // Because `stdin` does not live after the above calls, it is `drop`ed,
    // and the pipe is closed.
    //
    // This is very important, otherwise `wc` wouldn't start processing the
    // input we just sent.

    // The `stdout` field also has type `Option<ChildStdout>` so must be unwrapped.
    let mut s = String::new();
    match process.stdout.unwrap().read_to_string(&mut s) {
        Err(why) => panic!("couldn't read wc stdout: {}", why),
        Ok(_) => print!("wc responded with:\n{}", s),
    }
}
```

<a id="section-std_misc-process-wait"></a>

<a id="section-std_misc-process-wait--wait"></a>

### Wait

If you'd like to wait for a `process::Child` to finish, you must call
`Child::wait`, which will return a `process::ExitStatus`.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
use std::process::Command;

fn main() {
    let mut child = Command::new("sleep").arg("5").spawn().unwrap();
    let _result = child.wait().unwrap();

    println!("reached end of main");
}
```

```bash
$ rustc wait.rs && ./wait
# `wait` keeps running for 5 seconds until the `sleep 5` command finishes
reached end of main
```

<a id="section-std_misc-fs"></a>

<a id="section-std_misc-fs--filesystem-operations"></a>

## Filesystem Operations

The `std::fs` module contains several functions that deal with the filesystem.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
use std::fs;
use std::fs::{File, OpenOptions};
use std::io;
use std::io::prelude::*;
#[cfg(target_family = "unix")]
use std::os::unix;
#[cfg(target_family = "windows")]
use std::os::windows;
use std::path::Path;

// A simple implementation of `% cat path`
fn cat(path: &Path) -> io::Result<String> {
    let mut f = File::open(path)?;
    let mut s = String::new();
    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
}

// A simple implementation of `% echo s > path`
fn echo(s: &str, path: &Path) -> io::Result<()> {
    let mut f = File::create(path)?;

    f.write_all(s.as_bytes())
}

// A simple implementation of `% touch path` (ignores existing files)
fn touch(path: &Path) -> io::Result<()> {
    match OpenOptions::new().create(true).write(true).open(path) {
        Ok(_) => Ok(()),
        Err(e) => Err(e),
    }
}

fn main() {
    println!("`mkdir a`");
    // Create a directory, returns `io::Result<()>`
    match fs::create_dir("a") {
        Err(why) => println!("! {:?}", why.kind()),
        Ok(_) => {},
    }

    println!("`echo hello > a/b.txt`");
    // The previous match can be simplified using the `unwrap_or_else` method
    echo("hello", &Path::new("a/b.txt")).unwrap_or_else(|why| {
        println!("! {:?}", why.kind());
    });

    println!("`mkdir -p a/c/d`");
    // Recursively create a directory, returns `io::Result<()>`
    fs::create_dir_all("a/c/d").unwrap_or_else(|why| {
        println!("! {:?}", why.kind());
    });

    println!("`touch a/c/e.txt`");
    touch(&Path::new("a/c/e.txt")).unwrap_or_else(|why| {
        println!("! {:?}", why.kind());
    });

    println!("`ln -s ../b.txt a/c/b.txt`");
    // Create a symbolic link, returns `io::Result<()>`
    #[cfg(target_family = "unix")] {
        unix::fs::symlink("../b.txt", "a/c/b.txt").unwrap_or_else(|why| {
            println!("! {:?}", why.kind());
        });
    }
    #[cfg(target_family = "windows")] {
        windows::fs::symlink_file("../b.txt", "a/c/b.txt").unwrap_or_else(|why| {
            println!("! {:?}", why.to_string());
        });
    }

    println!("`cat a/c/b.txt`");
    match cat(&Path::new("a/c/b.txt")) {
        Err(why) => println!("! {:?}", why.kind()),
        Ok(s) => println!("> {}", s),
    }

    println!("`ls a`");
    // Read the contents of a directory, returns `io::Result<Vec<Path>>`
    match fs::read_dir("a") {
        Err(why) => println!("! {:?}", why.kind()),
        Ok(paths) => for path in paths {
            println!("> {:?}", path.unwrap().path());
        },
    }

    println!("`rm a/c/e.txt`");
    // Remove a file, returns `io::Result<()>`
    fs::remove_file("a/c/e.txt").unwrap_or_else(|why| {
        println!("! {:?}", why.kind());
    });

    println!("`rmdir a/c/d`");
    // Remove an empty directory, returns `io::Result<()>`
    fs::remove_dir("a/c/d").unwrap_or_else(|why| {
        println!("! {:?}", why.kind());
    });
}
```

Here's the expected successful output:

```shell
$ rustc fs.rs && ./fs
`mkdir a`
`echo hello > a/b.txt`
`mkdir -p a/c/d`
`touch a/c/e.txt`
`ln -s ../b.txt a/c/b.txt`
`cat a/c/b.txt`
> hello
`ls a`
> "a/b.txt"
> "a/c"
`rm a/c/e.txt`
`rmdir a/c/d`
```

And the final state of the `a` directory is:

```shell
$ tree a
a
|-- b.txt
`-- c
    `-- b.txt -> ../b.txt

1 directory, 2 files
```

An alternative way to define the function `cat` is with `?` notation:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn cat(path: &Path) -> io::Result<String> {
    let mut f = File::open(path)?;
    let mut s = String::new();
    f.read_to_string(&mut s)?;
    Ok(s)
}
```

<a id="section-std_misc-fs--see-also"></a>

#### See also:

[`cfg!`][section-std_misc-fs-ref-1]

[section-std_misc-fs-ref-1]: 13-attributes.md#section-attribute-cfg

<a id="section-std_misc-arg"></a>

<a id="section-std_misc-arg--program-arguments"></a>

## Program arguments

<a id="section-std_misc-arg--standard-library"></a>

### Standard Library

The command line arguments can be accessed using `std::env::args`, which
returns an iterator that yields a `String` for each argument:

```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    // The first argument is the path that was used to call the program.
    println!("My path is {}.", args[0]);

    // The rest of the arguments are the passed command line parameters.
    // Call the program like this:
    //   $ ./args arg1 arg2
    println!("I got {:?} arguments: {:?}.", args.len() - 1, &args[1..]);
}
```

```shell
$ ./args 1 2 3
My path is ./args.
I got 3 arguments: ["1", "2", "3"].
```

<a id="section-std_misc-arg--crates"></a>

### Crates

Alternatively, there are numerous crates that can provide extra functionality
when creating command-line applications. One of the more popular command line
argument crates being [`clap`][section-std_misc-arg-ref-1].

[section-std_misc-arg-ref-1]: https://rust-cli.github.io/book/tutorial/cli-args.html#parsing-cli-arguments-with-clap

<a id="section-std_misc-arg-matching"></a>

<a id="section-std_misc-arg-matching--argument-parsing"></a>

### Argument parsing

Matching can be used to parse simple arguments:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
use std::env;

fn increase(number: i32) {
    println!("{}", number + 1);
}

fn decrease(number: i32) {
    println!("{}", number - 1);
}

fn help() {
    println!("usage:
match_args <string>
    Check whether given string is the answer.
match_args {{increase|decrease}} <integer>
    Increase or decrease given integer by one.");
}

fn main() {
    let args: Vec<String> = env::args().collect();

    match args.len() {
        // no arguments passed
        1 => {
            println!("My name is 'match_args'. Try passing some arguments!");
        },
        // one argument passed
        2 => {
            match args[1].parse() {
                Ok(42) => println!("This is the answer!"),
                _ => println!("This is not the answer."),
            }
        },
        // one command and one argument passed
        3 => {
            let cmd = &args[1];
            let num = &args[2];
            // parse the number
            let number: i32 = match num.parse() {
                Ok(n) => {
                    n
                },
                Err(_) => {
                    eprintln!("error: second argument not an integer");
                    help();
                    return;
                },
            };
            // parse the command
            match &cmd[..] {
                "increase" => increase(number),
                "decrease" => decrease(number),
                _ => {
                    eprintln!("error: invalid command");
                    help();
                },
            }
        },
        // all the other cases
        _ => {
            // show a help message
            help();
        }
    }
}
```

If you named your program `match_args.rs` and compile it like this `rustc
match_args.rs`, you can execute it as follows:

```shell
$ ./match_args Rust
This is not the answer.
$ ./match_args 42
This is the answer!
$ ./match_args do something
error: second argument not an integer
usage:
match_args <string>
    Check whether given string is the answer.
match_args {increase|decrease} <integer>
    Increase or decrease given integer by one.
$ ./match_args do 42
error: invalid command
usage:
match_args <string>
    Check whether given string is the answer.
match_args {increase|decrease} <integer>
    Increase or decrease given integer by one.
$ ./match_args increase 42
43
```

<a id="section-std_misc-ffi"></a>

<a id="section-std_misc-ffi--foreign-function-interface"></a>

## Foreign Function Interface

Rust provides a Foreign Function Interface (FFI) to C libraries. Foreign
functions must be declared inside an `extern` block annotated with a `#[link]`
attribute containing the name of the foreign library.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
use std::fmt;

// this extern block links to the libm library
#[cfg(target_family = "windows")]
#[link(name = "msvcrt")]
extern {
    // this is a foreign function
    // that computes the square root of a single precision complex number
    fn csqrtf(z: Complex) -> Complex;

    fn ccosf(z: Complex) -> Complex;
}
#[cfg(target_family = "unix")]
#[link(name = "m")]
extern {
    // this is a foreign function
    // that computes the square root of a single precision complex number
    fn csqrtf(z: Complex) -> Complex;

    fn ccosf(z: Complex) -> Complex;
}

// Since calling foreign functions is considered unsafe,
// it's common to write safe wrappers around them.
fn cos(z: Complex) -> Complex {
    unsafe { ccosf(z) }
}

fn main() {
    // z = -1 + 0i
    let z = Complex { re: -1., im: 0. };

    // calling a foreign function is an unsafe operation
    let z_sqrt = unsafe { csqrtf(z) };

    println!("the square root of {:?} is {:?}", z, z_sqrt);

    // calling safe API wrapped around unsafe operation
    println!("cos({:?}) = {:?}", z, cos(z));
}

// Minimal implementation of single precision complex numbers
#[repr(C)]
#[derive(Clone, Copy)]
struct Complex {
    re: f32,
    im: f32,
}

impl fmt::Debug for Complex {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if self.im < 0. {
            write!(f, "{}-{}i", self.re, -self.im)
        } else {
            write!(f, "{}+{}i", self.re, self.im)
        }
    }
}
```
