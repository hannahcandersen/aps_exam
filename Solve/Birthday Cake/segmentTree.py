'''
The code is taken from the following link from the course page:
XXXXXXXX
'''

class SegmentTree():
    """
    A class representing a Segment Tree data structure.

    Args:
        n (int): The size of the array.

    Attributes:
        N (int): The size of the segment tree array.
        A (list): The segment tree array.

    Methods:
        get(i): Returns the value at index i in the segment tree.
        update(i, k): Updates the value at index i in the segment tree with k.
        query(i, j): Returns the sum of values in the range [i, j] in the segment tree.

    """

    def __init__(self, n):
        """
        Initializes a SegmentTree object.

        Args:
            n (int): The size of the array.

        """
        self.N = 1
        while self.N < n:
            self.N *= 2
        self.A = [0 for _ in range(2 * self.N)]
        print(self.A)

    def get(self, i):
        """
        Returns the value at index i in the segment tree.

        Args:
            i (int): The index of the value to retrieve.

        Returns:
            int: The value at index i in the segment tree.

        """
        return self.A[self.N + i]
    
    def update(self, i, k):
        """
        Updates the value at index i in the segment tree with k.

        Args:
            i (int): The index of the value to update.
            k (int): The new value to set at index i.

        """
        p = self.N + i
        self.A[p] = k
        p //= 2
        while p > 0:
            self.A[p] = self.A[2 * p] + self.A[2 * p + 1]
            p //= 2
    
    def query(self, i, j):
        """
        Returns the sum of values in the range [i, j] in the segment tree.

        Args:
            i (int): The start index of the range.
            j (int): The end index of the range.

        Returns:
            int: The sum of values in the range [i, j] in the segment tree.

        """
        #return self.__top_down_range_sum(1, 0, self.N, i, j + 1)
        return self.__bottom_up_range_sum(i, j)


    def __bottom_up_range_sum(self, i, j):
        """
        Helper method for query(). Returns the sum of values in the range [i, j] in the segment tree.

        Args:
            i (int): The start index of the range.
            j (int): The end index of the range.

        Returns:
            int: The sum of values in the range [i, j] in the segment tree.

        """
        # Convert the indices to correspond to the leaf nodes in the segment tree
        i += self.N
        j += self.N

        s = 0
        while i <= j:
            print(self.A)
            # If the left index is odd, add the corresponding value to the sum
            if i % 2 == 1:
                s += self.A[i]
                i += 1
            # If the right index is even, add the corresponding value to the sum
            if j % 2 == 0:
                s += self.A[j]
                j -= 1
            # Move up to the parent nodes
            i //= 2
            j //= 2
        return s

    def __top_down_range_sum(self, p, start, span, i, j):
        """
        Helper method for query(). Returns the sum of values in the range [i, j] in the segment tree.

        Args:
            p (int): The current node in the segment tree.
            start (int): The start index of the current node's range.
            span (int): The size of the current node's range.
            i (int): The start index of the range to query.
            j (int): The end index of the range to query.

        Returns:
            int: The sum of values in the range [i, j] in the segment tree.

        """
        # If the range [start, start + span) is completely outside the query range [i, j),
        # return 0 since there are no elements to sum
        if start + span <= i or j <= start:
            return 0
        # If the range [start, start + span) is completely inside the query range [i, j),
        # return the value stored at the current node p
        if i <= start and start + span <= j:
            return self.A[p]
        # Recursively compute the sum of the left and right child nodes
        left = self.__top_down_range_sum(2 * p, start, span // 2, i, j)
        right = self.__top_down_range_sum(2*p + 1, start + span // 2, span // 2, i, j)
        # Return the sum of the left and right child nodes
        return left + right