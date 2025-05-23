PGDMP                      }            vn_stock_dw    17.4 (Debian 17.4-1.pgdg120+2)    17.4 (Debian 17.4-1.pgdg120+2) >    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    24583    vn_stock_dw    DATABASE     w   CREATE DATABASE vn_stock_dw WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE vn_stock_dw;
                     postgres    false                        2615    25043    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                     pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                        pg_database_owner    false    5            �           0    0    SCHEMA public    ACL     +   REVOKE USAGE ON SCHEMA public FROM PUBLIC;
                        pg_database_owner    false    5            �            1259    25044    dim_date    TABLE     �   CREATE TABLE public.dim_date (
    date_key date NOT NULL,
    year integer,
    quarter integer,
    month integer,
    week integer,
    day_of_week integer
);
    DROP TABLE public.dim_date;
       public         heap r       postgres    false    5            �            1259    25047    dim_enterprises    TABLE     �  CREATE TABLE public.dim_enterprises (
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
 #   DROP TABLE public.dim_enterprises;
       public         heap r       postgres    false    5            �            1259    25052 1   dim_enterprises_dividends_and_additional_issuance    TABLE     �   CREATE TABLE public.dim_enterprises_dividends_and_additional_issuance (
    stock_code character varying(255) NOT NULL,
    registration_date date NOT NULL,
    event_type character varying(255) NOT NULL,
    event_content text
);
 E   DROP TABLE public.dim_enterprises_dividends_and_additional_issuance;
       public         heap r       postgres    false    5            �            1259    25057    dim_enterprises_industries    TABLE     �   CREATE TABLE public.dim_enterprises_industries (
    industry_code character varying(4) NOT NULL,
    industry_name character varying(255) NOT NULL,
    industry_group character varying(255)
);
 .   DROP TABLE public.dim_enterprises_industries;
       public         heap r       postgres    false    5            �            1259    25062    dim_enterprises_leaders_owners    TABLE       CREATE TABLE public.dim_enterprises_leaders_owners (
    executive_id character varying(255) NOT NULL,
    stock_code character varying(255) NOT NULL,
    board character varying(255),
    "position" character varying(255),
    shares integer,
    ownership_ratio numeric(10,4)
);
 2   DROP TABLE public.dim_enterprises_leaders_owners;
       public         heap r       postgres    false    5            �            1259    25067    dim_enterprises_news    TABLE     �   CREATE TABLE public.dim_enterprises_news (
    news_id integer NOT NULL,
    stock_code character varying(255),
    uploaded_date date NOT NULL,
    news_title character varying(255) NOT NULL,
    news_content text NOT NULL
);
 (   DROP TABLE public.dim_enterprises_news;
       public         heap r       postgres    false    5            �            1259    25072    dim_enterprises_personal_info    TABLE     8  CREATE TABLE public.dim_enterprises_personal_info (
    executive_id character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    date_of_birth date NOT NULL,
    place_of_origin character varying(255),
    residence character varying(255),
    education text,
    personal_assets text
);
 1   DROP TABLE public.dim_enterprises_personal_info;
       public         heap r       postgres    false    5            �            1259    25077    dim_enterprises_related_person    TABLE       CREATE TABLE public.dim_enterprises_related_person (
    related_person_id character varying(255) NOT NULL,
    executive_id character varying(255),
    related_person_name character varying(255) NOT NULL,
    relationship character varying(255) NOT NULL
);
 2   DROP TABLE public.dim_enterprises_related_person;
       public         heap r       postgres    false    5            �            1259    25082    dim_enterprises_sub_companies    TABLE     s  CREATE TABLE public.dim_enterprises_sub_companies (
    parent_stock_code character varying(255) NOT NULL,
    sub_company_name character varying(255) NOT NULL,
    company_type character varying(255),
    associated_company_stock_code character varying(255),
    charter_capital numeric(20,2),
    contributed_capital numeric(20,2),
    ownership_ratio numeric(10,4)
);
 1   DROP TABLE public.dim_enterprises_sub_companies;
       public         heap r       postgres    false    5            �            1259    25087 !   dividends_and_additional_issuance    TABLE     �   CREATE TABLE public.dividends_and_additional_issuance (
    stock_code character varying(255) NOT NULL,
    registration_date date NOT NULL,
    event_type character varying(255) NOT NULL,
    event_content text
);
 5   DROP TABLE public.dividends_and_additional_issuance;
       public         heap r       postgres    false    5            �            1259    25092    enterprises    TABLE     �  CREATE TABLE public.enterprises (
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
    DROP TABLE public.enterprises;
       public         heap r       postgres    false    5            �            1259    25097    fact_financial_statement    TABLE     9  CREATE TABLE public.fact_financial_statement (
    stock_code text NOT NULL,
    financial_year date NOT NULL,
    cash integer,
    cash_equivalents integer,
    trading_securities integer,
    provision_for_trading_securities_devaluation integer,
    held_to_maturity_investments integer,
    short_term_receivables_from_customers integer,
    short_term_advance_payments_to_suppliers integer,
    short_term_internal_receivables integer,
    receivables_under_construction_contracts integer,
    short_term_loan_receivables integer,
    other_short_term_receivables integer,
    provision_for_short_term_doubtful_debts integer,
    assets_pending_resolution integer,
    inventories integer,
    short_term_prepaid_expenses integer,
    deductible_vat integer,
    taxes_and_other_receivables_from_state integer,
    government_bond_repurchase_transactions integer,
    other_current_assets integer,
    non_current_assets integer,
    long_term_receivables_from_customers integer,
    long_term_advance_payments_to_suppliers integer,
    capital_in_subsidiaries integer,
    long_term_internal_receivables integer,
    long_term_loan_receivables integer,
    other_long_term_receivables integer,
    provision_for_long_term_doubtful_debts integer,
    tangible_fixed_assets integer,
    finance_leased_fixed_assets integer,
    intangible_fixed_assets integer,
    investment_properties integer,
    long_term_work_in_progress integer,
    construction_in_progress integer,
    investments_in_subsidiaries integer,
    investments_in_associates_and_joint_ventures integer,
    investments_in_other_entities integer,
    provision_for_long_term_investments integer,
    other_long_term_investments integer,
    long_term_prepaid_expenses integer,
    deferred_tax_assets integer,
    long_term_spare_parts_and_supplies integer,
    other_non_current_assets integer,
    goodwill integer,
    short_term_payables_to_suppliers integer,
    short_term_advance_payments_from_customers integer,
    taxes_and_other_payables_to_state integer,
    payables_to_employees integer,
    short_term_accrued_expenses integer,
    short_term_internal_payables integer,
    payables_under_construction_contracts integer,
    short_term_unearned_revenue integer,
    other_short_term_payables integer,
    short_term_borrowings_and_finance_leases integer,
    short_term_provisions integer,
    bonus_and_welfare_funds integer,
    price_stabilization_fund integer,
    long_term_payables_to_suppliers integer,
    long_term_advance_payments_from_customers integer,
    long_term_accrued_expenses integer,
    internal_payables_for_business_capital integer,
    long_term_internal_payables integer,
    long_term_unearned_revenue integer,
    other_long_term_payables integer,
    long_term_borrowings_and_finance_leases integer,
    convertible_bonds integer,
    deferred_tax_liabilities integer,
    long_term_provisions integer,
    science_and_technology_development_fund integer,
    provision_for_job_loss_allowance integer,
    voting_common_shares integer,
    preferred_shares integer,
    share_premium integer,
    convertible_bond_options integer,
    other_owner_equity integer,
    treasury_shares integer,
    revaluation_reserve integer,
    foreign_exchange_difference integer,
    development_investment_fund integer,
    enterprise_restructuring_support_fund integer,
    other_equity_funds integer,
    undistributed_profit_after_tax integer,
    construction_investment_capital integer,
    non_controlling_interests integer,
    financial_reserve_fund integer,
    funding_sources integer,
    funding_sources_for_fixed_assets integer,
    revenue_from_sales_and_services integer,
    deductions_from_revenue integer,
    net_revenue_from_sales_and_services integer,
    cost_of_goods_sold integer,
    gross_profit_from_sales_and_services integer,
    financial_income integer,
    financial_expenses integer,
    interest_expenses integer,
    share_of_profit_loss_in_associates integer,
    selling_expenses integer,
    general_and_administrative_expenses integer,
    net_profit_from_business_activities integer,
    other_income integer,
    other_expenses integer,
    other_profit integer,
    total_accounting_profit_before_tax integer,
    current_corporate_income_tax_expense integer,
    deferred_corporate_income_tax_expense integer,
    profit_after_corporate_income_tax integer,
    minority_interest integer,
    profit_after_tax_of_parent_company_shareholders integer,
    basic_earnings_per_share integer,
    diluted_earnings_per_share integer,
    profit_before_tax integer,
    depreciation_of_fixed_assets_and_investment_properties integer,
    provisions integer,
    foreign_exchange_gain_loss integer,
    investment_gain_loss integer,
    gain_loss_from_disposal_of_fixed_assets integer,
    interest_income_and_dividends integer,
    goodwill_amortization integer,
    adjustments_for_other_items integer,
    profit_from_business_activities_before_changes_in_working_capit integer,
    increase_decrease_in_receivables integer,
    increase_decrease_in_inventories integer,
    increase_decrease_in_payables integer,
    increase_decrease_in_prepaid_expenses integer,
    increase_decrease_in_trading_securities integer,
    interest_paid integer,
    corporate_income_tax_paid integer,
    other_cash_receipts_from_business_activities integer,
    other_cash_payments_for_business_activities integer,
    net_cash_flow_from_business_activities integer,
    cash_payments_for_purchase_of_fixed_assets_and_other_long_term_ integer,
    cash_receipts_from_disposal_of_fixed_assets_and_other_long_term integer,
    cash_payments_for_loans_and_purchase_of_debt_instruments_of_oth integer,
    cash_receipts_from_loans_and_sale_of_debt_instruments_of_other_ integer,
    cash_payments_for_investments_in_other_entities integer,
    cash_receipts_from_investments_in_other_entities integer,
    interest_and_dividends_received integer,
    increase_decrease_in_term_deposits integer,
    purchase_of_minority_interests_in_subsidiaries integer,
    other_cash_receipts_from_investment_activities integer,
    other_cash_payments_for_investment_activities integer,
    net_cash_flow_from_investment_activities integer,
    cash_receipts_from_issuance_of_shares_and_owner_contributions integer,
    cash_payments_for_owner_contributions_and_repurchase_of_issued_ integer,
    cash_receipts_from_borrowings integer,
    principal_repayments_of_borrowings integer,
    principal_repayments_of_finance_leases integer,
    dividends_and_profits_paid_to_owners integer,
    other_cash_receipts_from_financial_activities integer,
    other_cash_payments_for_financial_activities integer
);
 ,   DROP TABLE public.fact_financial_statement;
       public         heap r       postgres    false    5            �            1259    25102    fact_transaction_history    TABLE     u  CREATE TABLE public.fact_transaction_history (
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
 ,   DROP TABLE public.fact_transaction_history;
       public         heap r       postgres    false    5            �            1259    25105    news_news_id_seq    SEQUENCE     �   CREATE SEQUENCE public.news_news_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.news_news_id_seq;
       public               postgres    false    222    5            �           0    0    news_news_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.news_news_id_seq OWNED BY public.dim_enterprises_news.news_id;
          public               postgres    false    230            �           2604    25106    dim_enterprises_news news_id    DEFAULT     |   ALTER TABLE ONLY public.dim_enterprises_news ALTER COLUMN news_id SET DEFAULT nextval('public.news_news_id_seq'::regclass);
 K   ALTER TABLE public.dim_enterprises_news ALTER COLUMN news_id DROP DEFAULT;
       public               postgres    false    230    222            p          0    25044    dim_date 
   TABLE DATA           U   COPY public.dim_date (date_key, year, quarter, month, week, day_of_week) FROM stdin;
    public               postgres    false    217   ��       q          0    25047    dim_enterprises 
   TABLE DATA           �   COPY public.dim_enterprises (stock_code, industry_code, listing_date, enterprise_name, english_name, address, phone_number, email, website, tax_code, exchange) FROM stdin;
    public               postgres    false    218   ސ       r          0    25052 1   dim_enterprises_dividends_and_additional_issuance 
   TABLE DATA           �   COPY public.dim_enterprises_dividends_and_additional_issuance (stock_code, registration_date, event_type, event_content) FROM stdin;
    public               postgres    false    219   ��       s          0    25057    dim_enterprises_industries 
   TABLE DATA           b   COPY public.dim_enterprises_industries (industry_code, industry_name, industry_group) FROM stdin;
    public               postgres    false    220   �       t          0    25062    dim_enterprises_leaders_owners 
   TABLE DATA           ~   COPY public.dim_enterprises_leaders_owners (executive_id, stock_code, board, "position", shares, ownership_ratio) FROM stdin;
    public               postgres    false    221   5�       u          0    25067    dim_enterprises_news 
   TABLE DATA           l   COPY public.dim_enterprises_news (news_id, stock_code, uploaded_date, news_title, news_content) FROM stdin;
    public               postgres    false    222   R�       v          0    25072    dim_enterprises_personal_info 
   TABLE DATA           �   COPY public.dim_enterprises_personal_info (executive_id, full_name, date_of_birth, place_of_origin, residence, education, personal_assets) FROM stdin;
    public               postgres    false    223   o�       w          0    25077    dim_enterprises_related_person 
   TABLE DATA           |   COPY public.dim_enterprises_related_person (related_person_id, executive_id, related_person_name, relationship) FROM stdin;
    public               postgres    false    224   ��       x          0    25082    dim_enterprises_sub_companies 
   TABLE DATA           �   COPY public.dim_enterprises_sub_companies (parent_stock_code, sub_company_name, company_type, associated_company_stock_code, charter_capital, contributed_capital, ownership_ratio) FROM stdin;
    public               postgres    false    225   ��       y          0    25087 !   dividends_and_additional_issuance 
   TABLE DATA           u   COPY public.dividends_and_additional_issuance (stock_code, registration_date, event_type, event_content) FROM stdin;
    public               postgres    false    226   Ƒ       z          0    25092    enterprises 
   TABLE DATA           �   COPY public.enterprises (stock_code, industry_code, listing_date, enterprise_name, english_name, address, phone_number, email, website, tax_code, exchange) FROM stdin;
    public               postgres    false    227   �       {          0    25097    fact_financial_statement 
   TABLE DATA             COPY public.fact_financial_statement (stock_code, financial_year, cash, cash_equivalents, trading_securities, provision_for_trading_securities_devaluation, held_to_maturity_investments, short_term_receivables_from_customers, short_term_advance_payments_to_suppliers, short_term_internal_receivables, receivables_under_construction_contracts, short_term_loan_receivables, other_short_term_receivables, provision_for_short_term_doubtful_debts, assets_pending_resolution, inventories, short_term_prepaid_expenses, deductible_vat, taxes_and_other_receivables_from_state, government_bond_repurchase_transactions, other_current_assets, non_current_assets, long_term_receivables_from_customers, long_term_advance_payments_to_suppliers, capital_in_subsidiaries, long_term_internal_receivables, long_term_loan_receivables, other_long_term_receivables, provision_for_long_term_doubtful_debts, tangible_fixed_assets, finance_leased_fixed_assets, intangible_fixed_assets, investment_properties, long_term_work_in_progress, construction_in_progress, investments_in_subsidiaries, investments_in_associates_and_joint_ventures, investments_in_other_entities, provision_for_long_term_investments, other_long_term_investments, long_term_prepaid_expenses, deferred_tax_assets, long_term_spare_parts_and_supplies, other_non_current_assets, goodwill, short_term_payables_to_suppliers, short_term_advance_payments_from_customers, taxes_and_other_payables_to_state, payables_to_employees, short_term_accrued_expenses, short_term_internal_payables, payables_under_construction_contracts, short_term_unearned_revenue, other_short_term_payables, short_term_borrowings_and_finance_leases, short_term_provisions, bonus_and_welfare_funds, price_stabilization_fund, long_term_payables_to_suppliers, long_term_advance_payments_from_customers, long_term_accrued_expenses, internal_payables_for_business_capital, long_term_internal_payables, long_term_unearned_revenue, other_long_term_payables, long_term_borrowings_and_finance_leases, convertible_bonds, deferred_tax_liabilities, long_term_provisions, science_and_technology_development_fund, provision_for_job_loss_allowance, voting_common_shares, preferred_shares, share_premium, convertible_bond_options, other_owner_equity, treasury_shares, revaluation_reserve, foreign_exchange_difference, development_investment_fund, enterprise_restructuring_support_fund, other_equity_funds, undistributed_profit_after_tax, construction_investment_capital, non_controlling_interests, financial_reserve_fund, funding_sources, funding_sources_for_fixed_assets, revenue_from_sales_and_services, deductions_from_revenue, net_revenue_from_sales_and_services, cost_of_goods_sold, gross_profit_from_sales_and_services, financial_income, financial_expenses, interest_expenses, share_of_profit_loss_in_associates, selling_expenses, general_and_administrative_expenses, net_profit_from_business_activities, other_income, other_expenses, other_profit, total_accounting_profit_before_tax, current_corporate_income_tax_expense, deferred_corporate_income_tax_expense, profit_after_corporate_income_tax, minority_interest, profit_after_tax_of_parent_company_shareholders, basic_earnings_per_share, diluted_earnings_per_share, profit_before_tax, depreciation_of_fixed_assets_and_investment_properties, provisions, foreign_exchange_gain_loss, investment_gain_loss, gain_loss_from_disposal_of_fixed_assets, interest_income_and_dividends, goodwill_amortization, adjustments_for_other_items, profit_from_business_activities_before_changes_in_working_capit, increase_decrease_in_receivables, increase_decrease_in_inventories, increase_decrease_in_payables, increase_decrease_in_prepaid_expenses, increase_decrease_in_trading_securities, interest_paid, corporate_income_tax_paid, other_cash_receipts_from_business_activities, other_cash_payments_for_business_activities, net_cash_flow_from_business_activities, cash_payments_for_purchase_of_fixed_assets_and_other_long_term_, cash_receipts_from_disposal_of_fixed_assets_and_other_long_term, cash_payments_for_loans_and_purchase_of_debt_instruments_of_oth, cash_receipts_from_loans_and_sale_of_debt_instruments_of_other_, cash_payments_for_investments_in_other_entities, cash_receipts_from_investments_in_other_entities, interest_and_dividends_received, increase_decrease_in_term_deposits, purchase_of_minority_interests_in_subsidiaries, other_cash_receipts_from_investment_activities, other_cash_payments_for_investment_activities, net_cash_flow_from_investment_activities, cash_receipts_from_issuance_of_shares_and_owner_contributions, cash_payments_for_owner_contributions_and_repurchase_of_issued_, cash_receipts_from_borrowings, principal_repayments_of_borrowings, principal_repayments_of_finance_leases, dividends_and_profits_paid_to_owners, other_cash_receipts_from_financial_activities, other_cash_payments_for_financial_activities) FROM stdin;
    public               postgres    false    228    �       |          0    25102    fact_transaction_history 
   TABLE DATA           $  COPY public.fact_transaction_history (transaction_date, stock_code, open_price, ref_price, ceiling, floor, high, low, matched_qty, matched_amount, negotiated_qty, negotiated_amount, buy_orders, buy_qty, sell_orders, sell_qty, net_qty, foreign_net_qty, foreign_net_amount, foreign_buy_qty, foreign_buy_amount, foreign_sell_qty, foreign_sell_amount, remaining_foreign_room, current_foreign_ownership, proprietary_net_qty, proprietary_net_amount, proprietary_buy_qty, proprietary_buy_amount, proprietary_sell_qty, proprietary_sell_amount) FROM stdin;
    public               postgres    false    229   �       �           0    0    news_news_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.news_news_id_seq', 1, false);
          public               postgres    false    230            �           2606    25108    dim_date dim_date_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT dim_date_pkey PRIMARY KEY (date_key);
 @   ALTER TABLE ONLY public.dim_date DROP CONSTRAINT dim_date_pkey;
       public                 postgres    false    217            �           2606    25110 X   dim_enterprises_dividends_and_additional_issuance dividends_and_additional_issuance_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_dividends_and_additional_issuance
    ADD CONSTRAINT dividends_and_additional_issuance_pkey PRIMARY KEY (stock_code, registration_date, event_type);
 �   ALTER TABLE ONLY public.dim_enterprises_dividends_and_additional_issuance DROP CONSTRAINT dividends_and_additional_issuance_pkey;
       public                 postgres    false    219    219    219            �           2606    25112     dim_enterprises enterprises_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.dim_enterprises
    ADD CONSTRAINT enterprises_pkey PRIMARY KEY (stock_code);
 J   ALTER TABLE ONLY public.dim_enterprises DROP CONSTRAINT enterprises_pkey;
       public                 postgres    false    218            �           2606    25114 6   fact_financial_statement fact_financial_statement_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.fact_financial_statement
    ADD CONSTRAINT fact_financial_statement_pkey PRIMARY KEY (stock_code, financial_year);
 `   ALTER TABLE ONLY public.fact_financial_statement DROP CONSTRAINT fact_financial_statement_pkey;
       public                 postgres    false    228    228            �           2606    25116 *   dim_enterprises_industries industries_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY public.dim_enterprises_industries
    ADD CONSTRAINT industries_pkey PRIMARY KEY (industry_code);
 T   ALTER TABLE ONLY public.dim_enterprises_industries DROP CONSTRAINT industries_pkey;
       public                 postgres    false    220            �           2606    25118 2   dim_enterprises_leaders_owners leaders_owners_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_leaders_owners
    ADD CONSTRAINT leaders_owners_pkey PRIMARY KEY (executive_id, stock_code);
 \   ALTER TABLE ONLY public.dim_enterprises_leaders_owners DROP CONSTRAINT leaders_owners_pkey;
       public                 postgres    false    221    221            �           2606    25120    dim_enterprises_news news_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public.dim_enterprises_news
    ADD CONSTRAINT news_pkey PRIMARY KEY (news_id);
 H   ALTER TABLE ONLY public.dim_enterprises_news DROP CONSTRAINT news_pkey;
       public                 postgres    false    222            �           2606    25122 0   dim_enterprises_personal_info personal_info_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.dim_enterprises_personal_info
    ADD CONSTRAINT personal_info_pkey PRIMARY KEY (executive_id);
 Z   ALTER TABLE ONLY public.dim_enterprises_personal_info DROP CONSTRAINT personal_info_pkey;
       public                 postgres    false    223            �           2606    25124 2   dim_enterprises_related_person related_person_pkey 
   CONSTRAINT        ALTER TABLE ONLY public.dim_enterprises_related_person
    ADD CONSTRAINT related_person_pkey PRIMARY KEY (related_person_id);
 \   ALTER TABLE ONLY public.dim_enterprises_related_person DROP CONSTRAINT related_person_pkey;
       public                 postgres    false    224            �           2606    25126 0   dim_enterprises_sub_companies sub_companies_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_sub_companies
    ADD CONSTRAINT sub_companies_pkey PRIMARY KEY (parent_stock_code, sub_company_name);
 Z   ALTER TABLE ONLY public.dim_enterprises_sub_companies DROP CONSTRAINT sub_companies_pkey;
       public                 postgres    false    225    225            �           2606    25128 1   fact_transaction_history transaction_history_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.fact_transaction_history
    ADD CONSTRAINT transaction_history_pkey PRIMARY KEY (transaction_date, stock_code);
 [   ALTER TABLE ONLY public.fact_transaction_history DROP CONSTRAINT transaction_history_pkey;
       public                 postgres    false    229    229            �           2606    25129 j   dim_enterprises_dividends_and_additional_issuance dividends_and_additional_issuance_registration_date_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_dividends_and_additional_issuance
    ADD CONSTRAINT dividends_and_additional_issuance_registration_date_fkey FOREIGN KEY (registration_date) REFERENCES public.dim_date(date_key);
 �   ALTER TABLE ONLY public.dim_enterprises_dividends_and_additional_issuance DROP CONSTRAINT dividends_and_additional_issuance_registration_date_fkey;
       public               postgres    false    217    3260    219            �           2606    25134 c   dim_enterprises_dividends_and_additional_issuance dividends_and_additional_issuance_stock_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_dividends_and_additional_issuance
    ADD CONSTRAINT dividends_and_additional_issuance_stock_code_fkey FOREIGN KEY (stock_code) REFERENCES public.dim_enterprises(stock_code);
 �   ALTER TABLE ONLY public.dim_enterprises_dividends_and_additional_issuance DROP CONSTRAINT dividends_and_additional_issuance_stock_code_fkey;
       public               postgres    false    3262    219    218            �           2606    25139 .   dim_enterprises enterprises_industry_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises
    ADD CONSTRAINT enterprises_industry_code_fkey FOREIGN KEY (industry_code) REFERENCES public.dim_enterprises_industries(industry_code);
 X   ALTER TABLE ONLY public.dim_enterprises DROP CONSTRAINT enterprises_industry_code_fkey;
       public               postgres    false    220    218    3266            �           2606    25144 -   dim_enterprises enterprises_listing_date_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises
    ADD CONSTRAINT enterprises_listing_date_fkey FOREIGN KEY (listing_date) REFERENCES public.dim_date(date_key);
 W   ALTER TABLE ONLY public.dim_enterprises DROP CONSTRAINT enterprises_listing_date_fkey;
       public               postgres    false    217    3260    218            �           2606    25149 =   fact_financial_statement fact_financial_statement_dim_date_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.fact_financial_statement
    ADD CONSTRAINT fact_financial_statement_dim_date_fk FOREIGN KEY (financial_year) REFERENCES public.dim_date(date_key) ON UPDATE RESTRICT ON DELETE RESTRICT;
 g   ALTER TABLE ONLY public.fact_financial_statement DROP CONSTRAINT fact_financial_statement_dim_date_fk;
       public               postgres    false    228    217    3260            �           2606    25154 D   fact_financial_statement fact_financial_statement_dim_enterprises_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.fact_financial_statement
    ADD CONSTRAINT fact_financial_statement_dim_enterprises_fk FOREIGN KEY (stock_code) REFERENCES public.dim_enterprises(stock_code) ON UPDATE RESTRICT ON DELETE RESTRICT;
 n   ALTER TABLE ONLY public.fact_financial_statement DROP CONSTRAINT fact_financial_statement_dim_enterprises_fk;
       public               postgres    false    228    3262    218            �           2606    25159 ?   dim_enterprises_leaders_owners leaders_owners_executive_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_leaders_owners
    ADD CONSTRAINT leaders_owners_executive_id_fkey FOREIGN KEY (executive_id) REFERENCES public.dim_enterprises_personal_info(executive_id);
 i   ALTER TABLE ONLY public.dim_enterprises_leaders_owners DROP CONSTRAINT leaders_owners_executive_id_fkey;
       public               postgres    false    221    3272    223            �           2606    25164 =   dim_enterprises_leaders_owners leaders_owners_stock_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_leaders_owners
    ADD CONSTRAINT leaders_owners_stock_code_fkey FOREIGN KEY (stock_code) REFERENCES public.dim_enterprises(stock_code);
 g   ALTER TABLE ONLY public.dim_enterprises_leaders_owners DROP CONSTRAINT leaders_owners_stock_code_fkey;
       public               postgres    false    3262    218    221            �           2606    25169 )   dim_enterprises_news news_stock_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_news
    ADD CONSTRAINT news_stock_code_fkey FOREIGN KEY (stock_code) REFERENCES public.dim_enterprises(stock_code);
 S   ALTER TABLE ONLY public.dim_enterprises_news DROP CONSTRAINT news_stock_code_fkey;
       public               postgres    false    3262    218    222            �           2606    25174 ,   dim_enterprises_news news_uploaded_date_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_news
    ADD CONSTRAINT news_uploaded_date_fkey FOREIGN KEY (uploaded_date) REFERENCES public.dim_date(date_key);
 V   ALTER TABLE ONLY public.dim_enterprises_news DROP CONSTRAINT news_uploaded_date_fkey;
       public               postgres    false    3260    222    217            �           2606    25179 ?   dim_enterprises_related_person related_person_executive_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_related_person
    ADD CONSTRAINT related_person_executive_id_fkey FOREIGN KEY (executive_id) REFERENCES public.dim_enterprises_personal_info(executive_id);
 i   ALTER TABLE ONLY public.dim_enterprises_related_person DROP CONSTRAINT related_person_executive_id_fkey;
       public               postgres    false    3272    223    224            �           2606    25184 B   dim_enterprises_sub_companies sub_companies_parent_stock_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dim_enterprises_sub_companies
    ADD CONSTRAINT sub_companies_parent_stock_code_fkey FOREIGN KEY (parent_stock_code) REFERENCES public.dim_enterprises(stock_code);
 l   ALTER TABLE ONLY public.dim_enterprises_sub_companies DROP CONSTRAINT sub_companies_parent_stock_code_fkey;
       public               postgres    false    3262    218    225            �           2606    25189 <   fact_transaction_history transaction_history_stock_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.fact_transaction_history
    ADD CONSTRAINT transaction_history_stock_code_fkey FOREIGN KEY (stock_code) REFERENCES public.dim_enterprises(stock_code);
 f   ALTER TABLE ONLY public.fact_transaction_history DROP CONSTRAINT transaction_history_stock_code_fkey;
       public               postgres    false    229    218    3262            �           2606    25194 B   fact_transaction_history transaction_history_transaction_date_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.fact_transaction_history
    ADD CONSTRAINT transaction_history_transaction_date_fkey FOREIGN KEY (transaction_date) REFERENCES public.dim_date(date_key);
 l   ALTER TABLE ONLY public.fact_transaction_history DROP CONSTRAINT transaction_history_transaction_date_fkey;
       public               postgres    false    217    229    3260            p      x������ � �      q      x������ � �      r      x������ � �      s      x������ � �      t      x������ � �      u      x������ � �      v      x������ � �      w      x������ � �      x      x������ � �      y      x������ � �      z      x������ � �      {      x������ � �      |      x������ � �     