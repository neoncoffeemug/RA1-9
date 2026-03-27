.global _start
.text
_start:
    LDR r0, =const_2
    VLDR.F64 d0, [r0]
    SUB sp, sp, #8
    VSTR.F64 d0, [sp]
    LDR r0, =const_3
    VLDR.F64 d0, [r0]
    VLDR.F64 d1, [sp]
    ADD sp, sp, #8
    VADD.F64 d0, d1, d0
    LDR r0, =resultado_0
    VSTR.F64 d0, [r0]
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    SUB sp, sp, #8
    VSTR.F64 d0, [sp]
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VLDR.F64 d1, [sp]
    ADD sp, sp, #8
    VSUB.F64 d0, d1, d0
    LDR r0, =resultado_1
    VSTR.F64 d0, [r0]
    LDR r0, =const_6
    VLDR.F64 d0, [r0]
    SUB sp, sp, #8
    VSTR.F64 d0, [sp]
    LDR r0, =const_7
    VLDR.F64 d0, [r0]
    VLDR.F64 d1, [sp]
    ADD sp, sp, #8
    VMUL.F64 d0, d1, d0
    LDR r0, =resultado_2
    VSTR.F64 d0, [r0]
    LDR r0, =const_8
    VLDR.F64 d0, [r0]
    SUB sp, sp, #8
    VSTR.F64 d0, [sp]
    LDR r0, =const_3
    VLDR.F64 d0, [r0]
    VLDR.F64 d1, [sp]
    ADD sp, sp, #8
    VDIV.F64 d0, d1, d0
    LDR r0, =resultado_3
    VSTR.F64 d0, [r0]
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    SUB sp, sp, #8
    VSTR.F64 d0, [sp]
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VLDR.F64 d1, [sp]
    ADD sp, sp, #8
    BL inteiro_mod
    LDR r0, =resultado_4
    VSTR.F64 d0, [r0]
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    SUB sp, sp, #8
    VSTR.F64 d0, [sp]
    LDR r0, =const_3
    VLDR.F64 d0, [r0]
    VLDR.F64 d1, [sp]
    ADD sp, sp, #8
    BL potencia_int
    LDR r0, =resultado_5
    VSTR.F64 d0, [r0]
    LDR r0, =const_3
    VLDR.F64 d0, [r0]
    SUB sp, sp, #8
    VSTR.F64 d0, [sp]
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VLDR.F64 d1, [sp]
    ADD sp, sp, #8
    VADD.F64 d0, d1, d0
    SUB sp, sp, #8
    VSTR.F64 d0, [sp]
    LDR r0, =const_2
    VLDR.F64 d0, [r0]
    VLDR.F64 d1, [sp]
    ADD sp, sp, #8
    VMUL.F64 d0, d1, d0
    LDR r0, =resultado_6
    VSTR.F64 d0, [r0]
    LDR r0, =const_9
    VLDR.F64 d0, [r0]
    LDR r0, =mem_X
    VSTR.F64 d0, [r0]
    LDR r0, =resultado_7
    VSTR.F64 d0, [r0]
    LDR r0, =mem_X
    VLDR.F64 d0, [r0]
    LDR r0, =resultado_8
    VSTR.F64 d0, [r0]
    LDR r0, =resultado_8
    VLDR.F64 d0, [r0]
    LDR r0, =resultado_9
    VSTR.F64 d0, [r0]

fim:
    B fim

inteiro_div:
    VCVT.S32.F64 s2, d1
    VMOV r4, s2
    VCVT.S32.F64 s3, d0
    VMOV r5, s3
    CMP r5, #0
    BEQ erro_div_zero
    MOV r8, #0
div_loop:
    CMP r4, r5
    BLT div_fim
    SUB r4, r4, r5
    ADD r8, r8, #1
    B div_loop
div_fim:
    VMOV s0, r8
    VCVT.F64.S32 d0, s0
    BX lr

inteiro_mod:
    VCVT.S32.F64 s2, d1
    VMOV r4, s2
    VCVT.S32.F64 s3, d0
    VMOV r5, s3
    CMP r5, #0
    BEQ erro_div_zero
mod_loop:
    CMP r4, r5
    BLT mod_fim
    SUB r4, r4, r5
    B mod_loop
mod_fim:
    VMOV s0, r4
    VCVT.F64.S32 d0, s0
    BX lr

potencia_int:
    VCVT.S32.F64 s3, d0
    VMOV r5, s3
    LDR r0, =const_1
    VLDR.F64 d0, [r0]
pot_loop:
    CMP r5, #0
    BEQ pot_fim
    VMUL.F64 d0, d0, d1
    SUB r5, r5, #1
    B pot_loop
pot_fim:
    BX lr

erro_div_zero:
    B erro_div_zero

.data
mem_X: .double 0.0
resultado_0: .double 0.0
resultado_1: .double 0.0
resultado_2: .double 0.0
resultado_3: .double 0.0
resultado_4: .double 0.0
resultado_5: .double 0.0
resultado_6: .double 0.0
resultado_7: .double 0.0
resultado_8: .double 0.0
resultado_9: .double 0.0
const_0: .double 0.0
const_1: .double 1.0
const_2: .double 4
const_3: .double 2
const_4: .double 10
const_5: .double 3
const_6: .double 6
const_7: .double 5
const_8: .double 8
const_9: .double 20