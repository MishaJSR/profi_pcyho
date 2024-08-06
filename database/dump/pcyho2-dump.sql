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
    parent_id bigint,
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
89	Hhh	Subblock	f	2024-07-17 09:00:00	3	f	t	2024-08-06 12:58:39.816827	64bb1816-f836-4b94-983a-cd24e12968e7	1	t
85	Блок 2	Subblock	f	2024-07-16 09:00:00	2	f	t	2024-08-06 13:19:24.389332	d0e12083-d614-4f86-b940-6b1814269ada	26	t
70	Блок 1	Всем привет!\n\nНа связи Хэппи 😊\nСегодня мы начинаем проходить наш эмоциональный квест!\n\nИз первого видео вы узнаете, что такое эмоциональный интеллект и как он поможет вам в жизни.\nИ заодно познакомитесь с крутым инструментом, который научит вас погружаться в свои эмоции! \n\nА те, кто пройдет весь курс, откроет в себе такие суперспособности:\n➖ находить новых друзей и поддерживать дружбу\n➖ справляться со страхом, волнением и злостью\n➖ проявлять заботу и эмпатию к окружающим\n➖ чувствовать себя уверенно в новых ситуациях\n➖ мирно решать конфликты\n\nГотовы к приключению?\nТогда полетели вместе в мир эмоций ✨\n\nПриятного просмотра 😊	t	2024-07-15 09:00:00	1	f	t	2024-08-06 13:19:06.937562	40a3ee93-aaa1-4e73-8406-37d30529badf	277	f
\.


--
-- Data for Name: block_pool; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.block_pool (id, block_main_id, content, has_media, updated) FROM stdin;
18	85	**	t	2024-08-06 10:43:23.89714
19	85	**	t	2024-08-06 10:43:25.928404
20	85	**	t	2024-08-06 10:43:25.93743
21	85	**	t	2024-08-06 10:43:25.947047
22	85	**	t	2024-08-06 10:43:25.956748
17	85	Мы продолжаем наше увлекательное приключение в мир эмоций✨ \nСегодня ты познакомишься с потрясающей компанией, которая будет сопровождать тебя на квесте☺️ \nНаши герои помогут тебе лучше понять свои чувства и научат взаимодействовать с другими людьми. Каждый из них обладает уникальными особенностями. Понимание их характеров понадобится тебе для успешного прохождения испытаний. \n\nПодробнее о каждом герое читай в карточках!⬇️	t	2024-08-06 10:43:21.133175
23	89	Привет!\n\nВ предыдущих эпизодах мы узнали, что такое эмоциональный интеллект, как он работает и помогает в жизни, познакомились с Яной и персонажами, прошли интересные испытания и получили первые ачивки.\n\nТеперь пришло время заглянуть в себя. \nУ меня для тебя интересное задание, которое тебе точно понравится!\n\nЯ подготовила форму, где ты можешь оценить свои способности эмоционального интеллекта и узнать о себе что-то новое😉\n\nЗаполнение формы займет всего несколько минут, но ты сможешь лучше себя понять.\nХочешь стать эмоционально осознаннее? Тогда переходи по ссылке и начинай прямо сейчас!\n\nЖду твоих ответов! Удачи и до встречи в новой главе! 💕	t	2024-08-06 12:54:58.557451
24	89	https://forms.gle/ktSEHhuyimbAmzm68	f	2024-08-06 12:54:58.567302
\.


--
-- Data for Name: media_block; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_block (id, block_id, photo_id, video_id, updated) FROM stdin;
85	70	\N	BAACAgIAAxkBAAJ56GawASodx4HPsVR1XhHF8VfYwBeQAAI3XAACmsiBSRKn6_C8ql8TNQQ	2024-07-25 09:35:53.171222
124	70	AgACAgIAAxkBAAKHi2ax2MYp0Y1RHEh4cpFxnpUGOAGzAAKq4jEbTCqISSPTlZzrk0T7AQADAgADeQADNQQ	\N	2024-08-06 11:03:29.984429
126	74	AgACAgIAAxkBAAKIkWax29f2pFuAY79xsnOP51LbrCtuAAK64jEbTCqISe4OklCvH0amAQADAgADeQADNQQ	\N	2024-08-06 11:16:33.227457
\.


