#!/usr/bin/perl -w
# �������� ������������ ��������

open F, "short.txt"; # �������� �����
while (<F>) {
    chomp;
    @f = split /\//; # 0 - ����������, 1 - ����� ���������, 2 - �����
    $shr{$f[0]} = "$f[1]\t$f[2]";
}

open F, "ends.txt"; # �������� �����
chomp (@end = <F>);

open F, "suff.txt"; # ��������
while (<F>) {
    chomp;
    @f = split /\//; # 0 - �������, 1 - �����
    push @{$suf{$f[0]}}, $f[1]; # ��� ��������
}

open F, "pseu.txt"; # ��������������
while (<F>) {
    chomp;
    @f = split /\//; # 0 - �������������, 1 - �����
    $pse{"$f[0]$f[1]"} = 1;
}

open F, "pref.txt"; # ���������
while (<F>) {
    chomp;
    $pre{$_} = 1;;
}

open F, "alt.txt"; # �����������
while (<F>) {
    chomp;
    next if /^#/;
    @f = split /\t/; # 0 - �����, 1 - �����������
    $alt{"$f[0] $f[1]"} = 1;
}

while (<STDIN>) { # < test.txt
    chomp;
    next if /^#/;
    @wrd = split /\t/; # �������� ���� ����
    
    @flx1 = flx($wrd[0]); # ����� ���������+�����
    @suf1 = suf($wrd[0], $flx1[0], $flx1[1]); # ������ ���������
    
    @flx2 = flx($wrd[1]);
    @suf2 = suf($wrd[1], $flx2[0], $flx2[1]);
    
    $hyp = bas($wrd[0], $flx1[0], \@suf1, $wrd[1], $flx2[0], \@suf2); # �������� ������������ ��������
    print "$hyp\t$wrd[0]\t$wrd[1]\n";
    
    #if ($hyp == 0) { # �� ������������
    #    print "$wrd[0] [ @flx1 ][ @suf1 ]\n";
    #    print "$wrd[1] [ @flx2 ][ @suf2 ]\n";
    #    print "--\n";
    #}
}

# --- ����� ��������� ---
sub flx
{
    my ($wrd) = @_; # �������� �����

    my @a;
    if ($shr{$wrd}) { # ����� �� �����������
        @a = split /\t/, $shr{$wrd};
    } else { # ����� �� �������� ������
        @a = bs(join("", reverse split(//, $wrd)), \@end);
    }
    
    return ($a[0], $a[1]); # ��������� + �����
}

# --- �������� ����� ��������� ����� � ������� �������� ���� ---
sub bs
{
    my ($suf, $inv) = @_; # $suf - ������� (���� ������); $inv - ��������������� ������� �������� ����
    
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
    my @n1 = ($1, $2); # ����� ���������+����� �������� ������
    
    $lo = $#{$inv} if $lo > $#{$inv};
    $$inv[$lo] =~ /\t(.+?)\t(.+)$/;
    my @n2 = ($1, $2); # ����� ���������+����� ������� ������

#print STDERR "---\n$$inv[$hi]\n$$inv[$lo]\n---\n"; # ������ ��������� ����� �������
    
    return @n1 if $n1[0] eq $n2[0] && $n1[1] eq $n2[1];
    
    my @ls = split(//, $suf); # ���������� ����� ������ �������� � ��������� �����
    
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

# --- ����� ��������� ---
sub suf
{
    my ($wrd, $flx, $cls) = @_; # 0 - �������� �����, 1 - ����� ���������, 2 - �����
    
    my @suf = (); # ���������� ������ (������ ���������)
    
    my $a = substr($wrd, 0, length($wrd)-$flx); # ������ �����
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
    
    my $ps = substr($a, -2, 2)."$cls"; # �������������
#print "$ps\n" if $pse{$ps};
    push @suf, "" if $pse{$ps};
    
    @suf = ("") if @suf == 0;
    return @suf;
}

# --- �������� ������������ �������� ---
sub bas
{
    my ($wr1, $fl1, $sf1, $wr2, $fl2, $sf2) = @_; # 1-�_�����: �����+�����_���������+������ (������) ���������, 2-�_�����: �����+�����_���������+������ (������) ���������

    my $bs1 = substr($wr1, 0, length($wr1)-$fl1); # ������ 1-�� �����
    my $bs2 = substr($wr2, 0, length($wr2)-$fl2);
    
    my ($com, $ls1, $ls2) = (0, 0, 0); # max ����� ����. ���� ����� � ����� + ����. ���. ����� ����. 1-�� ����� + ����. ���. ����� ����. 2-�� �����
    
    for my $s1 (@{$sf1}) { # ������ ��������� 1-�� �����
        my $l1 = length($s1);
        my @d1 = split //, substr($bs1, 0, length($bs1)-$l1); # ����� �������������������� ������ 1-�� �����
        
        for my $s2 (@{$sf2}) {
            my $l2 = length($s2);
            my @d2 = split //, substr($bs2, 0, length($bs2)-$l2);
            
            # ����������� ����� ��������� ���� ����� � �����
            my ($sam, $i, $j) = (0, $#d1, $#d2);
            
            # ������ ����������� ��/�� � ������
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
            
            $pre1 = substr($bs1, 0, length($bs1)-$sam-$l1); # ��������� 1-�� �����
            $pre2 = substr($bs2, 0, length($bs2)-$sam-$l2);
           
            if (($pre1 eq "" || $pre{$pre1}) && ($pre2 eq "" || $pre{$pre2}) && $com < $sam) { # �������� ������� ���������
                $com = $sam; # ������
                $ls1 = $l1; # ������� 1-�� �����
                $ls2 = $l2; # ������� 2-�� �����
            }
        }
    }
    
    return $com > 0 ? 1 : 0; # 1 - ������������, 0 - ���
}
