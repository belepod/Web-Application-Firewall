docker exec -it datadic3 mysql -u root -p   -> open mysql console (docker)


docker run --name datadic3 -e MYSQL_ROOT_PASSWORD=arya -e MYSQL_DATABASE=ecommerce -p 3307:3306 -d mysql:latest    -> create container



lt --port 5000    -> host localhost


sql injections
' UNION SELECT id, username, password FROM users --

' OR 1=1 -- 

admin', 'hacked'); -- 
