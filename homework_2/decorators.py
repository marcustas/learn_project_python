from models import BookModel


def log_adding_publication(function):
    def wrapper(self, publication: BookModel):
        print("Adding new publication...")
        result = function(self, publication)
        print(f"Publication {publication.title} {publication.author} was added successfully")
        return result

    return wrapper


def is_publication_exist(function):
    def wrapper(self, current_publication: BookModel):
        for publication in self.collection:
            if publication.title == current_publication.title:
                print('Publication was deleted!')
                return function(self, current_publication)
        else:
            print('This publication is not exist!')

    return wrapper
