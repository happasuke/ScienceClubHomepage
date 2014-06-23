#������������������������������������������������������������������������������
#�� DELUXE LIGHT BORAD v1.29 (dlight2.cgi)
#��   Included...
#��       �r�炵�΍�@�\ v1.01
#��       Celluar D-LIGHT v.1.00 �i�g�ѓd�b�Ή��@�\�t���j
#�� Copyright(C) 1999-2005 by �j����
#�� kaneko628@yahoo.co.jp
#�� http://kei.s31.xrea.com/
#������������������������������������������������������������������������������

### �r�炵�΍�@�\ v1.01
## --- �N�b�L�[�����`�F�b�N
sub chk_cookie {
	unless($ENV{'HTTP_COOKIE'}){
		($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time + 120*24*60*60);
		$year += 1900;

		$sec = sprintf( "%02d",$sec);
		$min = sprintf( "%02d",$min);
		$hour = sprintf( "%02d",$hour);
		$mday = sprintf( "%02d",$mday);

		$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mon];
		$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wday];
		$date_gmt = "$youbi, $mday\-$month\-$year $hour:$min:$sec GMT";

		print "Set-Cookie: Cookie=on; expires=$date_gmt\n";

		$emode = 5;
		&error("�N�b�L�[���I���ɂ��Ă��������B");
	}
}

## ---�v���N�V���ۋ@�\
sub proxy{

	if ($pdeny[0]) {
		# �z�X�g�����擾
		&get_host;

		$p_flag = 1;
		foreach (@pdeny) {
			if ($_ eq '') { last; }
			$_ =~ s/\*/\.\*/g;
			# ���v���N�V
			if ($host =~ /$_/) { $p_flag = 0; last; }
		}
	}

	if ($p_flag) {

	# �v���N�V���ۋ@�\���C������
	if($host =~/delegate|gateway|gatekeeper|firewall|proxy|anony|squid|cache|^bbs|^http|^www|^web|^dns|^ftp|^mail|^news|^cgi|^gate|^server|^pop|^smtp|^w3\.|^ns\d{0,2}\.|^fw\d{0,2}\.|^gw\d{0,2}\./i) { &p_error; }
	if($agent =~ /via|proxy|gateway|delegate|anony|squid|cache|httpd|turing|wwwc/i) { &p_error; }
	if($ENV{'HTTP_CONNECTION'}!~ /Keep-Alive/i) { &p_error; }
	if($ENV{'HTTP_FORWARDED'}) { &p_error; }
	if($ENV{'HTTP_X_FORWARDED_FOR'}) { &p_error; }
	if($ENV{'HTTP_VIA'}) { &p_error; }
	if($ENV{'HTTP_CLIENT_IP'}) { &p_error; }
	if($ENV{'HTTP_SP_HOST'}) { &p_error; }
	if($ENV{'HTTP_FROM'}) { &p_error; }
	if($ENV{'HTTP_PROXY_CONNECTION'}) { &p_error; }
	if($ENV{'HTTP_CACHE_CONTROL'}) { &p_error; }
	if($ENV{'HTTP_CACHE_INFO'}) { &p_error; }
	if($ENV{'HTTP_X_LOOKING'}) { &p_error; }

		# ���ʃ��x������
		if($proxylevel){
			# ���x��1
			if($host !~/jp$/i) { &p_error; }

			# ���x��2
			if($proxylevel == 2){
			    if($host !~/[0-9]/) { &p_error; }
			}
		}

	}

}

## ---�v���N�V���ۃG���[
sub p_error {
	$emode = 2;
	&error("�v���N�V���g�p���Ă̏������݂͂������肢�܂�");
}

## --- �g���b�v�ϊ� from YY-BOARD Next
# Copyright(C) Logue 2000-2002
# http://www.prologue.info/
sub trip($){
	my $seed = shift;
	my $salt = substr($seed, 1, 2);
	$salt =~ tr/\x00-\x20\x7B-\xFF/./;
	$salt =~ tr/\x3A-\x40\x5B-\x60/A-Ga-f/;
	return(substr(crypt($seed, $salt), -8));
}

## --- �r�炵���O�֘A�ŏI����
sub alog_w {
	if ($a_flag) {
		# �r�炵���O�쐬
		if ($arashilog)	{ &a_log; }

		#�r�炵���O�̃��[�����M
		if ($amail) { &amailto; }
	}
}

