# Python-libraries
from threading import Thread

# Other modules from this project
# global variables (see conventions in *_global_variables.py):
import api.api_feedback_global_variables as api_globals
# functions
from calculate_next_step.calculation import _move_iteration

threads = []
control_thread: Thread


def initialize_threads():
    global threads, control_thread
    for i in range(api_globals.test_depth):
        t = Thread(name="ThreadNumber" + str(i), target=function_manager)
        threads.append(t)
        t.start()
    control_thread = Thread(name="ControlThread", target=control_threads)


def control_threads():
    global threads
    while True:
        for thread in threads:
            if not thread.is_alive():
                thread.start()


def function_manager():
    # Call function with value and wait for new one.
    print("")
