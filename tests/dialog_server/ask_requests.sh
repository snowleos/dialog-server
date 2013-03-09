# vim: set fileencoding=utf-8

echo "некоторая погода команда на русском"

curl --data-urlencode "ReqString=некоторая погода команда на русском" http://127.0.0.1:8080/SendRequest
sleep 5
curl --data-urlencode "ReqString=википедия барселона" http://127.0.0.1:8080/SendRequest
sleep 5
curl --data-urlencode "ReqString=всякий спам новости всякий спам" http://127.0.0.1:8080/SendRequest
