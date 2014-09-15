#!/usr/bin/env python2

import timer2
from BitVector import BitVector
#from bitarray import bitarray
import binstr
import helptext
from lib import octal

class Word(object):
    
    def __init__(self, name=None, description=None, octal_address=None, memory_type=None, info_text=None, value=None, bank=0):
        if value is not None:
            self.contents = BitVector(intVal=value, size=15)
        else:
            self.contents = BitVector(size=15)
        self.is_negative = False
        self.bank = bank
        self.name = name
        self.description = description
        self.octal_address = octal_address
        self.memory_type = memory_type
        self.info_text = info_text
        self.overflow = False
        self.overflow_sign = ""
    
        self.parity = False
    
    def __repr__(self):
        return "<{} at bank {} offset {}: {}, {}>".format(self.name, self.bank, str(self.octal_address).zfill(5), str(self), self.get_int)
    
    def __len__(self):
        return self.contents.length()
    
    def __add__(self, other_value):
        if isinstance(other_value, Word):
            return int(self) + int(other_value)
        else:
            return int(self) + other_value
    
    def __sub__(self, other_value):
        if isinstance(other_value, Word):
            return int(self) - int(other_value)
        else:
            return int(self) - other_value
    
    def __mul__(self, other_value):
        if isinstance(other_value, Word):
            return int(self) * int(other_value)
        else:
            return int(self) * other_value
    
    def __truediv__(self, other_value):
        if isinstance(other_value, Word):
            return int(self) / int(other_value)
        else:
            return int(self) / other_value
    
    def __floordiv__(self, other_value):
        if isinstance(other_value, Word):
            return int(self) // int(other_value)
        else:
            return int(self) // other_value
    
    def __mod__(self, other_value):
        if isinstance(other_value, Word):
            return int(self) % int(other_value)
        else:
            return int(self) % other_value
    
    def __lshift__(self, other_value):
        if isinstance(other_value, Word):
            return int(self) << int(other_value)
        else:
            return int(self) << other_value
    
    def __rshift__(self, other_value):
        if isinstance(other_value, Word):
            return int(self) >> int(other_value)
        else:
            return int(self) >> other_value
    
    def __int__(self):
        if self.contents[0] == 0:
            return int(self.contents)
        else:
            return int(-self.contents)
    
    def __str__(self):
        return str(self.contents)
    
    def __bool__(self):
        pass
    
    def invert(self):
        self.contents = ~self.contents
    
    @property
    def get_int(self):
        if str(self) == b"000000000000000":
            return 0
        elif str(self) == b"111111111111111":
            return -0
        else:
            return int(self.contents)

    
    def get_list(self):
        return self.contents.tolist()
    
    def zero(self):
        self.contents.setall(False)
        
    @get_int.setter
    def set_int(self, new_value):
        if (new_value > 16383) or (new_value < -16383):
            raise WordOverflow
            return
        if new_value >= 0 <= 16383:
            self.contents = BitVector(intVal=new_value, size=15)
            self.contents[0] = 0
            self.is_negative = False
        elif new_value < 0:
            self.contents = BitVector(intVal=abs(new_value), size=15)
            self.contents = ~self.contents
            self.contents[0] = 1
            self.is_negative = True
        print("New value of register {} set as int {}, binary {}".format(self.name, self.get_int, str(self)))
            
    
    def set_str(self, new_value):
        self.contents = bitarray(new_value)
    
    def shift_left(self, value=1):
        self.set_int = self.get_int << value
    
    def shift_right(self, value=1):
        self.set_int = self.get_int >> value

class CycleRightRegister(Word):
    
    def __init__(self, value=None, name=None, description=None, octal_address=None, memory_type=None, info_text=None):
        super(CycleRightRegister, self).__init__(name, value, description, octal_address, memory_type, info_text)
    
    @property
    def get_int(self):
        return super(CycleRightRegister, self).get_int
    
    @get_int.setter
    def set_int(self, new_value):
        if (new_value > 16383) or (new_value < -16383):
            raise WordOverflow
            return
        if new_value <= 16383:
            self.contents = bitarray(binstr.int_to_b(new_value, width=15))
            cycle_digit = self.contents.pop()
            self.contents.insert(0, cycle_digit)
        else: #negative
            self.contents = bitarray(binstr.int_to_b(new_value, width=15))
            self.contents.invert()
            cycle_digit = self.contents.pop()
            self.contents.insert(0, cycle_digit)

