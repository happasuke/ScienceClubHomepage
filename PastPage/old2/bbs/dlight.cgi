#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DELUXE LIGHT BORAD v1.29 (dlight.cgi)
#│ Copyright(C) 1999-2005 by Ｋｅｉ
#│ kaneko628@yahoo.co.jp
#│ http://kei.s31.xrea.com/
#｜
#｜ modified by ckuma
#├─────────────────────────────────
#│ Original CGI Script
#├─────────────────────────────────
#│ LIGHT BOARD v6.41  <light.cgi>
#│ Copyright(C) KENT WEB 2004
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────

# 外部ファイル取り込み
require './jcode.pl';
require './init.cgi';
require './dlight2.cgi';

&setfile;
&decode;
if ($mode eq "regist") { &regist; }
elsif ($mode eq "howto") { &howto; }
elsif ($mode eq "find") { &find; }
elsif ($mode eq "dellog") { &dellog; }
elsif ($mode eq "editlog") { &editlog; }
elsif ($mode eq "past") { &pastlog; }
elsif ($mode eq "check") { &check; }
&viewlog;

#------------#
#  記事表示  #
#------------#
sub viewlog {
	local($x,$y,$i,$flag,$no,$dat,$nam,$eml,$sub,$com,$url,$resub,$recom);

	# クッキー取得
	local($cnam,$ceml,$curl,$cpwd) = &get_cookie;
	$curl ||= "http://";

	# タイトル表示
	&header;

	print "<div align=\"left\">\n";
	print "[<a href=\"i_dlight.cgi\">携帯用</a>]</dev>\n";

	print "<div align=\"center\">\n";
	if ($t_img) {
		print "<img src=\"$t_img\" alt=\"$title\">\n";
	} else {
		print "<b style=\"color:$t_col; font-size:$t_size",
		"px; font-family:'$t_face'\">$title</b>\n";
	}

	# 表示開始
	print <<"EOM";
<hr width="90%">
[<a href="$home" target="_self">トップに戻る</a>]
[<a href="$script?mode=howto">留意事項</a>]
[<a href="$script?mode=find">ワード検索</a>]
EOM
	# 過去ログリンク
	print "[<a href=\"$script?mode=past\">過去ログ</a>]\n" if ($pastkey);

	# 荒らしログのリンク
	if ($arashilog) { if($a_view == 0) { print "[<a href=\"$admin\?mode=arashi\">荒らしログ</a>]\n"; } }

	# ログ編集機能のリンク
	print "[<a href=\"$admin?mode=admin\">管理用</a>]\n";

	# 返信モード
	$resub='';
	$recom='';
	if ($in{'res'}) {
		# 引用記事抽出
		open(IN,"$logfile") || &error("Open Error : $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com) = split(/<>/);
			last if ($in{'res'} == $no);
		}
		close(IN);

		# コメントに引用符付加
		$recom = "&gt; $com";
		$recom =~ s/<br>/\r&gt; /g;

		# 題名に引用項目付加
		$sub =~ s/^Re://;
		$resub = "Re:[$in{'res'}] $sub";
	}

	if ($tagkey == 1) { $tag_msg = "・メッセージには、<b>タグを使用することができます。</b><br>\n"; }
	elsif ($tagkey == 2) { $tag_msg = "・メッセージには、<b>一部のタグを使用することができます。</b><br>\n"; }
	else { $tag_msg = "・メッセージには、<b>タグは一切使用できません。</b><br>\n"; }

	if ($link) { $a_link = "・メッセージに含まれるＵＲＬには自動的にリンクが張られます。<br>\n"; }
#	if ($passkey) { $pass_msg = "・削除キーの入力は、<b>必須</b>です。<br>\n"; }
	if ($passkey) { $pass_msg = "・<b>暗証キーは「科学」の英単語</b>(7文字：トップページにあります^^)です。<br>\n"; }

	# 投稿フォーム
	print <<"EOM";
<hr width="90%"></div>
<form method="POST" action="$script">
<input type=hidden name=mode value="regist">
<blockquote>
<table cellpadding=1 cellspacing=1>
<tr>
  <td><b>おなまえ</b></td>
  <td><input type=text name=name size=28 value="$cnam"></td>
</tr>
<tr>
  <td><b>Ｅメール</b></td>
  <td><input type=text name=email size=28 value="$ceml"></td>
</tr>
<tr>
  <td><b>タイトル</b></td>
  <td><input type=text name=sub size=36 value="$resub">
	<input type=submit value="投稿する"><input type=reset value="リセット"></td>
</tr>
<tr>
  <td colspan=2><b>コメント</b><br>
  <textarea cols=56 rows=7 name=comment wrap="soft">$recom</textarea></td>
</tr>
<tr>
  <td><b>参照先</b></td>
  <td><input type=text size=50 name=url value="$curl"></td>
</tr>
<tr>
  <td><b>暗証キー</b></td>
  <td><input type=password name=pwd size=8 maxlength=8 value="$cpwd">
  （投稿・記事メンテ用）</td>
</tr>
</table>
</form>
<small>・$max件までのメッセージが保存され、それを超えると古いメッセージから過去ログに移動されます。<br>
$tag_msg
$a_link
$pass_msg
・<b>半角カナ</b>は一切使用しないでください。文字化けの原因となります。<br>
・メッセージの内容によっては、管理者が削除することもありますので御了承下さい。</small><br>
</blockquote>
<a name="top"></a>
<DL><hr noShade>
<div align=right><a href ="#bottom">To BBS Bottom</a></div>
EOM
	# 記事展開
	$i=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	while (<IN>) {
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $plog) { next; }

		($no,$dat,$nam,$eml,$sub,$com,$url,$host) = split(/<>/);
		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;
		$com .= "<P><a href=\"$url\" target=\"_blank\">$url</a>" if ($url);

		print "<DT><hr><table><tr><td valign=top>[<b>$no</b>] ";
		print "<b style=\"color:$subcol\">$sub</b> 投稿者：<b>$nam</b> ";
		print "投稿日：$dat &nbsp;</td><td valign=top>";
		print "<form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=res value=\"$no\">\n";
		print "<input type=submit value='返信'></td></form></tr></table><br>\n";
		print "<DD>$com<br><br>\n";
		# タグ暴走回避処理
		if ($tagwid) { print "$tagclose\n"; }

		# ホスト表示処理
		if ($hostview) { print "<small>ホスト名：<b>$host</b></small><br>\n"; }
	}
	close(IN);

	print "<a name=\"#bottom\"></a>\n";
	print "<DT><hr noShade><div align=right><a href =\"#top\">To BBS Top</a></div><hr></DL>\n";
	
	$next = $page + $plog;
	$back = $page - $plog;
	$flag=0;
	print "<P><table><tr>\n";
	if ($back >= 0) {
		$flag=1;
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=page value=\"$back\">\n";
		print "<input type=submit value=\"前ページ\"></td></form>\n";
	}
	if ($next < $i) {
		$flag=1;
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=submit value=\"次ページ\"></td></form>\n";
	}

	# ページ移動ボタン表示
	if ($flag) {
		print "<td width=10></td><td class=num>";
		$x=1;
		$y=0;
		while ($i > 0) {
			if ($page == $y) { print "<b>[$x]</b>\n"; }
			else { print "[<a href=\"$script?page=$y\">$x</a>]\n"; }
			$x++;
			$y += $plog;
			$i -= $plog;
		}
		print "</td>";
	}
	print <<"EOM";
