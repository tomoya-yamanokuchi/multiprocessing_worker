import multiprocessing as mp
from typing import Type, Any
from .BaseWorker import BaseWorker


class WorkerProcess(mp.Process):
    def __init__(self,
            task_queue: mp.Queue,
            result_queue: mp.Queue,
            worker_class: Type[BaseWorker],
            *worker_args: Any
        ):
        super(WorkerProcess, self).__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.worker_class = worker_class
        self.worker_args = worker_args

        if not issubclass(worker_class, BaseWorker):
            raise TypeError(f"worker_class must be a subclass of BaseWorker, but got {worker_class}")

    def run(self):
        worker = self.worker_class(*self.worker_args)
        while True:
            task = self.task_queue.get()
            if task is None:
                break  # 終了信号
            result = worker.execute(task)
            self.result_queue.put(result)
