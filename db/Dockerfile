FROM mysql/mysql-server

ENV MYSQL_DATABASE="VK_forms_scrapper" \
    MYSQL_ROOT_PASSWORD="" \
    MYSQL_ROOT_HOST=localhost

COPY dbDeployPipeline.sql /docker-entrypoint-initdb.d

EXPOSE 3306