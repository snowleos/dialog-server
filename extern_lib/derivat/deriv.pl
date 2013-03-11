#!/usr/bin/perl -w
# проверка однокоренной гипотезы

open F, "short.txt"; # короткие слова
while (<F>) {
    chomp;
    @f = split /\//; # 0 - словоформа, 1 - длина окончания, 2 - класс
    $shr{$f[0]} = "$f[1]\t$f[2]";
}

open F, "ends.txt"; # конечные буквы
chomp (@end = <F>);

open F, "suff.txt"; # суффиксы
while (<F>) {
    chomp;
    @f = split /\//; # 0 - суффикс, 1 - класс
    push @{$suf{$f[0]}}, $f[1]; # хеш массивов
}

open F, "pseu.txt"; # псевдосуффиксы
while (<F>) {
    chomp;
    @f = split /\//; # 0 - псевдосуффикс, 1 - класс
    $pse{"$f[0]$f[1]"} = 1;
}

open F, "pref.txt"; # приставки
while (<F>) {
    chomp;
    $pre{$_} = 1;;
}

open F, "alt.txt"; # чередования
while (<F>) {
    chomp;
    next if /^#/;
    @f = split /\t/; # 0 - буква, 1 - чередование
    $alt{"$f[0] $f[1]"} = 1;
}

while (<STDIN>) { # < test.txt
    chomp;
    next if /^#/;
    @wrd = split /\t/; # тестовая пара слов
    
    @flx1 = flx($wrd[0]); # длина окончания+класс
    @suf1 = suf($wrd[0], $flx1[0], $flx1[1]); # список суффиксов
    
    @flx2 = flx($wrd[1]);
    @suf2 = suf($wrd[1], $flx2[0], $flx2[1]);
    
    $hyp = bas($wrd[0], $flx1[0], \@suf1, $wrd[1], $flx2[0], \@suf2); # проверка однокоренной гипотезы
    print "$hyp\t$wrd[0]\t$wrd[1]\n";
    
    #if ($hyp == 0) { # не однокоренные
    #    print "$wrd[0] [ @flx1 ][ @suf1 ]\n";
    #    print "$wrd[1] [ @flx2 ][ @suf2 ]\n";
    #    print "--\n";
    #}
}

