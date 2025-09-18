CREATE TYPE medical_condition AS ENUM ('diabetes', 'hypertension', 'chronic_condition');

create table public.customer (
  id uuid not null default gen_random_uuid (),
  name character varying not null,
  age smallint not null,
  contact_info character varying not null,
  is_disabled boolean not null,
  medical_conditions medical_conditions[] null,
  constraint customer_pkey primary key (id)
) TABLESPACE pg_default;

create table public.rental (
  id uuid not null default gen_random_uuid (),
  customer_id uuid not null,
  rental_date timestamp with time zone not null default now(),
  shoe_size real not null,
  rental_fee real not null,
  discount real not null,
  total_fee real not null,
  constraint rental_pkey primary key (id),
  constraint rental_customer_id_fkey foreign KEY (customer_id) references customer (id) on update CASCADE on delete CASCADE
) TABLESPACE pg_default;