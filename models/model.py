from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Type, Dict

from common.database import Database

T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):
    # this way we force child classes to implemented the property collection
    # we don't give it value, cause if we would and then forget to implement it in child classes
    # data would be kept in the collection define here which is a bug
    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    #The definitions about of collection and init is just to get rid of the errors.
    # it does nothing and has to be overridden in the child class

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

#now you can create a class that extends Model,
# if you won't implelment json method inside youll get an error
    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        # if we would return just the items_from_db it will return a list like object.
        # instead we use cls to create an item object for each items that returns from the cursor
        return [cls(**elem) for elem in elements_from_db]

    def save_to_mongo(self):
        # the update method will insert new doc to the db
        # unless there is already a record with the relevant id
        # in this case it will update the row
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: str) -> T:
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value:str) -> List[T]:
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]

    @classmethod
    def find_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)
