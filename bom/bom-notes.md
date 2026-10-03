# BOM notes

- Rows 1 to 13 and 17 to 21 are numbered to match the callouts in `media/exploded.png`. Rows 14 to 16 are software and have no callout. Rows 17 to 21 were added on 2026-10-02 to make the design buildable (TWK-DDR-003).
- Costs are indicative single-unit prices in USD, checked against typical retail listings in September 2026 but not quoted by a supplier. Prices for single-board computers and radio modules change often.
- Every line is priced. Value-engineering target: USD 300 (`budget_usd`, a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: USD 334.00 (USD 34 over the target; TWK-CAL-001 [I1, I2]). The concept was USD 290.00. Amish raised `budget_usd` from $200 to $300 on 2026-09-25 (TWK-DDR-002).
- Design for construction (TWK-DDR-003): line 1 is now 6 mm aluminium ($6 to $15), line 2 is cut to 350 mm, line 3 is cut and drilled by the builder, line 11 is a 3-module UPS with no internal battery, and line 12 has a maximum size so it fits the battery box (line 17).
- TRL 3 changes: line 11 now specifies a buck-boost charger that charges the 12.8 V pack from a 9 to 30 V input ($25 to $30); line 13 fuse raised from 2 A to 3.15 A time-delay (TWK-CAL-001, section D).
- Choices marked "decided by Amish 2026-09-25" follow TWK-DDR-001 and TWK-DDR-002. The first build is US915 (line 7 and the 915 MHz antenna of line 9), decided by Amish on 2026-10-02 (TWK-DEC-001); prices are unchanged.
- A 12 V DC supply (mains adapter or existing 12 V system), a laptop or phone to view the dashboard, and a sensor node such as FieldNode are assumed to be on hand and are not included.
- Line 7 (US915, decided 2026-10-02): priced from the Seeed Studio WM1302 SPI US915 module and Seeed WM1302 Raspberry Pi HAT; the parts alone are about USD 60 and the line stays at USD 80 for shipping from two sellers and a HAT that fits a Pi 5 class computer. Line 9 stays at USD 12 and is not yet checked against a named supplier.
