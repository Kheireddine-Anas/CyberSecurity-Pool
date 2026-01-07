# Level 1 - Detailed Solution Guide

## How I Discovered the Password

This guide explains EXACTLY how I analyzed the assembly code to find the password `__stack_check`.

---

## Step-by-Step Analysis

### Step 1: Find the Important Function Call

I scanned through the assembly looking for **function calls**. The most important ones are:
```assembly
0x0000120f <+79>:    call   0x1060 <printf@plt>      # Prints something
0x00001227 <+103>:   call   0x1070 <__isoc99_scanf@plt>  # Gets user input
0x0000123c <+124>:   call   0x1040 <strcmp@plt>      # COMPARES strings!
```

**Why strcmp is key:** Programs that check passwords MUST compare your input with the correct password. That's what `strcmp` does!

### Step 2: Understand strcmp Parameters

The `strcmp` function needs TWO strings to compare:
```c
strcmp(string1, string2);
```

In x86 assembly (32-bit), function parameters are passed on the **stack**. Look at the code RIGHT BEFORE the strcmp call:

```assembly
0x00001232 <+114>:   lea    -0x7a(%ebp),%edx    # Load address of password into edx
0x00001235 <+117>:   mov    %esp,%eax           # Get stack pointer
0x00001237 <+119>:   mov    %edx,0x4(%eax)      # Put password address as 2nd parameter
0x0000123a <+122>:   mov    %ecx,(%eax)         # Put user input as 1st parameter
0x0000123c <+124>:   call   0x1040 <strcmp@plt> # Call strcmp
```

So:
- **First parameter** (your input): stored in `%ecx`, which comes from `-0x6c(%ebp)`
- **Second parameter** (password): stored in `%edx`, which comes from `-0x7a(%ebp)`

### Step 3: Find Where the Password is Stored

Now I trace back: where does `-0x7a(%ebp)` get its value? Look earlier in the code:

```assembly
0x000011e0 <+32>:    mov    -0x1ff8(%ebx),%eax   # Load from memory
0x000011e6 <+38>:    mov    %eax,-0x7a(%ebp)     # Store at -0x7a(%ebp)
```

**AHA!** The password is copied from `-0x1ff8(%ebx)` into `-0x7a(%ebp)`.

The program loads multiple parts:
```assembly
0x000011e0 <+32>:    mov    -0x1ff8(%ebx),%eax   # First 4 bytes
0x000011e6 <+38>:    mov    %eax,-0x7a(%ebp)     

0x000011e9 <+41>:    mov    -0x1ff4(%ebx),%eax   # Next 4 bytes
0x000011ef <+47>:    mov    %eax,-0x76(%ebp)     

0x000011f2 <+50>:    mov    -0x1ff0(%ebx),%eax   # Next 4 bytes
0x000011f8 <+56>:    mov    %eax,-0x72(%ebp)     

0x000011fb <+59>:    mov    -0x1fec(%ebx),%ax    # Last 2 bytes
0x00001202 <+66>:    mov    %ax,-0x6e(%ebp)
```

This is copying a **string** piece by piece from memory into the stack!

### Step 4: Visual Memory Layout

```
Stack (local variables):
-0x7a(%ebp) ← First 4 bytes of password  ("__st")
-0x76(%ebp) ← Next 4 bytes               ("ack_")
-0x72(%ebp) ← Next 4 bytes               ("chec")
-0x6e(%ebp) ← Last 2 bytes               ("k\0")
            (This forms the complete password string: "__stack_check")

-0x6c(%ebp) ← Your input goes here
```

### Step 5: Use GDB to Find the Actual Password

Instead of manually calculating memory addresses, I let GDB do it:

```bash
# Method 1: Set breakpoint before strcmp and examine the password parameter
gdb level1 -q
(gdb) break *0x0000123c
(gdb) run
# Enter anything when prompted
(gdb) info registers edx
# edx contains the address of the password
(gdb) x/s $edx
0xffffcf86:     "__stack_check"
```

OR

