# -*- coding:utf8 -*-

class data_to_es(object):
    def __init__(self, data):
        self.data = data

    def update_es(self):
        
        {
            '_op_type': 'delete',
            '_index': 'index-name',
            '_type': 'document',
            '_id': 42,
            };
        {
        '_op_type': 'update',
        '_index': 'index-name',
        '_type': 'document',
        '_id': 42,
        'doc': {'question': 'The life, universe and everything.'}
        };
        pass

    def index_new_data(self):
        pass

    def format_data(self):
        pass

