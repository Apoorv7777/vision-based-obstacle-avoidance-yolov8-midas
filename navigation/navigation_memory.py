from collections import deque


class NavigationMemory:

    def __init__(self, window_size=5):

        self.history = deque(
            maxlen=window_size
        )

    def smooth_direction(
            self,
            new_direction):

        self.history.append(
            new_direction
        )

        # Most frequent direction
        return max(
            set(self.history),
            key=self.history.count
        )