```bash
# Method 2: Set breakpoint where password is loaded and examine the source
gdb level1 -q
(gdb) break *main+32
(gdb) run
(gdb) x/s $ebx-0x1ff8
0x56557008:     "__stack_check"
```

The `x/s` command means "examine as string" - it shows me what string is at that address!

### Step 6: Verification

Test the password:
```bash
echo "__stack_check" | ./level1
```
Output: `Good job.`

Success! ✓

---

## The Logic Flow

```
1. Program starts
   ↓
2. Copies password from data section (-0x1ff8(%ebx)) 
   to stack (-0x7a(%ebp)) piece by piece
   ↓
3. Prints "Please enter key: "
   ↓
4. Reads your input with scanf into -0x6c(%ebp)
   ↓
5. Calls strcmp:
   - Parameter 1: your input at -0x6c(%ebp)
   - Parameter 2: password at -0x7a(%ebp)
   ↓
6. Checks result (cmp $0x0,%eax)
   - If 0 (equal): prints "Good job."
   - If not 0: prints "Nope."
```

---

## Key Concepts for Beginners

### 1. Function Parameters in 32-bit x86
In 32-bit x86, function parameters are pushed onto the stack before calling a function. For `strcmp(str1, str2)`:
- First parameter (str1) is at `(%esp)`
- Second parameter (str2) is at `0x4(%esp)`

### 2. strcmp Returns 0 When Strings Match
- `strcmp` returns 0 if strings are equal
- Returns non-zero if they're different
- That's why the code checks: `cmp $0x0,%eax` then `jne` (jump if not equal)

### 3. Memory Layout on the Stack
The stack grows downward in memory. When you see `-0x7a(%ebp)`, it means 122 bytes **before** the base pointer. Local variables are stored in negative offsets from `%ebp`.

### 4. Position-Independent Code (PIC)
Modern executables use PIC, where addresses are calculated relative to a base. The `%ebx` register holds this base, and offsets like `-0x1ff8(%ebx)` point to data sections.

### 5. GDB is Your Best Friend
You don't need to understand EVERY line of assembly! Just:
1. Find the password checking function (strcmp)
2. Find what it's comparing
3. Use GDB to extract the actual values from memory

---

## The Secret Trick

**You don't need to manually calculate addresses!** 

Instead of trying to compute where `-0x1ff8(%ebx)` points to, just:
1. Set a breakpoint in GDB
2. Run the program
3. Examine the register that holds the password address
4. Use `x/s $register` to see the string

GDB does all the calculation for you!

---

## Complete Assembly Code with Annotations