</tr></table>
<!--
<div align="center">
<form action="$script" method="POST">
処理 <select name=mode>
<option value=editlog>修正
<option value=dellog>削除</select>
記事No<input type=text name=no size=3>
暗証キー<input type=password name=pwd size=6 maxlength=8>
<input type=submit value='送信'></form></div>
-->
EOM

	&footer;
	exit;
}

#----------------#
#  ログ書き込み  #
#----------------#
sub regist {
	local($pwd,$past,@w,@past,@file);

	# 入力チェック
	if (!$post_flag) { &error("不正なアクセスです"); }
	if ($in{'name'} eq "") { &error("名前が入力されていません"); }
	if ($in{'comment'} eq "") { &error("コメントが入力されていません"); }
	if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/) {
		&error("Ｅメールの入力内容が正しくありません");
	}
	if ($passkey) {
#		if ($in{'pwd'} eq "") { &error("削除キーが入力されていません。"); }
		if ($in{'pwd'} ne "science") { &error("暗証キーが違います。"); }
	}
	if ($in{'url'} eq "http://") { $in{'url'}=""; }
	if ($in{'sub'} eq "") { $in{'sub'} = "無題"; }

	# トリップチェック
	if ($trip) {if ($in{'name'} =~ /◆/) { &error("名前に「◆」は使えません。"); } }

	# トリップ処理
	if ($trip) {
		$c_name = $in{'name'};
		if ($in{'name'} =~ /#/){
			$in{'name'} =~ /([^;]*)#([^;]*)$/;
			$in{'name'} = $1 . "◆" . &trip($2);
		}
	}

	# 指定ハンドル拒否
	foreach (@k_name) {
		if ($_ ne '') {
			if ($in{'name'} =~ /$_/) {
				$emode = 4;
				# 携帯用
				if ($b_mode) { &error("荒らし指定ﾊﾝﾄﾞﾙﾈｰﾑ"); }
				# PC用
				else { &error("荒らし指定ハンドルネームです。"); }
			}
		}
	}

	# 禁止ワード拒否
	foreach (@k_word) {
		if ($_ ne '') {
			if ($in{'comment'} =~ /$_/ || $in{'sub'} =~ /$_/ || $in{'name'} =~ /$_/) {
				$emode = 3;

				# 携帯用
				if ($b_mode) { &error("[ $_ ]は使用不可です"); }
				# PC用
				else {	&error("使用不可の単語が含まれています。[ $_ ]"); }
			}
		}
	}

	# ファイルロック
	&lock if ($lockkey);

	# ログを開く
	open(IN,"$logfile") || &error("Open Error : $logfile");
	@file = <IN>;
	close(IN);

	# 二重投稿禁止
	local($no,$dat,$nam,$eml,$sub,$com,$url,$ho,$pw,$tim) = split(/<>/, $file[0]);
	if ($ipcount || $wait) {

		# 時間取得
		$times = time;

		# IPアドレス取得
		&get_host;

		# IP補完ファイルを開く
		open(IP,"$ipfile") || &error("Can't open $ipfile");
		@lines2 = <IP>;
		close(IP);

		$init2 = $lines2[0];
		unless ($init2 =~ /^IPFILE/) {
			# 携帯用
			if ($b_mode) { &error("IP補完ﾛｸﾞが不正です"); }
			# PC用
			else { &error("IP保管ログが不正です"); }
		}

		shift(@lines2);

		# 補完IP読み込み
		foreach (1 .. $ipcount) {
			($ip,$time2) = split(/<>/, $lines2[$_]);

			# 連続投稿チェック
			if ($addr eq "$ip" && $wait > $times - $tim) {

				# 携帯用
				if ($b_mode) { &error("連続投稿は禁止です"); }
				# PC用
				else { &error("連続投稿はもうしばらく時間をおいて下さい"); }
			}
		}

		# 最大IP数超を切り捨て
		if ($#lines2 >= $ipcount-1) { splice(@lines2,$ipcount-1); }

		# ログをフォーマット
		unshift(@lines2,"$addr<>$times<>\n");

		# ヘッダ部を付加
		unshift (@lines2,$init2);

		# IPアドレス書き込み
		open(OUT,">$ipfile") || &error("Write Error : $ipfile");
		print OUT @lines2;
		close(OUT);

	}

	if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
		&error("二重投稿は禁止です");
	}

	# 記事数調整
	@past=();
	while ($max <= @file) {
		$past = pop(@file);
		push(@past,$past) if ($pastkey);
	}

	# 過去ログ
	if (@past > 0) { &pastmake(@past); }

	# 削除キーを暗号化
	if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }

	# 時間を取得
	local($min,$hour,$mday,$mon,$year,$wday) = (localtime(time))[1..6];
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);

	# ログを更新
	$time = time;
	$no++;
	unshift (@file,"$no<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>\n");
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @file;
	close(OUT);

	# ロック解除
	&unlock if ($lockkey);

	# クッキーを発行
	&set_cookie($in{'name'},$in{'email'},$in{'url'},$in{'pwd'},);

	# メール処理
	if ($sendmail && $mail && $in{'email'} ne $mail) { &mailto; }

	# 完了メッセージ
	&header;
	print "<div align=center><hr width=400>\n";
	print "<h3>$f_message</h3>\n";
	print "<form action=\"$script\">\n";
	print "<input type=submit value='掲示板へ戻る'></form>\n";
	print "<hr width=400></div>\n</body></html>\n";
	exit;
}

