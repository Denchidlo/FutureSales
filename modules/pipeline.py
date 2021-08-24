from sklearn.metrics import mean_squared_error as mse
import numpy as np
import pandas as pd

def get_features(date, train_df):
    return train_df[train_df.date_block_num == date].set_index(['id', 'date_block_num']).sort_index()
        
def get_target(date, target_vector):
    return target_vector.reset_index()[target_vector.reset_index().date_block_num == date].set_index(['id', 'date_block_num']).sort_index()

class RegressionValidator:
    def __init__(self, model, *args, **kwargs):
        self.model = model(**kwargs)
        
    def validate(self, X_features, target_vector, test_target):
        train_df = X_features
        
        def get_features(date):
            return train_df[train_df.date_block_num == date].set_index(['id', 'date_block_num']).sort_index()
        
        current_date = 23
        max_date = 32
        
        errors = [
            [], [], []
        ]
        
        while current_date < max_date:
            current_features = get_features(current_date)
            validation_window = get_features(current_date + 1)
            
            current_target = get_target(current_date, target_vector)
            validation_target = get_target(current_date + 1, test_target)

            fitted = self.model.fit(current_features, current_target)

            predictions = self.model.predict(validation_window)
            
            if predictions.transpose().shape[0] == 1:
                predictions = predictions.transpose()[0]
            else:
                predictions = predictions.transpose()
        
            errors[0].append(current_date)
            assert validation_target.loc[:,0].shape == predictions.shape, f'Shapes are pred:{validation_target.loc[:,0].shape} and truth:{predictions.shape}\nCurrent validation set: {current_date}'
            errors[1].append(mse(validation_target.loc[:,0].to_list(), predictions))
            
            report = pd.DataFrame({'true_values': validation_target.loc[:,0].to_list(), 'predicted': predictions})
            errors[2].append(report)
            
            current_date += 1
        
        return errors

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