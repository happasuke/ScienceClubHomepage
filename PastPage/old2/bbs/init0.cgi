#┌──────────────────────────────────────
#│ DELUXE LIGHT BORAD v1.28 (2005.11.30)
#│ Copyright(C) 1999-2005 by Ｋｅｉ
#│ kaneko628@yahoo.co.jp
#│ http://kei.s31.xrea.com/
#├──────────────────────────────────────
#│ Original CGI Script
#├──────────────────────────────────────
#│ LIGHT BOARD v6.41 (2005/11/27)
#│ Copyright(C) KENT WEB 2004
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'LIGHT BOARD v6.41'; # バージョン情報（修正、削除不可）
$ver2 = 'D-LIGHT v1.28'; # バージョン情報（修正、削除不可）
#┌──────────────────────────────────────
#│ [注意事項・合意事項]
#│ 1.このスクリプトはフリーソフトです。このスクリプトを使用したいかなる損害に
#│   対して作者はその責任を一切負いません。
#│ 2.設置に関する質問はサポート掲示板にお願いいたします。メールによる質問には
#│   お答えできません。
#│ 3.このスクリプトのオリジナルはKENT WEBさん作のLIGHT BOARDです。LIGHT BORAD
#│   に掲示板荒らし対策機能を主に、幅広いカスタマイズ機能、各種携帯電話向けに
#│   改良した掲示板システムを搭載しています。
#│   これらの機能は、改造者の独断と偏見及びユーザーの方々のご意見や感想を元に
#│   作成・追加しています。
#│ 4.現在のバージョンではDELUXE LIGHT BORADのログは LIGHT BOARDのログと互換性
#│   を確保してあるので、変換せずにそのままログを引き継ぐことができます。
#│ 5.プロクシサーバ拒否機構ルーチンおよび、荒らしログ用ファイル作成ルーチンの
#│   ベーススクリプトは、大祓祝詞さんにご教授頂きました。
#│ 6.トリップ機能は Logue氏(http://www.prologue.info/)製作、YY-BOARD Nextから
#│   拝借しました(^^ヾ
#│ 7.荒らしログ管理機能強化のため、v1.10以降のログはv1.10以前に作成したログと
#│   互換性はありませんので、ログファイルを上書きしてください。
#│   変換スクリプトは、大幅な形式変更のため付属しておりません。
#│   あらかじめご了承ください
#│ 8.携帯電話の対応状況は現在i-modeとJ-SKYのみです。
#│   EZwebはHDMLを理解したら実装する予定です(^^;
#│   本家の過去ログ形式の関係上、過去ログ機能はご利用頂けません。
#└──────────────────────────────────────
#
# [ 設置例 ] かっこ内はパーミッション
#
#    public_html / index.html (ホームページ)
#       |
#       +-- bbs / dlight.cgi  [755]
#            |    admin.cgi   [755]
#            |    init.cgi    [644]
#            |    dlight2.cgi [644]
#            |    jcode.pl    [644]
#            |    data.cgi    [666]
#            |    iplock.cgi  [666]
#            |    dlight.dat  [666]
#            |    pastno.dat  [666] .. 過去ログ用カウントファイル
#            |
#            +-- lock [777] /
#            |
#            +-- past [777] / 0001.cgi [666]
#============#
#  設定項目  #
#============#
	
# 管理者用パスワード(半角英数字)
$pass = 'ckuma6143';

# スクリプトURL
$script = './dlight.cgi';
$i_script = './i_dlight.cgi';

# 管理ファイルURL
$admin = './admin.cgi';

# ログファイル
$logfile = './data.cgi';

# 設定ファイル
$setfile = './dlight.dat';

# ファイルロック形式
#  → 0=no 1=symlink関数 2=mkdir関数
$lockkey = 0;

# ロックファイル名
$lockfile = './lock/dlight.lock';

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

#====================#
#  D-LIGHT 拡張機能  #
#====================#

# リンクの色設定 (0=両使用 1=スタイルシートのみ 2=通常表示のみ)
$lstyle = 0;

# ブラウザのキャッシュ無効 (0=no 1=yes)
$browser_c = 1;

# 半角カナ -> 全角カナ変換 (0=no 1=yes)
$kana = 1;

# 書き込完了メッセージ
$f_message = '正常に投稿されました';

# タグ広告挿入オプション (FreeWebなど）
#   → <!-- 上部 --> <!-- 下部 --> の代わりに「広告タグ」を挿入する。
#   → 広告タグ以外に、MIDIタグ や カウンタ用のタグ等にも使用可能です。
$banner1 = '<!-- 上部 -->';	# 掲示板上部に挿入
$banner2 = '<!-- 下部 -->';	# 掲示板下部に挿入

#================#
#  携帯電話対応  #
#================#

# 携帯電話対応 (0=no 1=yes)
$cellular = 1;

# 表示形式 (0=オリジナル形式 1=タイトル＆投稿者名のみ表示)
$c_type = 1;