#------------#
#  留意事項  #
#------------#
sub howto {
	if ($tagkey == 0) { $tag_msg = "メッセージには、<b>タグは一切使用できません。</b>\n"; }
	else { $tag_msg = "メッセージには、<b>タグを使用することができます。</b>\n"; }

	if ($passkey == 0) { $pass_msg ="記事を投稿する上での必須入力項目は<b>「おなまえ」</b>と<b>「メッセージ」</b>です。Ｅメール、ＵＲＬ、題名、暗証キーは任意です。\n"; }
	else { $pass_msg ="記事を投稿する上での必須入力項目は<b>「おなまえ」</b>と<b>「メッセージ」</b>と<b>暗証キー</b>です。Ｅメール、ＵＲＬ、題名は任意です。\n";}

	if ($tagkey == 2) {
		foreach (@tag) {
			if ($_ eq "") { last; }
			$notag = "$notag「&lt;$_&gt;」";
		}
		$tag_msg = "メッセージにはタグを使用することができますが、<b>$notagタグは使用できません。</b>\n";
	}

	if($trip) { $trip_msg ="<LI>トリップ対応です。「名前#********（*は任意の文字列半角8文字分）」と入力することで、個人を識別するためのトリップが付加されます。"; }

	&header;
	print <<EOM;
<div align="center">
<table border=1 width="85%" cellpadding=15>
<tr><td class="r">
<h3>掲示板利用上の注意</h3>
<OL>
<LI>この掲示板は<b>クッキー対応</b>です。１度記事を投稿いただくと、おなまえ、Ｅメール、ＵＲＬ、暗証キーの情報は2回目以降は自動入力されます。（ただし利用者のブラウザがクッキー対応の場合）
<LI>$tag_msg
<LI>$pass_msg
$trip_msg
<LI>記事には、<b>半角カナは一切使用しないで下さい。</b>文字化けの原因となります。
<!--
<LI>記事の投稿時に<b>暗証キー</b>（英数字で8文字以内）を入れておくと、その記事は次回暗証キーによって削除することができます。
-->
<LI>記事の保持件数は最大<b>$max件</b>です。それを超えると古い順に自動削除されます。
<LI>既存の記事に簡単に<b>「返信」</b>することができます。各記事にある<b>「返信」ボタン</b>を押すと投稿フォームが返信用となります。
<LI>過去の投稿記事から<b>「キーワード」によって簡易検索ができます。</b>トップメニューの<a href="$script?mode=find">「ワード検索」</a>のリンクをクリックすると検索モードとなります。
<LI>管理者が著しく不利益と判断する記事や他人を誹謗中傷する記事は予\告なく削除することがあります。
</OL>
</td></tr></table>
<form>
<input type=button value="掲示板に戻る" onClick="history.back()">
</form>
</div>
</body>
</html>
EOM

	exit;
}

