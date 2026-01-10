# Level 3 - Reverse Engineering Walkthrough

## Introduction
Level 3 looks like a completely new beast—it's a **64-bit** binary. However, as I dug deeper, I experienced a severe case of déjà vu. It turns out, this level recycles the clever encryption logic from Level 2 but updates it for the modern 64-bit architecture.

## The Challenge
```bash
./level3
Please enter key: test
Nope.
```
Same goal as always: find the password.

---

## Step-by-Step Analysis

### 1. 64-bit Architecture
The first command I ran changed my whole debugging strategy:
```bash
file level3
# level3: ELF 64-bit LSB pie executable...
```
**Key Difference:** In 64-bit Linux, function arguments aren't pushed onto the stack. They are passed in registers:
*   **RDI**: 1st argument
*   **RSI**: 2nd argument

### 2. Disassembly & Pattern Recognition
I opened GDB and started analyzing `main`.
```bash
gdb level3 -q
(gdb) disassemble main
```

I noticed a familiar structure:
1.  **Prefix Checks:**
    *   Checks if `input[1]` is '2' (0x32).
    *   Checks if `input[0]` is '4' (0x34).
    *   Target prefix: **"42"**.

2.  **The Loop:**
    *   Calls `atoi` on chunks of 3 characters.
    *   Increments pointer by 3.
    *   This is the **exact same logic** as Level 2!

### 3. The Target String
I set a breakpoint at the final `strcmp` to see the target.

```bash
(gdb) break *main+391   # Around the strcmp call
(gdb) run
Please enter key: 42000
```
I entered "42" to pass the prefix check.

Checking the registers (remember, RDI/RSI for arguments):
```bash
(gdb) x/s $rsi
0x555555556004: "********"
```

**The Target String is 8 asterisks: `********`**

---

## How the Binary Works

1.  **Validate Prefix**: Input must start with `42`.
2.  **Initialize Buffer**: Sets `buffer[0] = '*'` (ASCII 42).
3.  **Process Input**:
    *   Reads the rest of the input in groups of 3 chars.
    *   Converts groups to integers.
    *   Stores result as a character.
4.  **Compare**: Checks if result matches `********`.

### My Source Code Recreation
Start with `buffer[0] = '*'`, then loop through input chunks.

```c
// See source.c for full code
    char buffer[9];
    buffer[0] = '*'; // 0x2a
    
    // ... loop logic similar to Level 2 ...
```

---

## The Solution

We need to construct `********`.
*   Buffer starts with one `*`.
*   We need 7 more `*`.
*   ASCII for `*` is **42**.
*   We need to provide "042" seven times.

**Construction:**
Prefix `42` + `042` + `042` + `042` + `042` + `042` + `042` + `042`

**Password:** `42042042042042042042042`

**Verification:**
```bash
echo "42042042042042042042042" | ./level3
# Output: Good job.
```

---

## Bonus: Binary Patching

I patched the binary to bypass the checks. There are 3 main checks to defeat.

### The Patching Strategy
I replaced the conditional jumps (`je` - Jump if Equal) with unconditional jumps (`jmp`) to the success path.

**1. Bypass '2' Check**
*   Original: `je [fail]`
*   Patch: `jmp [next_instruction]`

**2. Bypass '4' Check**
*   Original: `je [fail]`
*   Patch: `jmp [next_instruction]`

**3. Bypass strcmp**
*   Original: `je [success]` (Wait, comparison success jumps to good job)
*   Patch: `jmp [success]` (Always jump to good job!)

### The Commands
I used `printf` and `dd` to modify the bytes directly.

```bash
# Copy binary
cp level3 level3_patched

# Patch 1: Bypass '2' check at offset 0x1370
# \xe9\x06... is valid for relative Jump (+6 bytes)
printf '\xe9\x06\x00\x00\x00\x90' | dd of=level3_patched bs=1 seek=$((0x1370)) count=6 conv=notrunc

# Patch 2: Bypass '4' check at offset 0x1386
printf '\xe9\x06\x00\x00\x00\x90' | dd of=level3_patched bs=1 seek=$((0x1386)) count=6 conv=notrunc

# Patch 3: Force Success at offset 0x14a7
# Jump 0xb2 bytes forward to the success function
printf '\xe9\xb2\x00\x00\x00\x90' | dd of=level3_patched bs=1 seek=$((0x14a7)) count=6 conv=notrunc
```

Now, the binary accepts everything!
