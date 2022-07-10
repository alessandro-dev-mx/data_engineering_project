CREATE SCHEMA "company";

CREATE TABLE "company"."contact" (
  "id" SERIAL UNIQUE PRIMARY KEY,
  "first_name" varchar(128) NOT NULL,
  "last_name" varchar(128) NOT NULL,
  "company_id" integer,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "created_by" varchar(64) DEFAULT (CURRENT_USER),
  "updated_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "updated_by" varchar(64) DEFAULT (CURRENT_USER),
  "deleted_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "deleted_by" varchar(64) DEFAULT (CURRENT_USER)
);

CREATE TABLE "company"."company" (
  "id" SERIAL UNIQUE PRIMARY KEY,
  "name" varchar(128) NOT NULL,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "created_by" varchar(64) DEFAULT (CURRENT_USER),
  "updated_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "updated_by" varchar(64) DEFAULT (CURRENT_USER),
  "deleted_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "deleted_by" varchar(64) DEFAULT (CURRENT_USER)
);

CREATE TABLE "company"."address" (
  "id" SERIAL UNIQUE PRIMARY KEY,
  "address_line_1" varchar(128),
  "address_line_2" varchar(128),
  "city" varchar(64),
  "state" varchar(64),
  "zip_code" varchar(16),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "created_by" varchar(64) DEFAULT (CURRENT_USER),
  "updated_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "updated_by" varchar(64) DEFAULT (CURRENT_USER),
  "deleted_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "deleted_by" varchar(64) DEFAULT (CURRENT_USER)
);

CREATE TABLE "company"."phone" (
  "id" SERIAL UNIQUE PRIMARY KEY,
  "contact_id" integer NOT NULL,
  "phone_number" varchar(128) NOT NULL,
  "phone_number_2" varchar(128),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "created_by" varchar(64) DEFAULT (CURRENT_USER),
  "updated_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "updated_by" varchar(64) DEFAULT (CURRENT_USER),
  "deleted_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "deleted_by" varchar(64) DEFAULT (CURRENT_USER)
);

CREATE TABLE "company"."email" (
  "id" SERIAL UNIQUE PRIMARY KEY,
  "contact_id" integer NOT NULL,
  "email_address" varchar(128) NOT NULL,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "created_by" varchar(64) DEFAULT (CURRENT_USER),
  "updated_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "updated_by" varchar(64) DEFAULT (CURRENT_USER),
  "deleted_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "deleted_by" varchar(64) DEFAULT (CURRENT_USER)
);

CREATE TABLE "company"."department" (
  "id" SERIAL UNIQUE PRIMARY KEY,
  "name" varchar(32) NOT NULL,
  "company_id" integer NOT NULL,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "created_by" varchar(64) DEFAULT (CURRENT_USER),
  "updated_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "updated_by" varchar(64) DEFAULT (CURRENT_USER),
  "deleted_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "deleted_by" varchar(64) DEFAULT (CURRENT_USER)
);

CREATE TABLE "company"."contact_address" (
  "id" SERIAL UNIQUE PRIMARY KEY,
  "contact_id" integer NOT NULL,
  "address_id" integer NOT NULL,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "created_by" varchar(64) DEFAULT (CURRENT_USER),
  "updated_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "updated_by" varchar(64) DEFAULT (CURRENT_USER),
  "deleted_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "deleted_by" varchar(64) DEFAULT (CURRENT_USER)
);

CREATE TABLE "company"."contact_department" (
  "id" SERIAL UNIQUE PRIMARY KEY,
  "contact_id" integer NOT NULL,
  "department_id" integer NOT NULL,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "created_by" varchar(64) DEFAULT (CURRENT_USER),
  "updated_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "updated_by" varchar(64) DEFAULT (CURRENT_USER),
  "deleted_at" timestamp DEFAULT (CURRENT_TIMESTAMP),
  "deleted_by" varchar(64) DEFAULT (CURRENT_USER)
);

ALTER TABLE "company"."contact_address" ADD FOREIGN KEY ("contact_id") REFERENCES "company"."contact" ("id");

ALTER TABLE "company"."contact_department" ADD FOREIGN KEY ("contact_id") REFERENCES "company"."contact" ("id");

ALTER TABLE "company"."contact" ADD FOREIGN KEY ("company_id") REFERENCES "company"."company" ("id");

ALTER TABLE "company"."contact_address" ADD FOREIGN KEY ("address_id") REFERENCES "company"."address" ("id");

ALTER TABLE "company"."phone" ADD FOREIGN KEY ("contact_id") REFERENCES "company"."contact" ("id");

ALTER TABLE "company"."email" ADD FOREIGN KEY ("contact_id") REFERENCES "company"."contact" ("id");

ALTER TABLE "company"."contact_department" ADD FOREIGN KEY ("department_id") REFERENCES "company"."department" ("id");

ALTER TABLE "company"."department" ADD FOREIGN KEY ("company_id") REFERENCES "company"."company" ("id");
