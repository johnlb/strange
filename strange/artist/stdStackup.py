"""Standard CMOS layer stackup


Layer 	Short  		
No.   	Name 		Description
------------------------------------------------------------------
31+ 				Process-specific layers
40 		Pin10		Pins for M10
 .		 . 			 	.
 .		 . 			 	.
 . 		 . 			 	.
32 		PIN2		Pins for M2
31 		PIN1		Pins for M1
30 		V10			Via 10 (to Redistribution layer, if available)
 .		 . 			 	.
 .		 . 			 	.
 . 		 . 			 	.
22 		V2			Via 2
21 		V1			Via 1
20 		M10 		Metal 10
 . 		 . 			 	.
 . 		 . 			 	.
 . 		 . 			 	.
12 		M2			Metal 2
11 		M1			Metal 1
10					RESERVED
9 					RESERVED
8 					RESERVED
7 		PIMP 		P Implant
6 		NIMP		N Implant
5 		DW			Deep Well (N/P depending on process)
4 		W			Well (N/P depending on process)
3 		CO			Contact (typ. for both PO and RX)
2 		PO			Polysilicon
1 		RX			Active Area


"""


# Layer Definitions
RX 	= 1
PO 	= 2
CO 	= 3
W 	= 4
DW 	= 5
NIMP= 6
PIMP= 7

M1 	= 11
M2 	= 12
M3 	= 13
M4 	= 14
M5 	= 15
M6 	= 16
M7 	= 17
M8 	= 18
M9 	= 19
M10	= 20

V1 	= 21
V2 	= 22
V3 	= 23
V4 	= 24
V5 	= 25
V6 	= 26
V7 	= 27
V8 	= 28
V9 	= 29
V10	= 30

PIN1 = 31
PIN2 = 32
PIN3 = 33
PIN4 = 34
PIN5 = 35
PIN6 = 36
PIN7 = 37
PIN8 = 38
PIN9 = 39
PIN10= 40

