class Observer:
    def __init__(self, observable):
        observable.register(self)

    def update(self, data):
        pass


class Observable:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def unregister(self, observer):
        self._observers.remove(observer)

    def update_observers(self, data):
        for observer in self._observers:
            observer.update(data)

    def cycle_pages(self):
        for observer in self._observers:
            if hasattr(observer, '_check_and_cycle_page'):
                observer._check_and_cycle_page()

    def full_refresh(self):
        for observer in self._observers:
            if hasattr(observer, 'full_refresh'):
                observer.full_refresh()

    def close(self):
        for observer in self._observers:
            observer.close()
