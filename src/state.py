# Ensures that start_listening() and limited_hear() read exactly the same variables.

import queue

q = queue.Queue()
is_processing = False  # flag to indicate if the listener is currently processing