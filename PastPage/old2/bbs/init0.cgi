#������������������������������������������������������������������������������
#�� DELUXE LIGHT BORAD v1.28 (2005.11.30)
#�� Copyright(C) 1999-2005 by �j����
#�� kaneko628@yahoo.co.jp
#�� http://kei.s31.xrea.com/
#������������������������������������������������������������������������������
#�� Original CGI Script
#������������������������������������������������������������������������������
#�� LIGHT BOARD v6.41 (2005/11/27)
#�� Copyright(C) KENT WEB 2004
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'LIGHT BOARD v6.41'; # �o�[�W�������i�C���A�폜�s�j
$ver2 = 'D-LIGHT v1.28'; # �o�[�W�������i�C���A�폜�s�j
#������������������������������������������������������������������������������
#�� [���ӎ����E���ӎ���]
#�� 1.���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p���������Ȃ鑹�Q��
#��   �΂��č�҂͂��̐ӔC����ؕ����܂���B
#�� 2.�ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B���[���ɂ�鎿��ɂ�
#��   �������ł��܂���B
#�� 3.���̃X�N���v�g�̃I���W�i����KENT WEB������LIGHT BOARD�ł��BLIGHT BORAD
#��   �Ɍf���r�炵�΍�@�\����ɁA���L���J�X�^�}�C�Y�@�\�A�e��g�ѓd�b������
#��   ���ǂ����f���V�X�e���𓋍ڂ��Ă��܂��B
#��   �����̋@�\�́A�����҂̓ƒf�ƕΌ��y�у��[�U�[�̕��X�̂��ӌ��⊴�z������
#��   �쐬�E�ǉ����Ă��܂��B
#�� 4.���݂̃o�[�W�����ł�DELUXE LIGHT BORAD�̃��O�� LIGHT BOARD�̃��O�ƌ݊���
#��   ���m�ۂ��Ă���̂ŁA�ϊ������ɂ��̂܂܃��O�������p�����Ƃ��ł��܂��B
#�� 5.�v���N�V�T�[�o���ۋ@�\���[�`������сA�r�炵���O�p�t�@�C���쐬���[�`����
#��   �x�[�X�X�N���v�g�́A���P�j������ɂ����������܂����B
#�� 6.�g���b�v�@�\�� Logue��(http://www.prologue.info/)����AYY-BOARD Next����
#��   �q�؂��܂���(^^�S
#�� 7.�r�炵���O�Ǘ��@�\�����̂��߁Av1.10�ȍ~�̃��O��v1.10�ȑO�ɍ쐬�������O��
#��   �݊����͂���܂���̂ŁA���O�t�@�C�����㏑�����Ă��������B
#��   �ϊ��X�N���v�g�́A�啝�Ȍ`���ύX�̂��ߕt�����Ă���܂���B
#��   ���炩���߂�������������
#�� 8.�g�ѓd�b�̑Ή��󋵂͌���i-mode��J-SKY�݂̂ł��B
#��   EZweb��HDML�𗝉��������������\��ł�(^^;
#��   �{�Ƃ̉ߋ����O�`���̊֌W��A�ߋ����O�@�\�͂����p�����܂���B
#������������������������������������������������������������������������������
#
# [ �ݒu�� ] ���������̓p�[�~�b�V����
#
#    public_html / index.html (�z�[���y�[�W)
#       |
#       +-- bbs / dlight.cgi  [755]
#            |    admin.cgi   [755]
#            |    init.cgi    [644]
#            |    dlight2.cgi [644]
#            |    jcode.pl    [644]
#            |    data.cgi    [666]
#            |    iplock.cgi  [666]
#            |    dlight.dat  [666]
#            |    pastno.dat  [666] .. �ߋ����O�p�J�E���g�t�@�C��
#            |
#            +-- lock [777] /
#            |
#            +-- past [777] / 0001.cgi [666]
#============#
#  �ݒ荀��  #
#============#
	
# �Ǘ��җp�p�X���[�h(���p�p����)
$pass = 'ckuma6143';

# �X�N���v�gURL
$script = './dlight.cgi';
$i_script = './i_dlight.cgi';

# �Ǘ��t�@�C��URL
$admin = './admin.cgi';

# ���O�t�@�C��
$logfile = './data.cgi';

# �ݒ�t�@�C��
$setfile = './dlight.dat';

