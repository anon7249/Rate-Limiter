from collections import defaultdict, deque
import time
from typing import Dict


class SlidingWindowLog:
    def __init__(self, window_size: float, max_requests: int):

        self.window_size = window_size
        self.max_requests = max_requests
        self.request_logs: Dict[str, deque] = defaultdict(deque)

    def is_allowed(self, ip_address: str) -> bool:
        current_time = time.time()
        client_log = self.request_logs[ip_address]

        while client_log and current_time - client_log[0] > self.window_size:
            client_log.popleft()

        if len(client_log) < self.max_requests:
            client_log.append(current_time)
            return True
        return False
