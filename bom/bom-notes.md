# BOM notes

- Rows 1 to 13 are numbered to match the callouts in `media/exploded.png`. Rows 14 to 16 are software and have no callout.
- Costs are indicative single-unit prices in USD, checked against typical retail listings in September 2026 but not quoted by a supplier. Prices for single-board computers and radio modules change often.
- Every line is priced. Total is $290.00 (TWK-CAL-001 [I1]), $10 within the $300 `budget_usd` in `project.yaml`. Amish raised the budget from $200 to $300 on 2026-09-25 (TWK-DDR-002).
- TRL 3 changes: line 11 now specifies a buck-boost charger that charges the 12.8 V pack from a 9 to 30 V input ($25 to $30); line 13 fuse raised from 2 A to 3.15 A time-delay (TWK-CAL-001, section D).
- Choices marked "decided by Amish 2026-09-25" follow TWK-DDR-001 and TWK-DDR-002.
- A 12 V DC supply (mains adapter or existing 12 V system), a laptop or phone to view the dashboard, and a sensor node such as FieldNode are assumed to be on hand and are not included.
