--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: block; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.block (
    id integer NOT NULL,
    block_name character varying(50) NOT NULL,
    content text NOT NULL,
    has_media boolean NOT NULL,
    date_to_post timestamp without time zone NOT NULL,
    progress_block integer NOT NULL,
    is_vebinar boolean NOT NULL,
    is_visible boolean NOT NULL,
    updated timestamp without time zone NOT NULL,
    callback_button_id text,
    count_send integer NOT NULL,
    is_sub_block boolean NOT NULL
);


ALTER TABLE public.block OWNER TO postgres;

--
-- Name: block_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.block_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.block_id_seq OWNER TO postgres;

--
-- Name: block_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.block_id_seq OWNED BY public.block.id;


--
-- Name: block_pool; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.block_pool (
    id integer NOT NULL,
    block_main_id integer NOT NULL,
    content text NOT NULL,
    has_media boolean NOT NULL,
    updated timestamp without time zone NOT NULL
);


ALTER TABLE public.block_pool OWNER TO postgres;

--
-- Name: block_pool_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.block_pool_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.block_pool_id_seq OWNER TO postgres;

--
-- Name: block_pool_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.block_pool_id_seq OWNED BY public.block_pool.id;


--
-- Name: media_block; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.media_block (
    id integer NOT NULL,
    block_id integer NOT NULL,
    photo_id text,
    video_id text,
    updated timestamp without time zone NOT NULL
);


ALTER TABLE public.media_block OWNER TO postgres;

--
-- Name: media_block_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.media_block_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.media_block_id_seq OWNER TO postgres;

--
-- Name: media_block_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.media_block_id_seq OWNED BY public.media_block.id;


--
-- Name: media_block_pool; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.media_block_pool (
    id integer NOT NULL,
    block_pool_id integer NOT NULL,
    photo_id text,
    video_id text,
    updated timestamp without time zone NOT NULL
);


ALTER TABLE public.media_block_pool OWNER TO postgres;

--
-- Name: media_block_pool_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.media_block_pool_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.media_block_pool_id_seq OWNER TO postgres;

--
-- Name: media_block_pool_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.media_block_pool_id_seq OWNED BY public.media_block_pool.id;


--
-- Name: media_task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.media_task (
    id integer NOT NULL,
    task_id integer NOT NULL,
    photo_id text NOT NULL,
    updated timestamp without time zone NOT NULL
);


ALTER TABLE public.media_task OWNER TO postgres;

--
-- Name: media_task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.media_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.media_task_id_seq OWNER TO postgres;

--
-- Name: media_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.media_task_id_seq OWNED BY public.media_task.id;


--
-- Name: task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task (
    id integer NOT NULL,
    block_id integer NOT NULL,
    description text NOT NULL,
    answer_mode character varying(20) NOT NULL,
    answers text,
    answer text NOT NULL,
    about text,
    addition text,
    points_for_task integer NOT NULL,
    updated timestamp without time zone NOT NULL,
    is_visible boolean NOT NULL
);


ALTER TABLE public.task OWNER TO postgres;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_id_seq OWNER TO postgres;

--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    username text NOT NULL,
    progress integer NOT NULL,
    is_subscribe boolean NOT NULL,
    day_start_subscribe timestamp without time zone,
    day_end_subscribe timestamp without time zone,
    points integer NOT NULL,
    updated timestamp without time zone NOT NULL,
    id_last_block_send integer NOT NULL,
    user_class text NOT NULL,
    parent_id integer,
    phone_number text,
    user_callback text,
    user_become_children boolean NOT NULL,
    name_of_user text,
    stop_spam boolean NOT NULL,
    user_block_bot boolean NOT NULL,
    user_tag text
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users_task_progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_task_progress (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    username text NOT NULL,
    task_id integer NOT NULL,
    answer_mode character varying(20) NOT NULL,
    result text NOT NULL,
    is_pass boolean NOT NULL,
    updated timestamp without time zone NOT NULL,
    block_id integer NOT NULL
);


ALTER TABLE public.users_task_progress OWNER TO postgres;