# �t�@�C�����b�N�`��
#  �� 0=no 1=symlink�֐� 2=mkdir�֐�
$lockkey = 0;

# ���b�N�t�@�C����
$lockfile = './lock/dlight.lock';

# sendmail�p�X�i���[���ʒm����ꍇ�j
# �� �� /usr/lib/sendmail
$sendmail = '';

# �ߋ����O�@�\ (0=no 1=yes)
$pastkey = 1;

# �ߋ����O�f�B���N�g��
$pastdir = './past/';

# �ߋ����O�J�E���g�t�@�C��
$pastno = './pastno.dat';

# �ߋ����O�P�t�@�C������̍ő匏��
$pastmax = 300;

#====================#
#  D-LIGHT �g���@�\  #
#====================#

# �����N�̐F�ݒ� (0=���g�p 1=�X�^�C���V�[�g�̂� 2=�ʏ�\���̂�)
$lstyle = 0;

# �u���E�U�̃L���b�V������ (0=no 1=yes)
$browser_c = 1;

# ���p�J�i -> �S�p�J�i�ϊ� (0=no 1=yes)
$kana = 1;

# �������������b�Z�[�W
$f_message = '����ɓ��e����܂���';

# �^�O�L���}���I�v�V���� (FreeWeb�Ȃǁj
#   �� <!-- �㕔 --> <!-- ���� --> �̑���Ɂu�L���^�O�v��}������B
#   �� �L���^�O�ȊO�ɁAMIDI�^�O �� �J�E���^�p�̃^�O���ɂ��g�p�\�ł��B
$banner1 = '<!-- �㕔 -->';	# �f���㕔�ɑ}��
$banner2 = '<!-- ���� -->';	# �f�������ɑ}��

#================#
#  �g�ѓd�b�Ή�  #
#================#

# �g�ѓd�b�Ή� (0=no 1=yes)
$cellular = 1;

# �\���`�� (0=�I���W�i���`�� 1=�^�C�g�������e�Җ��̂ݕ\��)
$c_type = 1;

# �g�ь����P�y�[�W������̋L���\����
$c_pagelog = 10;

# �g�ь��������P�y�[�W������̋L���\����
$cs_page = 10;

## �g�ѓd�b�����߂�y�[�W�i�t���p�X��http://����URL���L�q�j
# i-mode�p
$i_home = "../index.html";
# J-PHONE�p
$j_home = "../index.html";
# ezWEB�p�i���삵�܂���j
$ez_home = "../ez/index.html";

##�^�C�g���摜�ƁA�R�����g�͏��߂̃y�[�W�̂ݕ\��
## �^�C�g���摜�i�g�p����ꍇ�͉摜�܂ł̃p�X�j
# i-mode�p
$i_tg = "";
# J-PHONE�p
$j_tg = "";
# ezWEB�p�i���삵�܂���j
$ez_tg = "";

# ���߂̃y�[�W�ɕ\�������Ǘ��҃R�����g
$c_com = '���C�y�ɂǂ���';

# �������ݏI�����̃��b�Z�[�W
$cf_message = '�������݊���';

#==================#
#  �r�炵�΍�@�\  #
#==================#

# �������b�Z�[�W
$block_mes = "�����������p�ł��܂���";

# �^�O�\��������[�h�F�^�O�����̂ݗL�� (0=no 1=yes)
$tagwid = 1;

# ���^�O�F�^�O�\��������[�h�I�����̂ݗL��
$tagclose = "</font></span></b></u></s></i></marquee></a></em>";

# �^�O�̋��� (0=no 1=�S�ċ��� 2=�����t����)
$tagkey = 2;

# �񋖉^�O�i�^�O���������L�q�j
@tag =('script','meta','html','body','','','');

# ���e�L���ʂ̏��(0�œ��e�ʐ����Ȃ�)
# �o�C�g���Z�F�S�p�P�����Q�o�C�g
$mes_size = 51200;

# �폜�L�[�̓��͋��� (0=no 1=yes)
$passkey = 1;

# �w��z�X�g�A�N�Z�X�����@�\ (0=no 1=�w��z�X�g���� 2=�w��z�X�g�̂݋���)
$ac_lim = 1;

