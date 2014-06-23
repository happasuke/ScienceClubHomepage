#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DreamCounter
#│ drmgr.cgi - 2008/03/05
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

# IIS対策
if ($ENV{'SERVER_SOFTWARE'} =~ /IIS/i) {
	local($chdir) = $0;
	$chdir =~ s/[^\\]*$//;
	chdir($chdir);
}

# 設定ファイル取込
require './drinit.cgi';

&parse_form;
if ($in{'pass'} eq '') {
	&enter_disp;
} elsif ($in{'pass'} ne $pass) {
	&error('パスワードが違います');
}

# ログチェック
@file = &datadir;

# 新規作成
if ($mode eq 'new' && $in{'id'}) {

	# 入力チェック
	if ($in{'id'} =~ /[^A-Za-z0-9]/) {
		&error("使用できる文字は英数字のみです");
	}
	if ($in{'count'} =~ /\D/) {
		&error("開始カウント数は数字のみで指定して下さい");
	}

	my $flg;
	foreach (@file) {
		if ($_ eq "$in{'id'}.dat") { $flg = 1; last; }
	}
	if ($flg) { &error("$in{'id'} は既に存在するID名です"); }

	# 作成
	open(OUT,">$datadir$in{'id'}.dat") || &error("Write Error: $in{'id'}.dat");
	print OUT $in{'count'};
	close(OUT);

	chmod(0666, "$datadir$in{'id'}.dat");

	unshift(@file,"$in{'id'}.dat");

# ログメンテ画面
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
	print qq|ID名 : <b>$in{'id'}</b><br>\n|;
	print qq|カウント数 : <input type="text" name="count" size="8" value="$count"><br>\n|;
	print qq|<input type="submit" value="修正する"></form>\n|;
	print qq|</body></html>\n|;
	exit;

# ログメンテ実行
} elsif ($mode eq 'mente2' && $in{'id'}) {

	if ($in{'count'} =~ /\D/) {
		&error("開始カウント数は数字のみで指定して下さい");
	}

	open(DAT,"+< $datadir$in{'id'}.dat") || &error("Open Error: $in{'id'}.dat");
	eval "flock(DAT, 2);";
	my $log = <DAT>;

	my ($count, $ip) = split(/:/, $log);

	seek(DAT, 0, 0);
	print DAT "$in{'count'}:$ip";
	truncate(DAT, tell(DAT));
	close(DAT);

# ログ削除
} elsif ($mode eq 'del' && $in{'id'}) {

	unlink("$datadir$in{'id'}.dat") || &error("Del Error: $in{'id'}.dat");
	@file = &datadir;
}

&header;
print <<EOM;
<h3>管理画面</h3>
<form action="$drmgrcgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="mode" value="new">
<hr><b>1. 新規ログ作成</b><br><br>
ログID名 <input type="text" name="id" size="12"> (英数字でIDを指定)<br>
カウント開始数 <input type="text" name="count" size="8" value="0"><br>
<input type="submit" value="新規作成">
</form>
<form action="$drmgrcgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<hr>
<b>2. ログメンテ</b><br><br>
処理：
<select name="mode">
<option value="mente">修正
<option value="del">削除
</select>
<input type="submit" value="選択する">
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
#  入室画面
#-------------------------------------------------
sub enter_disp {
	&header;
	print <<EOM;
<div align="center">
<h4>パスワードを入力して下さい</h4>
<form action="$drmgrcgi" method="post">
<input type="password" name="pass" size="12">
<input type="submit" value=" 認証 ">
</form>
<br><br>
<!-- 著作権表\示（削除改変禁止）-->
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
#  エラー処理
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


