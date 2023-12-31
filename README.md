# Asynchronous Python Example

This is a simple Python script demonstrating the use of asynchronous programming with Python's `threading` module. It showcases how to run functions both synchronously and asynchronously using a custom library that provides decorators for managing asynchronous execution.

## Prerequisites

Make sure you have Python >= 3.9 installed on your system.

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/luowensheng/async-python-example.git
   ```

2. Change into the project directory:

   ```bash
   cd async-python-example
   ```

3. Run the main script:

   ```bash
   python main.py
   ```

## Code Overview

The script consists of the following components:

- `run_timer()`: A simple function that simulates a time-consuming task by sleeping for 2 seconds and then returning `True`.

```python
import threading
from time import sleep

def run_timer():
    thread_id = threading.current_thread().ident
    print(f"timer started for {thread_id = }")
    sleep(2)
    print(f"timer ended for {thread_id = }")
    return True
```

- `do_something_async()`: A function decorated with `@do_async` that runs two `run_timer` functions asynchronously in separate threads using the custom library.

```python
@do_async
def do_something_async():
    async_thread_1 = do_async(run_timer)()
    async_thread_2 = do_async(run_timer)()
    return (do_await(async_thread_1), do_await(async_thread_2))
```

- `do_something_sync()`: A function that runs two `run_timer` functions synchronously.

```python
def do_something_sync():
    output_1 = run_timer()
    output_2 = run_timer()
    return (output_1, output_2)
```

- `main()`: The entry point of the script decorated with `@entrypoint`. It demonstrates how to use the custom decorators to run functions asynchronously and synchronously and prints the results.

```python
@entrypoint
def main():
    print(do_await(do_something_async()))
    print(do_something_sync())
```

## Custom Decorators

The script uses custom decorators to manage asynchronous execution:

- `@do_async`: Decorator for running a function asynchronously in a separate thread.

- `@do_await`: Function for waiting for the completion of an asynchronous thread and retrieving its output.

- `@entrypoint`: Decorator to specify the entry point for a Python script, allowing you to run the script only when executed directly.

## Usage

You can use this code as a starting point to learn about asynchronous programming in Python or to handle asynchronous tasks in your own projects.

- Modify the `run_timer` function or create your own asynchronous functions.

- Decorate functions with `@do_async` to run them asynchronously.

- Use `@do_await` to wait for the completion of asynchronous threads and retrieve their output.

- Use `@entrypoint` to define the entry point for your Python script.


