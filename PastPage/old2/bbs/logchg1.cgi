#!/usr/local/bin/perl

## light6chg.cgi (2002/09/20)
## (LightBoard v5.xx ���Av6 �փ��O�ϊ����s���܂�)
## Copyright(C) Kent Web 2002
## webmaster@kent-web.com
## http://www.kent-web.com/
##
## [ �g���� ]
## (1) light.cgi �Ɠ���f�B���N�g���� light6chg.cgi �Ƀe�L�X�g���[�h
##     �œ]�����A�p�[�~�b�V������755�ɐݒ肷��B
## (2) �u���E�U���� light.cgi �ɃA�N�Z�X���A�u�ϊ���Ɗ����v��
##     ���b�Z�[�W���\�������Ί����B

# �����O
$old = './minibbs0.dat';

# �V���O
$new = './data0.cgi';

# �ݒ�t�@�C��
$set = './light.dat';

# ---------- ��ƊJ�n ----------

# �w�b�_�o��
print "Content-type: text/html\n\n";
print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>�ϊ��c�[��</title></head>
<body>
EOM

# ���O�ϊ�
open(IN,"$old") || &error("Open Error : $old");
@old = <IN>;
close(IN);

$top = shift(@old);

# �V���O�֏�������
$no = 307;
$host ="";
$pw ="";
open(OUT,">$new") || &error("Write Error : $new");
foreach (@old) {
	($date,$nam,$eml,$com,$sub,$url) = split(/\,/);
	$com =~ s/\0/\,/g; # �k���R�[�h�ɕϊ��L�^�������p�J���}�𕜋A������
		chop($hpage) if $hpage =~ /\n/;

#	($no,$date,$nam,$eml,$sub,$com,$url,$host,$pw) = split(/<>/);
#	if ($url) { $url = "http://$url"; }
	print OUT "$no<>$date<>$nam<>$eml<>$sub<>$com<>$url<>$host<>$pw<><>\n";
$no = $no -1;
}
close(OUT);

# �ݒ�f�[�^�ϊ�
#($head,$title,$t_col,$t_size,$t_face,$bg,$bc,$tx,$li,$vl,$al,$home,$max,$subcol,$namcol,$mail1,$mail2) = split(/<>/, $top);
#open(OUT,">$set") || &error("Write Error : $set");
#print OUT "$title<>$t_col<>24<>$t_face<>$t_img<>$bg<>$bc<>$tx<>$li<>$vl<>$al<>$home<>$max<>$subcol<>#800000<>10<>13<>$mail1<><>1<>0<>";
#close(OUT);

print <<"EOM";
�ϊ���Ɗ���3
</body>
</html>
EOM
exit;

# ERROR
sub error {
	print <<"EOM";
<h3>ERROR</h3>
$_[0]
</body>
</html>
EOM
	exit;
}

__END__