--
-- Data for Name: media_block_pool; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_block_pool (id, block_pool_id, photo_id, video_id, updated) FROM stdin;
30	18	AgACAgIAAxkBAAKGDmax098dpZrjmbMdC9jFn1OmOZmfAAJ64jEbTCqISWxYIectgUPnAQADAgADeQADNQQ	\N	2024-08-06 10:43:25.91745
31	18	AgACAgIAAxkBAAKGD2ax098qb5RC7eHvPL2vTjS66vFYAAJ74jEbTCqISa-ztXrpbdjxAQADAgADeQADNQQ	\N	2024-08-06 10:43:25.924932
32	19	AgACAgIAAxkBAAKGGmax0-xOQkMJwhGqQ46SApZmF2VdAAJY4jEbTCqIScPilfwQBDa6AQADAgADeQADNQQ	\N	2024-08-06 10:43:25.930962
33	19	AgACAgIAAxkBAAKGG2ax0-x_82720s2640Et51B0_CM7AAJZ4jEbTCqISZ6FKJuvXUNNAQADAgADeQADNQQ	\N	2024-08-06 10:43:25.934677
34	20	AgACAgIAAxkBAAKGJmax0_bJqaFl6Mm_cxiGW6i5CHSVAAJa4jEbTCqISaqFbQSbuSPWAQADAgADeQADNQQ	\N	2024-08-06 10:43:25.940217
35	20	AgACAgIAAxkBAAKGJ2ax0_aN7OKYvOfW46d8H7OkUAXCAAJb4jEbTCqISUgAAXuiKv7uHAEAAwIAA3kAAzUE	\N	2024-08-06 10:43:25.944262
36	21	AgACAgIAAxkBAAKGMmax1AABSokhjq2GXU5jwLZX5FTw4gACXeIxG0wqiEkHr89WiH9wAgEAAwIAA3kAAzUE	\N	2024-08-06 10:43:25.949736
37	21	AgACAgIAAxkBAAKGM2ax1AABm2_wDnkxwML0NzcVsVdVkQACXuIxG0wqiEnt-HFpC4003wEAAwIAA3kAAzUE	\N	2024-08-06 10:43:25.954051
38	22	AgACAgIAAxkBAAKGPmax1AvZe7YBGkI57lbjK9-VF1yFAAJW4jEbTCqISa962oeShahVAQADAgADeQADNQQ	\N	2024-08-06 10:43:25.959504
39	22	AgACAgIAAxkBAAKGP2ax1AubRFX_vq35DmPS46b2g9toAAJX4jEbTCqIScHzqFGbsSMIAQADAgADeQADNQQ	\N	2024-08-06 10:43:25.963677
21	17	AgACAgIAAxkBAAKH02ax2cx5F__TZJj45Q2jxBUU8cG1AAKv4jEbTCqISbIpdsBNn-j7AQADAgADeQADNQQ	\N	2024-08-06 10:29:25.653034
40	23	AgACAgIAAxkBAAKMTWax8szWN4vsPQcFeO1n9wLrvDt6AAK64jEbTCqISe4OklCvH0amAQADAgADeQADNQQ	\N	2024-08-06 12:54:58.562676
\.


--
-- Data for Name: media_task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.media_task (id, task_id, photo_id, updated) FROM stdin;
68	83	AgACAgIAAxkBAAJ_nmawxGtSAywaKh2U2XtYfIRIrxOmAAI04DEbmsiJSVRKTE1HvzwCAQADAgADeQADNQQ	2024-07-25 09:39:22.550923
69	84	AgACAgIAAxkBAAJ_n2awxGsCujcdo4ExUlXy9ebz1j-5AAI14DEbmsiJSV0Ps6QrWEquAQADAgADeQADNQQ	2024-07-25 09:39:46.001186
70	85	AgACAgIAAxkBAAJ_oGawxGvYoM1YmmtkbzGgoZl0IyWtAAI24DEbmsiJSZSGM2ktvKcMAQADAgADeQADNQQ	2024-07-25 09:40:12.502785
71	86	AgACAgIAAxkBAAJ_oWawxGv-KuCWYwRMYgIrbvx7AAG8RwACN-AxG5rIiUlNYCyLzPR97wEAAwIAA3kAAzUE	2024-07-25 09:40:36.944173
72	87	AgACAgIAAxkBAAJ_omawxGtw3QU88g4nXtbcu_oZMrxgAAI44DEbmsiJSR_kllekBZ6DAQADAgADeQADNQQ	2024-07-25 09:41:01.931167
\.