--
-- Name: users_task_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_task_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_task_progress_id_seq OWNER TO postgres;

--
-- Name: users_task_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_task_progress_id_seq OWNED BY public.users_task_progress.id;


--
-- Name: block id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.block ALTER COLUMN id SET DEFAULT nextval('public.block_id_seq'::regclass);


--
-- Name: block_pool id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.block_pool ALTER COLUMN id SET DEFAULT nextval('public.block_pool_id_seq'::regclass);


--
-- Name: media_block id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_block ALTER COLUMN id SET DEFAULT nextval('public.media_block_id_seq'::regclass);


--
-- Name: media_block_pool id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_block_pool ALTER COLUMN id SET DEFAULT nextval('public.media_block_pool_id_seq'::regclass);


--
-- Name: media_task id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_task ALTER COLUMN id SET DEFAULT nextval('public.media_task_id_seq'::regclass);


--
-- Name: task id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: users_task_progress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_task_progress ALTER COLUMN id SET DEFAULT nextval('public.users_task_progress_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: block; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.block (id, block_name, content, has_media, date_to_post, progress_block, is_vebinar, is_visible, updated, callback_button_id, count_send, is_sub_block) FROM stdin;
74	Блок 3	Привет!\n\nВ предыдущих эпизодах мы узнали, что такое эмоциональный интеллект, как он работает и помогает в жизни, познакомились с Яной и персонажами, прошли интересные испытания и получили первые ачивки.\n\nТеперь пришло время заглянуть в себя. \nУ меня для тебя интересное задание, которое тебе точно понравится!\n\nЯ подготовила форму, где ты можешь оценить свои способности эмоционального интеллекта и узнать о себе что-то новое😉\n\nЗаполнение формы займет всего несколько минут, но ты сможешь лучше себя понять.\nХочешь стать эмоционально осознаннее? Тогда переходи по ссылке и начинай прямо сейчас!\n\nЖду твоих ответов! Удачи и до встречи в новой главе! 💕\n\nhttps://forms.gle/ktSEHhuyimbAmzm68	f	2024-07-17 09:00:00	3	f	t	2024-07-29 14:41:01.741367	3de7958d-1389-42cf-b456-94af481be968	0	f
70	Блок 1	Всем привет!\n\nНа связи Хэппи 😊\nСегодня мы начинаем проходить наш эмоциональный квест!\n\nИз первого видео вы узнаете, что такое эмоциональный интеллект и как он поможет вам в жизни.\nИ заодно познакомитесь с крутым инструментом, который научит вас погружаться в свои эмоции! \n\nА те, кто пройдет весь курс, откроет в себе такие суперспособности:\n➖ находить новых друзей и поддерживать дружбу\n➖ справляться со страхом, волнением и злостью\n➖ проявлять заботу и эмпатию к окружающим\n➖ чувствовать себя уверенно в новых ситуациях\n➖ мирно решать конфликты\n\nГотовы к приключению?\nТогда полетели вместе в мир эмоций ✨\n\nПриятного просмотра 😊	t	2024-07-15 09:00:00	1	f	t	2024-08-05 01:32:41.056097	40a3ee93-aaa1-4e73-8406-37d30529badf	172	f
79	Блок 2	Привет, друзья 👋\n\nНа связи Хэппи, ваш проводник в мир эмоционального интеллекта.\nСегодня мы продолжим наше увлекательное приключение в мир эмоций и познакомимся с потрясающей компанией, которая будут сопровождать вас на курсе.\n\nОни помогут вам лучше понять свои чувства и научат взаимодействовать с другими людьми.\nВедь каждый наш герой обладает уникальными особенностями!\nА ещё — понимание их характеров пригодится вам для успешного выполнения заданий.\n\nПодробнее о каждом герое читайте в наших карточках 👆\nА затем практикуйтесь и решайте кейсы, в которых участвуют наши ребята.\nУ вас все получится 💯	t	2024-07-16 09:00:00	2	f	t	2024-08-05 01:23:45.90358	1d544258-5190-4641-811c-405c16a95359	3	f
\.


--
-- Data for Name: block_pool; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.block_pool (id, block_main_id, content, has_media, updated) FROM stdin;
\.


--
-- Data for Name: media_block; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_block (id, block_id, photo_id, video_id, updated) FROM stdin;
84	70	AgACAgIAAxkBAAJNL2ah8jcoZsHxD8QKlMKQfOpIJ22nAAJF4TEbR1wAAUkBeb9H7bw22AEAAwIAA3kAAzUE	\N	2024-07-25 09:35:53.155264
86	71	AgACAgIAAxkBAAJNamah8qXO39AT_c2hAW6RgaVXXqwJAAIB3DEbZhkRSdKsFhGk1sf0AQADAgADeQADNQQ	\N	2024-07-25 09:37:40.908349
87	71	AgACAgIAAxkBAAJNa2ah8qWtSYOjEDpO1FDwZ6pnl3uxAAIC3DEbZhkRSWVI77TOz4sbAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.914023
88	71	AgACAgIAAxkBAAJNbGah8qVdnHIdQRQiD1dN1gPPbp5mAAID3DEbZhkRSaYCivQXGqknAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.91847
89	71	AgACAgIAAxkBAAJNbWah8qWcoolHQT2z0HX0DhuoTcqvAAIE3DEbZhkRSSh_hE9sbNdEAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.922322
90	71	AgACAgIAAxkBAAJNbmah8qWteq6-LEcKGfueEntrhDKLAAIF3DEbZhkRSbL_DP5bFWvpAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.926161
91	71	AgACAgIAAxkBAAJNb2ah8qVTkGXk3WKMFOh0VmMXU7p6AAIG3DEbZhkRSd5prZWgvGHyAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.929791
92	71	AgACAgIAAxkBAAJNcGah8qU0UOo1d-ib7igHlOdv-H3LAAIH3DEbZhkRSeWNi3NO5SpNAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.932958
93	71	AgACAgIAAxkBAAJNcWah8qX_cOV8esvUWtJuVvJYHwL7AAII3DEbZhkRSesPVHRepFqEAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.93621
94	71	AgACAgIAAxkBAAJNcmah8qU5q-rlqjDnL0XTM30pNjG8AAIJ3DEbZhkRSWwXPctG63CWAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.939799
95	71	AgACAgIAAxkBAAJNc2ah8qXqcNyfY5YN1LjYTkzzjjXQAAIK3DEbZhkRSfsGlullhxoGAQADAgADeQADNQQ	\N	2024-07-25 09:37:40.943884
100	77	AgACAgIAAxkBAAJv_2as0UKxZxvBh88DWlh7JuwloYpoAAIe3DEb_61hSczznRle6I90AQADAgADeQADNQQ	\N	2024-08-02 15:30:16.945804
101	78	AgACAgIAAxkBAAJwOWas0jH8hAO9d1OeemtOBTxINgh9AAIi3DEb_61hSVa2lYnskmHsAQADAgADeQADNQQ	\N	2024-08-02 15:34:03.546973
102	79	AgACAgIAAxkBAAJ5dWav_wmpoIN05KPt2ugGm0WTWUPzAAJA4zEbmsiBSc1xfbLpVllNAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.004914
103	79	AgACAgIAAxkBAAJ5dmav_wmK-XCfKEH2RW3i-o_Ak6piAAJB4zEbmsiBSdmZQXWJeuWSAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.011299
104	79	AgACAgIAAxkBAAJ5d2av_wlswVfZvuRjNNggDZZP9bbdAAJC4zEbmsiBSeKFw9AszGiaAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.013912
105	79	AgACAgIAAxkBAAJ5eGav_wnDzVr8perDO-Rk3g60R9bHAAJD4zEbmsiBSdicZmbHrPTZAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.015482
106	79	AgACAgIAAxkBAAJ5eWav_wl_xH4HHETmAAENMZ6nOTOpWgACROMxG5rIgUlk8GlsZHrblwEAAwIAA3kAAzUE	\N	2024-08-05 01:22:30.017296
107	79	AgACAgIAAxkBAAJ5emav_wnMhIMkGTi2Dvg-jUXy0radAAJF4zEbmsiBSSVJXiDyddWHAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.018986
108	79	AgACAgIAAxkBAAJ5e2av_wm6PBn4movE_OvJPxHbJ9KQAAJG4zEbmsiBSdwpbVA9hb5MAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.020844
109	79	AgACAgIAAxkBAAJ5fGav_wkF_i25pRHd3WTDAr_q22ASAAJH4zEbmsiBSegvKZHhIL8yAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.022442
110	79	AgACAgIAAxkBAAJ5fWav_wkWAYgKqX_gfa-9ctAqcW5qAAJI4zEbmsiBSVOX8HNz_nVPAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.024234
111	79	AgACAgIAAxkBAAJ5fmav_wneNWzgtRZYaooLi80KKGFoAAJJ4zEbmsiBSYPOcAO5qwjAAQADAgADeQADNQQ	\N	2024-08-05 01:22:30.025936
85	70	\N	BAACAgIAAxkBAAJ56GawASodx4HPsVR1XhHF8VfYwBeQAAI3XAACmsiBSRKn6_C8ql8TNQQ	2024-07-25 09:35:53.171222
\.


--
-- Data for Name: media_block_pool; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_block_pool (id, block_pool_id, photo_id, video_id, updated) FROM stdin;
\.


--
-- Data for Name: media_task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_task (id, task_id, photo_id, updated) FROM stdin;
68	83	AgACAgIAAxkBAAJNwGah8xn-naz4PVtNzQu_YHTcFMwaAAIL3DEbZhkRST4ITS0i6yZMAQADAgADeQADNQQ	2024-07-25 09:39:22.550923
69	84	AgACAgIAAxkBAAJN0Gah8zGbKxqt_ginu397BAb1XBMIAAIM3DEbZhkRSWyHPX7b7y2DAQADAgADeQADNQQ	2024-07-25 09:39:46.001186
70	85	AgACAgIAAxkBAAJN4Gah80sIrd9rFlLupqZnfcgYAAExOQACDdwxG2YZEUkjGWX3hr4PqgEAAwIAA3gAAzUE	2024-07-25 09:40:12.502785
71	86	AgACAgIAAxkBAAJN8Gah82TazkCkIUF5VVVyPw1PLiUkAAIO3DEbZhkRSbF6qi1PSniIAQADAgADeQADNQQ	2024-07-25 09:40:36.944173
72	87	AgACAgIAAxkBAAJOAAFmofN9UQ1pOqqdUkwqlv8VoPaxmAACD9wxG2YZEUmqKm79lZQ0XAEAAwIAA3gAAzUE	2024-07-25 09:41:01.931167
\.


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task (id, block_id, description, answer_mode, answers, answer, about, addition, points_for_task, updated, is_visible) FROM stdin;
87	79	*Как София может использовать этот классный опыт для продвижения своего блога?*	Тест	1. Перестать стараться, ведь успех уже пришел и он никуда не денется\n2. Поблагодарить своих подписчиков за поддержку.\n3. Постоянно нагружать себя работой, чтобы соответствовать высоким ожиданиям подписчиков\n4. Подумать, а что именно понравилось аудитории и развивать эти сильные стороны дальше.	24	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:41:01.903498	t
86	79	*Что может сделать Давид, чтобы справиться с этой ситуацией и помочь себе подготовиться к важному матчу?*	Тест	1. Продолжать готовиться, но быть с другом на связи, поддерживая его морально\n2. Пропустить матч и провести время с другом.\n3. Подавлять свои чувства и просто стараться «быть сильным», ведь он лидер команды\n4. Вспомнить о положительных сторонах предстоящего матча и своей роли лидера команды	14	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:40:36.934298	t
83	79	*Что могла бы сделать Агата, чтобы помочь себе и подготовиться к выступлению?*	Тест	1. Поделиться с папой своими чувствами, чтобы получить его поддержку\n2. Прекратить общение с мачехой, чтобы избежать конфликтов.\n3. Помедетировать или глубоко подышать перед репетициями и выступлением.\n4. Сократить время репетиций, чтобы уменьшить стресс перед выступлением.	13	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:39:22.539893	t
81	70	*Чем отличается эмоциональный интеллект от обычного интеллекта?*	Тест	1. Эмоциональный интеллект помогает нам решать математические задачки, а обычный интеллект отвечает за взаимодействие с людьми\n2. Обычный интеллект отвечает за решение логических задач и запоминание информации, а эмоциональный интеллект позволяет нам понимать и управлять своими и чужими эмоциями\n3. Эмоциональный интеллект отвечает за творческое мышление, а обычный интеллект — за физическую активность.	2	\N		100	2024-07-25 09:38:21.052978	t
84	79	*Что может предпринять Динара, чтобы справиться с ситуацией и выполнить домашку?*	Тест	1. Прикрикнуть на детишек, чтобы они поняли, что я занята важными делами\n2. Позвонить маме и потребовать, чтобы она немедленно вернулась домой, иначе домашка не будет выполнена и учитель поставит двойку\n3. Поговорить с сестрами и братишкой. Объяснить им, что ей нужно немного тишины и предложить сыграть во что-то более тихое.\n4. Найти баланс: поиграть немного с детьми, а потом сесть за уроки.	34	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:39:45.996938	t
85	79	*Как Филипп может использовать этот случай для дальнейшей прокачки своих знаний?*	Тест	1. Перестать общаться с теми, кто не может решать такие задачи, чтобы они не тянули его на дно\n2. Понять, что помогло ему решить задачу, и применять этот подход к новым задачам в будущем\n3. Поделиться своим опытом с одноклассниками или друзьями, чтобы помочь тем, кто испытывает сложности с решением таких задач\n4. Посчитать это своим пиком и главным достижением и поэтому прекратить ставить перед собой новые цели. Ведь лучше этого триумфа уже не будет 	24	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:40:12.494196	t
82	70	*Ты совершенно не понимаешь новую тему на уроке и начинаешь чувствовать тревогу и неуверенность.\nКакие действия помогут тебе справиться с этими эмоциями и лучше понять тему урока?*	Тест	1. Сделать вид, что ты понимаешь тему, и не задавать никаких вопросов\n2. Признать, что ты чувствуешь тревогу и обсудить материал с учителем или репетитором\n3. Просто подождать, пока тема поменяется и с азартом включиться в изучение новой темы\n4. Поговорить с тем, кто понял тему, чтобы он объяснил и поддержал по возможности	24	\N		100	2024-07-25 09:38:45.179655	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, user_id, username, progress, is_subscribe, day_start_subscribe, day_end_subscribe, points, updated, id_last_block_send, user_class, parent_id, phone_number, user_callback, user_become_children, name_of_user, stop_spam, user_block_bot, user_tag) FROM stdin;
\.