# �z�X�g���擾���[�h
#  --> 0 : $ENV{'REMOTE_HOST'} �Ŏ擾�ł���ꍇ
#  --> 1 : gethostbyaddr �Ŏ擾�ł���ꍇ
$get_remotehost = 0;

# �������ݐ����i���O)
@k_name = (
	'',
	'',
	'',
	'',
	'');

# �������ݐ����i�P��)
@k_word = (
	'http',
	'sex',
	'',
	'',
	'');

# IP�A�h���X�⊮�t�@�C����
$ipfile = './iplock.cgi';

# �⊮IP�A�h���X��
$ipcount = 5;

# �L���Ƀz�X�g�A�h���X�\�� (0=no 1=yes)
$hostview = 0;

# �v���N�V���ۋ@�\ (0=no 1=yes)
$proxy = 0;

# �v���N�V���ʂ̃��x��
# 0 = �v���N�V����f���o���Ă���z�X�g�r��(�W��)
# 1 = 0�{[jp]���܂܂Ȃ��z�X�g�r��
# 2 = 0�{1�{�������܂܂Ȃ��z�X�g�r���i�ʏ��IP�A�h���X�{�z�X�g���Ńz�X�g�A�h���X�͒񋟂���Ă��邽�߁j
$proxylevel = 0;

# ���v���N�V�i�z�X�g�����L�q�j
@pdeny = (
	'*.hogehoge.ne.jp',
	'xxx.proxy.com',
	'',
	'',
	'');

# �N�b�L�[�����r�� (0=no 1=yes)
$cook = 0;

# �r�炵���O�쐬�@�\ (0=no 1=yes)
$arashilog = 0;

# �Ǘ��҂̂݉{������ (0=no 1=yes)
$a_view = 1;

# �r�炵���O�t�@�C����
$a_logfile = './arashi.cgi';

# �r�炵���O�̃��[���ʒm (0=no 1=yes)
$amail = 0;

# �r�炵���O�̃��[���ɖ{�����M (0=no 1=yes)
$mail_com = 0;

# �r�炵���O���쐬����r�炵�΍�@�\ (0=no 1=yes)
$alog1 = 1;        # Type 1�F�s���A�N�Z�X
$alog2 = 1;        # Type 2�F�v���N�V�G���[
$alog3 = 1;        # Type 3�F�֎~���[�h
$alog4 = 1;        # Type 4�F�r�炵�w��n���h��
$alog5 = 1;        # Type 5�F�N�b�L�[����
$alog6 = 1;        # Type 6�F�w��z�X�g����
$alog7 = 1;        # Type 7�FMETA�^�O�g�p

# �g���b�v�@�\ (0=no 1=yes)
$trip = 1;

# �Ǘ����[�h�������� (0=no 1=yes)
$c_lim = 0;

# �Ǘ����[�h�̓������i������z�X�g�����L�q�j
@cdeny = (
	'*.sendai-ct.ac.jp',
	'',
	'',
	'',
	'');

#============#
#  �ݒ芮��  #
#============#

