import time
from contextlib import contextmanager

class TimerResult:
    def __init__(self):
        self.elapsed_time = None

@contextmanager
def timer(name):
    """
    Context manager para medir el tiempo de ejecución.
    Guarda el tiempo transcurrido en el atributo 'elapsed_time' del objeto TimerResult.
    """
    start_time = time.perf_counter()
    result = TimerResult() # Creamos un objeto mutable para almacenar el tiempo
    try:
        yield result # <--- ESTA LÍNEA ES CLAVE: Devuelve el objeto 'result'
    finally:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        result.elapsed_time = elapsed_time # Guardamos el tiempo transcurrido en el objeto
        print(f"[TIMER] {name}: {elapsed_time:.3f}s")