#------------#
#  検索画面  #
#------------#
sub find {
	&header;
	print <<"EOM";
<form action="$script">
<input type=submit value="掲示板に戻る"></form>
<UL>
<LI>検索したい<b>キーワード</b>を入力し、「条件」「表\示」を選択して「検索」ボタンを押して下さい。
<LI>キーワードは半角スペースで区切って複数指定することができます。
</UL>
<table><tr>
EOM
	&search("find", $logfile);
	print "</body></html>\n";
	exit;
}

#------------#
#  検索処理  #
#------------#
sub search {
	local($md, $target) = @_;
	local($i, $flag, $next, $back, $enwd, $wd, @wd);

	print "<td><form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=mode value=\"$md\">\n";

	local($para)='';
	if ($md eq "past") {
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		$para = "&pastlog=$in{'pastlog'}";
	}

	print "キーワード <input type=text name=word size=35 value=\"$in{'word'}\"> ";
	print "条件 <select name=cond> &nbsp; ";

	if ($in{'cond'} eq "") { $in{'cond'} = "AND"; }
	foreach ("AND", "OR") {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select> 表\示 <select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = 10; }
	foreach (10,15,20,25,30) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_件\n";
		} else {
			print "<option value=\"$_\">$_件\n";
		}
	}
	print "</select> <input type=submit value=' 検索 '>";
	print "</td></form></tr></table>\n";

	# ワード検索の実行と結果表示
	if ($in{'word'} ne "") {

		# 入力内容を整理
		$in{'word'} =~ s/\x81\x40/ /g;
		@wd = split(/\s+/, $in{'word'});

		# ファイルを読み込み
		print "<DL>\n";
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

				print "<DT><hr>[<b>$no</b>] <b style='color:$subcol'>$sub</b> ";
				print "投稿者：<b>$nam</b> 投稿日：$ymd<br><br>\n";
				print "<DD>$com<br><br>\n";
			}
		}
		close(IN);
		print "<DT><hr>検索結果：<b>$i</b>件</DL>\n";

		$next = $page + $in{'view'};
		$back = $page - $in{'view'};
		$enwd = &url_enc($in{'word'});
		if ($back >= 0) {
			print "[<a href=\"$script?mode=$md&page=$back&word=$enwd&view=$in{'view'}&cond=$in{'cond'}$para\">前の$in{'view'}件</a>]\n";
		}
		if ($next < $i) {
			print "[<a href=\"$script?mode=$md&page=$next&word=$enwd&view=$in{'view'}&cond=$in{'cond'}$para\">次の$in{'view'}件</a>]\n";
		}
		print "</body></html>\n";
		exit;
	}
}

