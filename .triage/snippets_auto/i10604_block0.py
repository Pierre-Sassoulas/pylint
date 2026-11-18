@abstractmethod
def connect(self) -> contextlib.AbstractAsyncContextManager[AsyncConnection]:
   pass
