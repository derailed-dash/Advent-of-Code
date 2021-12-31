""" Timer class implemented using a callable function.
Author: Darren
"""
import time

class Timer:
    """ A timer object that tracks time since last called """
    
    def __init__(self, start_timer: bool=False) -> None:
        """ Initialise a Timer

        Args:
            start_timer (bool, optional): Initialise time to now. Defaults to False.
        """
        self._last_called = None
        
        if start_timer:
            self._last_called = time.time()
        
    def __call__(self):
        return self.elapsed_time()
    
    def elapsed_time(self):
        now = time.time()
        
        # first time we've run this?
        if self._last_called is None:
            self._last_called = now
            return None
        
        # else
        result = now - self._last_called
        self._last_called = now
        
        return result


        
        