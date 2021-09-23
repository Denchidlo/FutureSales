from sklearn.metrics import mean_squared_error as mse
import numpy as np
import pandas as pd

class Pipeline:
    
    class PipelineIterator:
        def __init__(self, dataset, tasks, task_queue):
            self.tasks = tasks
            self.task_queue = task_queue
            self.dataset = dataset
            self.current_task = None
            self.result_storage = {}
            self.proceed = False
            
        def __iter__(self):
            if not self.proceed:
                dataset = self.dataset
                for task in self.task_queue:
                    self.current_task = self.tasks[task]
                    try:
                        proceed_task = self.current_task(dataset)
                        if not proceed_task is None:
                            dataset = proceed_task
                        self.result_storage[task] = dataset
                        print(f'Stage - {task} complete')
                    except:
                        print(f'Exception occured in stage {task}')
                        raise
                    yield self.result_storage[task]
                self.proceed = True
            else:
                for task in self.task_queue:
                    yield self.result_storage[task]
            
        def proceed_all(self):
            if not self.proceed:
                dataset = self.dataset
                for task in self.task_queue:
                    self.current_task = self.tasks[task]
                    try:
                        proceed_task = self.current_task(dataset)
                        if not proceed_task is None:
                            dataset = proceed_task
                        self.result_storage[task] = dataset
                        print(f'Stage - {task} complete')
                    except:
                        print(f'Exception occured in stage {task}')
                        raise
                    self.proceed = True
            return self.result_storage
        
    def __init__(self, tasks, task_queue):
        self.tasks = tasks
        self.task_queue = task_queue
        
    def __call__(self, dataset):
        return self.PipelineIterator(dataset, self.tasks, self.task_queue)