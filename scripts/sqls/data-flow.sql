--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

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
-- Name: dim_date; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.dim_date (
    date_key date NOT NULL,
    year integer,
    quarter integer,
    month integer,
    week integer,
    day_of_week integer
);


ALTER TABLE public.dim_date OWNER TO postgres;

--
-- Name: dividends_and_additional_issuance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.dividends_and_additional_issuance (
    stock_code character varying(255) NOT NULL,
    registration_date date NOT NULL,
    event_type character varying(255) NOT NULL,
    event_content text
);


ALTER TABLE public.dividends_and_additional_issuance OWNER TO postgres;

--
-- Name: enterprises; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.enterprises (
    stock_code character varying(255) NOT NULL,
    industry_code character varying(4),
    listing_date date,
    enterprise_name character varying(255) NOT NULL,
    english_name character varying(255),
    address text,
    phone_number character varying(50),
    email character varying(255),
    website character varying(255),
    tax_code character varying(50) NOT NULL,
    exchange character varying(100)
);


ALTER table if not exists public.enterprises OWNER TO postgres;

--
-- Name: industries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.industries (
    industry_code character varying(4) NOT NULL,
    industry_name character varying(255) NOT NULL,
    industry_group character varying(255)
);


ALTER TABLE public.industries OWNER TO postgres;

--
-- Name: leaders_owners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.leaders_owners (
    executive_id character varying(255) NOT NULL,
    stock_code character varying(255) NOT NULL,
    board character varying(255),
    "position" character varying(255),
    shares integer,
    ownership_ratio numeric(10,4)
);


ALTER TABLE public.leaders_owners OWNER TO postgres;

--
-- Name: news; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.news (
    news_id integer NOT NULL,
    stock_code character varying(255),
    uploaded_date date NOT NULL,
    news_title character varying(255) NOT NULL,
    news_content text NOT NULL
);


ALTER TABLE public.news OWNER TO postgres;

--
-- Name: news_news_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE sequence if not exists public.news_news_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.news_news_id_seq OWNER TO postgres;

--
-- Name: news_news_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.news_news_id_seq OWNED BY public.news.news_id;


--
-- Name: personal_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.personal_info (
    executive_id character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    date_of_birth date NOT NULL,
    place_of_origin character varying(255),
    residence character varying(255),
    education text,
    personal_assets text
);


ALTER TABLE public.personal_info OWNER TO postgres;

--
-- Name: related_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.related_person (
    related_person_id character varying(255) NOT NULL,
    executive_id character varying(255),
    related_person_name character varying(255) NOT NULL,
    relationship character varying(255) NOT NULL
);


ALTER TABLE public.related_person OWNER TO postgres;

--
-- Name: sub_companies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.sub_companies (
    parent_stock_code character varying(255) NOT NULL,
    sub_company_name character varying(255) NOT NULL,
    company_type character varying(255),
    associated_company_stock_code character varying(255),
    charter_capital numeric(20,2),
    contributed_capital numeric(20,2),
    ownership_ratio numeric(10,4)
);


ALTER TABLE public.sub_companies OWNER TO postgres;

--
-- Name: transaction_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE table if not exists public.transaction_history (
    transaction_date date NOT NULL,
    stock_code character varying(255) NOT NULL,
    open_price double precision NOT NULL,
    ref_price double precision NOT NULL,
    ceiling double precision NOT NULL,
    floor double precision NOT NULL,
    high double precision NOT NULL,
    low double precision NOT NULL,
    matched_qty integer NOT NULL,
    matched_amount numeric(20,2) NOT NULL,
    negotiated_qty integer,
    negotiated_amount numeric(20,2),
    buy_orders integer,
    buy_qty integer,
    sell_orders integer,
    sell_qty integer,
    net_qty integer,
    foreign_net_qty integer,
    foreign_net_amount numeric(20,2),
    foreign_buy_qty integer,
    foreign_buy_amount numeric(20,2),
    foreign_sell_qty integer,
    foreign_sell_amount numeric(20,2),
    remaining_foreign_room double precision,
    current_foreign_ownership double precision,
    proprietary_net_qty integer,
    proprietary_net_amount numeric(20,2),
    proprietary_buy_qty integer,
    proprietary_buy_amount numeric(20,2),
    proprietary_sell_qty integer,
    proprietary_sell_amount numeric(20,2)
);


ALTER TABLE public.transaction_history OWNER TO postgres;

--
-- Name: news news_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news ALTER COLUMN news_id SET DEFAULT nextval('public.news_news_id_seq'::regclass);


--
-- Data for Name: dim_date; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dim_date (date_key, year, quarter, month, week, day_of_week) FROM stdin;
\.


--
-- Data for Name: dividends_and_additional_issuance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dividends_and_additional_issuance (stock_code, registration_date, event_type, event_content) FROM stdin;
\.


--
-- Data for Name: enterprises; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enterprises (stock_code, industry_code, listing_date, enterprise_name, english_name, address, phone_number, email, website, tax_code, exchange) FROM stdin;
\.


--
-- Data for Name: industries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.industries (industry_code, industry_name, industry_group) FROM stdin;
\.


--
-- Data for Name: leaders_owners; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leaders_owners (executive_id, stock_code, board, "position", shares, ownership_ratio) FROM stdin;
\.


--
-- Data for Name: news; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news (news_id, stock_code, uploaded_date, news_title, news_content) FROM stdin;
\.