# 携帯向け１ページ当たりの記事表示数
$c_pagelog = 10;

# 携帯向け検索１ページ当たりの記事表示数
$cs_page = 10;

## 携帯電話向け戻りページ（フルパスはhttp://からURLを記述）
# i-mode用
$i_home = "../index.html";
# J-PHONE用
$j_home = "../index.html";
# ezWEB用（動作しません）
$ez_home = "../ez/index.html";

##タイトル画像と、コメントは初めのページのみ表示
## タイトル画像（使用する場合は画像までのパス）
# i-mode用
$i_tg = "";
# J-PHONE用
$j_tg = "";
# ezWEB用（動作しません）
$ez_tg = "";

# 初めのページに表示される管理者コメント
$c_com = 'お気軽にどうぞ';

# 書き込み終了時のメッセージ
$cf_message = '書き込み完了';

#==================#
#  荒らし対策機構  #
#==================#

# 閉鎖時メッセージ
$block_mes = "ただ今ご利用できません";

# タグ暴走回避モード：タグ許可時のみ有効 (0=no 1=yes)
$tagwid = 1;

# 閉じタグ：タグ暴走回避モードオン時のみ有効
$tagclose = "</font></span></b></u></s></i></marquee></a></em>";

# タグの許可 (0=no 1=全て許可 2=条件付許可)
$tagkey = 2;

# 非許可タグ（タグ名だけを記述）
@tag =('script','meta','html','body','','','');

# 投稿記事量の上限(0で投稿量制限なし)
# バイト換算：全角１文字２バイト
$mes_size = 51200;

# 削除キーの入力強制 (0=no 1=yes)
$passkey = 1;

# 指定ホストアクセス制限機能 (0=no 1=指定ホスト拒否 2=指定ホストのみ許可)
$ac_lim = 1;

# ホスト名取得モード
#  --> 0 : $ENV{'REMOTE_HOST'} で取得できる場合
#  --> 1 : gethostbyaddr で取得できる場合
$get_remotehost = 0;

# 書きこみ制限（名前)
@k_name = (
	'',
	'',
	'',
	'',
	'');

# 書きこみ制限（単語)
@k_word = (
	'http',
	'sex',
	'',
	'',
	'');

# IPアドレス補完ファイル名
$ipfile = './iplock.cgi';

# 補完IPアドレス数
$ipcount = 5;

# 記事にホストアドレス表示 (0=no 1=yes)
$hostview = 0;

# プロクシ拒否機構 (0=no 1=yes)
$proxy = 0;

# プロクシ判別のレベル
# 0 = プロクシ情報を吐き出しているホスト排除(標準)
# 1 = 0＋[jp]を含まないホスト排除
# 2 = 0＋1＋数字を含まないホスト排除（通常はIPアドレス＋ホスト名でホストアドレスは提供されているため）
$proxylevel = 0;

# 許可プロクシ（ホスト名を記述）
@pdeny = (
	'*.hogehoge.ne.jp',
	'xxx.proxy.com',
	'',
	'',
	'');

# クッキー無効排除 (0=no 1=yes)
$cook = 0;

# 荒らしログ作成機構 (0=no 1=yes)
$arashilog = 0;

# 管理者のみ閲覧許可 (0=no 1=yes)
$a_view = 1;

# 荒らしログファイル名
$a_logfile = './arashi.cgi';

# 荒らしログのメール通知 (0=no 1=yes)
$amail = 0;

# 荒らしログのメールに本文送信 (0=no 1=yes)
$mail_com = 0;

# 荒らしログを作成する荒らし対策機構 (0=no 1=yes)
$alog1 = 1;        # Type 1：不正アクセス
$alog2 = 1;        # Type 2：プロクシエラー
$alog3 = 1;        # Type 3：禁止ワード
$alog4 = 1;        # Type 4：荒らし指定ハンドル
$alog5 = 1;        # Type 5：クッキー無効
$alog6 = 1;        # Type 6：指定ホスト拒否
$alog7 = 1;        # Type 7：METAタグ使用

# トリップ機能 (0=no 1=yes)
$trip = 1;

# 管理モード入室制限 (0=no 1=yes)
$c_lim = 0;

# 管理モードの入室許可（許可するホスト名を記述）
@cdeny = (
	'*.sendai-ct.ac.jp',
	'',
	'',
	'',
	'');

#============#
#  設定完了  #
#============#

