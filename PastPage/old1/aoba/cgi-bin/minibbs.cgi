#! /usr/local/bin/perl

;#  �����̃p�X�̓v���o�C�_�ɂ���ĈႤ�̂Œ��ׂĐݒ肷��
;#    (����͂��̃X�N���v�g�̍ŏ��̂P�s�ɂȂ���΂Ȃ炸�A�������ɋ�s�������Ă������܂���B)
;#    (���̐ݒ肪�K�v�Ȃ��T�[�o������܂��B��ʓI�ȏꍇ��z�肵�ĉ�������Ă��܂��B)
;#    (���ɁA�v���o�C�_����A�i�E���X����Ă�������\���������Ă����Ă��������B)
;#
;# �ȈՂa�a�r version 7.5c�i�t���[�\�t�g�j
;#
;# Script written by Kazu.Y
;# Created on: 02/05/96
;# Last Modified on: 07/03/97
;# I can be reached at: rescue@ask.or.jp
;# Scripts Found at: http://www.ask.or.jp/~rescue/
;#
;# <���p�K��̔���>
;#  1.���̃X�N���v�g�͎����Ŏg�����߂ɏ����Ȃ��Ɏ��R�ɉ������邱�Ƃ��ł��܂��B
;#  2.�����̗L���ɂ�����炸�A���̃X�N���v�g���Ĕz�z���邱�Ƃ͂ł��܂���B
;#  3.���̃V�X�e����L���ő��l�ɐݒu���Ă������肷��s�ׂ͖��f�ł͂ł��܂���B

###########################################################################################
#
# ���d�v�I ���� v7.5c �́Av7.5 �ɊǗ��p�X���[�h���Í�������@�\��t���������̂ł��B
# �ݒu����T�[�o�ɂ���Ă͐������Í����ł��܂���̂ŁA�ݒ肵���p�X���[�h��
# �F�؂���Ȃ��ꍇ�͂��̃g���u�����l�����܂��̂ŁAv7.5 �������p���������B
#
# ��U�ݒ肳�ꂽ�p�X���[�h��Y�ꂽ�ꍇ�A�܂��́A�������Í����ł��Ȃ��ꍇ�ɁA
# �L�^����Ă��܂����p�X���[�h���폜���邱�Ƃ͂ł��܂���B�f�[�^����ɂ��čŏ������蒼�����ƂɂȂ�܂��B
# �f�[�^���p�����������́A�\�ߑ��̏ꏊ�œ��쎎�����s�������ƂɎ{�H���Ă��������B
#
# ���݊����I v7.5 �Ő������ꂽ�f�[�^�� v7.5c �ŗ��p���邱�Ƃ��ł��܂����A���̋t��
# �ł��܂���B�f�[�^�t�@�C�����ɈÍ������ꂽ�p�X���[�h���L�^����邽�߁Av7.5c ��
# �������ꂽ��̃f�[�^�� v7.5 �Ŏg�����Ƃ͂ł��܂���B
#
#
# ��{�\���i�����ݒ�͂��̍\����O��ɉ�����܂��j
#
#   public_html�i�z�[���y�[�W�f�B���N�g���j
#        |
#        |-- cgi-bin�i�C�ӂ̃f�B���N�g���j
#               |
#               |-- jcode.pl (755)
#               |-- minibbs.cgi (755)
#               |-- minibbs.dat (666)
#
#                   �E���� minibbs.pl �� minibbs.cgi �Ƀt�@�C������ύX����
#                   �Eminibbs.dat �͒��g������ۂ̃t�@�C�����p�\�R����ō쐬���ē]������
#                   �E���̃V�X�e���ɕK�v�ȂR�̃t�@�C���𓯂��ꏊ�ɐݒu����
#                   �E( )���̓p�[�~�b�b�V�����l
#                   �Ejcode.pl�͒��g��S�������炸�ɂ��̂܂܃A�X�L�[�]������
#                   �Ejcode.pl��jperl�ł͗��p�ł��Ȃ��̂Œ��ӂ��邱��
#                   �E�����R�̃t�@�C���̓A�X�L�[���[�h�Ŏ�舵��(�]��)���邱��
#
###########################################################################################

