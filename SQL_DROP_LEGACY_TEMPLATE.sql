-- Run ONLY after:
-- 1) verify_legacy_drop_readiness => READY
-- 2) Full backup created and restore tested
-- 3) Explicit go/no-go approval

-- START TRANSACTION;

-- DROP TABLE main_injury;
-- DROP TABLE main_hitweekplanning;
-- DROP TABLE main_dayprogram;
-- DROP TABLE main_antropometry;
-- DROP TABLE main_playerintake;
-- DROP TABLE main_birthday;
-- DROP TABLE main_youthguest;

-- COMMIT;
