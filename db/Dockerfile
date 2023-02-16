FROM mysql/mysql-server

ENV MYSQL_DATABASE="VK_forms_scrapper" \
    MYSQL_ROOT_PASSWORD="" \
    MYSQL_ROOT_HOST=localhost

# docker build -t local-mysql:1 ../VkFormsScrapper/db   DEVOPS GOVNO!!! RUN FROM ~/Developer/Projects/VkFormsScrapper 

#~/Developer/Projects/VkFormsScrapper │ master !1  docker build -t local-mysql:1 ./db     DEV OPS POLNOE GOVNO!!!

COPY dbDeployPipeline.sql ./docker-entrypoint-initdb.d

EXPOSE 3306