class CycleLeftRegister(Word):
    
    def __init__(self, name=None, description=None, octal_address=None, memory_type=None, info_text=None, value=None):
        super(CycleLeftRegister, self).__init__(name, description, octal_address, memory_type, info_text, value)
        
    @property
    def get_int(self):
        return super(CycleLeftRegister, self).get_int
    
    @get_int.setter
    def set_int(self, new_value):
        if new_value <= 16383:
            self.contents = bitarray(binstr.int_to_b(new_value, width=15))
            cycle_digit = self.contents.pop(0)
            self.contents.append(cycle_digit)
        else: #negative
            self.contents = bitarray(binstr.int_to_b(new_value, width=15))
            self.contents.invert()
            cycle_digit = self.contents.pop(0)
            self.contents.append(cycle_digit)


class ShiftRightRegister(Word):
    
    def __init__(self, value=None, name=None, description=None, octal_address=None, memory_type=None, info_text=None):
        super(ShiftRightRegister, self).__init__(name, description, octal_address, memory_type, info_text, value)
        if value is None:
            self.shift_right()
    
    @property
    def get_int(self):
        return super(ShiftRightRegister, self).get_int
    
    @get_int.setter
    def set_int(self, new_value):
        if new_value <= 16383:
            new_value = new_value >> 1
            self.contents = BitVector(intVal=new_value, size=15)
        else: #negative
            new_value = new_value >> 1
            self.contents = BitVector(intVal=new_value, size=15)
            self.contents = ~self.contents

class EDOPRegister(Word):
    def __init__(self, value=None, name=None, description=None, octal_address=None, memory_type=None, info_text=None):
        super(EDOPRegister, self).__init__(name, description, octal_address, memory_type, info_text, value)
        if value is not None:
            self.shift_right(7)
    
    @property
    def get_int(self):
        return int(self.contents)
    
    @get_int.setter
    def set_int(self, new_value):
        if new_value <= 16383:
            self.contents = bitarray(binstr.int_to_b(new_value, width=15))
            self.shift_right(7)
        else: #negative
            self.contents = bitarray(binstr.int_to_b(new_value, width=15))
            self.contents.invert()
            self.shift_right(7)

class TIME1Register(Word):
    def __init__(self, overflow_register, value=None, name=None, description=None, octal_address=None, memory_type=None, info_text=None):
        super(TIME1Register, self).__init__(name, description, octal_address, memory_type, info_text, value)
        self.overflow_register = overflow_register
    
    def increment(self):
        self.set_int = self.get_int + 1
        if int(self) == 0:
            self.overflow_register.increment()

class TIME2Register(Word):
    def __init__(self, value=None, name=None, description=None, octal_address=None, memory_type=None, info_text=None):
        super(TIME2Register, self).__init__(name, description, octal_address, memory_type, info_text, value)
    
    def increment(self):
        self.set_int = self.get_int + 1

class Timer(Word):
    def __init__(self, value=None, name=None, description=None, octal_address=None, memory_type=None, info_text=None):
        super(Timer, self).__init__(name, description, octal_address, memory_type, info_text, value)
        self.duration = None
    
    # supposed to trigger on overflow, here i am going to trigger by zero value, FIXME
    def decriment(self):
        self.set_int = self.get_int - 1
        

class AccumulatorRegister(Word):
    def __init__(self, name=None, description=None, octal_address=None, memory_type=None, info_text=None, value=None):
        super(AccumulatorRegister, self).__init__(name, description, octal_address, memory_type, info_text, value)
        if value is not None:
            self.contents = BitVector(intVal=value, size=15)
        else:
            self.contents = BitVector(size=15)

class LowerAccumulatorRegister(Word):
    def __init__(self, value=None, name=None, description=None, octal_address=None, memory_type=None, info_text=None):
        super(LowerAccumulatorRegister, self).__init__(name, description, octal_address, memory_type, info_text, value)
        if value is not None:
            self.contents = BitVector(intVal=value, size=15)
        else:
            self.contents = BitVector(size=15)
        self.info = helptext.ACCUMULATOR_REGISTER_INFO

class WordOverflow(Exception):
    pass
