#┌──────────────────────────────────────
#│ DELUXE LIGHT BORAD v1.29 (dlight2.cgi)
#│   Included...
#│       荒らし対策機構 v1.01
#│       Celluar D-LIGHT v.1.00 （携帯電話対応機能付加）
#│ Copyright(C) 1999-2005 by Ｋｅｉ
#│ kaneko628@yahoo.co.jp
#│ http://kei.s31.xrea.com/
#└──────────────────────────────────────

### 荒らし対策機構 v1.01
## --- クッキー無効チェック
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
		&error("クッキーをオンにしてください。");
	}
}

## ---プロクシ拒否機構
sub proxy{

	if ($pdeny[0]) {
		# ホスト名を取得
		&get_host;

		$p_flag = 1;
		foreach (@pdeny) {
			if ($_ eq '') { last; }
			$_ =~ s/\*/\.\*/g;
			# 許可プロクシ
			if ($host =~ /$_/) { $p_flag = 0; last; }
		}
	}

	if ($p_flag) {

	# プロクシ拒否機構メイン処理
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

		# 判別レベル強化
		if($proxylevel){
			# レベル1
			if($host !~/jp$/i) { &p_error; }

			# レベル2
			if($proxylevel == 2){
			    if($host !~/[0-9]/) { &p_error; }
			}
		}

	}

}

## ---プロクシ拒否エラー
sub p_error {
	$emode = 2;
	&error("プロクシを使用しての書き込みはご遠慮願います");
}

## --- トリップ変換 from YY-BOARD Next
# Copyright(C) Logue 2000-2002
# http://www.prologue.info/
sub trip($){
	my $seed = shift;
	my $salt = substr($seed, 1, 2);
	$salt =~ tr/\x00-\x20\x7B-\xFF/./;
	$salt =~ tr/\x3A-\x40\x5B-\x60/A-Ga-f/;
	return(substr(crypt($seed, $salt), -8));
}

## --- 荒らしログ関連最終分岐
sub alog_w {
	if ($a_flag) {
		# 荒らしログ作成
		if ($arashilog)	{ &a_log; }

		#荒らしログのメール送信
		if ($amail) { &amailto; }
	}
}

## --- 荒らしログ書き込み
sub a_log {

	# ファイルロック
	if ($lockkey) { &lock; }

	# ログを開く
	open(IN,"$a_logfile") || &error("Can't open $a_logfile");
	@aread = <IN>;
	close(IN);

	# ログチェック
	$a_init = $aread[0];
	unless ($a_init =~ /^ARASHI_LOG/) { &error("荒らしログが正しくありません"); }

	# 設定を認識
	($head,$no) = split(/<>/,$a_init);

	# 時間を取得
	local($min,$hour,$mday,$mon,$year,$wday) = (localtime(time))[1..6];
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);

	# ログ番号カウントアップ
	$no++;

	shift(@aread);

	# ログをフォーマット
	unshift(@aread,"$no<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$e_type<>$ENV{'REMOTE_ADDR'}<>$ENV{'REMOTE_PORT'}<>$ENV{'HTTP_COOKIE'}<>$ENV{'HTTP_REFERER'}<>$ENV{'REMOTE_ADDR'}<>$ENV{'HTTP_CONNECTION'}<>$ENV{'HTTP_USER_AGENT'}<>$ENV{'HTTP_ACCEPT_LANGUAGE'}<>$ENV{'HTTP_ACCEPT_ENCODING'}<>$ENV{'HTTP_ACCEPT'}<>\n");

	# ヘッダを付加
	unshift (@aread,"$head<>$no<>\n");

	# ログを更新
	open(OUT,">$a_logfile") || &error("Can't write $a_logfile");
	print OUT @aread;
	close(OUT);

	# ロック解除
	if ($lockkey) { &unlock; }
}

