# vim: set fileencoding=utf-8

# for exact classifier
curl --data-urlencode "ReqString=некоторая погода команда на русском" http://127.0.0.1:8080/SendRequest
sleep 4
curl --data-urlencode "ReqString=википедия барселона" http://127.0.0.1:8080/SendRequest
sleep 4
curl --data-urlencode "ReqString=всякий спам новости всякий спам" http://127.0.0.1:8080/SendRequest
sleep 4
exit 0

# for bayes classifier
curl --data-urlencode "ReqString=читай википедию" http://127.0.0.1:8080/SendRequest
sleep 4
curl --data-urlencode "ReqString=скока градусов на улице" http://127.0.0.1:8080/SendRequest
sleep 4
curl --data-urlencode "ReqString=кто такой Билл Гейтс" http://127.0.0.1:8080/SendRequest
sleep 4
curl --data-urlencode "ReqString=новостная сводка" http://127.0.0.1:8080/SendRequest
sleep 4
curl --data-urlencode "ReqString=в чем смысл жизни" http://127.0.0.1:8080/SendRequest
sleep 4
curl --data-urlencode "ReqString=сегодня будет пурга" http://127.0.0.1:8080/SendRequest
sleep 4
