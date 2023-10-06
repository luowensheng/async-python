import threading
from time import sleep
from asynchronous import do_async, do_await, entrypoint


def run_timer():

    thread_id = threading.current_thread().ident
    
    print(f"timer started for {thread_id = }")
    sleep(2)
    print(f"timer ended for {thread_id = }")

    return True


@do_async
def do_something_async():

    async_thread_1 = do_async(run_timer)()
    async_thread_2 = do_async(run_timer)()

    return (do_await(async_thread_1), do_await(async_thread_2))


def do_something_sync():

    output_1 = run_timer()
    output_2 = run_timer()

    return (output_1, output_2)


@entrypoint
def main():
    
    print(do_await(do_something_async()))
    print(do_something_sync())
