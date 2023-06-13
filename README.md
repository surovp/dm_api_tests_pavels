# dm_api_tests_pavels
### Проект API автотестов для локального приложения DM.

В ветке main - фреймворк, который включает в себя все вспомогательные библиотеки.  
В ветке client - фреймворк, из которого вынесены вспомогательные библиотеки.  
В ветке client_gen - фреймворк, где клиент account и login сгенерированы, а так же сгенерирован клиент из gRPC модели.  

### Используемые технологии
<p  align="center">
  <code><img width="5%" title="Pycharm" src="images/logo_stacks/pycharm.png"></code>
  <code><img width="5%" title="Python" src="images/logo_stacks/python.png"></code>
  <code><img width="5%" title="Pytest" src="images/logo_stacks/pytest.png"></code>
  <code><img width="5%" title="Postman" src="images/logo_stacks/postman.png"></code>
  <code><img width="5%" title="Docker" src="images/logo_stacks/docker.png"></code>
  <code><img width="5%" title="Requests" src="images/logo_stacks/requests.png"></code>
  <code><img width="5%" title="GitHub" src="images/logo_stacks/github.png"></code>
  <code><img width="5%" title="Allure Report" src="images/logo_stacks/allure_report.png"></code>
  <code><img width="5%" title="gRPC" src="images/logo_stacks/grpc.png"></code>
  <code><img width="5%" title="OpenApi" src="images/logo_stacks/openapi.png"></code>
</p>

### В файле config настраиваются окружения и выносятся основные подключения.
![This is an image](images/screenshots/config.png)



### <img width="3%" title="Allure Report" src="images/logo_stacks/allure_report.png"> Allure report
##### После прохождения тестов, результаты можно посмотреть в генерируемом Allure отчете.
![This is an image](images/screenshots/allure-report.png)

##### Во вкладке Graphs можно посмотреть графики о прохождении тестов, по их приоритезации, по времени прохождения и др.
![This is an image](images/screenshots/allure-graphs.png)

##### Во вкладке Suites находятся собранные тест кейсы, у которых описаны шаги и добавлены логи.
![This is an image](images/screenshots/allure-suites.png)
