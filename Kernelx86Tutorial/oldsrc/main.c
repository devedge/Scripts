// main.c -- Defines the C-code kernel entry point, calls initialization routines.
// Made for JamesM's tutorials

// #include "monitor.h"

int main(struct multiboot *mboot_ptr) {
  // All initialization call will go here
  return 0xDEADBABA;
  // monitor_clear();
  // monitor_write("Hello, world!");
  // return 0;
}
