#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� LIGHT BOARD v6.12  <light.cgi>
#�� Copyright(C) KENT WEB
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#�b
#�b modified for i-mode by ckuma <i_light.cgi>
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require './jcode.pl';
require './init.pl';

# �\�����Œ�
$i_plog = 5;

&decode;
&setfile;
if ($mode eq "regist") { &regist; }
#elsif ($mode eq "howto") { &howto; }
elsif ($mode eq "find") { &find; }
#elsif ($mode eq "dellog") { &dellog; }
#elsif ($mode eq "editlog") { &editlog; }
elsif ($mode eq "past") { &pastlog; }
elsif ($mode eq "check") { &check; }
&viewlog;

#------------#
#  �L���\��  #
#------------#
sub viewlog {
	local($x,$y,$i,$flag,$no,$dat,$nam,$eml,$sub,$com,$url,$resub,$recom);

	# �N�b�L�[�擾
	local($cnam,$ceml,$curl,$cpwd) = &get_cookie;
	$curl ||= "http://";

	# �^�C�g���\��
	&header;

#	print "�i�b��^�p�j";

	print "<div align=\"center\">\n";
#	if ($t_img) {
#		print "<img src=\"$t_img\" alt=\"$title\">\n";
#	} else {
		print "<b style=\"color:$t_col; font-size:$t_size",
		"px; font-family:'$t_face'\">$title</b>\n";
#	}

	# �\���J�n
	print <<"EOM";
<hr width="90%">
[<a href="$home" target="_top">�g�b�v�ɖ߂�</a>]<br>
[<a href="$i_script?mode=find">���[�h����</a>]<br>
EOM
#[<a href="$i_script?mode=howto">���ӎ���</a>]<br>

	# �ߋ����O�����N
	print "[<a href=\"$i_script?mode=past\">�ߋ����O</a>]\n" if ($pastkey);

	# ���O�ҏW�@�\�̃����N
#	print "[<a href=\"$admin?mode=admin\">�Ǘ��p</a>]\n";

	# �ԐM���[�h
	$resub='';
	$recom='';
	if ($in{'res'}) {
		# ���p�L�����o
		open(IN,"$logfile") || &error("Open Error : $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com) = split(/<>/);
			last if ($in{'res'} == $no);
		}
		close(IN);

		# �R�����g�Ɉ��p���t��
		$recom = "&gt; $com";
		$recom =~ s/<br>/\r&gt; /g;

		# �薼�Ɉ��p���ڕt��
		$sub =~ s/^Re://;
		$resub = "Re:[$in{'res'}] $sub";
	}

$cpwd = "";
	# ���e�t�H�[��
	print <<"EOM";
<hr width="90%"></div>
<form method="POST" action="$i_script">
<input type=hidden name=mode value="regist">
<blockquote>

<b>���Ȃ܂�</b><br>
<input type=text name=name size=10 value="$cnam"><br>
<b>�d���[��</b><br>
<input type=text name=email size=10 value="$ceml"><br>
<b>�^�C�g��</b><br>
<input type=text name=sub size=10 value="$resub"><br>
<b>�R�����g</b><br>
<textarea cols=10 rows=1 name=comment wrap="soft">$recom</textarea><br>
<b>�Q�Ɛ�</b><br>
<input type=text size=10 name=url value="$curl"><br>
<input type=submit value="���e����"><br><input type=reset value="���Z�b�g"><br>

</form>
</blockquote>
EOM
#<b>�p�X���[�h</b><br>
#<input type=password name=pwd size=8 maxlength=8 value="$cpwd"><br>

	# �L���W�J
	$i=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	while (<IN>) {
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $i_plog) { next; }

		($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);
		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
		$com .= "<P><a href=\"$url\" target=\"_blank\">$url</a>" if ($url);

		# �L���ҏW

        print "<hr>\n";
        print "[<b>$no</b>] <font color=\"$subcol\"><b>$sub</b></font> ";
        print "���e�ҁF<b>$nam</b> ";
        print "<small>���e���F$dat</small>&nbsp;\n";
        print "<form action=\"$i_script\" method=\"POST\">\n";
        print "<br>$com<BR><BR>\n";
        print "<input type=hidden name=res value=\"$no\">\n";
        print "<input type=submit value=\"���̋L���ɕԐM\">";
        print "</form>";

	}
	close(IN);
	print "<hr>\n";

        # ���ŏ���
	$next = $page + $i_plog;
	$back = $page - $i_plog;
	$flag=0;
	print "<table cellpadding=0 cellspacing=0><tr>\n";

        # �O�ŏ���
	if ($back >= 0) {
		$flag=1;
		print "<td><form action=\"$i_script\" method=\"POST\">\n";
                print "<input type=hidden name=page value=\"$back\">\n";
                print "<input type=submit value=\"�O�y�[�W\">\n";
                print "</form></td>\n"; 
        }

        # ���ŏ���
	if ($next < $i) {
		$flag=1;
		print "<td><form action=\"$i_script\" method=\"POST\">\n";
		print "<input type=hidden name=page value=\"$next\">\n";
                print "<input type=submit value=\"���y�[�W\">\n";
                print "</form></td>\n";
        }

        # ���[�U�L���폜�t�H�[��
#	print <<"EOM";
#<P>
#<form acion="$i_script" method="POST">
#���e�L���폜<br>
#<input type=hidden name=mode value=dellog>
#���L��No<input type=text name=no size=6><br>
#���폜�L�[<input type=password name=pwd size=8 maxlength=8><br>
#<input type=submit value='�L���폜'>
#</form></P>
	print <<"EOM";
</tr></table>
<P><small>- <a href="http://www.kent-web.com/" target='_top'>Light Board</a> -
</body>
</html>
EOM
	exit;
}

#----------------#
#  ���O��������  #
#----------------#
sub regist {
	local($pwd,$past,@w,@past,@file);

	# ���̓`�F�b�N
	if (!$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }
	if ($in{'name'} eq "") { &error("���O�����͂���Ă��܂���"); }
	if ($in{'comment'} eq "") { &error("�R�����g�����͂���Ă��܂���"); }
	if ($in{'email'} && $in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/) {
		&error("�d���[���̓��͓��e������������܂���");
	}
	if ($in{'url'} eq "http://") { $in{'url'}=""; }
	if ($in{'sub'} eq "") { $in{'sub'} = "����"; }

	# �t�@�C�����b�N
	&lock if ($lockkey);

	# ���O���J��
	open(IN,"$logfile") || &error("Open Error : $logfile");
	@file = <IN>;
	close(IN);

	# ��d���e�֎~
	local($no,$dat,$nam,$eml,$sub,$com,$url,$ho,$pw,$tim) = split(/<>/, $file[0]);
	if ($host eq $ho && $wait > time - $tim) {
		&error("�A�����e�͂������΂炭���Ԃ�u���Ă�������");
	}
	if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
		&error("��d���e�͋֎~�ł�");
	}

	# �L��������
	@past=();
	while ($max <= @file) {
		$past = pop(@file);
		push(@past,$past) if ($pastkey);
	}

	# �ߋ����O
	if (@past > 0) { &pastmake(@past); }

	# �폜�L�[���Í���
	if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }

	# ���Ԃ��擾
	local($min,$hour,$mday,$mon,$year,$wday) = (localtime(time))[1..6];
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);

	# ���O���X�V
	$time = time;
	$no++;
	unshift (@file,"$no<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>\n");
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @file;
	close(OUT);

	# ���b�N����
	&unlock if ($lockkey);

	# �N�b�L�[�𔭍s
	&set_cookie;

	# ���[������
	if ($sendmail && $mail && $in{'email'} ne $mail) { &mailto; }

	# �������b�Z�[�W
	&header;
	print "<div align=center><hr width=400>\n";
	print "<h3>���e�͐���ɏ�������܂���</h3>\n";
	print "<form action=\"$i_script\">\n";
	print "<input type=submit value='�f���֖߂�'></form>\n";
	print "<hr width=400></div>\n</body></html>\n";
	exit;
}