#----------------#
#  クッキー発行  #
#----------------#
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 国際標準時を定義
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# 保存データをURLエンコード
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# 格納
	print "Set-Cookie: LIGHT_BOARD=$cook; expires=$gmt\n";
}

#----------------#
#  クッキー取得  #
#----------------#
sub get_cookie {
	local($key, $val, *cook);

	# クッキーを取得
	$cook = $ENV{'HTTP_COOKIE'};

	# 該当IDを取り出す
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# データをURLデコードして復元
	foreach ( split(/<>/, $cook{'LIGHT_BOARD'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;

		push(@cook,$_);
	}
	return (@cook);
}

#------------#
#  記事削除  #
#------------#
sub dellog {
	local($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,@new);

	# 入力チェック
	if (!$post_flag) { &error("不正なアクセスです"); }
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("削除No又はパスワードが入力されていません");
	}

	# ロック開始
	&lock if ($lockkey);

	# ログを読み込む
	$flag=0;
	@new=();
	open(IN,"$logfile") || &error("Open Error : $logfile");
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
	if (!$flag) { &error("該当記事が見当たりません"); }
	elsif ($flag == 2) { &error("パスワードが設定されていません"); }
	elsif ($flag == 3) { &error("パスワードが違います"); }

	# ログ更新
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ロック解除
	&unlock if ($lockkey);

	# 完了メッセージ
	&header;
	print <<"EOM";
<div align="center">
<h3>記事は正常に削除されました</h3>
<form action="$script">
<input type=submit value="掲示板に戻る"></form>
</div>
</body>
</html>
EOM
	exit;
}

#------------#
#  記事修正  #
#------------#
sub editlog {
	local($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,@new);

	# 入力チェック
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("記事No又はパスワードが入力されていません");
	}

	# 修正実行
	if ($in{'job'} eq "edit2") {
		# 入力チェック
		if ($in{'name'} eq "") { &error("名前が入力されていません"); }
		if ($in{'comment'} eq "") { &error("コメントが入力されていません"); }
		if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/) {
			&error("Ｅメールの入力内容が正しくありません");
		}
		if ($in{'url'} eq "http://") { $in{'url'}=""; }
		if ($in{'sub'} eq "") { $in{'sub'} = "無題"; }

		# ロック開始
		&lock if ($lockkey);

		# 差し替え
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

		# 認証チェック
		$check = &decrypt($in{'pwd'}, $pwd2);
		if (!$check) { &error("パスワードが違います"); }

		# 更新
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ロック解除
		&unlock if ($lockkey);

		return;
	}

	# 記事抽出
	$flag=0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);
		if ($in{'no'} == $no) { $flag=1; last; }
	}
	close(IN);

	if (!$flag) {
		&error("該当の記事が見つかりません");
	} elsif ($pwd eq "") {
		&error('この記事はパスワードが設定されていないため、修正不可能です');
	}
	$check = &decrypt($in{'pwd'}, $pwd);
	if (!$check) { &error("パスワードが違います"); }

	# 修正フォーム
	&edit_form($no,$dat,$nam,$eml,$sub,$com,$url);
}

