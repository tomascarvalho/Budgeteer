
-------------------- Migration 0001 --------------------

BEGIN;
--
-- Create model Account
--
CREATE TABLE "budgeteer_account" ("id" serial NOT NULL PRIMARY KEY, "name" varchar(200) NOT NULL, "description" varchar(500) NOT NULL);
--
-- Create model Objective
--
CREATE TABLE "budgeteer_objective" ("id" serial NOT NULL PRIMARY KEY, "deadline" date NOT NULL, "amount" numeric(10, 2) NOT NULL, "description" varchar(500) NOT NULL, "account_id" integer NOT NULL);
--
-- Create model Transaction
--
CREATE TABLE "budgeteer_transaction" ("id" serial NOT NULL PRIMARY KEY, "description" varchar(500) NOT NULL, "amount" numeric(10, 2) NOT NULL, "date" date NOT NULL, "account_id" integer NOT NULL);
--
-- Create model User
--
CREATE TABLE "budgeteer_user" ("id" serial NOT NULL PRIMARY KEY, "username" varchar(128) NOT NULL, "email" varchar(128) NOT NULL, "password" varchar(128) NOT NULL, "total_balance" numeric(10, 2) NOT NULL);
--
-- Add field user to transaction
--
ALTER TABLE "budgeteer_transaction" ADD COLUMN "user_id" integer NOT NULL;
ALTER TABLE "budgeteer_transaction" ALTER COLUMN "user_id" DROP DEFAULT;
--
-- Add field user to objective
--
ALTER TABLE "budgeteer_objective" ADD COLUMN "user_id" integer NOT NULL;
ALTER TABLE "budgeteer_objective" ALTER COLUMN "user_id" DROP DEFAULT;
--
-- Add field user to account
--
ALTER TABLE "budgeteer_account" ADD COLUMN "user_id" integer NOT NULL;
ALTER TABLE "budgeteer_account" ALTER COLUMN "user_id" DROP DEFAULT;
ALTER TABLE "budgeteer_objective" ADD CONSTRAINT "budgeteer_objective_account_id_052c5902_fk_budgeteer_account_id" FOREIGN KEY ("account_id") REFERENCES "budgeteer_account" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "budgeteer_objective_8a089c2a" ON "budgeteer_objective" ("account_id");
ALTER TABLE "budgeteer_transaction" ADD CONSTRAINT "budgeteer_transacti_account_id_137fe0cf_fk_budgeteer_account_id" FOREIGN KEY ("account_id") REFERENCES "budgeteer_account" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "budgeteer_transaction_8a089c2a" ON "budgeteer_transaction" ("account_id");
CREATE INDEX "budgeteer_transaction_e8701ad4" ON "budgeteer_transaction" ("user_id");
ALTER TABLE "budgeteer_transaction" ADD CONSTRAINT "budgeteer_transaction_user_id_26f7aabd_fk_budgeteer_user_id" FOREIGN KEY ("user_id") REFERENCES "budgeteer_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "budgeteer_objective_e8701ad4" ON "budgeteer_objective" ("user_id");
ALTER TABLE "budgeteer_objective" ADD CONSTRAINT "budgeteer_objective_user_id_70bdeaec_fk_budgeteer_user_id" FOREIGN KEY ("user_id") REFERENCES "budgeteer_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "budgeteer_account_e8701ad4" ON "budgeteer_account" ("user_id");
ALTER TABLE "budgeteer_account" ADD CONSTRAINT "budgeteer_account_user_id_7028dda9_fk_budgeteer_user_id" FOREIGN KEY ("user_id") REFERENCES "budgeteer_user" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;


-------------------- Migration 0002 --------------------