--
-- Data for Name: personal_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.personal_info (executive_id, full_name, date_of_birth, place_of_origin, residence, education, personal_assets) FROM stdin;
\.


--
-- Data for Name: related_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.related_person (related_person_id, executive_id, related_person_name, relationship) FROM stdin;
\.


--
-- Data for Name: sub_companies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sub_companies (parent_stock_code, sub_company_name, company_type, associated_company_stock_code, charter_capital, contributed_capital, ownership_ratio) FROM stdin;
\.


--
-- Data for Name: transaction_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transaction_history (transaction_date, stock_code, open_price, ref_price, ceiling, floor, high, low, matched_qty, matched_amount, negotiated_qty, negotiated_amount, buy_orders, buy_qty, sell_orders, sell_qty, net_qty, foreign_net_qty, foreign_net_amount, foreign_buy_qty, foreign_buy_amount, foreign_sell_qty, foreign_sell_amount, remaining_foreign_room, current_foreign_ownership, proprietary_net_qty, proprietary_net_amount, proprietary_buy_qty, proprietary_buy_amount, proprietary_sell_qty, proprietary_sell_amount) FROM stdin;
\.


--
-- Name: news_news_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.news_news_id_seq', 1, false);


--
-- Name: dim_date dim_date_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT dim_date_pkey PRIMARY KEY (date_key);


--
-- Name: dividends_and_additional_issuance dividends_and_additional_issuance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dividends_and_additional_issuance
    ADD CONSTRAINT dividends_and_additional_issuance_pkey PRIMARY KEY (stock_code, registration_date, event_type);


--
-- Name: enterprises enterprises_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enterprises
    ADD CONSTRAINT enterprises_pkey PRIMARY KEY (stock_code);


--
-- Name: industries industries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.industries
    ADD CONSTRAINT industries_pkey PRIMARY KEY (industry_code);


--
-- Name: leaders_owners leaders_owners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leaders_owners
    ADD CONSTRAINT leaders_owners_pkey PRIMARY KEY (executive_id, stock_code);


--
-- Name: news news_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_pkey PRIMARY KEY (news_id);


--
-- Name: personal_info personal_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personal_info
    ADD CONSTRAINT personal_info_pkey PRIMARY KEY (executive_id);


--
-- Name: related_person related_person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.related_person
    ADD CONSTRAINT related_person_pkey PRIMARY KEY (related_person_id);


--
-- Name: sub_companies sub_companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_companies
    ADD CONSTRAINT sub_companies_pkey PRIMARY KEY (parent_stock_code, sub_company_name);


--
-- Name: transaction_history transaction_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_history
    ADD CONSTRAINT transaction_history_pkey PRIMARY KEY (transaction_date, stock_code);


--
-- Name: dividends_and_additional_issuance dividends_and_additional_issuance_registration_date_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dividends_and_additional_issuance
    ADD CONSTRAINT dividends_and_additional_issuance_registration_date_fkey FOREIGN KEY (registration_date) REFERENCES public.dim_date(date_key);


--
-- Name: dividends_and_additional_issuance dividends_and_additional_issuance_stock_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dividends_and_additional_issuance
    ADD CONSTRAINT dividends_and_additional_issuance_stock_code_fkey FOREIGN KEY (stock_code) REFERENCES public.enterprises(stock_code);


--
-- Name: enterprises enterprises_industry_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enterprises
    ADD CONSTRAINT enterprises_industry_code_fkey FOREIGN KEY (industry_code) REFERENCES public.industries(industry_code);


--
-- Name: enterprises enterprises_listing_date_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enterprises
    ADD CONSTRAINT enterprises_listing_date_fkey FOREIGN KEY (listing_date) REFERENCES public.dim_date(date_key);


--
-- Name: leaders_owners leaders_owners_executive_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leaders_owners
    ADD CONSTRAINT leaders_owners_executive_id_fkey FOREIGN KEY (executive_id) REFERENCES public.personal_info(executive_id);


--
-- Name: leaders_owners leaders_owners_stock_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leaders_owners
    ADD CONSTRAINT leaders_owners_stock_code_fkey FOREIGN KEY (stock_code) REFERENCES public.enterprises(stock_code);


--
-- Name: news news_stock_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_stock_code_fkey FOREIGN KEY (stock_code) REFERENCES public.enterprises(stock_code);


--
-- Name: news news_uploaded_date_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_uploaded_date_fkey FOREIGN KEY (uploaded_date) REFERENCES public.dim_date(date_key);


--
-- Name: related_person related_person_executive_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.related_person
    ADD CONSTRAINT related_person_executive_id_fkey FOREIGN KEY (executive_id) REFERENCES public.personal_info(executive_id);


--
-- Name: sub_companies sub_companies_parent_stock_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sub_companies
    ADD CONSTRAINT sub_companies_parent_stock_code_fkey FOREIGN KEY (parent_stock_code) REFERENCES public.enterprises(stock_code);


--
-- Name: transaction_history transaction_history_stock_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_history
    ADD CONSTRAINT transaction_history_stock_code_fkey FOREIGN KEY (stock_code) REFERENCES public.enterprises(stock_code);


--
-- Name: transaction_history transaction_history_transaction_date_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transaction_history
    ADD CONSTRAINT transaction_history_transaction_date_fkey FOREIGN KEY (transaction_date) REFERENCES public.dim_date(date_key);


--
-- PostgreSQL database dump complete
--