```assembly
# Function prologue
0x000011c0 <+0>:     push   %ebp              # Save old base pointer
0x000011c1 <+1>:     mov    %esp,%ebp         # Set new base pointer
0x000011c3 <+3>:     push   %ebx              # Save ebx
0x000011c4 <+4>:     sub    $0x84,%esp        # Allocate 132 bytes for local variables

# Get program base address for PIC
0x000011ca <+10>:    call   0x11cf <main+15> # Trick to get current instruction address
0x000011cf <+15>:    pop    %ebx              # Now ebx = current address
0x000011d0 <+16>:    add    $0x2e31,%ebx      # Calculate data section base

# Copy password from data section to stack (14 bytes total)
0x000011e0 <+32>:    mov    -0x1ff8(%ebx),%eax  # Load "__st" (4 bytes)
0x000011e6 <+38>:    mov    %eax,-0x7a(%ebp)    # Store to stack
0x000011e9 <+41>:    mov    -0x1ff4(%ebx),%eax  # Load "ack_" (4 bytes)
0x000011ef <+47>:    mov    %eax,-0x76(%ebp)    # Store to stack
0x000011f2 <+50>:    mov    -0x1ff0(%ebx),%eax  # Load "chec" (4 bytes)
0x000011f8 <+56>:    mov    %eax,-0x72(%ebp)    # Store to stack
0x000011fb <+59>:    mov    -0x1fec(%ebx),%ax   # Load "k\0" (2 bytes)
0x00001202 <+66>:    mov    %ax,-0x6e(%ebp)     # Store to stack

# Print "Please enter key: "
0x00001206 <+70>:    lea    -0x1fea(%ebx),%eax  # Load string address
0x0000120c <+76>:    mov    %eax,(%esp)         # Put on stack as parameter
0x0000120f <+79>:    call   0x1060 <printf@plt> # Call printf

# Read user input
0x00001217 <+87>:    lea    -0x6c(%ebp),%eax    # Address where input will be stored
0x0000121a <+90>:    lea    -0x1fd7(%ebx),%ecx  # Format string "%s"
0x00001220 <+96>:    mov    %ecx,(%esp)         # First parameter: format
0x00001223 <+99>:    mov    %eax,0x4(%esp)      # Second parameter: buffer
0x00001227 <+103>:   call   0x1070 <__isoc99_scanf@plt>

# Prepare strcmp parameters
0x0000122f <+111>:   lea    -0x6c(%ebp),%ecx    # User input address
0x00001232 <+114>:   lea    -0x7a(%ebp),%edx    # Password address
0x00001235 <+117>:   mov    %esp,%eax           # Stack pointer
0x00001237 <+119>:   mov    %edx,0x4(%eax)      # Second parameter: password
0x0000123a <+122>:   mov    %ecx,(%eax)         # First parameter: user input

# Compare strings
0x0000123c <+124>:   call   0x1040 <strcmp@plt> # Compare!
0x00001241 <+129>:   cmp    $0x0,%eax           # Check if equal (0 = match)
0x00001244 <+132>:   jne    0x1260 <main+160>   # Jump to "Nope" if not equal

# Success path: print "Good job."
0x0000124d <+141>:   lea    -0x1fd4(%ebx),%eax  # Load "Good job." string
0x00001253 <+147>:   mov    %eax,(%esp)         # Put on stack
0x00001256 <+150>:   call   0x1060 <printf@plt> # Print it
0x0000125b <+155>:   jmp    0x1271 <main+177>   # Skip the fail path

# Fail path: print "Nope."
0x00001260 <+160>:   lea    -0x1fc9(%ebx),%eax  # Load "Nope." string
0x00001269 <+169>:   mov    %eax,(%esp)         # Put on stack
0x0000126c <+172>:   call   0x1060 <printf@plt> # Print it

# Function epilogue
0x00001271 <+177>:   xor    %eax,%eax           # Return 0
0x00001273 <+179>:   add    $0x84,%esp          # Deallocate local variables
0x00001279 <+185>:   pop    %ebx                # Restore ebx
0x0000127a <+186>:   pop    %ebp                # Restore ebp
0x0000127b <+187>:   ret                        # Return
```

---

## Summary

**Password:** `__stack_check`

**How I found it:**
1. Found the `strcmp` call at `<+124>`
2. Traced back to find its parameters
3. Discovered password is stored at `-0x7a(%ebp)` on the stack
4. Found it was copied from `-0x1ff8(%ebx)` in the data section
5. Used GDB to examine that memory location
6. Extracted the password string

**Files created:**
- `password` - Contains the correct password
- `source.c` - C program that replicates the binary's behavior
- `README.md` - This detailed explanation

---

## Bonus - Binary Patching

### Objective
Modify the binary to accept **any password** instead of just `__stack_check`.

### The Simple Solution

Replace the conditional jump (`jne`) with NOP instructions so it never jumps to the fail path.

**One-line command to patch:**
```bash
cp level1 level1_patched
printf '\x90\x90\x90\x90\x90\x90' | dd of=level1_patched bs=1 seek=$((0x1244)) count=6 conv=notrunc
```

**What this does:**
- Finds the `jne` instruction at file offset `0x1244`
- Replaces 6 bytes: `0f 85 16 00 00 00` → `90 90 90 90 90 90` (NOPs)
- Now the program never jumps to "Nope.", always prints "Good job."

**Test it:**
```bash
echo "wrong" | ./level1_patched
# Output: Good job.
```