#----------------#
#    �����ݒ�    #
#----------------#

#--- �K�����Ȃ��̊��ɍ��킹�ď����ւ��鍀�� --------------------------------------------#

# �f���̖��O
$title = '��˒[��c';

# ���̃X�N���v�g���t�q�k�Őݒ�
$reload = 'http://www.sendai-ct.ac.jp/~ckuma/kagakubu/old/aoba/cgi-bin/minibbs.cgi';

# ��ʂ́u�I���v�{�^���̕\������t�q�k�Őݒ�
$modoru = 'http://www.sendai-ct.ac.jp/~ckuma/kagakubu/old/aoba/';


#--- �K�v�ɉ����Đݒ肷�鍀�� ------------------------------------------------------------#

#�@�����F��w�i�Ȃǂ̐ݒ�i�ʏ��<body>�^�O�j
#�@�薼�Ɠ��e�ҐF�̓X�N���v�g����<font color>�^�O��T���Đݒ肵�Ă��������B
$body = '<body bgcolor="#eaeaae" text="#000000">';

#  �^�O���g����悤�ɂ��邩�ǂ����̐ݒ�
#  <a gref="�����N"></a>�ɂ��Ă͓��̓t�H�[�����p�ӂ��Ă���̂ŁA���������^�O��
#  ���Y�ꓙ�ɂ�鍬��������邽�߂ɂł��邾���g���Ȃ��悤�ɂ��Ă������Ƃ������߂��܂��B
#  �g����:1 �g���Ȃ�:0
$tag = 0;

#  �P�y�[�W�ɕ\�����錏��
$def = 50;

#  �������݌����̍ő�o�^���̐ݒ�ł��B���̌����𒴂���ƁA�Â����̂���폜����Ă����܂��B
#�@�y�[�W�����@�\���t���܂����̂ŁA���̌�����傫�����Ă���x�ɕ\�������L�����͌��肳��܂��B
#�@�L�^���ꂽ�t�@�C���̋��剻��h�~����ׂɁA������x�̌����Ŏ����폜�����悤�ɂ��܂��B
$max = '200';

#�@���{��R�[�h�ϊ����C�u����
#  ���� jcode.pl �� minibbs.cgi �ƈႤ�f�B���N�g���ɐݒu����ꍇ�͑��ΓI�ɐݒ肷�邱��
require './jcode.pl';

#�@���e���������܂��L�^�t�@�C���̃p�X��ݒ�
#  ���� minibbs.dat �� minibbs.cgi �ƈႤ�f�B���N�g���ɐݒu����ꍇ�͑��ΓI�ɐݒ肷�邱��
$file = './minibbs.dat';

#  �C�O�T�[�o���Ŏ�����������ꍇ�͏C�����܂�
#    �C�O���ԂɁ{�X���Ԃ���ꍇ�@= localtime(time + 9*60*60);
#    �C�O���ԂɁ|�X���Ԃ���ꍇ�@= localtime(time - 9*60*60);
#   �i�Q�l�jtime�ɂ�1970�N����̕b���������Ă��܂�
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

#  �N�b�L�[�̏����ݒ�
#    �ŏI�������݂���   30���� 30*24*60*60
#                        1���� 24*60*60
#                     10���Ԍ� 10*60*60
$ENV{'TZ'} = "GMT"; # ���ەW�������擾����
($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = localtime(time + 30*24*60*60);

# ���͌`���̐ݒ�@�W������:post ���̑�:get
# ���e�{�^���������� Method not implemented.. �Ƃ����G���[���o��ꍇ��  get �Ŏ�������
$method = 'post';

###########################################################################################
#
# �E�L�^�t�@�C���ɂ͏����̓s�������R�[�h���L�^����܂��̂ŁA���ڕҏW�͂ł��܂���B
# �E�X�N���v�g�̒��g�������ւ���ꍇ�́Aperl��CGI��HTML�Ȃǂ̂���Ȃ�̒m�����K�v�ł��B
# �E�ݒu�Ɋւ��鎿��̓`�������W�b�f�h��p�f���������p���������B�����̎���͎󂯂܂���B
#   http://www2r.meshnet.or.jp/~rescue/webboard/
#
###########################################################################################

# ��L��localtime�Ŏ擾����$mon�ɂ�0����11�܂ł̐���������̂ŏC������
$month = ($mon + 1);

# �������Q���ɓ��ꂷ�鏈���i�폜�����Ɋ֌W����̂ŏ����ւ��Ȃ����Ɓj
if ($month < 10) { $month = "0$month"; }
if ($mday < 10)  { $mday  = "0$mday";  }
if ($sec < 10)   { $sec   = "0$sec";   }
if ($min < 10)   { $min   = "0$min";   }
if ($hour < 10)  { $hour  = "0$hour";  }

# �j���ϊ�����
# $wday�ɂ�0����6�܂ł̐���������j���ɑΉ����Ă���
$y0="��"; $y1="��"; $y2="��"; $y3="��"; $y4="��"; $y5="��"; $y6="�y";
$youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6) [$wday];

