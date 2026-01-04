from typing import List


class ArrayUtil:
    @staticmethod
    def has_conjunctions(array1: List[any], array2: List[any]) -> bool:
        for item in array1:
            if item in array2:
                return True
        return False

    @staticmethod
    def get_conjunctions(array1: List[any], array2: List[any]) -> List[any]:
        result = []
        for item in array1:
            if item in array2:
                result.append(item)
        return result