--
-- Data for Name: users_task_progress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_task_progress (id, user_id, username, task_id, answer_mode, result, is_pass, updated, block_id) FROM stdin;
\.


--
-- Name: block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.block_id_seq', 80, true);


--
-- Name: block_pool_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.block_pool_id_seq', 10, true);


--
-- Name: media_block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_block_id_seq', 112, true);


--
-- Name: media_block_pool_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_block_pool_id_seq', 21, true);


--
-- Name: media_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_task_id_seq', 72, true);


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_id_seq', 88, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 412, true);


--
-- Name: users_task_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_task_progress_id_seq', 926, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: block block_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.block
    ADD CONSTRAINT block_pkey PRIMARY KEY (id);


--
-- Name: block_pool block_pool_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.block_pool
    ADD CONSTRAINT block_pool_pkey PRIMARY KEY (id);


--
-- Name: media_block media_block_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_block
    ADD CONSTRAINT media_block_pkey PRIMARY KEY (id);


--
-- Name: media_block_pool media_block_pool_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_block_pool
    ADD CONSTRAINT media_block_pool_pkey PRIMARY KEY (id);


--
-- Name: media_task media_task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.media_task
    ADD CONSTRAINT media_task_pkey PRIMARY KEY (id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_task_progress users_task_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_task_progress
    ADD CONSTRAINT users_task_progress_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