## --- �r�炵���O��������
sub a_log {

	# �t�@�C�����b�N
	if ($lockkey) { &lock; }

	# ���O���J��
	open(IN,"$a_logfile") || &error("Can't open $a_logfile");
	@aread = <IN>;
	close(IN);

	# ���O�`�F�b�N
	$a_init = $aread[0];
	unless ($a_init =~ /^ARASHI_LOG/) { &error("�r�炵���O������������܂���"); }

	# �ݒ��F��
	($head,$no) = split(/<>/,$a_init);

	# ���Ԃ��擾
	local($min,$hour,$mday,$mon,$year,$wday) = (localtime(time))[1..6];
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);

	# ���O�ԍ��J�E���g�A�b�v
	$no++;

	shift(@aread);

	# ���O���t�H�[�}�b�g
	unshift(@aread,"$no<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$e_type<>$ENV{'REMOTE_ADDR'}<>$ENV{'REMOTE_PORT'}<>$ENV{'HTTP_COOKIE'}<>$ENV{'HTTP_REFERER'}<>$ENV{'REMOTE_ADDR'}<>$ENV{'HTTP_CONNECTION'}<>$ENV{'HTTP_USER_AGENT'}<>$ENV{'HTTP_ACCEPT_LANGUAGE'}<>$ENV{'HTTP_ACCEPT_ENCODING'}<>$ENV{'HTTP_ACCEPT'}<>\n");

	# �w�b�_��t��
	unshift (@aread,"$head<>$no<>\n");

	# ���O���X�V
	open(OUT,">$a_logfile") || &error("Can't write $a_logfile");
	print OUT @aread;
	close(OUT);

	# ���b�N����
	if ($lockkey) { &unlock; }
}

