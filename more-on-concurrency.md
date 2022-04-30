# About this document

This document is the initial version of this workshops' primer on concurrency in Python. There are some additional details in here that didn't make it into the slides, but overall this is very optional reading.

## Intro to Concurrency

Parallelism is the technique of "performing multiple operations at the same time". There are two main techiques for achieving parallelism:
- [Multiprocessing](https://en.wikipedia.org/wiki/Multiprocessing), spawning more than one process, which the OS can distribute to more than one CPU core. Processes have their own memory space, and thus are less concerned with synchronization primitives (https://stackoverflow.com/a/3046201). Python provides this functionality in the `multiprocessing` module.
- [Multithreading](https://en.wikipedia.org/wiki/Multithreading_(computer_architecture)), spawning more than one threads, which may achieve parallelism if the threads are distributed to different cores by the operating system. This isn't possible on a single-core system where there can only be one thread being worked on at a given time. Threads do not have their own memory space and, in the case of Python, actually are restricted to the original process' core (https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python#comment40131752_3046201). Thus, Python's thread-level paralellism does not achieve parallelism in the strict sense we establish here. Python provides this functionality in the `threading` module.

Concurrency is the technique of switching between multiple operations, composing "independently executing computations". Examples of this are:
- Multithreading, splicing independent tasks together in the most literal sense. Task switching is achieved using preemption, with an external scheduler provided by the operating system choosing to interrupt a thread to run another.
- Asynchronous language features, which use a single-thread event that provides concurrency via cooperative multitasking (https://realpython.com/async-io-python/#the-10000-foot-view-of-async-io). Task switching is achieved by the code willingly yielding to the event loop. The best opportunity for a function to do so is when it has to wait for a response, or some kind of I/O transaction.

Some argue that concurrency encompasses parallelism, but I think it's less confusing if we really embrace the differences between the two, especially since threading can fulfill concurrency, but sometimes not parallelism.

## Concurrency in Python

A **generator** is a special type of function that itself is an iterable object. During each iteration, the function will run until it yields a value. When the `yield` statement is encountered, "the generator’s state of execution is suspended and local variables are preserved" [1](https://docs.python.org/3/howto/functional.html#generators). During subsequent iterations, the generator will pick up right where it left off.

```py
def yeild_test():
    print("This is the beginning of yeild_test().")
    yield 1

    print("This is the end of yeild_test().")
    yield 2

# "yield_test" refers to the the function.
# "yield_test()", however, produces a generator object, which is iterable.
for generated_item in yeild_test():
    print("Generated value: {}".format(generated_item))
```
```
This is the beginning of yeild_test().
Generated value: 1
This is the end of yeild_test().
Generated value: 2
```

Generators will be very useful for concurrency because cooperative multitasking depends on having the ability to switch between tasks while preserving state.

We now have the building blocks needed to get into concurrency with Python! The [asyncio](https://docs.python.org/3/library/asyncio-task.html) module provides the necessary framework for running asynchronous functions in an event loop. It makes use of some (relatively new) language features that facilitate asynchronous programming:

A **coroutine** is a special type of generator, repurposed for writing asynchronous functions. Coroutines are defined like normal functions, but with `async` before `def`. Coroutines are queued to run in asyncio's event loop, in which methods run until they yield their time.

To understand how coroutines work, let's look at an example of an inefficient synchronous program:
```py
def upload_files():
    print("Preparing files...")
    # Simulating time spent to do operation.
    time.sleep(1)
    print("Files prepared.")
    # Simulating time spent to do operation.
    time.sleep(4)
    print("Files uploaded.")


def send_emails():
    print("Sending emails...")
    # Simulating time spent to do operation.
    time.sleep(3)
    print("Emails sent...")


def main():
    print(f"STARTED AT {time.strftime('%X')}")

    upload_files()
    send_emails()

    print(f"FINISHED {time.strftime('%X')}")
```
```
STARTED AT 01:33:47
Preparing files...
Files prepared.
Files uploaded.
Sending emails...
Emails sent...
FINISHED 01:33:55
```
Look at all that wasted time! We could have been sending emails while waiting for our files to upload. Let's rewrite this as an asynchronous program. Within a coroutine, there are two main ways of invoking another coroutine:

- Starting the coroutine in the background as a task, and continuing in the current function, using [`asyncio.create_task`](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task).
- Awaiting the coroutine in the foreground. This will yield to the event loop until the coroutine is finished.

Here's the rewritten program:

```py
async def upload_files():
    print("Preparing files...")
    # Simulating time spent to do operation.
    await asyncio.sleep(1)
    print("Files prepared.")
    # Simulating time spent to do operation.
    await asyncio.sleep(4)
    print("Files uploaded.")


async def send_emails():
    print("Sending emails...")
    # Simulating time spent to do operation.
    await asyncio.sleep(3)
    print("Emails sent...")


async def main():
    print(f"STARTED AT {time.strftime('%X')}")

    # gather() concurrently runs the given coroutines.
    await asyncio.gather(
        upload_files(),
        send_emails())

    print(f"FINISHED {time.strftime('%X')}")

# run() enters the event loop, adding the provided coroutine to it.
asyncio.run(main())
```
```
STARTED AT 01:38:29
Preparing files...
Sending emails...
Files prepared.
Emails sent...
Files uploaded.
FINISHED 01:38:34
```

Let's go through this step by step:
- We define three coroutines: `main`, `upload_files` and `send_emails`.
- We `run()` the `main` coroutine, which creates a new event loop with the coroutine.
- In the new event loop, `main` executes until it `gather()`s the two other coroutines.
- Since `main` is `await`ing that result, it will be idle for the next while, and the event loop will not resume execution of it.
- The event loop works on `upload_files` until it has to do a blocking task. Since it's `await`ing the result, `upload_files` yields its time to `send_emails`.

This illustrates how concurrency is instrumental in optimizing the use of time.