#--------------------#
#  �t�H�[���f�R�[�h  #
#--------------------#
sub decode {
	local($buf, $key, $val);

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag = 1;
			# ���e�ʂ̐�������
			if ($mes_size != 0) {
				if ($ENV{'CONTENT_LENGTH'} > $mes_size) { &error("���e�ʂ��傫�����܂�"); }
			}
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$post_flag = 0;
		$buf = $ENV{'QUERY_STRING'};
	}
	%in=();
	foreach ( split(/&/, $buf) ) {
		($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		#���p�J�i -> �S�p�J�i�ϊ�
		if ($kana) { &jcode'h2z_sjis(*value); }

		# S-JIS�R�[�h�ϊ�
		&jcode'convert(*val, "sjis", "", "z");

		# �񋖉^�O���m����
		if ($tagkey == 2) {
			foreach (@tag) {
				if ($val =~ /<$_/i) {
					$emode = 7;
					&error("�u$_�v�^�O�̎g�p�͂�������������");
				}
			}
		}

		# �^�O����
		if ($tagkey == 0) {
			$val =~ s/&/&amp;/g;
			$val =~ s/\"/&quot;/g;
			$val =~ s/</&lt;/g;
			$val =~ s/>/&gt;/g;
			$val =~ s/\0//g;
		} else {
			$val =~ s/<!--(.|\n)*-->//g;
			$val =~ s/<>/&lt;&gt;/g;
		}

		# ���s����
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\r/<br>/g;
		$val =~ s/\n/<br>/g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$page = $in{'page'};
	$mode = $in{'mode'};
	$headflag = 0;
	$lockflag = 0;
	$ENV{'TZ'} = "JST-9";
}

#--------------------#
#  �ݒ�t�@�C���F��  #
#--------------------#
sub setfile {
	# �ݒ�t�@�C���ǂݍ���
	open(IN,"$setfile") || &error("Open Error : $setfile");
	local($file) = <IN>;
	close(IN);

	# �ݒ���e�F��
	($title,$t_col,$t_size,$t_face,$t_img,$bg,$bc,$tx,$li,$vl,$al,$home,$max,$subcol,$refcol,$plog,$b_size,$mail,$deny,$link,$wait) = split(/<>/, $file);

	# �v���N�V����
	if ($proxy) { &proxy; }

	# �N�b�L�[�����r��
	if ($cook) { &chk_cookie; }

	# �A�N�Z�X����
	&get_host;

	# �A�N�Z�X����
	if ($deny) {
	    $flag = 0;
	    foreach ( split(/\s+/, $deny) ) {

			# �z�X�g�����s�g�p
			if ($ac_lim == 0) { last; }

			# �w��z�X�g����
			elsif ($ac_lim == 1) {
			    if ($_ eq '') { last; }
			    $_ =~ s/\*/\.\*/g;
			    if ($host =~ /$_/i) { $flag = 1; last; }
			}

			# �w��z�X�g����
			elsif ($ac_lim == 2) {
			    $flag = 1;
			    if ($_ eq '') { last; }
			    $_ =~ s/\*/\.\*/g;
			    if ($host =~ /$_/i) { $h_flag = 0; last; }
			}

			# �s���Ȓl������̃G���[���
			else { last; }

		}

		if ($flag) {
			# �G���[�\��
			$emode = 6;
			&error("$block_mes");
		}
	}

	$b_size .= "px";
}

#--------------#
#  HTML�w�b�_  #
#--------------#
sub header {
	if ($headflag) { return; }
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<!--nobanner-->
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
EOM

	# �u���E�U�̃L���b�V������
	if ($browser_c) {
		print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
		print "<META HTTP-EQUIV=\"Cache-Control\" CONTENT=\"no-cache\">\n";
	}
	
	print <<"EOM";
<STYLE TYPE="text/css">
<!--
body,tr,td,th {
	font-size:$b_size;
	font-family:"MS UI Gothic,�l�r �o�S�V�b�N,Osaka";
}
.num { font-family:Verdana,Helvetica,Arial; }
.l { background-color: #666666; color: #ffffff; }
.r { background-color: #ffffff; color: #000000; }
EOM

	# �����N�̃X�^�C���V�[�g�g�p
	if ($lstyle != 2) {
		print "A:link {color: #$li; text-decoration: none;}\n";
		print "A:active {color: #$al; text-decoration: underline;}\n";
		print "A:hover {color: #$al; text-decoration: underline;}\n";
		print "A:visited {color: #$vl; text-decoration: underline;}\n";
	}

	print <<"EOM";
-->
</STYLE>
<title>$title</title></head>
EOM
	if ($lstyle == 2) {
		if ($bg) {
		  print "<body background=\"$bg\" bgcolor=$bc text=$tx>\n";
		} else {
		  print "<body bgcolor=$bc text=$tx>\n";
		}
	} else {
		if ($bg) {
		  print "<body background=\"$bg\" bgcolor=$bgc tx=$text link=$li vlink=$vl alink=$al>\n";
		} else {
		  print "<body bgcolor=$bc text=$tx link=$li vlink=$vl alink=$al>\n";
		}
	}
#	print "<center>$banner1</center><P>\n";
	$headflag=1;
}

#----------------#
#  HTML�̃t�b�^  #
#----------------#
sub footer {
	## ���쌠�\���i�폜�s�j
	print <<"EOM";
<center>$banner2<P>
<span style='font-size:10px;font-family:Verdana,Helvetica'>
- <a href="http://www.kent-web.com/" target='_blank'>Light Board</a> -<!-- $ver --><br>
- <a href="http://kei.s31.xrea.com/" target='_blank'>Deluxe Light Board</a> -<!-- $ver2 -->
</span></center>
</body></html>
EOM
}

#--------------#
#  �G���[����  #
#--------------#
sub error {
	if ($lockflag) { &unlock; }

	$title = "�G���[";;

	if ($b_mode) {
	  # �g��

	  &c_header;

	  # ezWEB�i�������j
	  # if ( $b_mode == 3) {
	  # }

	  # i-mode��J-SKY
	  # else {
	    print "<center>ERROR !<hr>";
	    print "<p>$_[0]</p>";
	    print "<hr></center>";
	    print "</body></html>";
	  # }

	} else {
	  # PC�����̑�
	  &header;

	  print "<center><hr width=75%><h3>ERROR !</h3>\n";
	  print "<P><font color=#DD0000><B>$_[0]</B></font>\n";
	  print "<P><hr width=75%></center>\n";
	  print "</body></html>";
	}

	## �r�炵�G���[����
	$a_flag = 0;
	# Type 1�F�s���A�N�Z�X
	if ($emode == 1 || $alog1) {
		$e_type = "�s���A�N�Z�X";
		$a_flag = 1;
	}
	# Type 2�F�v���N�V�G���[
	elsif ($emode == 2 || $alog2) {
		$e_type = "�v���N�V����";
		$a_flag = 1;
	}
	# Type 3�F�֎~���[�h
	elsif ($emode == 3 || $alog3) {
		$e_type = "�֎~���[�h�g�p";
		$a_flag = 1;
	}
	# Type 4�F�r�炵�w��n���h��
	elsif ($emode == 4 || $alog4) {
		$e_type = "�r�炵�w��n���h���g�p";
		$a_flag = 1;
	}
	# Type 5�F�N�b�L�[����
	elsif ($emode == 5 || $alog5) {
		$e_type = "�N�b�L�[����";
		$a_flag = 1;
	}
	# Type 6�F�w��z�X�g����
	elsif ($emode == 6 || $alog6) {
		$e_type = "�w��z�X�g����";
		$a_flag = 1;
	}
	# Type 7�F�񋖉^�O�g�p
	elsif ($emode == 7 || $alog7) {
		$e_type = "�񋖉^�O�g�p";
		$a_flag = 1;
	}
	# �s���Ȓl������̃G���[���
	else { $a_flag = 0; }

	&alog_w;

	exit;
}

#--------------#
#  ���b�N����  #
#--------------#
sub lock {
	# 1���ȏ�Â����b�N�͍폜����
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 60) { &unlock; }
	}
	local($retry) = 5;
	# symlink�֐������b�N
	if ($lockkey == 1) {
	
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	# mkdir�֐������b�N
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}
	$lockflag=1;
}

#--------------#
#  ���b�N����  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }

	$lockflag=0;
}

#----------------#
#  �ҏW�t�H�[��  #
#----------------#
sub edit_form {
	local($no,$dat,$nam,$eml,$sub,$com,$url) = @_;
	$url ||= "http://";
	$com =~ s/<br>/\r/g;

	&header;
	print <<"EOM";
[<a href="javascript:history.back()">�O��ʂɖ߂�</a>]
<h3>�ҏW�t�H�[��</h3>
<UL>
<LI>�C�����镔���̂ݕύX���Ă��������B
EOM

	if ($in{'pass'} ne "") {
		print "<form action=\"$admin\" method=\"POST\">\n";
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
		print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=hidden name=job value=\"edit2\">\n";
	} else {
		print "<form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=\"editlog\">\n";
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
		print "<input type=hidden name=pwd value=\"$in{'pwd'}\">\n";
		print "<input type=hidden name=job value=\"edit2\">\n";
	}

	print <<"EOM";
���e�Җ�<br><input type=text name=name size=28 value="$nam"><br>
�d���[��<br><input type=text name=email size=28 value="$eml"><br>
�^�C�g��<br><input type=text name=sub size=36 value="$sub"><br>
�Q�Ɛ�<br><input type=text name=url size=45 value="$url"><br>
�R�����g<br><textarea name=comment cols=58 rows=7 wrap=soft>$com</textarea><br>
<input type=submit value=" �C�����s�� "></form>
</UL>
</body>
</html>
EOM
	exit;
}

#----------------#
#  �z�X�g���擾  #
#----------------#
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($get_remotehost && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }
}
1;

__END__

