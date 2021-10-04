# Example Binja Platform Plugin

This is an example Binja platform plugin which fixes up linux kernel module
calls to `__fentry__`. `__fentry__` is the linux kernel function tracing
framework that you can read more about [here](lwn).

The problem, as far as Binja is concerned, is that fentry calls clobber
registers on entry to the function, effectively discarding the functions actual
arguments from analysis. For example, from the decompilation we would see:

```
00000050  int64_t kernote_ioctl()
       00000050  kernote_ioctl:
   0 @ 00000050  int64_t rdx_2
   1 @ 00000050  int32_t rsi_2
   2 @ 00000050  rdx_2, rsi_2 = __fentry__()
   ...

```

Note that the ioctl call has no parameters, and `__fentry__` clobbers rdx and
rsi. The solution is to create a calling convetion that modifies nothing, then
automatically apply it to all of our fentry calls, which is exactly what this
plugin does. With this plugin, we now see:

```
00000050  int64_t kernote_ioctl(int64_t arg1, int32_t arg2, int64_t arg3)
       00000050  kernote_ioctl:
   0 @ 00000050  __fentry__()
   ...

```

Ideally this plugin will be rolled into Binja's default linux platform types
and be made obsolete. This code should be easily adaptable to apply a custom
calling convention to any external call.

[lwn]: https://lwn.net/Articles/747256/
