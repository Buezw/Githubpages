---
title: "CO 3. Subroutines"
date: 2026-01-20
tags: ["CO", "Docs"]
math: mathjax
---

> Last Edit: 1/20/26

> Last Edit: 1/20/25
> 

# Directives

Directives are not the code for CPU to run, instead, its a guidance for Assembler to order code

- Directives start with an `.`
- Commonly seen Directive are `.text` , `.data` ,`.align`

## .text

Text Segment tells the Assembler that the following are runnable code that are read only

## .data

Data Segment tells the Assembler that following code are data, like constant, and so on

## .align

Alignment make sure the following code or data start with specific address, i.e. 4 or 8

# Subroutines

## Program Counter PC

Inside Processor, there’s a specific Register called PC, that is pointing to the next instruction’s address

- Normally, PC increase by 4 each time, because the Processor we use is 32 bits
- Though we can manually change PC to address the instruction we want to call next, and that will be the case in Conditional Branch, or Subroutines

## Subroutines

Subroutines can also being interpreted by Functions, that can be reused for several times, consider this C program

```c
int main(void){
	int mysub(int p){
		return(p+p);
	}
	int x,y;
	x = mysub(3);
	y = mysub(4);
```

The above section indicated how PC works, while there’s a second Register tells the PC the original address to return to before calling the Subroutine (Function)

Now we can write the Assembly Code for the above C program

```nasm
my_sub: add a0,a0,a0
				ret

li a0,3
call my-sub

next: li a0,4
			call my-sub
			
done: j done
```

## Return Address

In Subroutines, they need to deal with he Return Address `ra` , that is the return address

The case is that, if `A` is calling `B` , then `B`  return directly, everything is fine

But if `A` is calling `B` , and `B`  is calling `C` , then the address of `A` will be overwrite

## Stack - Data Structure

Thus we can use the Stack Data Structure to fix this problem

Having the property of $LIFO, Last In First Out$, Stack have two operations

- **Push**: Put on top
- **Pop**: Remove from top

## Stack Pointer - Implementation of Stack

In NIOS V, A special Register `x2`  is designed as the top of a stack pointer

- It is pointing to the address of the top word on the stack
- And we call it **Stack Pointer** or `sp`

The Stack Pointer has the property of growing downwards (towards smaller addresses) in memory, so we init it in a **higher memory address**

- In this course, we init `sp` at `0x20000`
- Notice that if `sp` is at `0x20000` , then it means the stack is empty

---

### Push in SP

Now let’s try to push a word `0x1234f678` into stack, that will be `li t0, 0x1234f678`

- First we change the `sp` and allocate a memory for a word (4 Bytes)
- `addi sp,sp,-4`
- Then we push the value into stack
- `sw t0,(sp)`

### Pop in SP

Now we are going to try to pop a word out, we basically do the reverse of push

- First get the value of current `sp`
- `lw t1,(sp)`
- Then put `sp` back, notice that the value is not being deleted, but `sp` has been mov
- `addi sp,sp,4`

## Code Example: Nested Subroutine Calls

```nasm
# --- Initialization ---
la sp, 0x20000        # Initialize stack pointer high in memory
li a0, 1              # Load immediate value 1 into register a0
call sub_1            # Jump to sub_1; ra is set to 'done' address

done: 
    j done            # Infinite loop once the program is finished

# --- Subroutine 1 ---
sub_1:
    addi sp, sp, -4   # Push ra onto stack: decrement stack pointer
    sw   ra, (sp)     # Save the return address (pointing to 'done')

    # ... logic for sub_1 ...

    call sub_2        # Call sub_2; ra is now overwritten with address in sub_1

    # ... execution continues here after sub_2 returns ...

    lw   ra, (sp)     # Pop top of stack into ra just before returning
    addi sp, sp, 4    # Increment stack pointer to "remove" item
    ret               # Return to the caller (PC <- ra)

# --- Subroutine 2 ---
sub_2:
    addi sp, sp, -4   # Push ra onto stack so we can call other subroutines
    sw   ra, (sp)     # Save ra (which currently points back to sub_1)

    # ... logic for sub_2 ...

    call sub_3        # Go off to sub_3, then come back

    # ... execution continues here after sub_3 returns ...

    lw   ra, (sp)     # Pop top of stack into ra
    addi sp, sp, 4    # Restore the stack pointer
    ret               # Return to sub_1 (PC <- ra - the correct one!)

# --- Subroutine 3 ---
sub_3:
    # sub_3 would look similar if it called more functions
    # If it is a leaf function (calls no one), it may not need to save ra
    ret               # Return to sub_2
```