--
-- Data for Name: task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task (id, block_id, description, answer_mode, answers, answer, about, addition, points_for_task, updated, is_visible) FROM stdin;
86	85	*Как Давид может справиться с этой ситуацией и проявить себя на матче?*	Тест	1. Продолжить тренироваться, но быть с другом на связи, поддерживая его морально.\n2. Пропустить матч и провести время с другом.\n3. Подавить свои чувства и стараться быть сильным.\n4. Вспомнить о своей роли лидера команды и положительных сторонах матча.	14	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:40:36.934298	t
87	85	*Как София может использовать этот опыт для продвижения своего блога?*	Тест	1. Расслабиться, ведь успех уже пришел, и он никуда не денется.\n2. Поблагодарить своих подписчиков за поддержку.\n3. Постоянно нагружать себя работой, чтобы соответствовать высоким ожиданиям подписчиков.\n4. Подумать, а что именно понравилось аудитории и развивать эти сильные стороны дальше.	24	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:41:01.903498	t
84	85	*Что может предпринять Динара, чтобы справиться с ситуацией и выполнить домашку?*	Тест	1. Прикрикнуть на детишек, чтобы они поняли, что я занята важными делами.\n2. Позвонить маме и потребовать, чтобы она немедленно вернулась домой, иначе домашка не будет выполнена и учитель поставит двойку.\n3. Поговорить с сестрами и братишкой. Объяснить им, что ей нужно немного тишины и предложить сыграть во что-то более тихое.\n4. Найти баланс: поиграть немного с детьми, а потом сесть за уроки.	34	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:39:45.996938	t
85	85	*Как Филипп может использовать этот случай для дальнейшей прокачки своих знаний?*	Тест	1. Перестать общаться с теми, кто не может решать такие задачи, чтобы они не тянули его на дно.\n2. Понять, что помогло ему решить задачу, и применять этот подход к новым задачам в будущем.\n3. Поделиться своим опытом с одноклассниками или друзьями, чтобы помочь тем, кто испытывает сложности с решением таких задач.\n4. Прекратить ставить перед собой новые цели, ведь он и так лучший.	23	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:40:12.494196	t
83	85	*Что могла бы сделать Агата, чтобы помочь себе и подготовиться к выступлению?*	Тест	1. Поделиться с папой своими чувствами, чтобы получить его поддержку.\n2. Прекратить общение с мачехой, чтобы избежать конфликтов.\n3. Помедетировать или глубоко подышать перед репетициями и выступлением.\n4. Сократить время репетиций, чтобы уменьшить стресс перед выступлением.	13	\N	Выбери правильные ответы и напиши их цифры.	100	2024-07-25 09:39:22.539893	t
81	70	*Чем отличается эмоциональный интеллект от обычного интеллекта?*	Тест	1. Эмоциональный интеллект помогает нам решать математические задачки, а обычный интеллект отвечает за взаимодействие с людьми.\n2. Обычный интеллект отвечает за решение логических задач и запоминание информации, а эмоциональный интеллект позволяет нам понимать и управлять своими и чужими эмоциями.\n3. Эмоциональный интеллект отвечает за творческое мышление, а обычный интеллект — за физическую активность.	2	\N		100	2024-07-25 09:38:21.052978	t
82	70	*Ты совершенно не понимаешь новую тему на уроке и начинаешь чувствовать тревогу и неуверенность.\nКакие действия помогут тебе справиться с этими эмоциями и лучше понять тему урока?*	Тест	1. Сделать вид, что ты понимаешь тему, и не задавать никаких вопросов.\n2. Признать, что ты чувствуешь тревогу и обсудить материал с учителем или репетитором.\n3. Просто подождать, пока тема поменяется и с азартом включиться в изучение новой темы.\n4. Поговорить с тем, кто понял тему, чтобы он объяснил и поддержал по возможности.	24	\N		100	2024-07-25 09:38:45.179655	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, user_id, username, progress, is_subscribe, day_start_subscribe, day_end_subscribe, points, updated, id_last_block_send, user_class, parent_id, phone_number, user_callback, user_become_children, name_of_user, stop_spam, user_block_bot, user_tag) FROM stdin;
539	548349299	Михаил	4	t	\N	\N	0	2024-08-06 13:20:40.660975	89	Педагог	\N	\N	skip	t	\N	f	f	@mshsor
\.


--
-- Data for Name: users_task_progress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_task_progress (id, user_id, username, task_id, answer_mode, result, is_pass, updated, block_id) FROM stdin;
1206	548349299	Михаил	81	Тест	12	f	2024-08-06 13:19:12.025466	70
1207	548349299	Михаил	82	Тест	12	f	2024-08-06 13:19:14.969966	70
1208	548349299	Михаил	83	Тест	13	t	2024-08-06 13:20:01.230514	85
1209	548349299	Михаил	84	Тест	12	f	2024-08-06 13:20:04.354836	85
1210	548349299	Михаил	85	Тест	12	f	2024-08-06 13:20:11.078776	85
1211	548349299	Михаил	86	Тест	12	f	2024-08-06 13:20:13.610841	85
1212	548349299	Михаил	87	Тест	12	f	2024-08-06 13:20:16.075324	85
\.


--
-- Name: block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.block_id_seq', 89, true);


--
-- Name: block_pool_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.block_pool_id_seq', 24, true);


--
-- Name: media_block_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_block_id_seq', 126, true);


--
-- Name: media_block_pool_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.media_block_pool_id_seq', 40, true);


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

SELECT pg_catalog.setval('public.users_id_seq', 539, true);


--
-- Name: users_task_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_task_progress_id_seq', 1212, true);


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

