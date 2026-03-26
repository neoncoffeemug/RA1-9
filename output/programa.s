.text
.global _start
_start:

; (2 3 +)
MOV R0, #2
PUSH {R0}
MOV R0, #3
PUSH {R0}
POP {R1}
POP {R0}
ADD R0, R0, R1
PUSH {R0}

; (8 5 -)
MOV R0, #8
PUSH {R0}
MOV R0, #5
PUSH {R0}
POP {R1}
POP {R0}
SUB R0, R0, R1
PUSH {R0}

; (4 6 *)
MOV R0, #4
PUSH {R0}
MOV R0, #6
PUSH {R0}
POP {R1}
POP {R0}
MUL R0, R0, R1
PUSH {R0}

; (8.0 2.0 /)
MOV R0, #8.0
PUSH {R0}
MOV R0, #2.0
PUSH {R0}
POP {R1}
POP {R0}
SDIV R0, R0, R1
PUSH {R0}

; (9 2 //)
MOV R0, #9
PUSH {R0}
MOV R0, #2
PUSH {R0}
POP {R1}
POP {R0}
SDIV R0, R0, R1
PUSH {R0}

; (9 2 %)
MOV R0, #9
PUSH {R0}
MOV R0, #2
PUSH {R0}
POP {R1}
POP {R0}
SDIV R2, R0, R1
MUL R2, R2, R1
SUB R0, R0, R2
PUSH {R0}

; (2.0 3 ^)
MOV R0, #2.0
PUSH {R0}
MOV R0, #3
PUSH {R0}
POP {R1}
POP {R0}
; potência (implementar loop)
PUSH {R0}

; (2 RES)
MOV R0, #2
PUSH {R0}


; fim