## --- �r�炵���O���[�����M
sub amailto {
	$mail_sub = "$title �ɍr�炵�w��҂�����܂����B";

    	&jcode'convert(*mail_sub,'jis');
    	&jcode'convert(*name,'jis');
    	&jcode'convert(*sub,'jis');
    	&jcode'convert(*comment,'jis');
	if ($date_type) { &jcode'convert(*date,'jis'); }

	$comment =~ s/<br>/\n/g;
	$comment =~ s/&lt;/</g;
	$comment =~ s/&gt;/>/g;
	$comment =~ s/&amp;/\&/g;

	if ($in{'email'} eq "") { $email = $mail1; }

	if (!open(MAIL,"| $sendmail -t")) { &error("���[�����M�Ɏ��s���܂����B");}
	print MAIL "To: $mail1\n";
	print MAIL "From: $email\n";
	if ($mail2) { print MAIL "CC: $mail2\n"; }
	print MAIL "Subject: $mail_sub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	print MAIL "--------------------------------------------------------\n";
	print MAIL "TIME : $date\n";
	print MAIL "NAME : $name\n";
	print MAIL "EMAIL: $in{'email'}\n";
	if ($url ne "") { print MAIL "URL  : http://$url\n"; }
	if ($in{'sub'} eq "") { $sub = "no title"; }
	print MAIL "TITLE: $sub\n\n\n";
	print MAIL "ERROR: $e_type\n\n";
	if ($mail_com) { print MAIL "$comment\n\n"; }
	print MAIL "�ȉ��A�r�炵�̏��\n";
	print MAIL "REMOTE_HOST\=$host\n";
	print MAIL "REMOTE_ADDR\=$ENV{'REMOTE_ADDR'}\n";
	print MAIL "REMOTE_PORT\=$ENV{'REMOTE_PORT'}\n\n";
	print MAIL "HTTP_COOKIE\=$ENV{'HTTP_COOKIE'}\n";
	print MAIL "HTTP_REFERER\=$ENV{'HTTP_REFERER'}\n";
	print MAIL "HTTP_HOST\=$ENV{'REMOTE_ADDR'}\n";
	print MAIL "HTTP_CONNECTION\=$ENV{'HTTP_CONNECTION'}\n";
	print MAIL "HTTP_USER_AGENT\=$ENV{'HTTP_USER_AGENT'}\n";
	print MAIL "HTTP_ACCEPT_LANGUAGE\=$ENV{'HTTP_ACCEPT_LANGUAGE'}\n";
	print MAIL "HTTP_ACCEPT_ENCODING\=$ENV{'HTTP_ACCEPT_ENCODING'}\n";
	print MAIL "HTTP_ACCEPT\=$ENV{'HTTP_ACCEPT'}\n\n";
	print MAIL "--------------------------------------------------------\n";
	close(MAIL);
}


### Celluar D-LIGHT v.1.00
## --- �L�����A����
sub browser {

	$u_agent = $ENV{'HTTP_USER_AGENT'};

	# i���[�h
	if ($u_agent =~ /DoCoMo\//) { $b_mode = 1; }

	# J-SKY
	elsif ($u_agent =~ /J-PHONE\//) { $b_mode = 2; }

	# ezWEB�i�������j
	# elsif($u_agent =~ /UP\.Browser\//) { $b_mode = 3; }

	# PC�����̑�
	else { $b_mode = 0; }
}

## --- �g�ѓd�b�������C������
sub c_main {

	if ($mode eq "msg") { &regist; }			# �������ݏ���
	elsif ($mode eq "find") { &c_find; }		# ����
	elsif ($mode eq "res") { &c_write; }		# �������݃t�H�[���i�ԐM�j
	elsif ($mode eq "usr_del") { &usr_del; }	# ���[�U�[�L���폜����
	elsif ($mode eq "del") { &c_del; }			# �폜�t�H�[��
	elsif ($mode eq "write") { &c_write; }		# �������݃t�H�[���i�V�K�j
	elsif ($mode eq "howto") { &c_howto; }		# ���p�K��

	&c_html_log;
}

## --- �g�ѓd�b�����w�b�_�[
sub c_header {

	print "Content-type: text/html\n\n";
	print "<html><head>";
	print "<title>$title</title></head>";

	# BODY�^�O
	if ($c_bgr eq '') {
		print "<body bgcolor=$bgc text=$text link=$link>";
	} else {
		print "<body background=\"$c_bgr\" bgcolor=$bgc text=$text link=$link>";
	}
}

## --- �g�ѓd�b�����t�b�^�[
sub c_footer {
	print "<hr>";

	## �t�b�^�[�����쌠�\���i�폜�s�j
	print "<a href=\"http://www.kent-web.com/i/\">$ver</a><br>";
	# J-SKY
	if ($b_mode == 2) {
		$url = "http://www.aya.or.jp/~nyanko/kei/j/";
	# i-mode
	} else {
		$url = "http://www.aya.or.jp/~nyanko/kei/i/";
	}

		print "<a href=\"$url\">$ver2</a>";

	print "</body></html>";
}

## --- �g�ѓd�b�����L���\��
sub c_html_log {

	# ���O��ǂݍ���
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# ���ݒ蕔��F��
	$init = $lines[0];
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,
		$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2)
								 = split(/<>/,$init);

	# ���O�`�F�b�N
	unless ($init =~ /^LIGHT/) { &error("۸ނ��s���ł�"); }

	shift(@lines);

	&c_header;

	# �\���J�n
	if ($in{'page'} eq '') { $page = 0; } 
	else { $page = $in{'page'}; }

	# �^�C�g�����Ǘ��҃R�����g
	# �ŏ��̃y�[�W�ȊO�͕\�����Ȃ�
	if ($page == 0) {
		if ($i_tg eq '') {
			print "<center><b>$title</b>";
		} else {
			print "<img src=\"$i_tg\">";
		}
		print "</center><br>";
		print "$c_com";
		print "<hr>";
	}

	# �L�������擾
	$end_data = @lines - 1;
	$page_end = $page + ($c_pagelog - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }

	foreach ($page .. $page_end) {
		($number,$date,$name,$email,$subj,$comment,$url,$host,$pwd)
						 = split(/<>/,$lines[$_]);

		# �\���`������
		if ($c_type) {

			# �L���\��
			print "[$number] <a href=\"$script?mode=res&no=$number\">$subj</a>:$name<br>";

			$hr = 1;

		} else {
			# E-mail�AURL�����N�y�ѓ��t�\���ϊ�����
			if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
			if ($url) { $url = "<a href=\"http://$url\">&gt;HP&lt;</a>"; }
			# ������͌g�ѓd�b�����ɍœK���������t�\���ɂ���\��
			$date =~ s/\) /\)<br>/g;

			# ���������N�iURL�j
			if ($autolink) { &ij_link($comment); }

			# �L���\��
			print "[$number] $subj<br>";
			print "$date<br>";
			print "$name<p>";
			print "$comment<br>";
			print "$url";
			print "<p>[<a href=\"$script?mode=res&no=$number\">�ԐM</a>]</p>";

			# �^�O�\���������
			if ($tagwid) { print "$tagclose"; }

			# �z�X�g�\������
			if ($hostview) { print "<small>$host</small>"; }

			print "<hr>";
		}

	}

	# ���ŏ���
	$next_line = $page_end + 1;
	$back_line = $page - $c_pagelog;

	$page_flag = 0;

	# �O�ŏ���
	if ($back_line >= 0) {
		print "<a href=\"$script?page=$back_line\"><<�V</a> ";
		$page_flag = 1;
	}

	# ���ŏ���
	if ($page_end ne $end_data) {
		print "<a href=\"$script?page=$next_line\">��>></a>";
		$page_flag = 1;
	}

	# ���`����
	if ($page_flag) {
		# �c���[�\������<hr�^�O���}������Ȃ����ۉ��
		if ($hr) {
			print "<hr>";
			$hr = 0;
		}

		# �t���O�������Ă����琮�`�̂���<p>�^�O��}��
		print "<p>";

	}

	# ���j���[�g�ݗ���
	# J-SKY
	if ($b_mode == 2) {
		print "<a href=\"$j_home\" DIRECTKEY=\"1\">[1] HOME</a><br>";
		print "<a href=\"$script?mode=write\" DIRECTKEY=\"2\">[2] �V�K</a><br>";
		print "<a href=\"$script?mode=howto\" DIRECTKEY=\"3\">[3] ���p�K��</a><br>";
		print "<a href=\"$script?mode=find\" DIRECTKEY=\"4\">[4] ����</a><p>";
		print "<a href=\"$script?mode=del\" DIRECTKEY=\"5\">[5] �L���폜</a><p>";
	# i-mode
	} else {
		print "<a href=\"$i_home\" ACCESSKEY=\"1\">&#63879; HOME</a><br>";
		print "<a href=\"$script?mode=write\" ACCESSKEY=\"2\">&#63880; �V�K</a><br>";
		print "<a href=\"$script?mode=howto\" ACCESSKEY=\"3\">&#63881; ���p�K��</a><br>";
		print "<a href=\"$script?mode=find\" ACCESSKEY=\"4\">&#63882; ����</a><br>";
		print "<a href=\"$script?mode=del\" ACCESSKEY=\"5\">&#63883; �L���폜</a><br>";
	}

	&c_footer;
	exit;
}