# --- поиск окончаний ---
sub flx
{
    my ($wrd) = @_; # исходное слово

    my @a;
    if ($shr{$wrd}) { # поиск по словоформам
        @a = split /\t/, $shr{$wrd};
    } else { # поиск по конечным буквам
        @a = bs(join("", reverse split(//, $wrd)), \@end);
    }
    
    return ($a[0], $a[1]); # окончание + класс
}

# --- бинарный поиск ближайших узлов в словаре конечных букв ---
sub bs
{
    my ($suf, $inv) = @_; # $suf - суффикс (ключ поиска); $inv - инвертированный словарь конечных букв
    
    my $lo = 0;
    my $hi = $#{$inv};
    while ($lo <= $hi) {
        my $mi = int(($lo + $hi) / 2);
        if ($suf lt $$inv[$mi]) {
            $hi = $mi - 1;
        } elsif ($suf gt $$inv[$mi]) {
            $lo = $mi + 1;
        }
    }
    
    $hi = 0 if $hi < 0;
    $$inv[$hi] =~ /\t(.+?)\t(.+)$/;
    my @n1 = ($1, $2); # длина окончания+класс верхнего соседа
    
    $lo = $#{$inv} if $lo > $#{$inv};
    $$inv[$lo] =~ /\t(.+?)\t(.+)$/;
    my @n2 = ($1, $2); # длина окончания+класс нижнего соседа

#print STDERR "---\n$$inv[$hi]\n$$inv[$lo]\n---\n"; # печать ближайших узлов словаря
    
    return @n1 if $n1[0] eq $n2[0] && $n1[1] eq $n2[1];
    
    my @ls = split(//, $suf); # определяем общее начало суффикса и ближайших узлов
    
    my @l1 = split(//, $$inv[$hi]);
    my $c1 = 0;
    for (my $i = 0; $i <= $#ls && $i <= $#l1; $i++) {
        last if $ls[$i] ne $l1[$i];
        $c1++;
    }
    
    my @l2 = split(//, $$inv[$lo]);
    my $c2 = 0;
    for (my $i = 0; $i <= $#ls && $i <= $#l2; $i++) {
        last if $ls[$i] ne $l2[$i];
        $c2++;
    }
    
    return $c1 >= $c2 ? @n1 : @n2;
}

# --- поиск суффиксов ---
sub suf
{
    my ($wrd, $flx, $cls) = @_; # 0 - исходное слово, 1 - длина окончания, 2 - класс
    
    my @suf = (); # результаты поиска (список суффиксов)
    
    my $a = substr($wrd, 0, length($wrd)-$flx); # основа слова
    my @a = split //, $a;
    my $b = "";
    for (my $i = $#a; $i > 0; $i--) {
        $b = "$a[$i]$b";
        my $flag = 0;
        if ($suf{$b}) {
            my @b = @{$suf{$b}};
            for (@b) {
                if ($_ eq $cls) {
                    $flag = 1;
                    last;
                }
            }
        }
        
        push @suf, $b if $flag == 1;
    }
    
    my $ps = substr($a, -2, 2)."$cls"; # псевдосуффикс
#print "$ps\n" if $pse{$ps};
    push @suf, "" if $pse{$ps};
    
    @suf = ("") if @suf == 0;
    return @suf;
}

# --- проверка однокоренной гипотезы ---
sub bas
{
    my ($wr1, $fl1, $sf1, $wr2, $fl2, $sf2) = @_; # 1-е_слово: слово+длина_окончания+список (массив) суффиксов, 2-е_слово: слово+длина_окончания+список (массив) суффиксов

    my $bs1 = substr($wr1, 0, length($wr1)-$fl1); # основа 1-го слова
    my $bs2 = substr($wr2, 0, length($wr2)-$fl2);
    
    my ($com, $ls1, $ls2) = (0, 0, 0); # max число совп. букв основ с конца + наиб. вер. длина суфф. 1-го слова + наиб. вер. длина суфф. 2-го слова
    
    for my $s1 (@{$sf1}) { # список суффиксов 1-го слова
        my $l1 = length($s1);
        my @d1 = split //, substr($bs1, 0, length($bs1)-$l1); # буквы словообразовательной основы 1-го слова
        
        for my $s2 (@{$sf2}) {
            my $l2 = length($s2);
            my @d2 = split //, substr($bs2, 0, length($bs2)-$l2);
            
            # определение числа совпавших букв основ с конца
            my ($sam, $i, $j) = (0, $#d1, $#d2);
            
            # анализ чередования Гл/Сг в корнях
            for my $k (0..2) {
                if ($d1[$#d1-$k] && $d2[$#d2-$k] && $d1[$#d1-$k] ne $d2[$#d2-$k]) {
                    $d2[$#d2-$k] = $d1[$#d1-$k] if $alt{"$d1[$#d1-$k] $d2[$#d2-$k]"} || $alt{"$d2[$#d2-$k] $d1[$#d1-$k]"};
                }
            }

            while (1) {
                last if $i < 0 || $j < 0 || $d1[$i] ne $d2[$j];
                $sam++;
                $i--;
                $j--;
            }
            
            $pre1 = substr($bs1, 0, length($bs1)-$sam-$l1); # приставка 1-го слова
            $pre2 = substr($bs2, 0, length($bs2)-$sam-$l2);
           
            if (($pre1 eq "" || $pre{$pre1}) && ($pre2 eq "" || $pre{$pre2}) && $com < $sam) { # проверка наличия приставок
                $com = $sam; # корень
                $ls1 = $l1; # суффикс 1-го слова
                $ls2 = $l2; # суффикс 2-го слова
            }
        }
    }
    
    return $com > 0 ? 1 : 0; # 1 - однокоренные, 0 - нет
}
