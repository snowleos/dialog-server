https://arcadia.yandex.ru/arc/trunk/arcadia/junk/yuryz/derivat/

convert encoding to utf-8
for f  in *.* ; do cat $f | iconv -f cp1251 -t utf-8 > $f.res ; mv $f.res $f ; done

