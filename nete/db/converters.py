from dictlib.convert import Converter
from dictlib.schema import Schema

class NeteJsonConverter(Converter):
    exclude = []
    rename = [(u'_id', u'id'),
              (u'_rev', u'rev'),
              (u'_attachments', u'attachments')]

def make_schema(schema):
    """ Create a schema 
    """ 
    cls_dict = dict(schema.__dict__)
    if cls_dict.get(u'name') is not None:
        cls_dict[u'name'] = u'Json%s' % cls_dict[u'name']
    cls_dict[u'schema'] = NeteJsonConverter(schema).from_schema(schema.get_schema())
    if u'_schema' in cls_dict:
        del cls_dict[u'_schema']

    return type('Json%s' % schema.__class__.__name__, (Schema,), cls_dict)