#------------#
#  ���ӎ���  #
#------------#
sub howto {
	&header;
	print <<"EOM";
[<a href="$i_script?">�f���ɖ߂�</a>]
<P><table border=1 bgcolor="white" align="center" width="85%" cellpadding=15><tr><td>
<font color="black">
<h3 style="font-size:12pt">�f�����p��̒���</h3>
<OL>
<LI>���̌f����<b>�N�b�L�[�Ή�</b>�ł��B�P�x�L���𓊍e���������ƁA���Ȃ܂��A�d���[���A�t�q�k<!--�A�폜�L�[-->�̏���2��ڈȍ~�͎������͂���܂��B�i���������p�҂̃u���E�U���N�b�L�[�Ή��̏ꍇ�j
<LI>���e���e�ɂ́A<b>�^�O�͈�؎g�p�ł��܂���B</b>
<LI>�L���𓊍e�����ł̕K�{���͍��ڂ�<b>�u���Ȃ܂��v</b>��<b>�u���b�Z�[�W�v</b>�ł��B�d���[���A�t�q�k�A�薼<!--�A�폜�L�[-->�͔C�ӂł��B
<LI>�L���ɂ́A<b>���p�J�i�͈�؎g�p���Ȃ��ŉ������B</b>���������̌����ƂȂ�܂��B
<!--<LI>�L���̓��e����<b>�p�X���[�h</b>�i�p������8�����ȓ��j�����Ă����ƁA���̋L���͎���p�X���[�h�ɂ���č폜���邱�Ƃ��ł��܂��B-->
<LI>�L���̕ێ������͍ő�<b>$max��</b>�ł��B����𒴂���ƌÂ����ɉߋ����O�Ɉړ����܂��B
<LI>�����̋L���ɊȒP��<b>�u�ԐM�v</b>���邱�Ƃ��ł��܂��B�e�L���ɂ���<b>�u�ԐM�v�{�^��</b>�������Ɠ��e�t�H�[�����ԐM�p�ƂȂ�܂��B
<LI>�ߋ��̓��e�L������<b>�u�L�[���[�h�v�ɂ���ĊȈՌ������ł��܂��B</b>�g�b�v���j���[��<a href="$i_script?mode=find">�u���[�h�����v</a>�̃����N���N���b�N����ƌ������[�h�ƂȂ�܂��B
<LI>�Ǘ��҂��������s���v�Ɣ��f����L���⑼�l���排�������L����\�\\��\�Ȃ��폜���邱�Ƃ�����܂��B
</OL>
</font>
</td></tr></table>
</body>
</html>
EOM

	exit;
}

#------------#
#  �������  #
#------------#
sub find {
	&header;
	print <<"EOM";
[<a href="$i_script?">�f���ɖ߂�</a>]
<UL>
<LI>����������<b>�L�[���[�h</b>����͂��A�u�����v�u�\\���v��I�����āu�����v�{�^���������ĉ������B
<LI>�L�[���[�h�́u���p�X�y�[�X�v�ŋ�؂��ĕ����w�肷�邱�Ƃ��ł��܂��B
</UL>
EOM
#<table><tr>
	&search("find", $logfile);
	print "</body></html>\n";
	exit;
}

#------------#
#  ��������  #
#------------#
sub search {
	local($md, $target) = @_;
	local($i, $flag, $next, $back, $enwd, $wd, @wd);

	print "<!--<td>--><form action=\"$i_script\" method=\"POST\">\n",
	"<input type=hidden name=mode value=\"$md\">\n";

	local($para)='';
	if ($md eq "past") {
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		$para = "&pastlog=$in{'pastlog'}";
	}

	print "<b>�L�[���[�h</b><br><input type=text name=word size=10 value=\"$in{'word'}\"><br>",
	"<b>����</b> <select name=cond> &nbsp; ";

	if ($in{'cond'} eq "") { $in{'cond'} = "AND"; }
	foreach ("AND", "OR") {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select><br><b>�\\��</b> <select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = 10; }
	foreach (10,15,20,25,30) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_��\n";
		} else {
			print "<option value=\"$_\">$_��\n";
		}
	}
	print "</select><br><input type=submit value=' ���� '>",
	"<!--</td>--></form><!--</tr></table>-->\n";

	# ���[�h�����̎��s�ƌ��ʕ\��
	if ($in{'word'} ne ""){

		# ���͓��e�𐮗�
		$in{'word'} =~ s/\x81\x40/ /g;
		@wd = split(/\s+/, $in{'word'});

		# �t�@�C����ǂݍ���
		print "\n";
		$i=0;
		open(IN,"$target") || &error("Open Error : $target");
		while (<IN>) {
			$flag=0;
			foreach $wd (@wd) {
				if (index($_,$wd) >= 0) {
					$flag=1;
					if ($in{'cond'} eq 'OR') { last; }
				} else {
					if ($in{'cond'} eq 'AND') { $flag=0; last; }
				}
			}
			if ($flag) {
				$i++;
				if ($i < $page + 1) { next; }
				if ($i > $page + $in{'view'}) { next; }

				($no,$ymd,$nam,$eml,$sub,$com,$url) = split(/<>/);
				if ($eml) { $nam="<a href=\"mailto:$eml\">$nam</a>"; }
				if ($url) { $com .= "<P><a href=\"$url\" target=\"_blank\">$url</a>"; }

				print "<hr>[<b>$no</b>] ",
				"<font color=\"$subcol\"><b>$sub</b></font> ",
				"���e�ҁF<b>$nam</b> ���e���F$ymd<br><br>\n",
				"$com<br><br>\n";
			}
		}
		close(IN);
		print "<hr>�������ʁF<b>$i</b>��<br>\n";

		$next = $page + $in{'view'};
		$back = $page - $in{'view'};
		$enwd = &url_enc($in{'word'});
		if ($back >= 0) {
			print "[<a href=\"$i_script?mode=$md&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}$para\">�O��$in{'view'}��</a>]\n";
		}
		if ($next < $i) {
			print "[<a href=\"$i_script?mode=$md&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}$para\">����$in{'view'}��</a>]\n";
		}
		print "</body></html>\n";
		exit;
	}
}

#------------------#
#  �N�b�L�[�̔��s  #
#------------------#
sub set_cookie {
	local($gmt, $cook, @t, @m, @w);
	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	$cook = "$in{'name'}<>$in{'email'}<>$in{'url'}<>$in{'pwd'}";
	print "Set-Cookie: LightBoard=$cook; expires=$gmt\n";
}

#------------------#
#  �N�b�L�[���擾  #
#------------------#
sub get_cookie {
	local($key, $val, *ck);

	$ck = $ENV{'HTTP_COOKIE'};
	foreach (split(/;/, $ck)) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$ck{$key} = $val;
	}
	@ck = split(/<>/, $ck{'LightBoard'});
	return (@ck);
}

#------------#
#  �L���폜  #
#------------#
sub dellog {
	local($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,@new);
exit;
	# ���̓`�F�b�N
	if (!$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("�L��No���̓p�X���[�h�����͂���Ă��܂���");
	}

	# ���b�N�J�n
	&lock if ($lockkey);

	# ���O��ǂݍ���
	$flag=0;
	@new=();
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);
		if ($in{'no'} == $no) {
			if ($pwd eq "") { $flag=2; last; }
			$check = &decrypt($in{'pwd'}, $pwd);
			if ($check) { $flag=1; next; }
			else { $flag=3; last; }
		}
		push(@new,$_);
	}
	close(IN);
	if (!$flag) { &error("�Y���L������������܂���"); }
	elsif ($flag == 2) { &error("�p�X���[�h���ݒ肳��Ă��܂���"); }
	elsif ($flag == 3) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# ���O�X�V
	open(OUT,">$logfile") || &error("Write Error: $logfile");
	print OUT @new;
	close(OUT);

	# ���b�N����
	&unlock if ($lockkey);

	# �������b�Z�[�W
	&header;
	print <<"EOM";
<div align="center">
<h3>�L���͐���ɍ폜����܂���</h3>
<form action="$i_script">
<input type=submit value="�f���ɖ߂�"></form>
</div>
</body>
</html>
EOM
	exit;
}

#------------#
#  �L���C��  #
#------------#
sub editlog {
	local($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,@new);
return;
	# ���̓`�F�b�N
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("�L��No���̓p�X���[�h�����͂���Ă��܂���");
	}

	# �C�����s
	if ($in{'job'} eq "edit2") {
		# ���̓`�F�b�N
		if ($in{'name'} eq "") { &error("���O�����͂���Ă��܂���"); }
		if ($in{'comment'} eq "") { &error("�R�����g�����͂���Ă��܂���"); }
		if ($in{'email'} && $in{'email'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/) {
			&error("�d���[���̓��͓��e������������܂���");
		}
		if ($in{'url'} eq "http://") { $in{'url'}=""; }
		if ($in{'sub'} eq "") { $in{'sub'} = "����"; }

		# ���b�N�J�n
		&lock if ($lockkey);

		# �����ւ�
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);
			if ($in{'no'} == $no) {
				$_="$no<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pwd<>$tim<>\n";
				$pwd2 = $pwd;
			}
			push(@new,$_);
		}
		close(IN);

		# �F�؃`�F�b�N
		$check = &decrypt($in{'pwd'}, $pwd2);
		if (!$check) { &error("�p�X���[�h���Ⴂ�܂�"); }

		# �X�V
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);

		return;
	}

	# �L�����o
	$flag=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);
		if ($in{'no'} == $no) { $flag=1; last; }
	}
	close(IN);

	if (!$flag) {
		&error("�Y���̋L����������܂���");
	} elsif ($pwd eq "") {
		&error('���̋L���̓p�X���[�h���ݒ肳��Ă��Ȃ����߁A�C���s�\�ł�');
	}
	$check = &decrypt($in{'pwd'}, $pwd);
	if (!$check) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# �C���t�H�[��
	&edit_form($no,$dat,$nam,$eml,$sub,$com,$url);
}

#--------------#
#  ���[�����M  #
#--------------#
sub mailto {
	local($mail_sub, $mail_body, $email);

	# ���[���^�C�g�����`
	$mail_sub = "[$title : $no] $in{'sub'}";

	# �L���̉��s�E�^�O�𕜌�
	$com  = $in{'comment'};
	$com =~ s/<br>/\n/g;
	$com =~ s/&lt;/</g;
	$com =~ s/&gt;/>/g;
	$com =~ s/&quot;/"/g;
	$com =~ s/&amp;/&/g;

	# ���[���{�����`
	$mail_body = <<"EOM";
--------------------------------------------------------
���e�����F$date
�z�X�g���F$host
�u���E�U�F$ENV{'HTTP_USER_AGENT'}

���e�Җ��F$in{'name'}
�d���[���F$in{'email'}
�t�q�k  �F$in{'url'}
�^�C�g���F$in{'sub'}
���e�L���F

$com
--------------------------------------------------------
EOM
	# JIS�R�[�h�ϊ�
    	&jcode'convert(*mail_sub, 'jis', 'sjis');
    	&jcode'convert(*mail_body, 'jis', 'sjis');

	# ���[���A�h���X���Ȃ��ꍇ
	if ($in{'email'} eq "") { $email = $mailto; }
	else { $email = $in{'email'}; }

	open(MAIL,"| $sendmail -t") || &error("���[�����M���s");
	print MAIL "To: $mail\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $mail_sub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	print MAIL $mail_body;
	close(MAIL);
}

#------------------#
#  �p�X���[�h�Í�  #
#------------------#
sub encrypt {
	local($inp) = $_[0];
	local($salt, $crypt, @char);

	# ��╶������`
	@char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');

	# �����Ŏ�𒊏o
	srand;
	$salt = $char[int(rand(@char))] . $char[int(rand(@char))];

	# �Í���
	$crypt = crypt($inp, $salt) || crypt ($inp, '$1$' . $salt);
	$crypt;
}

#------------------#
#  �p�X���[�h�ƍ�  #
#------------------#
sub decrypt {
	local($inp, $log) = @_;

	# �풊�o
	local($salt) = $log =~ /^\$1\$(.*)\$/ && $1 || substr($log, 0, 2);

	# �ƍ�
	if (crypt($inp, $salt) eq $log || crypt($inp, '$1$' . $salt) eq $log) { return (1); }
	else { return (0); }
}

#--------------#
#  ���������N  #
#--------------#
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"$2\" target=\"_top\">$2<\/a>/g;
}

#-----------------#
#  URL�G���R�[�h  #
#-----------------#
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#----------------#
#  �ߋ����O���  #
#----------------#
sub pastlog {
	local($no, $i, $file, $next, $back);

	open(IN,"$pastno") || &error("Open Error: $pastno");
	$no = <IN>;
	close(IN);

	$in{'pastlog'} =~ s/\D//g;
	if (!$in{'pastlog'}) { $in{'pastlog'} = $no; }

	&header;
	print <<"EOM";
[<a href="$i_script?">�f���ɖ߂�</a>]<hr>
<form action="$i_script" method="POST">
<input type=hidden name=mode value=past>
<!--<table><tr><td>--><b>�ߋ����O</b><br><select name=pastlog>
EOM
	# �ߋ����O�I��
	for ($i=$no; $i>0; --$i) {
		$i = sprintf("%04d", $i);
		next unless (-e "$pastdir$i\.cgi");
		if ($in{'pastlog'} == $i) {
			print "<option value=\"$i\" selected>$i\n";
		} else {
			print "<option value=\"$i\">$i\n";
		}
	}
	print "</select> <input type=submit value='�ړ�'></form>";

	$file = sprintf("%s%04d\.cgi", $pastdir,$in{'pastlog'});
	&search("past", $file);

	print "\n";
	$i=0;
	open(IN,"$file") || &error("Open Error: $file");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $i_plog) { last; }

		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;

		if ($eml) { $nam = "<a href=\"mailto:$eml\">$nam</a>"; }
		if ($url) { $url = "&lt;<a href=\"$url\" target=\"_blank\">URL</a>&gt;"; }

		print "<hr>[<b>$no</b>] <b style='color:$subcol'>$sub</b> ",
		"���e�ҁF<b>$nam</b> ���e���F$dat &nbsp; $url <br><br>$com<br><br>\n";

	}
	close(IN);
	print "<hr>\n";

	$next = $page + $i_plog;
	$back = $page - $i_plog;
	print "<table><tr>\n";
	if ($back >= 0) {
		print "<td><form action=\"$i_script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$back\">\n";
		print "<input type=submit value=\"�O��$i_plog��\"></td></form>\n";
	}
	if ($next < $i) {
		print "<td><form action=\"$i_script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=submit value=\"����$i_plog��\"></td></form>\n";
	}
	print "</tr></table>\n</body></html>\n";
	exit;

}

#----------------#
#  �ߋ����O����  #
#----------------#
sub pastmake {
	local(@past) = @_;
	local($count,$pastfile,$i,$f);

	@past = reverse @past;

	# �ߋ����O�t�@�C�������`
	open(NO,"$pastno") || &error("Open Error : $pastno");
	$count = <NO>;
	close(NO);
	$pastfile = sprintf("%s%04d\.cgi", $pastdir,$count);

	# �ߋ����O���J��
	$i=0; $f=0;
	@data=();
	open(IN,"$pastfile") || &error("Open Error : $pastfile");
	while (<IN>) {
		$i++;
		push(@data,$_);

		# �ő匏���𒴂���ƒ��f
		if ($i >= $pastmax) { $f++; last; }
	}
	close(IN);

	# �ő匏�����I�[�o�[����Ǝ��t�@�C������������
	if ($f) {
		# �J�E���g�t�@�C���X�V
		$count++;
		open(NO,">$pastno") || &error("Write Error : $pastno");
		print NO $count;
		close(NO);

		$pastfile = sprintf("%s%04d\.cgi", $pastdir,$count);
		@data = @past;
	} else {
		unshift(@data,@past);
	}

	# �ߋ����O���X�V
	open(OUT,">$pastfile") || &error("Write Error : $pastfile");
	print OUT @data;
	close(OUT);

	if ($f) { chmod(0666, $pastfile); }
}

#------------------#
#  �`�F�b�N���[�h  #
#------------------#
sub check {
	&header;
	print "<h2>Check Mode</h2><UL>\n";

	# ���O�`�F�b�N
	foreach ($logfile, $setfile) {
		if (-e $_) {
			print "<LI>�p�X�F$_ �� OK\n";
			if (-r $_ && -w $_) { print "<LI>�p�[�~�b�V�����F$_ �� OK\n"; }
			else { print "�p�[�~�b�V�����F$_ �� NG\n"; }
		} else {
			print "<LI>�p�X�F$_ �� NG\n";
		}
	}

	# ���b�N�f�B���N�g��
	print "<LI>���b�N�`���F";
	if ($lockkey == 0) { print "���b�N�ݒ�Ȃ�\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }
		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<LI>���b�N�f�B���N�g���F$lockdir\n";

		if (-d $lockdir) {
			print "<LI>���b�N�f�B���N�g���̃p�X�FOK\n";
			if (-r $lockdir && -w $lockdir && -x $lockdir) {
				print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FOK\n";
			} else {
				print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FNG �� $lockdir\n";
			}
		} else { print "<LI>���b�N�f�B���N�g���̃p�X�FNG �� $lockdir\n"; }
	}

	# �ߋ����O
	@yn = ('�Ȃ�', '����');
	print "<LI>�ߋ����O�F$yn[$pastkey]\n";
	if ($pastkey) {
		if (-e $pastno) {
			print "<LI>�p�X�F$pastno �� OK\n";
			if (-r $pastno && -w $pastno) {
				print "<LI>�p�[�~�b�V�����F$pastno �� OK\n";
			} else {
				print "<LI>�p�[�~�b�V�����F$pastno �� NG\n";
			}
		} else {
			print "<LI>�p�X�F$pastno �� NG\n";
		}
		if (-d $pastdir) {
			print "<LI>�p�X�F$pastdir �� OK\n";
			if (-r $pastdir && -w $pastdir && -x $pastdir) {
				print "<LI>�p�[�~�b�V�����F$pastdir �� OK\n";
			} else {
				print "<LI>�p�[�~�b�V�����F$pastdir �� NG\n";
			}
		} else {
			print "<LI>�p�X�F$pastdir �� NG\n";
		}
	}
	print "</UL>\n</body></html>\n";
	exit;
}

__END__

