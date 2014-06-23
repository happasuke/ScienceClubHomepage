#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� DreamCounter
#�� drmgr.cgi - 2008/03/05
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# IIS�΍�
if ($ENV{'SERVER_SOFTWARE'} =~ /IIS/i) {
	local($chdir) = $0;
	$chdir =~ s/[^\\]*$//;
	chdir($chdir);
}

# �ݒ�t�@�C���捞
require './drinit.cgi';

&parse_form;
if ($in{'pass'} eq '') {
	&enter_disp;
} elsif ($in{'pass'} ne $pass) {
	&error('�p�X���[�h���Ⴂ�܂�');
}

# ���O�`�F�b�N
@file = &datadir;

# �V�K�쐬
if ($mode eq 'new' && $in{'id'}) {

	# ���̓`�F�b�N
	if ($in{'id'} =~ /[^A-Za-z0-9]/) {
		&error("�g�p�ł��镶���͉p�����݂̂ł�");
	}
	if ($in{'count'} =~ /\D/) {
		&error("�J�n�J�E���g���͐����݂̂Ŏw�肵�ĉ�����");
	}

	my $flg;
	foreach (@file) {
		if ($_ eq "$in{'id'}.dat") { $flg = 1; last; }
	}
	if ($flg) { &error("$in{'id'} �͊��ɑ��݂���ID���ł�"); }

	# �쐬
	open(OUT,">$datadir$in{'id'}.dat") || &error("Write Error: $in{'id'}.dat");
	print OUT $in{'count'};
	close(OUT);

	chmod(0666, "$datadir$in{'id'}.dat");

	unshift(@file,"$in{'id'}.dat");

# ���O�����e���
} elsif ($mode eq 'mente' && $in{'id'}) {

	open(IN,"$datadir$in{'id'}.dat") || &error("Open Error: $in{'id'}.dat");
	my $log = <IN>;
	close(IN);

	my ($count, $ip) = split(/:/, $log);

	&header;
	print qq|<form action="$drmgrcgi" method="post">\n|;
	print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
	print qq|<input type="hidden" name="mode" value="mente2">\n|;
	print qq|<input type="hidden" name="id" value="$in{'id'}">\n|;
	print qq|ID�� : <b>$in{'id'}</b><br>\n|;
	print qq|�J�E���g�� : <input type="text" name="count" size="8" value="$count"><br>\n|;
	print qq|<input type="submit" value="�C������"></form>\n|;
	print qq|</body></html>\n|;
	exit;

# ���O�����e���s
} elsif ($mode eq 'mente2' && $in{'id'}) {

	if ($in{'count'} =~ /\D/) {
		&error("�J�n�J�E���g���͐����݂̂Ŏw�肵�ĉ�����");
	}

	open(DAT,"+< $datadir$in{'id'}.dat") || &error("Open Error: $in{'id'}.dat");
	eval "flock(DAT, 2);";
	my $log = <DAT>;

	my ($count, $ip) = split(/:/, $log);

	seek(DAT, 0, 0);
	print DAT "$in{'count'}:$ip";
	truncate(DAT, tell(DAT));
	close(DAT);

# ���O�폜
} elsif ($mode eq 'del' && $in{'id'}) {

	unlink("$datadir$in{'id'}.dat") || &error("Del Error: $in{'id'}.dat");
	@file = &datadir;
}

&header;
print <<EOM;
<h3>�Ǘ����</h3>
<form action="$drmgrcgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="mode" value="new">
<hr><b>1. �V�K���O�쐬</b><br><br>
���OID�� <input type="text" name="id" size="12"> (�p������ID���w��)<br>
�J�E���g�J�n�� <input type="text" name="count" size="8" value="0"><br>
<input type="submit" value="�V�K�쐬">
</form>
<form action="$drmgrcgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<hr>
<b>2. ���O�����e</b><br><br>
�����F
<select name="mode">
<option value="mente">�C��
<option value="del">�폜
</select>
<input type="submit" value="�I������">
<dl>
EOM

foreach (@file) {
	s/\.dat$//;
	print qq|<dt><input type="radio" name="id" value="$_">$_\n|;
}

print <<EOM;
</dl>
</form>
<hr>
</body>
</html>
EOM
exit;

#-------------------------------------------------
#  �������
#-------------------------------------------------
sub enter_disp {
	&header;
	print <<EOM;
<div align="center">
<h4>�p�X���[�h����͂��ĉ�����</h4>
<form action="$drmgrcgi" method="post">
<input type="password" name="pass" size="12">
<input type="submit" value=" �F�� ">
</form>
<br><br>
<!-- ���쌠�\\���i�폜���ϋ֎~�j-->
- <a href="http://www.kent-web.com/">$ver</a> -
</div>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �G���[����
#-------------------------------------------------
sub error {
	&header;
	print <<EOM;
<div align="center">
<h3>ERROR !</h3>
<font color="red">$_[0]</font>
</div>
</body>
</html>
EOM
	exit;
}