# --- �g�ѓd�b�������e�t�H�[��
sub c_write {

	# ���O��ǂݍ���
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# ���ݒ蕔��F��
	$init = $lines[0];
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,
		$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2)
								 = split(/<>/,$init);

	# ���O�`�F�b�N
	unless ($init =~ /^LIGHT/) { &error("۸ނ��s���ł�"); }

	shift(@lines);

	&c_header;

	# �ԐM���[�h�̏ꍇ
	if ($mode eq "res") {
		foreach $line (@lines) {
			($number,$date,$name,$email,$subj,$comment) = split(/<>/,$line);
			if ($number eq $in{'no'}) { last; }
		}

		# �c���[�\��������
		if ($c_type) {
			# E-mail�AURL�����N�y�ѓ��t�\���ϊ�����
			if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
			if ($url) { $url = "<a href=\"http://$url\">&gt;HP&lt;</a>"; }
			# ������͌g�ѓd�b�����ɍœK���������t�\���ɂ���\��
			$date =~ s/\) /\)<br>/g;

			# ���������N�iURL�j
			if ($autolink) { &ij_link($comment); }

			# �L���\��
			print "[$number] $subj<br>";
			print "$date<br>";
			print "$name<p>";
			print "$comment<br>";
			print "$url";

			# �^�O�\���������
			if ($tagwid) { print "$tagclose"; }

			# �z�X�g�\������
			if ($hostview) { print "<small>$host</small>"; }

			print "<hr>";
		}


		# �ԐM�p���ڂ��쐬
		if ($subj =~ /^Re/) {
			$subj =~ s/Re//;
			$res_sub = "Re\[$number\]" . "$subj";

		} else {
			$res_sub = "Re\[$number\]\: $subj";
		}

	}

	# ���e�t�H�[���g�ݗ���
	# J-SKY
	if ($b_mode == 2) {
		print "<form action=\"$script\" method=\"GET\">";
	# i-mode
	} else {
		print "<form action=\"$script\" method=\"POST\">";
	}

	print "<input type=hidden name=mode value=\"msg\">";
	print "���O:<input type=text name=name size=10><br>";
	print "Mail:<input type=text name=email istyle=\"3\" size=10><br>";

	# �ԐM���[�h�̏ꍇ
	if ($mode eq "res") {
		print "����:<input type=text name=sub size=10 value=\"$res_sub\"><br>";
	} else {
		print "����:<input type=text name=sub size=10><br>";
	}

	print "<textarea cols=15 rows=3 name=comment wrap=\"$wrap\">$res_comment</textarea><br>";
	print "URL :<input type=text istyle=\"3\" size=10 name=url value=\"http://\"><br>";
	print "PASS:<input type=password name=pwd size=8 maxlength=8><br>";

	# J-SKY
	if ($b_mode == 2) {
		print "<input type=submit name=\"send\" value=\"���M\"><input type=reset name=\"reset\" value=\"�ر\"></form>";
	# i-mode
	} else {
		print "<input type=submit value=\"���M\"><input type=reset value=\"�ر\"></form>";
	}

	print "<hr><a href=\"$script\">�߂�</a>";

	&c_footer;
	exit;
}