## --- 荒らしログメール送信
sub amailto {
	$mail_sub = "$title に荒らし指定者が現れました。";

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

	if (!open(MAIL,"| $sendmail -t")) { &error("メール送信に失敗しました。");}
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
	print MAIL "以下、荒らしの情報\n";
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
## --- キャリア判別
sub browser {

	$u_agent = $ENV{'HTTP_USER_AGENT'};

	# iモード
	if ($u_agent =~ /DoCoMo\//) { $b_mode = 1; }

	# J-SKY
	elsif ($u_agent =~ /J-PHONE\//) { $b_mode = 2; }

	# ezWEB（未実装）
	# elsif($u_agent =~ /UP\.Browser\//) { $b_mode = 3; }

	# PC＆その他
	else { $b_mode = 0; }
}

## --- 携帯電話向けメイン処理
sub c_main {

	if ($mode eq "msg") { &regist; }			# 書き込み処理
	elsif ($mode eq "find") { &c_find; }		# 検索
	elsif ($mode eq "res") { &c_write; }		# 書き込みフォーム（返信）
	elsif ($mode eq "usr_del") { &usr_del; }	# ユーザー記事削除処理
	elsif ($mode eq "del") { &c_del; }			# 削除フォーム
	elsif ($mode eq "write") { &c_write; }		# 書き込みフォーム（新規）
	elsif ($mode eq "howto") { &c_howto; }		# 利用規定

	&c_html_log;
}

## --- 携帯電話向けヘッダー
sub c_header {

	print "Content-type: text/html\n\n";
	print "<html><head>";
	print "<title>$title</title></head>";

	# BODYタグ
	if ($c_bgr eq '') {
		print "<body bgcolor=$bgc text=$text link=$link>";
	} else {
		print "<body background=\"$c_bgr\" bgcolor=$bgc text=$text link=$link>";
	}
}

## --- 携帯電話向けフッター
sub c_footer {
	print "<hr>";

	## フッター＆著作権表示（削除不可）
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

## --- 携帯電話向け記事表示
sub c_html_log {

	# ログを読み込み
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# 環境設定部を認識
	$init = $lines[0];
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,
		$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2)
								 = split(/<>/,$init);

	# ログチェック
	unless ($init =~ /^LIGHT/) { &error("ﾛｸﾞが不正です"); }

	shift(@lines);

	&c_header;

	# 表示開始
	if ($in{'page'} eq '') { $page = 0; } 
	else { $page = $in{'page'}; }

	# タイトル＆管理者コメント
	# 最初のページ以外は表示しない
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

	# 記事数を取得
	$end_data = @lines - 1;
	$page_end = $page + ($c_pagelog - 1);
	if ($page_end >= $end_data) { $page_end = $end_data; }

	foreach ($page .. $page_end) {
		($number,$date,$name,$email,$subj,$comment,$url,$host,$pwd)
						 = split(/<>/,$lines[$_]);

		# 表示形式処理
		if ($c_type) {

			# 記事表示
			print "[$number] <a href=\"$script?mode=res&no=$number\">$subj</a>:$name<br>";

			$hr = 1;

		} else {
			# E-mail、URLリンク及び日付表示変換処理
			if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
			if ($url) { $url = "<a href=\"http://$url\">&gt;HP&lt;</a>"; }
			# いずれは携帯電話向けに最適化した日付表示にする予定
			$date =~ s/\) /\)<br>/g;

			# 自動リンク（URL）
			if ($autolink) { &ij_link($comment); }

			# 記事表示
			print "[$number] $subj<br>";
			print "$date<br>";
			print "$name<p>";
			print "$comment<br>";
			print "$url";
			print "<p>[<a href=\"$script?mode=res&no=$number\">返信</a>]</p>";

			# タグ暴走回避処理
			if ($tagwid) { print "$tagclose"; }

			# ホスト表示処理
			if ($hostview) { print "<small>$host</small>"; }

			print "<hr>";
		}

	}

	# 改頁処理
	$next_line = $page_end + 1;
	$back_line = $page - $c_pagelog;

	$page_flag = 0;

	# 前頁処理
	if ($back_line >= 0) {
		print "<a href=\"$script?page=$back_line\"><<新</a> ";
		$page_flag = 1;
	}

	# 次頁処理
	if ($page_end ne $end_data) {
		print "<a href=\"$script?page=$next_line\">旧>></a>";
		$page_flag = 1;
	}

	# 整形処理
	if ($page_flag) {
		# ツリー表示時に<hrタグが挿入されない現象回避
		if ($hr) {
			print "<hr>";
			$hr = 0;
		}

		# フラグが立っていたら整形のため<p>タグを挿入
		print "<p>";

	}

	# メニュー組み立て
	# J-SKY
	if ($b_mode == 2) {
		print "<a href=\"$j_home\" DIRECTKEY=\"1\">[1] HOME</a><br>";
		print "<a href=\"$script?mode=write\" DIRECTKEY=\"2\">[2] 新規</a><br>";
		print "<a href=\"$script?mode=howto\" DIRECTKEY=\"3\">[3] 利用規定</a><br>";
		print "<a href=\"$script?mode=find\" DIRECTKEY=\"4\">[4] 検索</a><p>";
		print "<a href=\"$script?mode=del\" DIRECTKEY=\"5\">[5] 記事削除</a><p>";
	# i-mode
	} else {
		print "<a href=\"$i_home\" ACCESSKEY=\"1\">&#63879; HOME</a><br>";
		print "<a href=\"$script?mode=write\" ACCESSKEY=\"2\">&#63880; 新規</a><br>";
		print "<a href=\"$script?mode=howto\" ACCESSKEY=\"3\">&#63881; 利用規定</a><br>";
		print "<a href=\"$script?mode=find\" ACCESSKEY=\"4\">&#63882; 検索</a><br>";
		print "<a href=\"$script?mode=del\" ACCESSKEY=\"5\">&#63883; 記事削除</a><br>";
	}

	&c_footer;
	exit;
}

# --- 携帯電話向け投稿フォーム
sub c_write {

	# ログを読み込み
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# 環境設定部を認識
	$init = $lines[0];
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,
		$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2)
								 = split(/<>/,$init);

	# ログチェック
	unless ($init =~ /^LIGHT/) { &error("ﾛｸﾞが不正です"); }

	shift(@lines);

	&c_header;

	# 返信モードの場合
	if ($mode eq "res") {
		foreach $line (@lines) {
			($number,$date,$name,$email,$subj,$comment) = split(/<>/,$line);
			if ($number eq $in{'no'}) { last; }
		}

		# ツリー表示時処理
		if ($c_type) {
			# E-mail、URLリンク及び日付表示変換処理
			if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
			if ($url) { $url = "<a href=\"http://$url\">&gt;HP&lt;</a>"; }
			# いずれは携帯電話向けに最適化した日付表示にする予定
			$date =~ s/\) /\)<br>/g;

			# 自動リンク（URL）
			if ($autolink) { &ij_link($comment); }

			# 記事表示
			print "[$number] $subj<br>";
			print "$date<br>";
			print "$name<p>";
			print "$comment<br>";
			print "$url";

			# タグ暴走回避処理
			if ($tagwid) { print "$tagclose"; }

			# ホスト表示処理
			if ($hostview) { print "<small>$host</small>"; }

			print "<hr>";
		}


		# 返信用項目を作成
		if ($subj =~ /^Re/) {
			$subj =~ s/Re//;
			$res_sub = "Re\[$number\]" . "$subj";

		} else {
			$res_sub = "Re\[$number\]\: $subj";
		}

	}

	# 投稿フォーム組み立て
	# J-SKY
	if ($b_mode == 2) {
		print "<form action=\"$script\" method=\"GET\">";
	# i-mode
	} else {
		print "<form action=\"$script\" method=\"POST\">";
	}

	print "<input type=hidden name=mode value=\"msg\">";
	print "名前:<input type=text name=name size=10><br>";
	print "Mail:<input type=text name=email istyle=\"3\" size=10><br>";

	# 返信モードの場合
	if ($mode eq "res") {
		print "ﾀｲﾄﾙ:<input type=text name=sub size=10 value=\"$res_sub\"><br>";
	} else {
		print "ﾀｲﾄﾙ:<input type=text name=sub size=10><br>";
	}

	print "<textarea cols=15 rows=3 name=comment wrap=\"$wrap\">$res_comment</textarea><br>";
	print "URL :<input type=text istyle=\"3\" size=10 name=url value=\"http://\"><br>";
	print "PASS:<input type=password name=pwd size=8 maxlength=8><br>";

	# J-SKY
	if ($b_mode == 2) {
		print "<input type=submit name=\"send\" value=\"送信\"><input type=reset name=\"reset\" value=\"ｸﾘｱ\"></form>";
	# i-mode
	} else {
		print "<input type=submit value=\"送信\"><input type=reset value=\"ｸﾘｱ\"></form>";
	}

	print "<hr><a href=\"$script\">戻る</a>";

	&c_footer;
	exit;
}

