# Level 2 - Reverse Engineering Walkthrough

## Introduction
This level ramps up the difficulty significantly. Unlike Level 1, the password isn't just lying around in plain text. The program performs a complex transformation on our input before comparing it to a target string. This walkthrough details how I reverse-engineered the logic to generate the correct key.

## The Challenge
```bash
./level2
Please enter key: test
Nope.
```
As standard, we need to find the correct input to trigger the success message.

---

## Step-by-Step Analysis

### 1. Initial Inspection
I started by running the binary in GDB to see what we're dealing with.
```bash
gdb level2 -q
(gdb) disassemble main
```

I noticed a few immediate checks at the start of `main`:
1.  **Strict Input Format**: The program checks specifically for the character '0' (ASCII `0x30`) at current positions.
2.  **The Loop**: A large section of the code loops, calling `atoi` (Ascii to Integer) repeatedly.
3.  **The Target**: Finally, there's a `strcmp` call.

### 2. The Input Validation
Looking closely at the assembly:
```assembly
cmpb   $0x30,0x1(%esp)   # Check input[1] == '0'
jne    <fail>
cmpb   $0x30,(%esp)      # Check input[0] == '0'
jne    <fail>
```
The program **demands** that the first two characters of our input be `00`. If we type anything else, it fails immediately.

### 3. The Transformation Loop
After the `00` check, the program enters a loop that processes the rest of the string.
Crucially, I noticed this pattern:
```assembly
call   0x10d0 <atoi@plt>  # Convert string segment to int
add    $0x3,%eax          # Move pointer forward by 3
```
It takes a chunks of **3 characters** from our input, converts them to an integer (using `atoi`), and stores that integer as a *character* in a new buffer.

So, `100` becomes the character 'd' (ASCII 100).
`097` becomes 'a' (ASCII 97).

### 4. The Hidden Character
Before the loop even starts, there's a sneaky instruction:
```assembly
movb   $0x64,-0x1d(%ebp)  # Hex 0x64 = Decimal 100 = 'd'
```
The first character of the target buffer is hardcoded to **'d'**. It simulates the first character being '100', but without reading it from input.

---

## The Discovery

I set a breakpoint at the `strcmp` call to see what my transformed input turned into, and what it was being compared against.

```bash
(gdb) break *main+405   # The location of the strcmp call
(gdb) run
Please enter key: 00101108
```

I entered `00` (required prefix) followed by `101` and `108` (trying to create chars).

When the breakpoint hit, I checked the memory:
```bash
(gdb) x/s $eax        # The Target String (Address passed to strcmp)
0xffffca2b:     "delabere"
```

**The Target String is "delabere".**

---

## How the Binary Works

1.  **Check Prefix**: Input must start with `00`.
2.  **Initialize Buffer**: Sets `buffer[0] = 'd'`.
3.  **Process Input**:
    *   Reads the rest of the input in **groups of 3 characters**.
    *   Converts each group to an integer (e.g., "097" -> 97).
    *   Appends the character with that ASCII value to the buffer.
4.  **Compare**: Checks if the constructed buffer matches `"delabere"`.

### My Source Code Recreation
I reverse-engineered this logic back into C:

```c
// See source.c for full code
// Key algorithm snippet:
    memset(buffer, 0, 9);
    buffer[0] = 'd';  // 0x64
    
    // Loop: extract groups of 3 digits from input
    while (strlen(buffer) < 8 && index < strlen(input)) {
        char temp[4];
        temp[0] = input[index];
        temp[1] = input[index+1];
        temp[2] = input[index+2];
        temp[3] = '\0';
        int val = atoi(temp);
        buffer[buf_pos] = (char)val;
        buf_pos++;
        index += 3;
    }
```

---

## The Solution

To solve this, we need to construct "delabere".
*   'd' is already there (hardcoded).
*   We need to provide the ASCII codes for the rest: `e`, `l`, `a`, `b`, `e`, `r`, `e`.

**Calculation:**
*   e = 101
*   l = 108
*   a = 097
*   b = 098
*   e = 101
*   r = 114
*   e = 101

**Final Key Construction:**
Prefix `00` + `101` + `108` + `097` + `098` + `101` + `114` + `101`

**Password:** `00101108097098101114101`

**Verification:**
```bash
echo "00101108097098101114101" | ./level2
# Output: Good job.
```

---

## Bonus: Binary Patching

To make the binary accept *any* password, I had to patch multiple checks.

### The Vulnerabilities
1.  **Prefix Check**: The binary checks `input[0]` and `input[1]` separately.
2.  **Validation Check**: Inside the loop, it validates the integers.
3.  **Final Compare**: The big `strcmp` at the end.

### The Patches
I decided to brute-force the logic by NOP-ing (No Operation) or jumping over *every* failure condition.

**The Command:**
```bash
# Copy binary
cp level2 level2_patched

# Patch 1: Scanf Check (convert JE to JMP) - Skip failure if scanf fails
printf '\xeb\x0c\x90\x90\x90\x90' | dd of=level2_patched bs=1 seek=$((0x131e)) count=6 conv=notrunc

# Patch 2: Skip '0' check for 2nd char
printf '\xeb\x0c\x90\x90\x90\x90' | dd of=level2_patched bs=1 seek=$((0x1337)) count=6 conv=notrunc

# Patch 3: Skip '0' check for 1st char
printf '\xeb\x0c\x90\x90\x90\x90' | dd of=level2_patched bs=1 seek=$((0x1350)) count=6 conv=notrunc

# Patch 4: Bypass strcmp failure (NOP the JNE instruction)
printf '\x90\x90\x90\x90\x90\x90' | dd of=level2_patched bs=1 seek=$((0x146d)) count=6 conv=notrunc
```

### Why it works
I systematically removed every "goto fail" instruction.
*   The `00` checks? Skipped.
*   The `strcmp` result? Ignored.

Now the binary is a "YES man". It accepts anything.
