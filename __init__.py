from binaryninja import *

#
# While technically __fentry__ can exist on any platform, I'm only worried about x64 for right now
# and it makes everything easier to just do it for one, so that's the focus here.
#
arch = Architecture['x86_64']

#
# We need a new a new calling convention that does nothing. By applying this cc to our fentry hook
# point, we can turn those register-clobbering indirect calls into nothing.
#
class NopCallingConvention(CallingConvention):
  pass

#
# Register that calling convention and give it a name. Note that this name should match the name used
# in the header I'm specifying below, using __convention("<convention name here>").
#
arch.register_calling_convention(NopCallingConvention(arch, 'nop'))

#
# Create a new platform for the thing we want to apply our calling convention to. type_file_path is
# just the location of fentry.h, relative to this module.
#
class LinuxKernelModule(Platform):
    name = "linux-kernel-module"
    type_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'headers', 'fentry.h')

#
# Since our platform is basically just linux kernel, we steal the defaults from the linux-platform
# module. See: https://github.com/Vector35/platform-linux/blob/master/platform_linux.cpp#L73-L93
#
kmod = LinuxKernelModule(arch)
kmod.default_calling_convention = arch.calling_conventions['sysv']
kmod.cdecl_calling_convention = arch.calling_conventions['sysv']
kmod.fastcall_calling_convention = arch.calling_conventions['sysv']
kmod.stdcall_calling_convention = arch.calling_conventions['sysv']
kmod.register("linux-kernel-module")

#
# we need something to recognize our new platform. Linux kernel modules have a .modinfo section.
# Normally with would be `'.modinfo' in bv.sections`, but the parent bv passed in here is a raw
# file. As a result, we just yolo it and look for the section name.
#
# Basically this function just needs to identify if we should use our new platform.
#
def linux_kmod_recognizer(parent_bv, metadata):
  if b'\x00.modinfo\x00' in parent_bv.read(0, 0x99999999):
    return kmod

#
# Finally we register our new platform recognizers. 62 is the ELF machine identifier for x64, this
# would need to be updated for another platform or another bv types (e.g. PE).
#
BinaryViewType['ELF'].register_platform_recognizer(62, Endianness.LittleEndian, linux_kmod_recognizer)
