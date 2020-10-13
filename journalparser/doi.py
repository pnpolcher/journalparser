class DOIData(object):
    def __init__(self, doi_object):
        self.doi_object = doi_object

    @property
    def publisher(self):
        return self.doi_object['message']['publisher']

    @property
    def volume(self):
        return self.doi_object['message']['volume']

    @property
    def issue(self):
        return self.doi_object['message']['issue']

    @property
    def page(self):
        return self.doi_object['message']['page']

    @property
    def short_container_title(self):
        return self.doi_object['message']['short-container-title']

    @property
    def type(self):
        return self.doi_object['message']['type']

    @property
    def title(self):
        return self.doi_object['message']['title']

    @property
    def is_referenced_by_count(self):
        return self.doi_object['message']['is_referenced_by_count']

    @property
    def authors(self):
        return self.doi_object['message']['author']

    @property
    def container_title(self):
        return self.doi_object['message']['container-title']