# --- �g�ѓd�b�������[�U�L���폜�t�H�[��
sub c_del {

	# ���O��ǂݍ���
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# ���ݒ蕔��F��
	$init = $lines[0];
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,
		$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2)
								 = split(/<>/,$init);

	# ���O�`�F�b�N
	unless ($init =~ /^LIGHT/) { &error("۸ނ��s���ł�"); }

	&c_header;

	# �폜�t�H�[���g�ݗ���
	print "<br><center>�L���폜</center><p>";

	# J-SKY
	if ($b_mode == 2) {
		print "<form action=\"$script\" method=\"GET\">";
	# i-mode
	} else {
		print "<form action=\"$script\" method=\"POST\">";
	}

	print "<input type=hidden name=mode value=\"usr_del\">";
	print "No :<input type=text name=usr_no size=8><br>";
	print "PASS:<input type=password name=usr_key size=8><br>";

	# J-SKY
	if ($b_mode == 2) {
		print "<input type=submit name=\"del\" value=\"�폜\">";
	# i-mode
	} else {
		print "<input type=submit value=\"�폜\">";
	}
	print "</form>";

	print "<hr><a href=\"$script\">�߂�</a>";
	&c_footer;
	exit;
}

## --- �g�ѓd�b�����f���̎g�������b�Z�[�W
sub c_howto {

	# ���O��ǂݍ���
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# ���ݒ蕔��F��
	$init = $lines[0];
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,
		$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2)
								 = split(/<>/,$init);

	# ���O�`�F�b�N
	unless ($init =~ /^LIGHT/) { &error("۸ނ��s���ł�"); }

	if ($tagkey == 0) { $tag_msg = "��ނ͎g�p�s�ł�"; }
	else { $tag_msg = "��ނ͎g�p�ł�"; }

	if ($passkey ==0) { $pass_msg ="���O����Ă͕K�{�ł��MAIL�URL����٤PASS�͔C�ӂł�"; }
	else { $pass_msg ="���O����ĤPASS�͕K�{�ł��MAIL�URL����٤PASS�͔C�ӂł�"; }

	&c_header;

	print "<br><center>���p��̒���</center><hr><P>";
	print "$tag_msg<P>";
	print "�G�����͎g�p�֎~�ł�";
	print "$pass_msg<P>";
	print "PASS����͂���Ƥ��œ��e�����L�����폜�ł��܂�<P>";
	print "�L���͍ő�$max���ۑ�����܂�<P>";
	print "�Ǘ��҂̔��f�ɂ�褓��e�L����\�\\��\�Ȃ��폜���邱�Ƃ�����܂��";
	print "<hr><a href=\"$script\">�߂�</a>";

	&c_footer;
	exit;
}

