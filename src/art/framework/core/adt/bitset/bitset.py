# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" BitSet """
from art.framework.core.algorithm.algorithms import Algorithms
from art.framework.core.domain.base import Base


class BitSet(Base):
    """
    BitSet C++ implementation, see C++ projects.
    """
    BYTE_SIZE = 1
    BITS_IN_BYTE = 8
    CHUNK_SIZE = BITS_IN_BYTE * BYTE_SIZE  # in bits

    class Bit:
        """
        """
        def __init__(self, bitset, position):
            """
            """
            super().__init__()
            self.bitset = bitset      # referenced bitset
            self.position = position  # position in bitset

        def __bool__(self):
            """
            """
            return (self.bitset.bits[self.position // BitSet.CHUNK_SIZE] &
                    (1 << (self.position % BitSet.CHUNK_SIZE))) != 0

        def set(self, value=1):
            """
            """
            self.bitset.set(self.position, value)

        def reset(self):
            """
            """
            self.bitset.set(self.position, value=0)

        def flip(self):
            """
            """
            self.bitset.flip(self.position)

    def __init__(self, size):
        """
        """
        super().__init__()
        self.size = int(size)  # how many bits
        self.capacity = (0 if size == 0 else size // BitSet.CHUNK_SIZE) + 1  # how many chunks
        self.capacity = int(Algorithms.calculate_alignment_up(self.capacity * BitSet.BYTE_SIZE, 8) / BitSet.BYTE_SIZE)
        self.bits = bytearray(self.capacity)  # bit array - sequence of chunks of bytes

    def __getitem__(self, position):
        """
        operator []
        """  # noqa
        return self.bits[position // BitSet.CHUNK_SIZE] & (1 << (position % BitSet.CHUNK_SIZE))

    def ref(self, position):
        """
        operator& []
        """  # noqa
        return BitSet.Bit(self, position)

    def set(self, position, value):
        """
        """
        chunk = position // BitSet.CHUNK_SIZE
        mask = 1 << (position % BitSet.CHUNK_SIZE)
        if value:
            self.bits[chunk] |= mask
        else:
            self.bits[chunk] &= ~mask

    def reset(self):
        """
        """
        self.bits[:] = b'\x00' * self.capacity

    def flip(self, position):
        """
        """
        self.bits[position // BitSet.CHUNK_SIZE] ^= 1 << (position % BitSet.CHUNK_SIZE)

    def __and__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            for k in range(self.capacity):
                self.bits[k] &= other.bits[k]
        else:
            raise NotImplemented(f"Invalid argument {other.__qualname__}, expected {self.__qualname__}.")
        return self

    def __iand__(self, other):
        """
        """
        return self.__and__(other)

    def __or__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            for k in range(self.capacity):
                self.bits[k] |= other.bits[k]
        else:
            raise NotImplemented(f"Invalid argument {other.__qualname__}, expected {self.__qualname__}.")
        return self

    def __ior__(self, other):
        """
        """
        return self.__or__(other)

    def __xor__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            for k in range(self.capacity):
                self.bits[k] ^= other.bits[k]
        else:
            raise NotImplemented(f"Invalid argument {other.__qualname__}, expected {self.__qualname__}.")
        return self

    def __ixor__(self, other):
        """
        """
        return self.__xor__(other)

    def __invert__(self):
        """
        not b
        """
        for k in range(self.capacity):
            self.bits[k] = ~self.bits[k]
        return self

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = self.bits == other.bits
        else:
            result = NotImplemented
        return result

    def find_first(self, position=0):
        """
        Finds first non zero bit.
        """
        result = -1
        chunk = position // BitSet.CHUNK_SIZE
        for k in range(chunk, self.capacity):
            if self.bits[k] != 0:
                n = self.bits[k]
                result = k * BitSet.CHUNK_SIZE + Algorithms.integer_log2(n - (n & (n - 1))) - 1  # -1 -> zero based
                assert result < self.size, f'Out of index: {self.find_first.__qualname__}.'
                break
        return result

    def find_next(self, position):
        """
        Finds next non zero bit.
        """
        result = 0
        return result

    def stringify(self):
        """
        """
        result = ''.join(['1' if self.__getitem__(k) else '0' for k in reversed(range(0, self.size))])
        return result
