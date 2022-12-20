class MinHeap:

    def __init__(self, array=[], index={}):
        self.array = array
        self.index = index
        self.make()

    def make(self):
        for i in range(len(self.array) // 2).__reversed__():
            self.min_heapify(i)
        for curr_index, curr_vertex in enumerate(self.array):
            self.index[curr_vertex.correspondence()] = curr_index

    def add(self, curr_vertex):
        curr_index = len(self.array)
        self.array.append(curr_vertex)
        self.index[curr_vertex.correspondence()] = curr_index
        self.min_up_heapify(curr_index)

    def remove(self, curr_vertex_id=None, curr_index=None):
        if curr_index is None:
            curr_index = self.index[curr_vertex_id]
        last_item = self.array[-1]
        self.index[last_item.correspondence()] = curr_index
        self.array[curr_index] = last_item

        del self.index[curr_vertex_id]
        del self.array[-1]

        if len(self.array) != 0:
            self.min_heapify(curr_index)
            self.min_up_heapify(curr_index)

    def modify(self, curr_vertex_id, new_value):
        curr_index = self.index[curr_vertex_id]
        self.array[curr_index].value = new_value
        self.min_up_heapify(curr_index)
        self.min_heapify(curr_index)

    def pop(self):
        root = self.array[0]
        self.remove(self.array[0].correspondence(), 0)
        return root

    def is_empty(self):
        return len(self.array) == 0

    def value_of(self, curr_vertex_id):
        return self.array[self.index[curr_vertex_id]]

    def get_vertex(self, curr_vertex_id):
        curr_index = self.index[curr_vertex_id]
        return self.array[curr_index]

    def min_heapify(self, i):
        # Makes a heap when the item with index i has a right and left
        # subtrees which both are heaps.
        le = self.left(i)
        ri = self.right(i)
        smallest = self.minimum(le, ri, i)
        if smallest != i:
            self.swap(i, smallest)
            self.min_heapify(smallest)

    def min_up_heapify(self, i):
        pa = self.parent(i)
        smallest = self.minimum(pa, i)
        if smallest != pa:
            self.swap(pa, i)
            self.min_up_heapify(pa)

    def right(self, i):
        ri = 2 * i + 2
        if ri < len(self.array):
            return ri
        return i

    def left(self, i):
        ri = 2 * i + 1
        if ri < len(self.array):
            return ri
        return i

    def parent(self, i):
        pa = (i - 1) // 2
        if pa < 0:
            return 0
        return pa

    def swap(self, i, j):
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp

        self.index[self.array[i].correspondence()] = i
        self.index[self.array[j].correspondence()] = j

    def minimum(self, *curr_index):
        smallest = curr_index[0]
        for i in curr_index:
            if self.array[i] < self.array[smallest]:
                smallest = i
        return smallest

    def __str__(self):
        return str(self.array)

    def __contains__(self, curr_vertex_id):
        return curr_vertex_id in self.index

    def print(self):
        for i in self.array:
            print(i)
        print(self.index)
        print()
