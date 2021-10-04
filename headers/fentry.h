/*
 * This header comes originally from [1], but we want to annotate it with our
 * empty, no-op calling convention. This calling convention needs to match what
 * we register with the architecture in the python script.
 *
 * 1. https://elixir.bootlin.com/linux/v4.8/source/arch/x86/include/asm/ftrace.h#L19
 */
void __convention("nop") __fentry__(void);
