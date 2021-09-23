import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error as mse
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials


def hyperopt_objective(model, train_data, test_data):

    train_x, train_y = train_data
    test_x, test_y = test_data

    def _loss(kwargs):
        _m_instance = model(**kwargs)
        _m_instance.fit(train_x, train_y)
        result = {
            'loss': np.sqrt(mse(_m_instance.predict(test_x), test_y)),
            'status': STATUS_OK,
            'other_stuff': {
                'kwargs': kwargs,
                'train_rmse': np.sqrt(mse(_m_instance.predict(train_x), train_y))
            },
        }
        return result

    return _loss


# Spliter 
def fs_dataset_cv(train_x, train_y, test_x, test_y):
    def _cv_generator():
        yield X.head(sz_train).index, X.tail(sz_test).index
    
    sz_train = len(train_x)
    sz_test = len(test_x)

    X = pd.concat([train_x, test_x], axis=0).reset_index().drop('id', axis=1)
    Y = pd.concat([train_y, test_y], axis=0).reset_index().drop('id', axis=1)

    return (X, Y), _cv_generator


# Validators
class Validator:
    def __init__(self, model, **kwargs) -> None:
        self.model = model(**kwargs)
        self._context = {}

    def fit(self, x, y, trained_model=None):
        if trained_model is None:
            self.model.fit(x, y)
        else:
            self.model = trained_model

        return self.model

    def validate(self, x, y):
        
        predictions = self.model.predict(x)
        truth = y

        return mse(predictions, truth), predictions, truth

class RegressionValidator:
    """
        DEPRECATED
    """
    def __init__(self, model, *args, **kwargs):
        self.model = model(**kwargs)
        
    def validate(self, cfg, joined_dataset, test_target):
        """
            Validate selected model on a dataset

            Input:

            1) 'joined_dataset' has the following format: ['id', 'window', feature_1, ... , target]
            2) 'test_target': ['id', 'window', 'target']
            3) 'cfg' is a dictionary containig ('min_window', 'max_window') in keys


            Out:
                - Residual statistics
        """
        train_df = joined_dataset.drop(['target'], axis=1)
        target_vector = joined_dataset.loc[:, ['id', 'window', 'target']]
        
        def get_features(date):
            return train_df[train_df.window == date].set_index(['id', 'window']).sort_index()
        
        current_date = cfg['min_window']
        max_date = cfg['max_window']
        
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
            assert validation_target.loc[:,'target'].shape == predictions.shape, f'Shapes are pred:{validation_target.loc[:,"target"].shape} and truth:{predictions.shape}\nCurrent validation set: {current_date}'
            errors[1].append(mse(validation_target.loc[:,'target'].to_list(), predictions))
            
            report = pd.DataFrame({'true_values': validation_target.loc[:,'target'].to_list(), 'predicted': predictions})
            errors[2].append(report)
            
            current_date += 1
        
        return errors