## --- �g�ѓd�b�������[�h�����T�u���[�`��
sub c_find {
	# ���O��ǂݍ���
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# ���ݒ蕔��F��
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2) = split(/<>/,$lines[0]);

	&c_header;

	# �����t�H�[���g�ݗ���
	print "<br><center>ܰ�ތ���</center><br>";
	print "������ܰ�ނ͋󔒂ŋ�؂��ĉ�����<P>";

	# J-SKY
	if ($b_mode == 2) {
		print "<form action=\"$script\" method=\"GET\">";
	# i-mode
	} else {
		print "<form action=\"$script\" method=\"POST\">";
	}

	print "<input type=hidden name=mode value=\"find\">";
	print "��ܰ�� :";
	print "<input type=text name=word size=8><br>";
	print "��������:";
	print "<input type=radio name=cond value=\"and\" checked>AND";
	print "<input type=radio name=cond value=\"or\">OR<br>";

	# J-SKY
	if ($b_mode == 2) {
		print "<input type=submit name=\"serc\" value=\"����\"><input type=reset name=\"reset\" value=\"�ر\"></form>";
	# i-mode
	} else {
		print "<input type=submit value=\"����\"><input type=reset value=\"�ر\"></form>";
	}

	print "</center>";

	# ���[�h�����̎��s�ƌ��ʕ\��
	if ($in{'word'} ne "") {

		# ���͓��e�𐮗�
		$cond = $in{'cond'};
		$word = $in{'word'};
		$word =~ s/\t/ /g;
		@pairs = split(/ /,$word);

		shift(@lines);

		# ��������
		foreach $line (@lines) {
			$flag = 0;
			foreach $pair (@pairs){

			if (index($line,$pair) >= 0){
				$flag = 1;
				if ($cond eq 'or') { last; }
			} else {
				if ($cond eq 'and'){ $flag = 0; last; }
			}
		}
		if ($flag == 1) { push(@new,$line); }
	}
	# �����I��


		# �L�������擾
		$count = @new;
		print "<hr>�������ʁF$count��<br>����ܰ�ށF$word";

		# �y�[�W�����ݒ�
		if ($in{'page'} eq '') { $page = 0; } 
		else { $page = $in{'page'}; }

		$end_data = @new - 1;
		$page_end = $page + ($cs_page - 1);
		if ($page_end >= $end_data) { $page_end = $end_data; }

		print "<hr>";

		# �\���J�n
		foreach ($page .. $page_end) {
			($number,$date,$name,$email,$subj,$comment,$url,$host) = split(/<>/,$new[$_]);

			# �\���`������
			if ($c_type) {

				# �L���\��
				print "[$number] <a href=\"$script?mode=res&no=$number\">$subj</a>:$name<br>";

				$hr = 1;

			} else {
				# E-mail�AURL�����N�y�ѓ��t�\���ϊ�����
				if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
				if ($url) { $url = "<a href=\"http://$url\">&gt;HP&lt;</a>"; }
				# ������͌g�ѓd�b�����ɍœK���������t�\���ɂ���\��
				$date =~ s/\) /\)<br>/g;

				# ���������N�iURL�j
				if ($autolink) { &ij_link($comment); }

				# �L���\��
				print "[$number] $subj<br>";
				print "$date<br>";
				print "$name<p>";
				print "$comment<br>";
				print "$url";
				print "<p>[<a href=\"$script?mode=res&no=$number\">�ԐM</a>]</p>";

				# �^�O�\���������
				if ($tagwid) { print "$tagclose"; }

				# �z�X�g�\������
				if ($hostview) { print "<small>$host</small>"; }

				print "<hr>";
			}
		}

	}

	# ���ŏ���
	$next_line = $page_end + 1;
	$back_line = $page - $cs_page;

	$page_flag = 0;
	# �O�ŏ���
	if ($back_line >= 0) {
		print "<a href=\"$script?mode=find&page=$back_line&cond=$cond&word=$word\"><<�V</a> ";
		$page_flag = 1;
	}

	# ���ŏ���
	if ($page_end ne $end_data) {
		print "<a href=\"$script?mode=find&page=$next_line&cond=$cond&word=$word\">��>></a>";
		$page_flag = 1;
	}

	# ���`����
	if ($page_flag) {
		# �c���[�\������<hr�^�O���}������Ȃ����ۉ��
		if ($hr) {
			print "<hr>";
			$hr = 0;
		}

		# �t���O�������Ă����琮�`�̂���<p>�^�O��}��
		print "<p>";

	}

	print "<a href=\"$script\">�߂�</a><br>";

	&c_footer;
	exit;
}

## --- i-mode J-SKY�p���������N
sub ij_link {
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<a href=$2>$2<\/a>/g;
}

1;

__END__