#--------------#
#  メール送信  #
#--------------#
sub mailto {
	local($msub,$mbody,$email,$com);

	# 記事の改行・タグを復元
	$com  = $in{'comment'};
	$com =~ s/<br>/\n/g;
	$com =~ s/&lt;/</g;
	$com =~ s/&gt;/>/g;
	$com =~ s/&quot;/"/g;
	$com =~ s/&amp;/&/g;

	# メール本文を定義
	$mbody = <<"EOM";
投稿日時：$date
ホスト名：$host
ブラウザ：$ENV{'HTTP_USER_AGENT'}

投稿者名：$in{'name'}
Ｅメール：$in{'email'}
ＵＲＬ  ：$in{'url'}
タイトル：$in{'sub'}

$com
EOM

	# 題名をBASE64化
	$msub = &base64("[$title : $no] $in{'sub'}");

	# メールアドレスがない場合
	if ($in{'email'} eq "") { $email = $mail; }
	else { $email = $in{'email'}; }

	open(MAIL,"| $sendmail -t") || &error("メール送信失敗");
	print MAIL "To: $mail\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	foreach ( split(/\n/, $mbody) ) {
		&jcode'convert(*_, 'jis', 'sjis');
		print MAIL $_, "\n";
	}
	close(MAIL);
}

#--------------#
#  BASE64変換  # とほほのWWW入門で公開されているルーチンを
#--------------# 参考にしました。( http://tohoho.wakusei.ne.jp/ )
sub base64 {
	local($sub) = @_;
	&jcode'convert(*sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch)="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i=0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#------------------#
#  パスワード暗号  #
#------------------#
sub encrypt {
	local($inp) = $_[0];
	local($salt, $crypt, @char);

	# 候補文字列を定義
	@char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');

	# 乱数で種を抽出
	srand;
	$salt = $char[int(rand(@char))] . $char[int(rand(@char))];

	# 暗号化
	$crypt = crypt($inp, $salt) || crypt ($inp, '$1$' . $salt);
	$crypt;
}

#------------------#
#  パスワード照合  #
#------------------#
sub decrypt {
	local($inp, $log) = @_;

	# 種抽出
	local($salt) = $log =~ /^\$1\$(.*)\$/ && $1 || substr($log, 0, 2);

	# 照合
	if (crypt($inp, $salt) eq $log || crypt($inp, '$1$' . $salt) eq $log) { return (1); }
	else { return (0); }
}

#--------------#
#  自動リンク  #
#--------------#
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"$2\" target=\"_top\">$2<\/a>/g;
}

#-----------------#
#  URLエンコード  #
#-----------------#
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#----------------#
#  過去ログ画面  #
#----------------#
sub pastlog {
	local($no,$i,$file,$next,$back);

	open(IN,"$pastno") || &error("Open Error: $pastno");
	$no = <IN>;
	close(IN);

	$in{'pastlog'} =~ s/\D//g;
	if (!$in{'pastlog'}) { $in{'pastlog'} = $no; }

	&header;
	print <<"EOM";
[<a href="$script?">掲示板に戻る</a>]<hr>
<form action="$script" method="POST">
<input type=hidden name=mode value=past>
<table><tr><td><b>過去ログ</b> <select name=pastlog>
EOM
	# 過去ログ選択
	for ($i=$no; $i>0; --$i) {
		$i = sprintf("%04d", $i);
		next unless (-e "$pastdir$i\.cgi");
		if ($in{'pastlog'} == $i) {
			print "<option value=\"$i\" selected>$i\n";
		} else {
			print "<option value=\"$i\">$i\n";
		}
	}
	print "</select> <input type=submit value='移動'>";
	print "</td></form><td width=20></td>\n";

	$file = sprintf("%s%04d\.cgi", $pastdir,$in{'pastlog'});
	&search("past", $file);

	print "<DL>\n";
	$i=0;
	open(IN,"$file") || &error("Open Error : $file");
	while (<IN>) {
		($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $plog) { last; }

		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color=\"$refcol\">$2<\/font>/g;

		if ($eml) { $nam = "<a href=\"mailto:$eml\">$nam</a>"; }
		if ($url) { $url = "&lt;<a href=\"$url\" target=\"_blank\">URL</a>&gt;"; }

		print "<DT><hr>[<b>$no</b>] <b style='color:$subcol'>$sub</b> ",
		"投稿者：<b>$nam</b> 投稿日：$dat &nbsp; $url <br><br><DD>$com<br><br>\n";

	}
	close(IN);
	print "<DT><hr></DL>\n";

	$next = $page + $plog;
	$back = $page - $plog;
	print "<table><tr>\n";
	if ($back >= 0) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$back\">\n";
		print "<input type=submit value=\"前の$plog件\"></td></form>\n";
	}
	if ($next < $i) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=submit value=\"次の$plog件\"></td></form>\n";
	}
	print "</tr></table>\n</body></html>\n";
	exit;

}