# --- 携帯電話向けユーザ記事削除フォーム
sub c_del {

	# ログを読み込み
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# 環境設定部を認識
	$init = $lines[0];
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,
		$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2)
								 = split(/<>/,$init);

	# ログチェック
	unless ($init =~ /^LIGHT/) { &error("ﾛｸﾞが不正です"); }

	&c_header;

	# 削除フォーム組み立て
	print "<br><center>記事削除</center><p>";

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
		print "<input type=submit name=\"del\" value=\"削除\">";
	# i-mode
	} else {
		print "<input type=submit value=\"削除\">";
	}
	print "</form>";

	print "<hr><a href=\"$script\">戻る</a>";
	&c_footer;
	exit;
}

## --- 携帯電話向け掲示板の使い方メッセージ
sub c_howto {

	# ログを読み込み
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# 環境設定部を認識
	$init = $lines[0];
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,
		$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2)
								 = split(/<>/,$init);

	# ログチェック
	unless ($init =~ /^LIGHT/) { &error("ﾛｸﾞが不正です"); }

	if ($tagkey == 0) { $tag_msg = "ﾀｸﾞは使用不可です"; }
	else { $tag_msg = "ﾀｸﾞは使用可です"; }

	if ($passkey ==0) { $pass_msg ="名前､ｺﾒﾝﾄは必須です｡MAIL､URL､ﾀｲﾄﾙ､PASSは任意です"; }
	else { $pass_msg ="名前､ｺﾒﾝﾄ､PASSは必須です｡MAIL､URL､ﾀｲﾄﾙ､PASSは任意です"; }

	&c_header;

	print "<br><center>利用上の注意</center><hr><P>";
	print "$tag_msg<P>";
	print "絵文字は使用禁止です";
	print "$pass_msg<P>";
	print "PASSを入力すると､後で投稿した記事を削除できます<P>";
	print "記事は最大$max件保存されます<P>";
	print "管理者の判断により､投稿記事は\予\告\なく削除することがあります｡";
	print "<hr><a href=\"$script\">戻る</a>";

	&c_footer;
	exit;
}

