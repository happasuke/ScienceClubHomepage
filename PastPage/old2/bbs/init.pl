#┌─────────────────────────────────
#│ LIGHT BOARD v6.12 (2003/04/18)
#│ Copyright(C) KENT WEB
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'LIGHT BOARD v6.12';
#┌─────────────────────────────────
#│[ 注意事項 ]
#│ 1.このスクリプトはフリーソフトです。このスクリプトを使用した
#│   いかなる損害に対して作者はその責任を一切負いません。
#│ 2.設置に関する質問はサポート掲示板にお願いいたします。メールに
#│   よる質問にはお答えできません。
#└─────────────────────────────────
#
# [ 設置例 ] かっこ内はパーミッション
#
#    public_html / index.html (ホームページ)
#       |
#       +-- bbs / light.cgi  [755]
#            |    admin.cgi  [755]
#            |    init.pl    [644]
#            |    jcode.pl   [644]
#            |    data.cgi   [666]
#            |    light.dat  [666]
#            |    pastno.dat [666] .. 過去ログ用カウントファイル
#            |
#            +-- lock [777] /
#            |
#            +-- past [777] / 0001.cgi [666]

#============#
#  設定項目  #
#============#

# スクリプトURL
$script = './light.cgi';
$i_script = './i_light.cgi';

# 管理ファイルURL
$admin = './admin.cgi';

# ログファイル
$logfile = './data.cgi';

# 設定ファイル
$setfile = './light.dat';

# ファイルロック形式
#  → 0=no 1=symlink関数 2=mkdir関数
$lockkey = 1;

# ロックファイル名
$lockfile = './lock/light.lock';

# sendmailパス（メール通知する場合）
# → 例 /usr/lib/sendmail
$sendmail = '';

# 過去ログ機能 (0=no 1=yes)
$pastkey = 1;

# 過去ログディレクトリ
$pastdir = './past/';

# 過去ログカウントファイル
$pastno = './pastno.dat';

# 過去ログ１ファイル当りの最大件数
$pastmax = 300;

#============#
#  設定完了  #
#============#

#--------------------#
#  フォームデコード  #
#--------------------#
sub decode {
	local($buf, $key, $val);

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag=1;
		if ($ENV{'CONTENT_LENGTH'} > 51200) { &error("投稿量が大きすぎます"); }
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$post_flag=0;
		$buf = $ENV{'QUERY_STRING'};
	}
	%in=();
	foreach (split(/&/, $buf)) {
		($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		# S-JISコード変換
		&jcode'convert(*val, "sjis", "", "z");

		# タグ処理
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;

		# 改行処理
		if ($key eq "comment") {
			$val =~ s/\r\n/<br>/g;
			$val =~ s/\r/<br>/g;
			$val =~ s/\n/<br>/g;
		} else {
			$val =~ s/\r//g;
			$val =~ s/\n//g;
		}
		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$page = $in{'page'};
	$mode = $in{'mode'};
	$headflag=0;
	$lockflag=0;
	$ENV{'TZ'} = "JST-9";
}

#--------------------#
#  設定ファイル認識  #
#--------------------#
sub setfile {
	# 設定ファイル読み込み
	open(IN,"$setfile") || &error("Open Error : $setfile");
	local($file) = <IN>;
	close(IN);

	# 設定内容認識
	($title,$t_col,$t_size,$t_face,$t_img,$bg,$bc,$tx,$li,$vl,$al,$home,$max,$subcol,$refcol,$plog,$b_size,$mail,$deny,$link,$wait) = split(/<>/, $file);

	# アクセス拒否
	&get_host;
	if ($deny) {
		$flag=0;
		foreach (split(/\s+/, $deny)) {
			if ($host =~ /$_/i) { $flag=1; last; }
		}
		if ($flag) { &error("ただ今ご利用できません"); }
	}

	$b_size .= "px";
}

#--------------#
#  HTMLヘッダ  #
#--------------#
sub header {
	if ($headflag) { return; }
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
<STYLE TYPE="text/css">
<!--
body,tr,td,th { font-size:$b_size; font-family:"MS UI Gothic" }
.num { font-size:9pt; font-family:Verdana,Helvetica,Arial }
-->
</STYLE>
<title>$title</title></head>
EOM
	if ($bg) {
		print "<body background=\"$bg\" bgcolor=\"$bc\" text=\"$tx\" link=\"$li\" vlink=\"$vl\" alink=\"$al\">\n";
	} else {
		print "<body bgcolor=\"$bc\" text=\"$tx\" link=\"$li\" vlink=\"$vl\" alink=\"$al\">\n";
	}
	$headflag=1;
}

#--------------#
#  エラー処理  #
#--------------#
sub error {
	if ($lockflag) { &unlock; }

	&header;
	print <<"EOM";
<div align="center">
<h3>ERROR !</h3>
<font color="#dd0000">$_[0]</font>
</div>
</body>
</html>
EOM
	exit;
}

#--------------#
#  ロック処理  #
#--------------#
sub lock {
	# 1分以上古いロックは削除する
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 60) { &unlock; }
	}
	local($retry) = 5;
	# symlink関数式ロック
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	# mkdir関数式ロック
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}
	$lockflag=1;
}

#--------------#
#  ロック解除  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }

	$lockflag=0;
}

#----------------#
#  編集フォーム  #
#----------------#
sub edit_form {
	local($no,$dat,$nam,$eml,$sub,$com,$url) = @_;
	$url ||= "http://";
	$com =~ s/<br>/\r/g;

	&header;
	print <<"EOM";
[<a href="javascript:history.back()">前画面に戻る</a>]
<h3>編集フォーム</h3>
<UL>
<LI>修正する部分のみ変更してください。
EOM
	if ($in{'pass'} ne "") {
		print "<form action=\"$admin\" method=\"POST\">\n",
		"<input type=hidden name=no value=\"$in{'no'}\">\n",
		"<input type=hidden name=pass value=\"$in{'pass'}\">\n",
		"<input type=hidden name=mode value=\"admin\">\n",
		"<input type=hidden name=job value=\"edit2\">\n";
	} else {
		print "<form action=\"$script\" method=\"POST\">\n",
		"<input type=hidden name=mode value=\"editlog\">\n",
		"<input type=hidden name=no value=\"$in{'no'}\">\n",
		"<input type=hidden name=pwd value=\"$in{'pwd'}\">\n",
		"<input type=hidden name=job value=\"edit2\">\n";
	}

	print <<"EOM";
投稿者名<br><input type=text name=name size=28 value="$nam"><br>
Ｅメール<br><input type=text name=email size=28 value="$eml"><br>
タイトル<br><input type=text name=sub size=36 value="$sub"><br>
参照先<br><input type=text name=url size=45 value="$url"><br>
コメント<br><textarea name=comment cols=58 rows=7 wrap=soft>$com</textarea><br>
<input type=submit value=" 修正を行う "></form>
</UL>
</body>
</html>
EOM
	exit;
}

#----------------#
#  ホスト名取得  #
#----------------#
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($host eq "" || $host eq $addr) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2) || $addr;
	}
}

1;

__END__