#----------------#
#  過去ログ生成  #
#----------------#
sub pastmake {
	local(@past) = @_;
	local($count,$pastfile,$i,$f);

	# 過去ログファイル名を定義
	open(NO,"$pastno") || &error("Open Error : $pastno");
	$count = <NO>;
	close(NO);
	$pastfile = sprintf("%s%04d\.cgi", $pastdir,$count);

	# 過去ログを開く
	$i=0; $f=0;
	@data=();
	open(IN,"$pastfile") || &error("Open Error : $pastfile");
	while (<IN>) {
		$i++;
		push(@data,$_);

		# 最大件数を超えると中断
		if ($i >= $pastmax) { $f++; last; }
	}
	close(IN);

	# 最大件数をオーバーすると次ファイルを自動生成
	if ($f) {
		# カウントファイル更新
		$count++;
		open(NO,">$pastno") || &error("Write Error : $pastno");
		print NO $count;
		close(NO);

		$pastfile = sprintf("%s%04d\.cgi", $pastdir,$count);
		@data = @past;
	} else {
		unshift(@data,@past);
	}

	# 過去ログを更新
	open(OUT,">$pastfile") || &error("Write Error : $pastfile");
	print OUT @data;
	close(OUT);

	if ($f) { chmod(0666, $pastfile); }
}

#------------------#
#  チェックモード  #
#------------------#
sub check {
	&header;
	print <<EOM;
<h2>Check Mode</h2>
<UL>
EOM

	# ログチェック
	foreach ($logfile, $setfile) {
		if (-e $_) {
			print "<LI>パス：$_ → OK\n";
			if (-r $_ && -w $_) { print "<LI>パーミッション：$_ → OK\n"; }
			else { print "パーミッション：$_ → NG\n"; }
		} else {
			print "<LI>パス：$_ → NG\n";
		}
	}

	# ロックディレクトリ
	print "<LI>ロック形式：";
	if ($lockkey == 0) { print "ロック設定なし\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }
		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<LI>ロックディレクトリ：$lockdir\n";

		if (-d $lockdir) {
			print "<LI>ロックディレクトリのパス：OK\n";
			if (-r $lockdir && -w $lockdir && -x $lockdir) {
				print "<LI>ロックディレクトリのパーミッション：OK\n";
			} else {
				print "<LI>ロックディレクトリのパーミッション：NG → $lockdir\n";
			}
		} else { print "<LI>ロックディレクトリのパス：NG → $lockdir\n"; }
	}

	# 過去ログ
	@yn = ('なし', 'あり');
	print "<LI>過去ログ：$yn[$pastkey]\n";
	if ($pastkey) {
		if (-e $pastno) {
			print "<LI>パス：$pastno → OK\n";
			if (-r $pastno && -w $pastno) {
				print "<LI>パーミッション：$pastno → OK\n";
			} else {
				print "<LI>パーミッション：$pastno → NG\n";
			}
		} else {
			print "<LI>パス：$pastno → NG\n";
		}
		if (-d $pastdir) {
			print "<LI>パス：$pastdir → OK\n";
			if (-r $pastdir && -w $pastdir && -x $pastdir) {
				print "<LI>パーミッション：$pastdir → OK\n";
			} else {
				print "<LI>パーミッション：$pastdir → NG\n";
			}
		} else {
			print "<LI>パス：$pastdir → NG\n";
		}
	}
	print "</UL>\n</body></html>\n";
	exit;
}

__END__