## --- 携帯電話向けワード検索サブルーチン
sub c_find {
	# ログを読み込み
	open(LOG,"$logfile") || &error("Can't open $logfile");
	@lines = <LOG>;
	close(LOG);

	# 環境設定部を認識
	($head,$title,$t_color,$t_size,$t_face,$bgr,$bgc,$text,$link,$vlink,$alink,$home,$max,$subj_color,$name_color,$mail1,$mail2) = split(/<>/,$lines[0]);

	&c_header;

	# 検索フォーム組み立て
	print "<br><center>ﾜｰﾄﾞ検索</center><br>";
	print "複数ｷｰﾜｰﾄﾞは空白で区切って下さい<P>";

	# J-SKY
	if ($b_mode == 2) {
		print "<form action=\"$script\" method=\"GET\">";
	# i-mode
	} else {
		print "<form action=\"$script\" method=\"POST\">";
	}

	print "<input type=hidden name=mode value=\"find\">";
	print "ｷｰﾜｰﾄﾞ :";
	print "<input type=text name=word size=8><br>";
	print "検索条件:";
	print "<input type=radio name=cond value=\"and\" checked>AND";
	print "<input type=radio name=cond value=\"or\">OR<br>";

	# J-SKY
	if ($b_mode == 2) {
		print "<input type=submit name=\"serc\" value=\"検索\"><input type=reset name=\"reset\" value=\"ｸﾘｱ\"></form>";
	# i-mode
	} else {
		print "<input type=submit value=\"検索\"><input type=reset value=\"ｸﾘｱ\"></form>";
	}

	print "</center>";

	# ワード検索の実行と結果表示
	if ($in{'word'} ne "") {

		# 入力内容を整理
		$cond = $in{'cond'};
		$word = $in{'word'};
		$word =~ s/\t/ /g;
		@pairs = split(/ /,$word);

		shift(@lines);

		# 検索処理
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
	# 検索終了


		# 記事数を取得
		$count = @new;
		print "<hr>検索結果：$count件<br>検索ﾜｰﾄﾞ：$word";

		# ページ初期設定
		if ($in{'page'} eq '') { $page = 0; } 
		else { $page = $in{'page'}; }

		$end_data = @new - 1;
		$page_end = $page + ($cs_page - 1);
		if ($page_end >= $end_data) { $page_end = $end_data; }

		print "<hr>";

		# 表示開始
		foreach ($page .. $page_end) {
			($number,$date,$name,$email,$subj,$comment,$url,$host) = split(/<>/,$new[$_]);

			# 表示形式処理
			if ($c_type) {

				# 記事表示
				print "[$number] <a href=\"$script?mode=res&no=$number\">$subj</a>:$name<br>";

				$hr = 1;

			} else {
				# E-mail、URLリンク及び日付表示変換処理
				if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
				if ($url) { $url = "<a href=\"http://$url\">&gt;HP&lt;</a>"; }
				# いずれは携帯電話向けに最適化した日付表示にする予定
				$date =~ s/\) /\)<br>/g;

				# 自動リンク（URL）
				if ($autolink) { &ij_link($comment); }

				# 記事表示
				print "[$number] $subj<br>";
				print "$date<br>";
				print "$name<p>";
				print "$comment<br>";
				print "$url";
				print "<p>[<a href=\"$script?mode=res&no=$number\">返信</a>]</p>";

				# タグ暴走回避処理
				if ($tagwid) { print "$tagclose"; }

				# ホスト表示処理
				if ($hostview) { print "<small>$host</small>"; }

				print "<hr>";
			}
		}

	}

	# 改頁処理
	$next_line = $page_end + 1;
	$back_line = $page - $cs_page;

	$page_flag = 0;
	# 前頁処理
	if ($back_line >= 0) {
		print "<a href=\"$script?mode=find&page=$back_line&cond=$cond&word=$word\"><<新</a> ";
		$page_flag = 1;
	}

	# 次頁処理
	if ($page_end ne $end_data) {
		print "<a href=\"$script?mode=find&page=$next_line&cond=$cond&word=$word\">旧>></a>";
		$page_flag = 1;
	}

	# 整形処理
	if ($page_flag) {
		# ツリー表示時に<hrタグが挿入されない現象回避
		if ($hr) {
			print "<hr>";
			$hr = 0;
		}

		# フラグが立っていたら整形のため<p>タグを挿入
		print "<p>";

	}

	print "<a href=\"$script\">戻る</a><br>";

	&c_footer;
	exit;
}

## --- i-mode J-SKY用自動リンク
sub ij_link {
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<a href=$2>$2<\/a>/g;
}

1;

__END__

