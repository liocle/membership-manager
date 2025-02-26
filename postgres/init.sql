--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Debian 16.8-1.pgdg120+1)
-- Dumped by pg_dump version 16.6

-- Started on 2025-02-26 16:57:54 UTC

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

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 3383 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 16402)
-- Name: invoices; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.invoices (
    id integer NOT NULL,
    member_id integer,
    amount numeric(10,2) NOT NULL,
    due_date date NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying,
    viitenumero character varying(20) NOT NULL
);


ALTER TABLE public.invoices OWNER TO admin;

--
-- TOC entry 217 (class 1259 OID 16401)
-- Name: invoices_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.invoices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invoices_id_seq OWNER TO admin;

--
-- TOC entry 3384 (class 0 OID 0)
-- Dependencies: 217
-- Name: invoices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.invoices_id_seq OWNED BY public.invoices.id;


--
-- TOC entry 216 (class 1259 OID 16390)
-- Name: members; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.members (
    id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    company character varying(255),
    email character varying(255),
    address text,
    notes text,
    join_date date DEFAULT CURRENT_DATE
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
-- TOC entry 3385 (class 0 OID 0)
-- Dependencies: 215
-- Name: members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.members_id_seq OWNED BY public.members.id;


--
-- TOC entry 220 (class 1259 OID 16417)
-- Name: payments; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    invoice_id integer,
    payment_date date DEFAULT CURRENT_DATE,
    amount numeric(10,2) NOT NULL,
    viitenumero character varying(20) NOT NULL
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
-- TOC entry 3386 (class 0 OID 0)
-- Dependencies: 219
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- TOC entry 3215 (class 2604 OID 16405)
-- Name: invoices id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.invoices ALTER COLUMN id SET DEFAULT nextval('public.invoices_id_seq'::regclass);


--
-- TOC entry 3213 (class 2604 OID 16393)
-- Name: members id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members ALTER COLUMN id SET DEFAULT nextval('public.members_id_seq'::regclass);


--
-- TOC entry 3217 (class 2604 OID 16420)
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- TOC entry 3224 (class 2606 OID 16408)
-- Name: invoices invoices_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_pkey PRIMARY KEY (id);


--
-- TOC entry 3226 (class 2606 OID 16410)
-- Name: invoices invoices_viitenumero_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_viitenumero_key UNIQUE (viitenumero);


--
-- TOC entry 3220 (class 2606 OID 16400)
-- Name: members members_email_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_email_key UNIQUE (email);


--
-- TOC entry 3222 (class 2606 OID 16398)
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (id);


--
-- TOC entry 3228 (class 2606 OID 16423)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- TOC entry 3230 (class 2606 OID 16425)
-- Name: payments payments_viitenumero_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_viitenumero_key UNIQUE (viitenumero);


--
-- TOC entry 3233 (class 2606 OID 16438)
-- Name: payments fk_invoice; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT fk_invoice FOREIGN KEY (invoice_id) REFERENCES public.invoices(id) ON DELETE CASCADE;


--
-- TOC entry 3231 (class 2606 OID 16433)
-- Name: invoices fk_member; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT fk_member FOREIGN KEY (member_id) REFERENCES public.members(id) ON DELETE CASCADE;


--
-- TOC entry 3232 (class 2606 OID 16411)
-- Name: invoices invoices_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.members(id) ON DELETE CASCADE;


--
-- TOC entry 3234 (class 2606 OID 16426)
-- Name: payments payments_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoices(id) ON DELETE CASCADE;


-- Completed on 2025-02-26 16:57:54 UTC

--
-- PostgreSQL database dump complete
--

