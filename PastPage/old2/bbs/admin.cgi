#!/usr/local/bin/perl

#������������������������������������������������������������������������������
#�� DELUXE LIGHT BORAD v1.29 (admin.cgi)
#�� Copyright(C) 1999-2005 by �j����
#�� kaneko628@yahoo.co.jp
#�� http://kei.s31.xrea.com/
#������������������������������������������������������������������������������
#�� Original CGI Script
#������������������������������������������������������������������������������
#�� LIGHT BOARD v6.41 (admin.cgi)
#�� Copyright(C) KENT WEB 2004
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require './jcode.pl';
require './dlight2.cgi';
require './init.cgi';

&decode;
&setfile;

# �Ǘ����[�h�����w��z�X�g�̂݋���
if ($c_lim) { &c_axs_check; }

if ($mode eq "admin") { &admin; }
elsif ($mode eq "setup") { &setup; }
elsif ($mode eq 'arashi') { &arashi_log; }
elsif ($mode eq "regist") { &regist; }
&error("�s���ȃA�N�Z�X�ł�");

#--------------#
#  �Ǘ����[�h  #
#--------------#
sub admin {

	# ���O�C�����
	if ($in{'pass'} eq "") {
		&header;
		print "<div align=\"center\">\n";
		print "<h4>�p�X���[�h����͂��Ă�������</h4>\n";
		print "<form action=\"$admin\" method=POST>\n";
		print "<input type=radio name=mode value=admin checked>�L��\n";
		print "<input type=radio name=mode value=arashi>�r�炵���O�{��\n";
		print "<input type=radio name=mode value=setup>�ݒ�<br><br>\n";
		print "<input type=password name=pass size=8>\n";
		print "<input type=submit value=\" �F�� \"></form></div>\n";
		print "</body></html>\n";
		exit;
	# �F��
	} elsif ($in{'pass'} ne $pass) {
		&error("�p�X���[�h���Ⴂ�܂�");
	}

	# �폜
	if ($in{'job'} eq "del" && $in{'no'}) {

		# ���b�N�J�n
		&lock if ($lockkey);

		# �폜�L���������
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no) = split(/<>/);
			next if ($in{'no'} == $no);
			push(@new,$_);
		}
		close(IN);

		# �X�V
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);

	# �C���t�H�[��
	} elsif ($in{'job'} eq "edit" && $in{'no'}) {

		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);
			last if ($in{'no'} == $no);
		}
		close(IN);

		&edit_form($no,$dat,$nam,$eml,$sub,$com,$url);

	# �C�����s
	} elsif ($in{'job'} eq "edit2") {

		# ���̓`�F�b�N
		if ($in{'url'} eq "http://") { $in{'url'}=""; }

		# ���b�N�J�n
		&lock if ($lockkey);

		# �폜�L���������
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);
			if ($in{'no'} == $no) {
				$_="$no<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pwd<>$tim<>\n";
			}
			push(@new,$_);
		}
		close(IN);

		# �X�V
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);
	}

	# �Ǘ����
	&header;
	print <<"EOM";
[<a href="$script?">�f���ɖ߂�</a>]
<h3>�L�������e�i���X</h3>
<form action="$admin" method="POST">
<input type=hidden name=mode value="admin">
<input type=hidden name=pass value="$in{'pass'}">
<select name=job>
<option value="edit">�C��
<option value="del">�폜</select>
<input type=submit value="���M����">
<DL>
EOM

	# �L���W�J
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);
		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		$com =~ s/<([^>]|\n)*>//g;
		if (length($com) > 70) {
			$com = substr($com,0,70);
			$com .= "...";
		}

		print "<DT><hr><input type=radio name=no value=\"$no\">";
		print "[<b>$no</b>] <b style='color:$subcol'>$sub</b> - <b>$nam</b> ";
		print "- $dat<DD>$com <font color=\"$subcol\">&lt;$hos&gt;</font>\n";
	}
	close(IN);

	print "<DT><hr></DL></form>\n</body></html>\n";
	exit;
}

