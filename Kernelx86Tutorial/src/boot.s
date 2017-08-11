;
; boot.s -- Kernel start location. Also defines multiboot header.
; Based on Bran's kernel development tutorial file start.asm
;

MBOOT_PAGE_ALIGN    equ 1<<0        ; Load kernel and modules on a page boundary
MBOOT_MEM_INFO      equ 1<<1        ; Provide your kernel with memory info
MBOOT_HEADER_MAGIC  equ 0x1BADB002  ; Multiboot Magic value
; NOTE: We do not use MBOOT_AOUT_KLUDGE. It means that GRUB does not
; pass us a symbol table.
