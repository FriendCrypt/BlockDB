# BlockDB
BlockDB is a database designed for high-performance storage of blockchains.

## Basic concepts

A BlockDB database is split into several parts:

  1. The blockchain itself
  2. Global dynamic properties derived from the blockchain
  3. Dynamic properties of single accounts derived from the blockchain

Dynamic properties are updated as new blocks come in and are validated by
application-provided hooks.

The application also provides a hook for checking if a block has any effect
on an account, and if so what changes need to be made.

In case of a blockchain fork or replay, blocks can be replayed and re-verified
automatically.

## Architecture

Like most pieces of software these days, BlockDB uses a layered architecture.
At the bottom layer are 3 simple file formats:

 1. Block files store blocks of arbitary binary data
 2. Index files store indexes that map IDs (of various datatypes) to block files and offsets
 3. Consensus files store key/value data alongside a blockheight and hash

Block files are treated as immutable except in the case of forks - in which case the older blockchain
may be backed up before overwriting. The library provides facilities to perform the following operations on
block files:

 1. Appending a new block of data
 2. Iterating through all blocks from a particular point
 3. Cut all blocks from a particular point - used for blockchain forks

The basic format of blockfiles is simple: a chain of blocks (duh), each one having a 32-bit unsigned integer
in little endian format
