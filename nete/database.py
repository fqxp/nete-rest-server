# Map/reduce functions #########################################################
def objects_by_name(doc):
    if u'type' in doc and doc[u'type']:
        yield doc.get(u'name'), doc

def objects_by_sort_order(doc):
    if u'type' in doc and doc[u'type']:
        yield doc.get(u'sort_order'), doc

def objects_by_parent_id(doc):
    if u'type' in doc and doc[u'type']:
        yield [doc.get(u'parent_id'), doc.get(u'sort_order')], doc
        
def objects_by_type(doc):
    if u'type' in doc and doc[u'type']:
        yield [doc[u'type'], doc[u'sort_order']], doc
