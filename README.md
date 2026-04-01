# ASRock Challenger 360 Digital AIO – USB Protocol

## Overview

The device exposes itself as a USB HID device, but communicates using a **vendor-specific protocol over the interrupt OUT endpoint**. Standard HID feature reports are not used.

The LCD is updated by sending a sequence of **64-byte packets**, where only the first 8 bytes are meaningful.

---

## Transport Details

* **USB Class:** HID
* **Report ID:** `0x07`
* **Transfer Type:** Interrupt OUT

---

## Packet Structure

Each packet is **64 bytes**, but only the first 8 bytes are used. Byte indices are 0-based (e.g., byte 0 is the first byte).

| Byte Index | Description                                     |
| ---------- | ----------------------------------------------- |
| 0          | Report ID (always `0x07`)                       |
| 1          | System information index                        |
| 2–5        | Encoded value (varies by mode)                  |
| 6          | Mode selector (only meaningful in final packet) |
| 7          | Bar indicator (only meaningful in final packet) |

Remaining bytes should be padded with `0x00`. The remaining 56 bytes (indices 8–63) must be set to `0x00` for valid packets.

---

## Packet Types

The second byte (`index 1`) determines the type of system information on display:

| Value  | Meaning                          |
| ------ | -------------------------------- |
| `0x00` | CPU Temperature                  |
| `0x01` | Not required (unused)            |
| `0x02` | Not required (unused)            |
| `0x03` | CPU Frequency (MHz)              |
| `0x04` | Pump RPM                         |

---

## LCD Update Sequence

The LCD requires a **sequence of 3 packets** out of 5 possible types. The sequence must be sent in this exact order for the LCD to update:

1. Temperature packet (`0x00`)
2. CPU Frequency packet (`0x03`)
3. Pump RPM packet (`0x04`) ← **Final packet**

Only the **last packet in the sequence** determines:

* Display mode
* Bar graph

---

## Display Modes

The display mode is determined by **the last hex digit of byte index 6 in the final packet**:

| Value Pattern               | Mode   | Description                                  |
| --------------------------- | ------ | -------------------------------------------- |
| Digit ends in `0`, `4`, `8` | Mode 3 | CPU Temperature (centered)                   |
| Digit ends in `2`, `6`, `9` | Mode 1 | Pump RPM (centered) + CPU Temp (corner)      |
| Digit ends in `3`, `5`, `7` | Mode 2 | CPU Frequency (centered) + CPU Temp (corner) |

---

## Bar Indicator

* Located at **byte index 7 of the final packet**
* Range: `0x00` – `0x14` (0–20 bars)

---

## Data Encoding

### CPU Temperature

* Packet type: `0x00`
* Encoded in **bytes 3 and 4**
* Example:

```text
[0x07, 0x00, 0x00, 0x33, 0x09, ...]
```

Represents:

```
39°C
```

---

### CPU Frequency (MHz)

* Packet type: `0x03`
* Encoded in **bytes 2–5**

Example:

```text
[0x07, 0x03, 0x03, 0x06, 0x00, 0x70, ...]
```

Represents:

```
3600 MHz
```

Note: Some references may show `0x60` in byte 5, but the correct value for 3600 MHz is `0x70`.

---

### Pump RPM

* Packet type: `0x04`
* Encoded in **bytes 2–5**

Example:

```text
[0x07, 0x04, 0x02, 0x09, 0x06, 0x07, ...]
```

Represents:

```
2967 RPM
```

---

## Example Packet Sequence

```python
# Temperature: 39°C
[0x07, 0x00, 0x00, 0x33, 0x09, 0x00, 0x00, 0x48],

# CPU Frequency: 3600 MHz
[0x07, 0x03, 0x03, 0x06, 0x00, 0x70, 0x00, 0x00],

# Pump RPM: 2967 RPM (final packet also controls mode + bars)
[0x07, 0x04, 0x02, 0x09, 0x06, 0x07, 0x04, 0x08],
```

---

## Important Notes

* The LCD **does not update** unless all required packets are sent in sequence.
* Intermediate packet types (`0x01`, `0x02`) exist but are not required for basic operation.

---
