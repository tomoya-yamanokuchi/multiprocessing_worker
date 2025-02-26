import multiprocessing as mp
from typing import Type, Any
from .BaseWorker import BaseWorker
from domain_object.builder import DomainObject


class WorkerProcess(mp.Process):
    def __init__(self, input_queue: mp.Queue, output_queue: mp.Queue, worker_class: Type[BaseWorker], domain_object: DomainObject, task_counter: mp.Value, total_tasks: int):
        super(WorkerProcess, self).__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.worker_class = worker_class
        self.domain_object = domain_object
        self.task_counter = task_counter
        self.total_tasks = total_tasks  # 全タスク数

        if not issubclass(worker_class, BaseWorker):
            raise TypeError(f"worker_class must be a subclass of BaseWorker, but got {worker_class}")

    def run(self):
        worker = self.worker_class(self.output_queue, self.domain_object)
        while True:
            task = self.input_queue.get()
            if task is None:
                break  # 終了信号

            task_index, task_data = task  # タスクデータを展開

            with self.task_counter.get_lock():  # カウンターをロックしてスレッドセーフに
                self.task_counter.value += 1
                processed_count = self.task_counter.value

            print(f"Processing task {task_index + 1}/{self.total_tasks} ({processed_count}/{self.total_tasks} completed)")
            result = worker.execute(task_index, task_data, self.total_tasks)
            self.output_queue.put(result)
