# The REST API

    Method  Path                Description                         Parameters

    GET     /pages              Return a list of pages              `parent`: only return pages that are
                                                                    children of `parent`

    POST    /pages              Create a new page

    GET     /pages/{id}         Return detail information about 
                                `id` page

    PUT     /pages/{id}         Update `id` page

    DELETE  /pages/{id}         Delete `id` page and all documents
                                contained


    GET     /documents          Return a list of all documents      `type`: e.g., `'note'`, `'contact'`
                                                                    `parent`: only return documents that are
                                                                    children of `parent`

    GET     /documents/{id}     Return detail information about
                                `id` document

    PUT     /documents          Create a new document

    POST    /documents/{id}     Update `id` document

    DELETE  /documents/{id}     Delete `id` document