# �����t�H�[�}�b�g�i�폜�����Ɋ֌W����̂ŏ����ւ��Ȃ����Ɓj
$date_now = "$month��$mday��($youbi)$hour��$min��$sec�b";

# �t�H�[�����͂��ꂽ�f�[�^��$buffer�Ɋi�[����iget��post���ɂ���Ď擾���@���قȂ�j
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

# $buffer�Ɋi�[���ꂽFORM�`���̃f�[�^�����o��

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	# �����̓s����̏���
	$value =~ s/\n//g; # ���s�����̓f�[�^�̋L�^�ɉe��������̂ŏ�������

	if ($tag) { # �f���ɏ������܂ꂽ���Ȃ��^�O��ݒ肷��(�^�O���g����ꍇ�ɗL��)

		if ($value =~ /<table(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<meta(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<pre(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<!--(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<form(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<embed(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<script(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<frame(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<a(.|\n)*on(.*)=(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<img(.|\n)*on(.*)=(.|\n)*>/i) { &error(tag); }
	}

	if ($tag eq '0' && $name eq 'value') { # �^�O�𖳌�

		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
	}

	if ($tag eq '0' && $name eq 'value') { $value =~ s/\,/\0/g; } # ���p�J���}�̓f�[�^��CSV�L�^�ɉe��������̂Ńk���R�[�h�ϊ�����
	elsif ($name eq 'value') { $value =~ s/&/&amp\;/g; $value =~ s/\,/\0/g; }
	elsif ($name ne 'page') { $value =~ s/\,//g; $value =~ s/\;//g; $value =~ s/\://g; $value =~ s/\=//g; }
	else { $value =~ s/\,//g; }

	# �L�^����f�[�^��sjis�ɓ��ꂷ��
	&jcode'convert(*value,'sjis');

	if ($name eq "target") { push(@RM,$value); }
	else { $FORM{$name} = $value; }
}

# �Ǘ��L�[�̐ݒ胋�[�`��
# �L�^�t�@�C����ǂݏo���I�[�v�����āA�z��<@lines>�Ɋi�[����
if (!open(DB,"$file")) { &error(0); }
@lines = <DB>;
close(DB);

# �f�[�^�̍ŏ��ɋL�^�����Í������ꂽ�p�X���[�h�����o��
$password = shift(@lines);
chop($password) if $password =~ /\n$/;
($header,$password) = split(/:/,$password);
if ($FORM{'action'} eq 'password') { &encode; }
if ($FORM{'admin'} eq 'change') { &password; }
if ($header ne 'crypt_password') { $first = 1; &password; }

#  �S�̗̂�������肷��iaction��pwd�̓t�H�[�����͂��ꂽ�f�[�^���i�[���閼�O�j
#    action=remove ���� pwd=�ݒ�p�X���[�h --> �폜�������Ēʏ��ʂ�
#    action=remove  --> �폜�L���I����ʂ�
#    action=regist  --> �L���L�^�������Ēʏ��ʂ�
#    ���̑�  --> �ʏ��ʂ�
if ($FORM{'action'} eq 'remove' && crypt($FORM{'pwd'}, substr($password,0,2)) eq $password) { &remove2; &remove1; exit; }
elsif (crypt($FORM{'pwd'}, substr($password,0,2)) eq $password) { &remove1; exit; }
elsif ($FORM{'action'} eq 'regist') { &regist; }
&html;

sub html {

	#--- �N�b�L�[�̎擾�i�Ǝ������j-----------------------#

	$cookies = $ENV{'HTTP_COOKIE'};

	@pairs = split(/;/,$cookies);
	foreach $pair (@pairs) {

		($name, $value) = split(/=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}

	@pairs = split(/,/,$DUMMY{$reload});
	foreach $pair (@pairs) {

		($name, $value) = split(/:/, $pair);
		$COOKIE{$name} = $value;
	}

	#--- ���̓t�H�[����� --------------------------------#

	# �b�f�h�ŏo�͂��ꂽ�f�[�^���g�s�l�k�Ƃ��ĔF��������w�b�_�̏o��
	print "Content-type: text/html; charset=Shift_JIS\n\n";

	print "<html><head><title>$title</title></head>\n";
	print "$body\n";

	print "<font size=+2><b>$title</b></font><p>\n";

    print "<P ALIGN=RIGHT><FONT SIZE=+2><A HREF=\"../\">�g�b�v�ɖ߂�</A></FONT></P>\n";
	print "<form method=$method action=\"$reload\">\n";
	print "<input type=hidden name=\"action\" value=\"regist\">\n";
	print "���e�� <input type=text name=\"name\" size=20 value=\"$COOKIE{'name'}\" maxlength=19><br>";
	print "���[�� <input type=text name=\"email\" size=30 value=\"$COOKIE{'email'}\"><br>\n";
	print "�薼�@ <input type=text name=\"subject\" size=30>  \n";
	print "<input type=submit value=\"     ���e     \"><input type=reset value=\"����\"><p>\n";

	print "���e<i>�i�L���ʂ�ɋL�^���܂��̂œK���ɉ��s�����Ă��������B\n";

	if (!$tag) { print "�^�O�͎g���܂���B"; }
	print "�j</i><br>\n";

	print "<textarea name=\"value\" rows=5 cols=70></textarea><p>\n";
	print "�t�q�k�i�����N����ꂽ���ꍇ�͂����ɋL�����܂��j<br>\n";
	print "<input type=text name=\"page\" size=70 value=\"http://\"><p></form>\n";

	print "<hr><font size=-1><i>�V�����L������\\�����܂��B�ō�$max���̋L�����L�^����A����𒴂���ƌÂ��L������폜����܂��B<br>\n";
	print "�P��̕\\����$def�����z����ꍇ�́A���̃{�^�����������ƂŎ��̉�ʂ̋L����\\�����܂��B</i></font>\n\n";

	#--- �L�^�L���̏o�� ----------------------------------#

	if ($FORM{'page'} eq '') { $page = 0; } else { $page = $FORM{'page'}; }

	$accesses = @lines; $accesses--;
	$page_end = $page + $def - 1;
	if ($page_end > $accesses) { $page_end = $accesses; }

	foreach ($page .. $page_end) {

		# �f�[�^���e�ϐ��ɑ������
		($date,$name,$email,$value,$subject,$hpage) = split(/\,/,$lines[$_]);
		$value =~ s/\0/\,/g; # �k���R�[�h�ɕϊ��L�^�������p�J���}�𕜋A������
		chop($hpage) if $hpage =~ /\n/;

		print "<hr><font size=+1 color=\"#ff0000\"><b>$subject</b></font>";

		# ���[���A�h���X���L�^����Ă���f�[�^�ɂ̓����N��t����
		if ($email ne '') { print "�@���e�ҁF<b><a href=\"mailto:$email\">$name</a></b>\n"; }
		else { print "�@���e�ҁF<font color=\"#555555\"><b>$name</b></font>\n"; }

		print "<font size=-1>�@���e���F$date</font><p>\n";
		print "<blockquote><pre>$value</pre><p>\n\n";

		# �t�q�k���L�^����Ă���f�[�^�ɂ̓����N��t����
		if ($hpage ne '') { print "<a href=\"$hpage\" target=\"_top\">$hpage</a><p>\n"; }

		print "</blockquote>\n";
	}

	#--- ���y�[�W���� ------------------------------------#

	print "<hr><p>\n";

	$page_next = $page_end + 1;
	$i = $page + 1; $j = $page_end + 1;

	if ($page_end ne $accesses) {

		print "<font size=-1><i>�ȏ�́A���ݓo�^����Ă���V����$i�Ԗڂ���$j�Ԗڂ܂ł̋L���ł��B</i></font><p>\n";
		print "<form method=$method action=\"$reload\">\n";
		print "<input type=hidden name=\"page\" value=\"$page_next\">\n";
		print "<input type=submit value=\"���̃y�[�W\"></form>\n";
	}
	else {

		print "<font size=-1><i>�ȏ�́A���ݓo�^����Ă���V����$i�Ԗڂ���$j�Ԗڂ܂ł̋L���ł��B";
		print "����ȉ��̋L���͂���܂���B</i></font>\n";
	}

	print "<form action=\"$modoru\"><input type=submit value=\"�@�I�@���@\"></form><p>\n";

	print "<form method=$method action=\"$reload\">\n";
	print "<hr><p>\n";
	print "<input type=checkbox name=\"admin\" value=\"change\">�Ǘ��p�X���[�h�̕ύX<br>";
	print "�L���̍폜�͊Ǘ��p�X���[�h����� <input type=password name=\"pwd\" size=10> ";
	print "<input type=submit value=\"�ύX/�폜\"></form>\n";

	# ���̃X�N���v�g�̒��쌠�\���i���Ȃ炸�\�����Ă��������j
	print "<h4 align=right><hr><a href=\"http://www.ask.or.jp/~rescue/\" target=\"_top\">MiniBBS v7.5c</a> is Free.</h4>\n";
	print "</body></html>\n";
	exit;
}

sub regist {

	# �ʂ̃y�[�W���炱�̂b�f�h�ւ̓��e��r�����鏈��
	# �����F���̂b�f�h����̓��e���ł��Ȃ��悤�ɂ���ꍇ�͎���3�s��#���폜���Ă�������

	#$ref = $ENV{'HTTP_REFERER'};
	#$ref_url = $reload; $ref_url =~ s/\~/.*/g;
	#if (!($ref =~ /$ref_url/i)) { &error(form); }

	# ���͂��ꂽ�f�[�^�̃`�F�b�N

	if ($FORM{'name'} eq "") { &error(1); }
	if ($FORM{'value'} eq "") { &error(2); }
	if ($FORM{'email'} =~ /,/) { &error(4); }
	if ($FORM{'email'} ne "") { if (!($FORM{'email'} =~ /(.*)\@(.*)\.(.*)/)) { &error(3); }}
	if ($FORM{'subject'} eq "") { $FORM{'subject'} = '(����)'; }
	if ($FORM{'page'} eq "" || $FORM{'page'} eq "http://") { $FORM{'page'} = ''; }

	$FORM{'name'} =~ s/<//g; $FORM{'name'} =~ s/>//g;
	$FORM{'subject'} =~ s/</&lt;/g; $FORM{'subject'} =~ s/>/&gt;/g;
	$FORM{'email'} =~ s/<//g; $FORM{'email'} =~ s/>//g;

	#  �N�b�L�[�̎d�l��  http://www.netscape.com/newsref/std/cookie_spec.html

	if ($yearg < 10)  { $yearg = "0$yearg"; }
	if ($secg < 10)   { $secg  = "0$secg";  }
	if ($ming < 10)   { $ming  = "0$ming";  }
	if ($hourg < 10)  { $hourg = "0$hourg"; }
	if ($mdayg < 10)  { $mdayg = "0$mdayg"; }

	$y0="Sunday"; $y1="Monday"; $y2="Tuesday"; $y3="Wednesday"; $y4="Thursday"; $y5="Friday"; $y6="Saturday";
	$youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6) [$wdayg];

	$m0="Jan"; $m1="Feb"; $m2="Mar"; $m3="Apr"; $m4="May"; $m5="Jun";
	$m6="Jul"; $m7="Aug"; $m8="Sep"; $m9="Oct"; $m10="Nov"; $m11="Dec";
	$month = ($m0,$m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9,$m10,$m11) [$mong];

	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";

	#�@�Ǝ������̃N�b�L�[�t�H�[�}�b�g
	#
	#�@���̊ȈՂa�a�r�ł͖��O�ƃ��[���A�h���X��ۑ��̑Ώۂɂ��Ă��܂��B
	#�@���ꂼ���Ɨ������N�b�L�[�Ƃ��ău���E�U�ɐH�ׂ�����΂ƂĂ��ȒP�ł����A
	#�@�u���E�U���N�b�L�[���i�[�ł��鐔�ɐ��������邽�߁A�ł��邾����̃N�b�L�[��
	#�@�ۑ��f�[�^���܂Ƃ߂ĐH�ׂ����邱�Ƃ��]�܂�܂��B���̂��߂ɂ����ł͓Ǝ��̕��@��
	#�@�P�̃N�b�L�[���ɕ����̃f�[�^���l�ߍ��݁A�N�b�L�[�̎擾���ɂ�����W�J���ė��p���Ă��܂��B
	#�@
	#�@name:<name>,email:<email> �Ƃ����`���ɂ܂Ƃ߂āA�������̃N�b�L�[�Ƃ���
	#�@cookie�Ƃ������O�Ńu���E�U�ɑ��M���Ă��܂��B
	#
	#�@�Ǝ��t�H�[�}�b�g�@cookie=name:<name>,email:<email>

	$cook="name\:$FORM{'name'}\,email\:$FORM{'email'}";
	print "Set-Cookie: $reload=$cook; expires=$date_gmt\n";

	# �L���҂̃����[�g�z�X�g�����擾����i����͕\�����ꂸ�g�s�l�k�\�[�X�ŉ{���ł���j
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }

	# �L�^�t�@�C����ǂݏo���I�[�v�����āA�z��<@lines>�Ɋi�[����
	if (!open(DB,"$file")) { &error(0); }
	@lines = <DB>; $password = shift(@lines);
	close(DB);

	# �ő�ێ��L�^���̏���
	$i = 0;
	foreach $line (@lines) {

		$i++;
		if ($i == $max) { last; }
		push(@new,$line);
	}

	$value = "$date_now\,$FORM{'name'}\,$FORM{'email'}\,$FORM{'value'}<!--remote_host�F$host-->\,$FORM{'subject'}\,$FORM{'page'}\n";
	unshift(@new,$value);

	# �L�^�t�@�C�����㏑���I�[�v�����āA�z��<@new>�������o��
	if (!open(DB,">$file")) { &error(0); }
	print DB $password;
	print DB @new;
	close(DB);

	# �L�^������A�ēǂݍ��݂���
	print "Location: $reload" . '?' . "\n\n";
	exit;
}

sub error {

	#  &error(xx); �ŌĂяo���ꂽ���[�`���́A()���̐����� $error �ɑ�������B

	$error = $_[0];

	if    ($error eq "0") { $error_msg = '�L�^�t�@�C���̓��o�͂ɃG���[���������܂����B'; }
	elsif ($error eq "1") {	$error_msg = '���e�Җ����L������Ă��܂���B'; }
	elsif ($error eq "2") {	$error_msg = '���e��������Ă��܂���B�܂��͋L�^�֎~�̃^�O��������Ă��܂��B'; }
	elsif ($error eq "3") {	$error_msg = '���[���A�h���X�����������͂���Ă��܂���B'; }
	elsif ($error eq "4") {	$error_msg = '���[���A�h���X�͕����w��ł��܂���B'; }
	elsif ($error eq "tag") { $error_msg = '���p���ł��Ȃ��^�O���L�q����Ă��܂��̂œ��e�ł��܂���B'; }
	elsif ($error eq "form") { $error_msg = "���e��ʂ̂t�q�k��<br>$reload<br>" . '�ȊO����̓��e�͂ł��܂���B'; }

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
        print "<h3>$error_msg</h3>\n";
        print "</body></html>\n";
        exit;
}


sub remove1 {

	if (!open(DB,"$file")) { &error(0); }
	@lines = <DB>; $password = shift(@lines);
	close(DB);

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
	print "<font size=+2><b>�폜���[�h</b></font>  [<a href=\"$reload\">�߂�</a>]<p>\n";

	print "<form method=$method action=\"$reload\">\n";
	print "<input type=hidden name=\"action\" value=\"remove\">\n";
	print "<pre>";
	print "   �o�^��                  ���e��               �^�C�g��              ���e<hr>\n";

	foreach $line (@lines) {

		($date,$name,$email,$value,$subject) = split(/\,/,$line);

		$value =~ s/\0/\,/g;
		chop($subject) if $subject =~ /\n/;
		$value =~ s/<!--.*-->//ig; $value =~ s/</&lt;/ig; $value =~ s/>/&gt;/ig; $value =~ s/\n/./g; $value =~ s/\r/./g;

		$i1 = length($subject);
		if ($i1 > 20) { $subject = substr($subject,0,18); $subject = $subject . '..'; }
		elsif ($i1 < 20) { $blank = ' ' x (20 - $i1); $subject = $subject . $blank; }

		$i2 = length($name);
		if ($i2 > 20) { $name = substr($name,0,18); $name = $name . '..'; }
		elsif ($i2 < 20) { $blank = ' ' x (20 - $i2); $name = $name . $blank; }

		if (length($value) > 40) { $value = substr($value,0,40); }
		print "<input type=checkbox name=\"target\" value=\"$date\">";
		print "$date $name $subject $value\n";
	}

	print "</pre><p><input type=hidden name=\"pwd\" value=\"$FORM{'pwd'}\">\n";
	print "<input type=submit value=\"     �폜     \"><input type=reset value=\"���Z�b�g\"></form><p>\n";
	print "</body></html>\n";
}

sub remove2 {

	if (!open(DB,"$file")) { &error(0); }
	@lines = <DB>; $password = shift(@lines);
	close(DB);

	foreach $line (@lines) {

		($date,$name,$email,$value,$subject) = split(/\,/,$line);
		$del = 0;
		foreach $target (@RM) {	if ($target eq $date) { $del = 1; } }
		if ($del == 0) { push(@new,$line); }
	}

	if (!open(DB,">$file")) { &error(0); }
	print DB $password;
	print DB @new;
	close(DB);
}

sub password {

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
	print "<h1>�Ǘ��p�X���[�h�̐ݒ�/�ύX</h1>\n";

	if ($first && $message eq '') { print "�L�����폜���邽�߂̊Ǘ��p�X���[�h��o�^���܂��B<p>\n"; }
	else { print "$message<p>\n"; }

	print "<form method=$method action=\"$reload\">\n";
	print "<input type=hidden name=\"action\" value=\"password\">\n";
	if ($first != 1) { print "���p�X���[�h <input type=password name=\"password_old\" size=10><br>\n"; }
	print "�V�p�X���[�h <input type=password name=\"password\" size=10><br>\n";
	print "�V�p�X���[�h <input type=password name=\"password2\" size=10>�i�m�F�̂��߂�����x�j<p>\n";
	print "<input type=submit value=\"     �o�^     \"></form><p>\n";
	print "</body></html>\n";
	exit;
}

sub encode {

	if ($header eq 'crypt_password') {

		if (crypt($FORM{'password_old'}, substr($password,0,2)) ne $password) { $message = '���p�X���[�h���F�؂���܂���ł���.'; &password; }
	}
	else {
		if (!open(DB,"$file")) { &error(0); }
		@lines = <DB>;
		close(DB);

		$first = 1;
	}

	if ($FORM{'password'} =~ /\W/ || $FORM{'password'} eq '') { $message = '�V�p�X���[�h�ɉp�����ȊO�̕������܂܂�Ă��邩�󗓂ł�.'; &password; }
	if ($FORM{'password'} ne $FORM{'password2'}) { $message = '�m�F�̂��߂ɓ��͂��ꂽ�V�p�X���[�h����v���܂���.'; &password; }

	$now = time;
	($p1, $p2) = unpack("C2", $now);
	$wk = $now / (60*60*24*7) + $p1 + $p2 - 8;
	@saltset = ('a'..'z','A'..'Z','0'..'9','.','/');
	$nsalt = $saltset[$wk % 64] . $saltset[$now % 64];
	$pwd = crypt($FORM{'password'}, $nsalt);

	if (!open(DB,">$file")) { &error(0); }
	print DB "crypt_password:$pwd\n";
	print DB @lines;
	close(DB);

	&html;
}

#end_of_script

