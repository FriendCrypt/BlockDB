"""
FriendCrypt Application framework
Copyright (C) 2016 Gareth Nelson

This file is part of the FriendCrypt BlockDB database

The FriendCrypt BlockDB database is free software: you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 2 of the License, 
or (at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import mmap
import struct

class BlockFile:
   """ This class represents a BlockFile
       If the file does not exist, it creates it with a size of 4GB
   """
   def __init__(self,filename):
       if not os.path.exists(filename):
          fd = open(filename,'wb')
          fd.truncate(4294967296)
          fd.close()
       self.fd      = open(filename,'r+b')
       self.mm      = mmap.mmap(self.fd.fileno(), 0)
       self.cur_pos = 0
       self.highest = 0
   def append_block(self,data):
       """ Appends a new block to the end of the file
           If the block will not fit, throws an exception
           The data parameter is a binary blob
           After appending, the current position is NOT updated
           If the block was appended, returns the offset to the block starting with the uint32 block size
       """
       retval = self.highest
       data_len = len(data)
       if (self.highest + data_len + 4) >= self.mm.size():
          raise Exception('Too big') # TODO - make this better
       self.mm[self.highest:self.highest+4] = struct.pack('<L',data_len)
       self.mm[self.highest+4:self.highest+4+data_len] = data
       self.highest += 4+data_len
       self.mm.flush()
       return retval
   def get_block(self,offset):
       """ Get a single block from the specified offset without updating current position
       """
       block_size = struct.unpack('<L',self.mm[offset:offset+4])[0]
       block_data = self.mm[offset+4:offset+4+block_size]
       return block_data
   def get_blocks(self,offset=-1):
       """ An iterator to get blocks
           If you pass an offset parameter and it's aligned to a block header, it'll reset the current position
       """
       if offset != -1: self.cur_pos = offset
       if (self.cur_pos == self.highest) and (self.cur_pos==0):
          return # there's no blocks in this file
       block_size = struct.unpack('<L',self.mm[self.cur_pos:self.cur_pos+4])
       while block_size >= 0:       
          if self.cur_pos >= self.highest: return
          block_data    = self.get_block(self.cur_pos)
          block_size    = len(block_data)
          self.cur_pos += block_size+4
          yield block_data
   def close(self):
       self.mm.flush()
       self.fd.close()

if __name__=='__main__':
   b = BlockFile('test.dat')
   print 'Appended block at %s' % b.append_block('Test the first')
   print 'Appended block at %s' % b.append_block('Test the second')
   print 'Appended block at %s' % b.append_block('Test the third')
   for block in b.get_blocks():
       print 'Block contents: %s' % block
