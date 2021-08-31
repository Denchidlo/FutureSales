# Useful wrapper
def make_transformer(func, **kwargs):
    def wrapped(*frames):
        return func(*frames, **kwargs)
    return wrapped


# Full extraction cycle class 
class FeatureExtractor():

    class _SubframeGenerator():
        def __init__(self, tasks, building_context = {}, index=None):
            self._context = {
                'tasks': tasks,
            }
            self._results = building_context
            self._index = index

        def fit(self, df, target=None):
            self._results['id_subsets'] = {
                'original': df
            }

            self._process_tasks()

        def _get_frames(self, names):
            try:
                return [self._results['id_subsets'][name] for name in names]
            except:
                raise

        def _process_tasks(self):
            for task_name, handler in self._context['tasks'].items():
                affected_serieses = self._get_frames(handler['serieses'])
                self._results['id_subsets'][task_name] = handler['executor'](*affected_serieses)
            return self._results['id_subsets']

    class _SubframeAggregator:
        def __init__(self, tasks, building_context = {}, index=None):
            self._context = {
                'tasks': tasks,
            }
            self._results = building_context
            self._index = index

        def fit(self, df=None, target=None):
            self._results['features'] = {}
            self._results['feature_map'] = {}
            
            self._process_tasks()

        def _process_tasks(self):
            pass

    class _TaskTranslator():
        @staticmethod
        def _process_subseries_cfg(cfg):
            translated = {}
            for task_name, encoded_task in cfg.items():
                translated[task_name] = {
                    'executor': make_transformer(encoded_task['func_name'], **encoded_task['params']),
                    'serieses': encoded_task['series_order'],
                }
            return translated

        @staticmethod
        def _process_feature_cfg(cfg):
            translated = {}
            for task in cfg:
                translated[task] = {
                    'executor': make_transformer(task['func_name'], **task['params']),
                    'from': task['from'],
                }
            return translated

    def __init__(self, subseries_cfg, feature_cfg, index) -> None:
        self._cfg = {
            'subserieses': self._TaskTranslator._process_subseries_cfg(subseries_cfg),
            'features': self._TaskTranslator._process_feature_cfg(feature_cfg),
            'index': index
        }

    def __call__(self, df):
        _building_context = {}

        subset_generator = self._SubframeGenerator(
            self._cfg['subserieses'],
            _building_context,
            self._cfg['index']
        )

        subset_generator.fit(df)

        return _building_context
        