#------------#
#  �ݒ菈��  #
#------------#
sub setup {
	if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# �ҏW���s
	if ($in{'job'} eq "setup") {

		# �`�F�b�N
		if (!$in{'home'}) { &error('�߂��̓��͂�����܂���'); }
		if (!$in{'max'}) { &error('�ő�L�����̓��͂�����܂���'); }
		if (!$in{'plog'}) { &error('�\�������̓��͂�����܂���'); }
		if (!$in{'b_size'}) { &error('�{�������T�C�Y�̓��͂�����܂���'); }
		if ($in{'t_img'} eq "http://") { $in{'t_img'}=""; }
		if ($in{'bg'} eq "http://") { $in{'bg'}=""; }

		# �X�V
		open(OUT,">$setfile") || &error("Write Error : $setfile");
		print OUT "$in{'title'}<>$in{'t_col'}<>$in{'t_size'}<>$in{'t_face'}<>$in{'t_img'}<>$in{'bg'}<>$in{'bc'}<>$in{'tx'}<>$in{'li'}<>$in{'vl'}<>$in{'al'}<>$in{'home'}<>$in{'max'}<>$in{'subcol'}<>$in{'refcol'}<>$in{'plog'}<>$in{'b_size'}<>$in{'mail'}<>$in{'deny'}<>$in{'link'}<>$in{'wait'}<>";
		close(OUT);

		# �������b�Z�[�W
		&header;
		print "<div align=center><h3>�ݒ肪�������܂���</h3>\n";
		print "<form action=\"$script\">\n";
		print "<input type=submit value='�f���ɖ߂�'></form>\n";
		print "</body></html>\n";
		exit;
	}

	&header;

	$t_img ||= "http://";
	$bg    ||= "http://";
	$home  ||= "http://";
	$b_size =~ s/\D//g;

	print <<"EOM";
[<a href="$script?">�f���ɖ߂�</a>]
<h3>�ݒ���</h3>
<UL>
<LI>�C�����镔���̂ݕύX���Ă��������B
<form action="$admin" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="setup">
<input type=hidden name=job value="setup">
<table border=0>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>�^�C�g����</td>
  <td><input type=text name=title size=30 value="$title"></td>
</tr>
<tr>
  <td>�^�C�g���F</td>
  <td><input type=text name=t_col size=12 value="$t_col">
	<font color="$t_col">��</font></td>
</tr>
<tr>
  <td>�^�C�g���T�C�Y</td>
  <td><input type=text name=t_size size=5 value="$t_size"> �s�N�Z��</td>
</tr>
<tr>
  <td>�^�C�g���t�H���g</td>
  <td><input type=text name=t_face size=30 value="$t_face"></td>
</tr>
<tr>
  <td>�^�C�g���摜</td>
  <td><input type=text name=t_img size=40 value="$t_img"> �i�C�Ӂj</td>
</tr>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>�ǎ�</td>
  <td><input type=text name=bg size=40 value="$bg"> �i�C�Ӂj</td>
</tr>
<tr>
  <td>�w�i�F</td>
  <td><input type=text name=bc size=12 value="$bc">
	<font color="$bc">��</font></td>
</tr>
<tr>
  <td>�����F</td>
  <td><input type=text name=tx size=12 value="$tx">
	<font color="$tx">��</font></td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type=text name=li size=12 value="$li">
	<font color="$li">��</font> �i���K��j</td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type=text name=vl size=12 value="$vl">
	<font color="$vl">��</font> �i�K��ρj</td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type=text name=al size=12 value="$al">
	<font color="$al">��</font> �i�K�⒆�j</td>
</tr>
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>�L���薼�F</td>
  <td><input type=text name=subcol size=12 value="$subcol">
	<font color="$subcol">��</font></td>
</tr>
<tr>
  <td>���p���F</td>
  <td><input type=text name=refcol size=12 value="$refcol">
	<font color="$refcol">��</font></td>
</tr>
<tr>
  <td>�߂��</td>
  <td><input type=text name=home size=40 value="$home"></td>
</tr>
<tr>
  <td>�ő�L����</td>
  <td><input type=text name=max size=5 value="$max"></td>
</tr>
<tr>
  <td>�\\������</td>
  <td><input type=text name=plog size=5 value="$plog">
	�i1�y�[�W����̋L���\\�����j</td>
</tr>
<tr>
  <td>�{������</td>
  <td><input type=text name=b_size size=5 value="$b_size"> �s�N�Z��</td>
</tr>
<tr>
  <td>URL�����N</td>
  <td>
EOM
	if ($link) {
		print "<input type=radio name=link value=1 checked>����\n",
		"<input type=radio name=link value=0>���Ȃ�\n";
	} else {
		print "<input type=radio name=link value=1>����\n",
		"<input type=radio name=link value=0 checked>���Ȃ�\n";
	}
	print "&nbsp;&nbsp;�i�L������URL�����������N�j</td></tr>\n";
	print "<tr><td>���e�Ԋu</td><td>";
	print "<input type=text name=wait size=5 value=\"$wait\"> �b &nbsp; ";
	print "�i����z�X�g�̘A�����e����j</td></tr>\n";

	if ($sendmail) {
		print "<tr><td colspan=2><hr></td></tr>\n";
		print "<tr><td>�d���[��</td>";
		print "<td><input type=text name=mail size=30 value=\"$mail\"><br>\n";
		print "�i���[���ʒm����ꍇ�j</td></tr>\n";
	}

	print <<"EOM";
<tr><td colspan=2><hr></td></tr>
<tr>
  <td>�w��z�X�g�A�N�Z�X����</td>
  <td><input type=text name=deny size=40 value="$deny"><br>
  �A�N�Z�X�ݒ��init.cgi�Őݒ肷�邱��</td>
</tr>
<tr><td colspan=2><hr></td></tr>
</table>
<input type=submit value="��L�ݒ���C������"></form>
</body>
</html>
EOM
	exit;
}

## --- �Ǘ��҃��[�h�A�N�Z�X����
sub c_axs_check {

	if ($cdeny[0]) {
		# �z�X�g�����擾
		&get_host;

		$c_flag = 1;
		foreach (@cdeny) {

		if ($_ eq '') { last; }
		$_ =~ s/\*/\.\*/g;
		if ($host =~ /$_/) { $c_flag = 0; last; }

		}
	}

		if ($c_flag) {
			# �G���[�\��
			$emode = 6;
			&error("�Ǘ����[�h�ւ̓����͊Ǘ��҈ȊO�ł��܂���B");
		}

}

## �r�炵���O�\����
sub arashi_log {

	# �r�炵���O��ǂݍ���
	open(LOG,"$a_logfile") || &error("Can't open $a_logfile");
	@alines = <LOG>;
	close(LOG);

	shift(@alines);

	# �\���J�n
	&header;
	print "<div align=\"center\">\n";

	print "<b style=\"color:$t_col; font-size:$t_size",
	"px; font-family:'$t_face'\">�r�炵���O</b>\n";

	print <<"EOM";
<hr width=90% size=2></div>
<a name="top"></a>
<div align=right><a href ="#bottom">To Log Bottom</a></div>
<hr noShade><hr>
EOM

	if ($in{'page'} eq '') { $page = 0; } 
	else { $page = $in{'page'}; }

	# �L�������擾
	$end_data = @alines - 1;
	$page_end = $page + ($plog - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }

	foreach ($page .. $page_end) {

	$buf = $alines[$_];

	# ���O�ǂݍ���
	($number,$date,$name,$email,$subj,$comment,$url,$host,$pwd,$e_type,
		$addr,$port,$cook,$ref,$addr2,$conect,$u_agent,
			$acc_lang,$acc_enc,$acc) = split(/<>/,$buf);

		# �^�O����
		$buf =~ s/\"/&quot;/g;
		$buf =~ s/</&lt;/g;
		$buf =~ s/>/&gt;/g;

		# E-mail�y��URL�����N����
		if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
		if ($url) { $url = "<a href=\"http://$url\" target='_brank'>�z�[���y�[�W</a>\n"; }

		# ���������N
		if ($autolink) { &auto_link($comment); }

	print "<table border=0 cellpadding=0 cellspacing=0><tr>\n";
	print "<td valign=top>[$number] <font color=\"$subj_color\"><b>�u$subj�v</b></font>&nbsp<small>$date</small><br>\n";
	print "<font color=\"$name_color\"><b>$name</b></font><td>&nbsp;</td>\n";
	print "</tr></table>\n";
	print "�G���[���e�F<b>$e_type</b><br>\n";
	print "<blockquote>\n";
	print "$comment<p>\n";

	print "URL=<b>$url</b><br>\n";
	print "PASS WORD=<b>$pwd</b><p>\n";
	print "REMOTE_HOST=<b>$host</b><br>\n";
	print "REMOTE_ADDR=<b>$addr</b><br>\n";
	print "REMOTE_PORT=<b>$port</b><p>\n";
	print "HTTP_COOKIE=<b>$cook</b><br>\n";
	print "HTTP_REFERER=<b>$ref</b><br>\n";
	print "HTTP_HOST=<b>$addr2</b><br>\n";
	print "HTTP_CONNECTION=<b>$conect</b><br>\n";
	print "HTTP_USER_AGENT=<b>$u_agent</b><br>\n";
	print "HTTP_ACCEPT_LANGUAGE=<b>$acc_lang</b><br>\n";
	print "HTTP_ACCEPT_ENCODING=<b>$acc_enc</b><br>\n";
	print "HTTP_ACCEPT=<b>$acc</b><p>\n";

	print "</blockquote><hr>\n";

	}

	print "<a name=\"#bottom\"></a>\n";
	print "<hr noShade><div align=right><a href =\"#top\">To Log Top</a></div><hr>\n";

	print "<table border=0 width='100%'><tr>\n";

	# ���ŏ���
	$next_line = $page_end + 1;
	$back_line = $page - $plog;

	# �O�ŏ���
	if ($back_line >= 0) {
		print "<td><form method=\"POST\" action=\"$admin\">\n";
		print "<input type=hidden name=mode value=\"arashi\">\n";
		print "<input type=hidden name=page value=\"$back_line\">\n";
		print "<input type=submit value=\"�O��$plog��\">\n";
		print "</form></td>\n";
	}

	# ���ŏ���
	if ($page_end ne $end_data) {
		print "<td><form method=\"POST\" action=\"$admint\">\n";
		print "<input type=hidden name=mode value=\"arashi\">\n";
		print "<input type=hidden name=page value=\"$next_line\">\n";
		print "<input type=submit value=\"����$plog��\">\n";
		print "</form></td>\n";
	}

	print "<P>$banner2</P></center>\n";
	print "</body></html>\n";
	exit;
}

__END__

