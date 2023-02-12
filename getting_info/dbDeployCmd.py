create_tables_query = """create table FORMS_TABLE
(
    form_id              bigint auto_increment comment 'system form id'
        primary key,
    vk_form_id           bigint          not null comment 'vk form id',
    form_vk_created_date bigint          null comment 'When form was created at VK',
    form_scrapped_date   bigint          not null comment 'When form was scrapped by system',
    multiple_answers     enum ('0', '1') not null comment 'User can select several answers',
    form_content         text            null,
    constraint FORMS_TABLE_pk
        unique (vk_form_id)
);

create index FORMS_TABLE_vk_form_id_index
    on FORMS_TABLE (vk_form_id);


create table VK_forms_scrapper.FORMS_DETAIL_TABLE
(
    answer_id    bigint auto_increment comment 'system answer id',
    vk_answer_id bigint not null comment 'vk answer id',
    form_id      bigint not null comment 'system linked form id',
    vk_form_id   bigint null comment 'vk linked form id',
    answer_content text,
    constraint FORMS_DETAIL_TABLE_pk
        primary key (answer_id)
);


create table VK_forms_scrapper.USER_TABLE
(
    user_id                bigint auto_increment comment 'system user id',
    vk_user_id             bigint                  not null comment 'vk user id',
    user_vk_profile_url    text                    null comment 'user vk profile url',
    user_first_name        text                    null comment 'user name',
    user_sec_name          text                    null comment 'user sec name',
    user_sex               ENUM ('male', 'female') null,
    user_birth_date        text                    null,
    user_city              text                    null,
    user_country           text                    null,
    user_job_place         text                    null,
    user_education_place   text                    null,
    user_number_of_friends int                     null,
    user_status            text                    null,
    constraint USER_TABLE_pk
        primary key (user_id),
    constraint USER_TABLE_pk
        unique (vk_user_id)
);

create table VK_forms_scrapper.USER_ANSWERS_TABLE
(
    record_id    bigint auto_increment,
    user_id      bigint not null,
    vk_user_id   bigint not null,
    answer_id    bigint not null,
    vk_answer_id bigint not null,
    form_id      bigint null,
    vk_form_id   bigint null,
    constraint USER_ANSWERS_TABLE_pk
        primary key (record_id)
);

# alter table VK_forms_scrapper.FORMS_DETAIL_TABLE
#     add constraint detail_to_main_system
#         foreign key (form_id) references VK_forms_scrapper.FORMS_TABLE (form_id);
#
# alter table VK_forms_scrapper.FORMS_DETAIL_TABLE
#     add constraint detail_to_main_vk
#         foreign key (vk_form_id) references VK_forms_scrapper.FORMS_TABLE (vk_form_id);

# alter table VK_forms_scrapper.FORMS_DETAIL_TABLE
#     drop foreign key detail_to_main_system;

alter table VK_forms_scrapper.FORMS_DETAIL_TABLE
    add constraint detail_to_main_system
        foreign key (form_id) references VK_forms_scrapper.FORMS_TABLE (form_id)
            on delete cascade;

# alter table VK_forms_scrapper.FORMS_DETAIL_TABLE
#     drop foreign key detail_to_main_vk;

alter table VK_forms_scrapper.FORMS_DETAIL_TABLE
    add constraint detail_to_main_vk
        foreign key (vk_form_id) references VK_forms_scrapper.FORMS_TABLE (vk_form_id)
            on delete cascade;

alter table VK_forms_scrapper.USER_ANSWERS_TABLE
    add constraint ans_to_ans_system
        foreign key (answer_id) references VK_forms_scrapper.FORMS_DETAIL_TABLE (answer_id)
            on delete cascade;


alter table VK_forms_scrapper.USER_ANSWERS_TABLE
    add constraint ans_to_forms_system
        foreign key (form_id) references VK_forms_scrapper.FORMS_TABLE (form_id)
            on delete cascade;

alter table VK_forms_scrapper.USER_ANSWERS_TABLE
    add constraint ans_to_forms_vk
        foreign key (vk_form_id) references VK_forms_scrapper.FORMS_TABLE (vk_form_id)
            on delete cascade;

alter table VK_forms_scrapper.USER_ANSWERS_TABLE
    add constraint ans_to_user_system
        foreign key (user_id) references VK_forms_scrapper.USER_TABLE (user_id)
            on delete cascade;

alter table VK_forms_scrapper.USER_ANSWERS_TABLE
    add constraint ans_to_user_vk
        foreign key (vk_user_id) references VK_forms_scrapper.USER_TABLE (vk_user_id)
            on delete cascade;

"""