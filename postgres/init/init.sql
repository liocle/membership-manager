--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Debian 16.8-1.pgdg120+1)
-- Dumped by pg_dump version 16.6

-- Started on 2025-02-27 14:33:36 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16390)
-- Name: members; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.members (
    id integer NOT NULL,
    full_name character varying(200) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    company_name character varying(100),
    address text,
    postal_code character varying(20),
    municipality character varying(100),
    country character varying(100),
    email character varying(255),
    member_creation_date date DEFAULT CURRENT_DATE,
    member_last_modification timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    special_notes text
);


ALTER TABLE public.members OWNER TO admin;

--
-- TOC entry 215 (class 1259 OID 16389)
-- Name: members_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.members_id_seq OWNER TO admin;

--
-- TOC entry 3381 (class 0 OID 0)
-- Dependencies: 215
-- Name: members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.members_id_seq OWNED BY public.members.id;


--
-- TOC entry 218 (class 1259 OID 16403)
-- Name: memberships; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.memberships (
    id integer NOT NULL,
    member_id integer,
    membership_year integer NOT NULL,
    price numeric(10,2) NOT NULL,
    is_discounted boolean DEFAULT false,
    status character varying(20) DEFAULT 'pending'::character varying
);


ALTER TABLE public.memberships OWNER TO admin;

--
-- TOC entry 217 (class 1259 OID 16402)
-- Name: memberships_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.memberships_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.memberships_id_seq OWNER TO admin;

--
-- TOC entry 3382 (class 0 OID 0)
-- Dependencies: 217
-- Name: memberships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.memberships_id_seq OWNED BY public.memberships.id;


--
-- TOC entry 220 (class 1259 OID 16417)
-- Name: payments; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    membership_id integer,
    payment_date date DEFAULT CURRENT_DATE,
    amount numeric(10,2) NOT NULL,
    reference_number character varying(20) NOT NULL
);


ALTER TABLE public.payments OWNER TO admin;

--
-- TOC entry 219 (class 1259 OID 16416)
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_id_seq OWNER TO admin;

--
-- TOC entry 3383 (class 0 OID 0)
-- Dependencies: 219
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- TOC entry 3213 (class 2604 OID 16393)
-- Name: members id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members ALTER COLUMN id SET DEFAULT nextval('public.members_id_seq'::regclass);


--
-- TOC entry 3216 (class 2604 OID 16406)
-- Name: memberships id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.memberships ALTER COLUMN id SET DEFAULT nextval('public.memberships_id_seq'::regclass);


--
-- TOC entry 3219 (class 2604 OID 16420)
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- TOC entry 3222 (class 2606 OID 16401)
-- Name: members members_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_email_key UNIQUE (email);


--
-- TOC entry 3224 (class 2606 OID 16399)
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (id);


--
-- TOC entry 3226 (class 2606 OID 16410)
-- Name: memberships memberships_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_pkey PRIMARY KEY (id);


--
-- TOC entry 3228 (class 2606 OID 16423)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- TOC entry 3230 (class 2606 OID 16425)
-- Name: payments payments_reference_number_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_reference_number_key UNIQUE (reference_number);


--
-- TOC entry 3231 (class 2606 OID 16411)
-- Name: memberships memberships_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.memberships
    ADD CONSTRAINT memberships_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id) ON DELETE CASCADE;


--
-- TOC entry 3232 (class 2606 OID 16426)
-- Name: payments payments_membership_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_membership_id_fkey FOREIGN KEY (membership_id) REFERENCES public.memberships(id) ON DELETE CASCADE;


-- Completed on 2025-02-27 14:33:36 UTC

--
-- PostgreSQL database dump complete
--