#--------------------#
#  フォームデコード  #
#--------------------#
sub decode {
	local($buf, $key, $val);

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag = 1;
			# 投稿量の制限処理
			if ($mes_size != 0) {
				if ($ENV{'CONTENT_LENGTH'} > $mes_size) { &error("投稿量が大きすぎます"); }
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

		#半角カナ -> 全角カナ変換
		if ($kana) { &jcode'h2z_sjis(*value); }

		# S-JISコード変換
		&jcode'convert(*val, "sjis", "", "z");

		# 非許可タグ検知処理
		if ($tagkey == 2) {
			foreach (@tag) {
				if ($val =~ /<$_/i) {
					$emode = 7;
					&error("「$_」タグの使用はご遠慮ください");
				}
			}
		}

		# タグ処理
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

		# 改行処理
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
#  設定ファイル認識  #
#--------------------#
sub setfile {
	# 設定ファイル読み込み
	open(IN,"$setfile") || &error("Open Error : $setfile");
	local($file) = <IN>;
	close(IN);

	# 設定内容認識
	($title,$t_col,$t_size,$t_face,$t_img,$bg,$bc,$tx,$li,$vl,$al,$home,$max,$subcol,$refcol,$plog,$b_size,$mail,$deny,$link,$wait) = split(/<>/, $file);

	# プロクシ拒否
	if ($proxy) { &proxy; }

	# クッキー無効排除
	if ($cook) { &chk_cookie; }

	# アクセス拒否
	&get_host;

	# アクセス拒否
	if ($deny) {
	    $flag = 0;
	    foreach ( split(/\s+/, $deny) ) {

			# ホスト制限不使用
			if ($ac_lim == 0) { last; }

			# 指定ホスト拒否
			elsif ($ac_lim == 1) {
			    if ($_ eq '') { last; }
			    $_ =~ s/\*/\.\*/g;
			    if ($host =~ /$_/i) { $flag = 1; last; }
			}

			# 指定ホスト許可
			elsif ($ac_lim == 2) {
			    $flag = 1;
			    if ($_ eq '') { last; }
			    $_ =~ s/\*/\.\*/g;
			    if ($host =~ /$_/i) { $h_flag = 0; last; }
			}

			# 不正な値代入時のエラー回避
			else { last; }

		}

		if ($flag) {
			# エラー表示
			$emode = 6;
			&error("$block_mes");
		}
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
<!--nobanner-->
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
EOM

	# ブラウザのキャッシュ無効
	if ($browser_c) {
		print "<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n";
		print "<META HTTP-EQUIV=\"Cache-Control\" CONTENT=\"no-cache\">\n";
	}
	
	print <<"EOM";
<STYLE TYPE="text/css">
<!--
body,tr,td,th {
	font-size:$b_size;
	font-family:"MS UI Gothic,ＭＳ Ｐゴシック,Osaka";
}
.num { font-family:Verdana,Helvetica,Arial; }
.l { background-color: #666666; color: #ffffff; }
.r { background-color: #ffffff; color: #000000; }
EOM

	# リンクのスタイルシート使用
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
#  HTMLのフッタ  #
#----------------#
sub footer {
	## 著作権表示（削除不可）
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
#  エラー処理  #
#--------------#
sub error {
	if ($lockflag) { &unlock; }

	$title = "エラー";;

	if ($b_mode) {
	  # 携帯

	  &c_header;

	  # ezWEB（未実装）
	  # if ( $b_mode == 3) {
	  # }

	  # i-mode＆J-SKY
	  # else {
	    print "<center>ERROR !<hr>";
	    print "<p>$_[0]</p>";
	    print "<hr></center>";
	    print "</body></html>";
	  # }

	} else {
	  # PC＆その他
	  &header;

	  print "<center><hr width=75%><h3>ERROR !</h3>\n";
	  print "<P><font color=#DD0000><B>$_[0]</B></font>\n";
	  print "<P><hr width=75%></center>\n";
	  print "</body></html>";
	}

	## 荒らしエラー分岐
	$a_flag = 0;
	# Type 1：不正アクセス
	if ($emode == 1 || $alog1) {
		$e_type = "不正アクセス";
		$a_flag = 1;
	}
	# Type 2：プロクシエラー
	elsif ($emode == 2 || $alog2) {
		$e_type = "プロクシ拒否";
		$a_flag = 1;
	}
	# Type 3：禁止ワード
	elsif ($emode == 3 || $alog3) {
		$e_type = "禁止ワード使用";
		$a_flag = 1;
	}
	# Type 4：荒らし指定ハンドル
	elsif ($emode == 4 || $alog4) {
		$e_type = "荒らし指定ハンドル使用";
		$a_flag = 1;
	}
	# Type 5：クッキー無効
	elsif ($emode == 5 || $alog5) {
		$e_type = "クッキー無効";
		$a_flag = 1;
	}
	# Type 6：指定ホスト拒否
	elsif ($emode == 6 || $alog6) {
		$e_type = "指定ホスト拒否";
		$a_flag = 1;
	}
	# Type 7：非許可タグ使用
	elsif ($emode == 7 || $alog7) {
		$e_type = "非許可タグ使用";
		$a_flag = 1;
	}
	# 不正な値代入時のエラー回避
	else { $a_flag = 0; }

	&alog_w;

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
	if ($get_remotehost && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }
}
1;

__END__

