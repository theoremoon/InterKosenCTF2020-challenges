import angr
import claripy
from logging import getLogger, WARN

flag = b''

getLogger("angr").setLevel(WARN + 1)
getLogger("claripy").setLevel(WARN + 1)

"""
Emulate emperor_flag
"""
p = angr.Project("../distfiles/libemperor.so")
state = p.factory.blank_state(addr=0x400000 + 0xa25)
simgr = p.factory.simulation_manager(state)

class hook_citizen_secret(angr.SimProcedure):
    def run(self):
        """
        Emulate citizen_secret
        """
        print("[+] citizen_secret: enter")
        p = angr.Project("../distfiles/libcitizen.so",
                 auto_load_libs=False)
        state = p.factory.blank_state(addr=0x400000 + 0x8da)
        simgr = p.factory.simulation_manager(state)
        simgr.explore(find=0x400000 + 0xa24)
        try:
            found = simgr.found[0]
        except IndexError:
            exit("Not Found")
        data = found.memory.load(found.regs.rax, 0x100)
        self.state.memory.store(found.regs.rax, data)
        print("[+] citizen_secret: exit")
        return found.regs.rax

p.hook_symbol("citizen_secret", hook_citizen_secret())

print("[+] emperor_flag: start")
simgr.explore(find=0x400000 + 0xb76)

try:
    found = simgr.found[0]
    emperor_flag = found.memory.load(found.regs.rax, 0x20)
    flag += state.solver.eval(emperor_flag, cast_to=bytes).rstrip(b'\x00')
    print("[+] emperor_flag: done")
    print(flag)
except IndexError:
    print("Not Found")

"""
Emulate citizen_flag
"""
p = angr.Project("../distfiles/libcitizen.so")
state = p.factory.blank_state(addr=0x400000 + 0xa25)
simgr = p.factory.simulation_manager(state)

class hook_slave_secret(angr.SimProcedure):
    def run(self):
        """
        Emulate slave_secret
        """
        print("[+] slave_secret: enter")
        p = angr.Project("../distfiles/libslave.so",
                 auto_load_libs=False)
        state = p.factory.blank_state(addr=0x400000 + 0x8da)
        simgr = p.factory.simulation_manager(state)
        simgr.explore(find=0x400000 + 0xa21)
        try:
            found = simgr.found[0]
        except IndexError:
            exit("Not Found")
        data = found.memory.load(found.regs.rax, 0x100)
        self.state.memory.store(found.regs.rax, data)
        print("[+] slave_secret: exit")
        return found.regs.rax

p.hook_symbol("slave_secret", hook_slave_secret())

print("[+] citizen_flag: start")
simgr.explore(find=0x400000 + 0xb76)

try:
    found = simgr.found[0]
    emperor_flag = found.memory.load(found.regs.rax, 0x20)
    flag += state.solver.eval(emperor_flag, cast_to=bytes).rstrip(b'\x00')
    print("[+] citizen_flag: done")
    print(flag)
except IndexError:
    print("Not Found")

"""
Emulate slave_flag
"""
p = angr.Project("../distfiles/libslave.so")
state = p.factory.blank_state(addr=0x400000 + 0xa22)
simgr = p.factory.simulation_manager(state)

class hook_emperor_secret(angr.SimProcedure):
    def run(self):
        """
        Emulate emperor_secret
        """
        print("[+] emperor_secret: enter")
        p = angr.Project("../distfiles/libemperor.so",
                 auto_load_libs=False)
        state = p.factory.blank_state(addr=0x400000 + 0x8da)
        simgr = p.factory.simulation_manager(state)
        simgr.explore(find=0x400000 + 0xa24)
        try:
            found = simgr.found[0]
        except IndexError:
            exit("Not Found")
        data = found.memory.load(found.regs.rax, 0x100)
        self.state.memory.store(found.regs.rax, data)
        print("[+] emperor_secret: exit")
        return found.regs.rax

p.hook_symbol("emperor_secret", hook_emperor_secret())

print("[+] slave_flag: start")
simgr.explore(find=0x400000 + 0xb6b)

try:
    found = simgr.found[0]
    emperor_flag = found.memory.load(found.regs.rax, 0x20)
    flag += state.solver.eval(emperor_flag, cast_to=bytes).rstrip(b'\x00')
    print("[+] slave_flag: done")
    print(flag)
except IndexError:
    print("Not Found")
