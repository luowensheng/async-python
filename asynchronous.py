import inspect
from multiprocessing import pool
from time import perf_counter
from typing import Any, Callable

# Create a ThreadPool instance for managing asynchronous tasks.
_THREADPOOL = pool.ThreadPool()

class _AsyncThread:


    def __init__(self, func: Callable):

        super().__init__()

        self.elapsed = -perf_counter()
        self.function_name = func.__name__
        self.done = False
        self.output = None
        self.result = None
        self.__fn = func
 
    def run(self, *args, **kwargs):
        """
        Execute the wrapped function asynchronously.

        This method executes the wrapped function asynchronously and stores its output.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Example:
            async_thread.run(arg1, kwarg1=value)
        """

        output = self.__fn(*args, **kwargs)
        self.output = output
        self.elapsed += perf_counter() 
        self.done = True


    def join(self, timeout:float=None) -> None:
        """
        Wait for the asynchronous function to complete.

        This method blocks until the asynchronous function has completed its execution
        or the specified timeout has elapsed.

        Args:
            timeout (float, optional): Maximum time to wait for the asynchronous function
                to complete, in seconds.

        Example:
            async_thread.join()  # Wait indefinitely
            async_thread.join(10.0)  # Wait for a maximum of 10 seconds
        """

        if not self.result:
            return None
        
        self.result.wait(timeout)


    def start(self, *args, **kwargs) -> None:
        """
        Start the execution of the asynchronous function.

        This method starts the execution of the wrapped function in a separate thread.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Example:
            async_thread.start(arg1, kwarg1=value)
        """

        self.result = _THREADPOOL.apply_async(self.run, args, kwargs)


    def __repr__(self) -> str:

        return f"<AsyncThread object {self.function_name} at {id(self)}>"


def do_async(func: Callable):
    """
    Decorator for running a function asynchronously in a separate thread.

    This decorator allows you to easily run a function asynchronously in a separate thread.
    It wraps the provided function and returns a new function that, when called, starts
    the wrapped function in a new thread and returns the thread object.

    Args:
        func (Callable): The function to be executed asynchronously.

    Returns:
        Callable[..., _AsyncThread]: A decorated function that starts the specified function
        in a new thread and returns the thread object.

    Example:
        @do_async
        def my_async_function(arg1, arg2):
            # Your asynchronous logic goes here.
            pass

        # Call the asynchronous function and get the thread object
        async_thread = my_async_function(arg1_value, arg2_value)

        # You can later use async_thread to manage the asynchronous execution.
    """

    def wrapper(*args, **kwargs)-> _AsyncThread:
        thread = _AsyncThread(func)
        thread.start(*args, *kwargs)

        return thread

    return wrapper


def do_await(thread: _AsyncThread):
    """
    Wait for the completion of an asynchronous thread and return its output.

    Args:
        thread (_AsyncThread): An asynchronous thread object to wait for.

    Returns:
        Any: The output of the completed thread.

    Note:
        This function blocks until the specified thread has finished executing.
        If the input thread is `None`, this function will return `None` without waiting.

    Example:
        # Create an asynchronous thread

        async_thread = do_async(my_function)

        # Wait for the thread to complete and get its output
        result = do_await(async_thread)
        print(result)
    """

    if not thread: 
        return 
    
    thread.join()

    return thread.output


def entrypoint(fn:Callable[[], None]):
    """
    Decorator to specify the entry point for a Python script.

    This decorator is typically used for functions that serve as the entry point
    for a Python script. It checks whether the script is being executed directly
    (not imported as a module) and then calls the provided function.

    Args:
        fn (Callable[[], None]): A function that serves as the entry point for the script.

    Raises:
        Exception: If an exception is raised while executing the provided function,
                   it terminates the thread pool and re-raises the exception.

    Example:
        @entrypoint
        def main():
            # Your script's main logic goes here.
            pass

        if __name__ == "__main__":
            main()
    """
    
    f_locals = inspect.currentframe().f_back.f_locals

    if f_locals.get("__name__") == "__main__":

        try: 
            
            fn()

        except Exception as e:

            _THREADPOOL.terminate()  
            raise e  