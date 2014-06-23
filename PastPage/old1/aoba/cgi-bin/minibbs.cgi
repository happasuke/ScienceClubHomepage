#! /usr/local/bin/perl

;#  ↑このパスはプロバイダによって違うので調べて設定する
;#    (これはこのスクリプトの最初の１行になければならず、それより上に空行があってもいけません。)
;#    (この設定が必要ないサーバもあります。一般的な場合を想定して解説を入れています。)
;#    (他に、プロバイダからアナウンスされている情報を十分理解しておいてください。)
;#
;# 簡易ＢＢＳ version 7.5c（フリーソフト）
;#
;# Script written by Kazu.Y
;# Created on: 02/05/96
;# Last Modified on: 07/03/97
;# I can be reached at: rescue@ask.or.jp
;# Scripts Found at: http://www.ask.or.jp/~rescue/
;#
;# <利用規定の抜粋>
;#  1.このスクリプトは自分で使うために承諾なしに自由に改造することができます。
;#  2.改造の有無にかかわらず、このスクリプトを再配布することはできません。
;#  3.このシステムを有償で他人に設置してあげたりする行為は無断ではできません。

###########################################################################################
#
# ■重要！ この v7.5c は、v7.5 に管理パスワードを暗号化する機能を付加したものです。
# 設置するサーバによっては正しく暗号化できませんので、設定したパスワードが
# 認証されない場合はこのトラブルが考えられますので、v7.5 をご利用ください。
#
# 一旦設定されたパスワードを忘れた場合、または、正しく暗号化できない場合に、
# 記録されてしまったパスワードを削除することはできません。データを空にして最初からやり直すことになります。
# データを継承したい方は、予め他の場所で動作試験を行ったあとに施工してください。
#
# ■互換性！ v7.5 で生成されたデータは v7.5c で利用することができますが、その逆は
# できません。データファイル内に暗号化されたパスワードも記録されるため、v7.5c で
# 処理された後のデータを v7.5 で使うことはできません。
#
#
# 基本構成（初期設定はこの構成を前提に解説します）
#
#   public_html（ホームページディレクトリ）
#        |
#        |-- cgi-bin（任意のディレクトリ）
#               |
#               |-- jcode.pl (755)
#               |-- minibbs.cgi (755)
#               |-- minibbs.dat (666)
#
#                   ・この minibbs.pl は minibbs.cgi にファイル名を変更する
#                   ・minibbs.dat は中身が空っぽのファイルをパソコン上で作成して転送する
#                   ・このシステムに必要な３つのファイルを同じ場所に設置する
#                   ・( )内はパーミッッション値
#                   ・jcode.plは中身を全くいじらずにそのままアスキー転送する
#                   ・jcode.plはjperlでは利用できないので注意すること
#                   ・これら３つのファイルはアスキーモードで取り扱う(転送)すること
#
###########################################################################################

#----------------#
#    初期設定    #
#----------------#

#--- 必ずあなたの環境に合わせて書き替える項目 --------------------------------------------#

# 掲示板の名前
$title = '井戸端会議';

# このスクリプトをＵＲＬで設定
$reload = 'http://www.sendai-ct.ac.jp/~ckuma/kagakubu/old/aoba/cgi-bin/minibbs.cgi';

# 画面の「終了」ボタンの表示先をＵＲＬで設定
$modoru = 'http://www.sendai-ct.ac.jp/~ckuma/kagakubu/old/aoba/';


#--- 必要に応じて設定する項目 ------------------------------------------------------------#

#　文字色や背景などの設定（通常の<body>タグ）
#　題名と投稿者色はスクリプト内の<font color>タグを探して設定してください。
$body = '<body bgcolor="#eaeaae" text="#000000">';

#  タグを使えるようにするかどうかの設定
#  <a gref="リンク"></a>については入力フォームが用意してあるので、いたずらやタグの
#  閉じ忘れ等による混乱を避けるためにできるだけ使えないようにしておくことをお勧めします。
#  使える:1 使えない:0
$tag = 0;

#  １ページに表示する件数
$def = 50;

#  書き込み件数の最大登録数の設定です。この件数を超えると、古いものから削除されていきます。
#　ページ処理機能が付きましたので、この件数を大きくしても一度に表示される記事数は限定されます。
#　記録されたファイルの巨大化を防止する為に、ある程度の件数で自動削除されるようにします。
$max = '200';

#　日本語コード変換ライブラリ
#  この jcode.pl を minibbs.cgi と違うディレクトリに設置する場合は相対的に設定すること
require './jcode.pl';

#　内容が書き込まれる記録ファイルのパスを設定
#  この minibbs.dat を minibbs.cgi と違うディレクトリに設置する場合は相対的に設定すること
$file = './minibbs.dat';

#  海外サーバ等で時差が生じる場合は修正します
#    海外時間に＋９時間する場合　= localtime(time + 9*60*60);
#    海外時間に－９時間する場合　= localtime(time - 9*60*60);
#   （参考）timeには1970年からの秒数が入っています
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

#  クッキーの消化設定
#    最終書き込みから   30日後 30*24*60*60
#                        1日後 24*60*60
#                     10時間後 10*60*60
$ENV{'TZ'} = "GMT"; # 国際標準時を取得する
($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = localtime(time + 30*24*60*60);

# 入力形式の設定　標準入力:post その他:get
# 投稿ボタンを押して Method not implemented.. というエラーが出る場合は  get で試すこと
$method = 'post';

###########################################################################################
#
# ・記録ファイルには処理の都合上特殊コードが記録されますので、直接編集はできません。
# ・スクリプトの中身を書き替える場合は、perlやCGIやHTMLなどのそれなりの知識が必要です。
# ・設置に関する質問はチャレンジＣＧＩ専用掲示板をご利用ください。改造の質問は受けません。
#   http://www2r.meshnet.or.jp/~rescue/webboard/
#
###########################################################################################

# 上記のlocaltimeで取得した$monには0から11までの数字が入るので修正処理
$month = ($mon + 1);

# 時刻を２桁に統一する処理（削除処理に関係するので書き替えないこと）
if ($month < 10) { $month = "0$month"; }
if ($mday < 10)  { $mday  = "0$mday";  }
if ($sec < 10)   { $sec   = "0$sec";   }
if ($min < 10)   { $min   = "0$min";   }
if ($hour < 10)  { $hour  = "0$hour";  }

# 曜日変換処理
# $wdayには0から6までの数字が入り曜日に対応している
$y0="日"; $y1="月"; $y2="火"; $y3="水"; $y4="木"; $y5="金"; $y6="土";
$youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6) [$wday];

# 時刻フォーマット（削除処理に関係するので書き替えないこと）
$date_now = "$month月$mday日($youbi)$hour時$min分$sec秒";

# フォーム入力されたデータを$bufferに格納する（getかpostかによって取得方法が異なる）
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
else { $buffer = $ENV{'QUERY_STRING'}; }

# $bufferに格納されたFORM形式のデータを取り出す

@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {

	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	# 処理の都合上の処理
	$value =~ s/\n//g; # 改行文字はデータの記録に影響があるので消去する

	if ($tag) { # 掲示板に書き込まれたくないタグを設定する(タグが使える場合に有効)

		if ($value =~ /<table(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<meta(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<pre(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<!--(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<form(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<embed(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<script(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<frame(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<a(.|\n)*on(.*)=(.|\n)*>/i) { &error(tag); }
		if ($value =~ /<img(.|\n)*on(.*)=(.|\n)*>/i) { &error(tag); }
	}

	if ($tag eq '0' && $name eq 'value') { # タグを無効

		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
	}

	if ($tag eq '0' && $name eq 'value') { $value =~ s/\,/\0/g; } # 半角カンマはデータのCSV記録に影響があるのでヌルコード変換する
	elsif ($name eq 'value') { $value =~ s/&/&amp\;/g; $value =~ s/\,/\0/g; }
	elsif ($name ne 'page') { $value =~ s/\,//g; $value =~ s/\;//g; $value =~ s/\://g; $value =~ s/\=//g; }
	else { $value =~ s/\,//g; }

	# 記録するデータはsjisに統一する
	&jcode'convert(*value,'sjis');

	if ($name eq "target") { push(@RM,$value); }
	else { $FORM{$name} = $value; }
}

# 管理キーの設定ルーチン
# 記録ファイルを読み出しオープンして、配列<@lines>に格納する
if (!open(DB,"$file")) { &error(0); }
@lines = <DB>;
close(DB);

# データの最初に記録される暗号化されたパスワードを取り出す
$password = shift(@lines);
chop($password) if $password =~ /\n$/;
($header,$password) = split(/:/,$password);
if ($FORM{'action'} eq 'password') { &encode; }
if ($FORM{'admin'} eq 'change') { &password; }
if ($header ne 'crypt_password') { $first = 1; &password; }

#  全体の流れを決定する（actionやpwdはフォーム入力されたデータを格納する名前）
#    action=remove かつ pwd=設定パスワード --> 削除処理して通常画面へ
#    action=remove  --> 削除記事選択画面へ
#    action=regist  --> 記事記録処理して通常画面へ
#    その他  --> 通常画面へ
if ($FORM{'action'} eq 'remove' && crypt($FORM{'pwd'}, substr($password,0,2)) eq $password) { &remove2; &remove1; exit; }
elsif (crypt($FORM{'pwd'}, substr($password,0,2)) eq $password) { &remove1; exit; }
elsif ($FORM{'action'} eq 'regist') { &regist; }
&html;

sub html {

	#--- クッキーの取得（独自方式）-----------------------#

	$cookies = $ENV{'HTTP_COOKIE'};

	@pairs = split(/;/,$cookies);
	foreach $pair (@pairs) {

		($name, $value) = split(/=/, $pair);
		$name =~ s/ //g;
		$DUMMY{$name} = $value;
	}

	@pairs = split(/,/,$DUMMY{$reload});
	foreach $pair (@pairs) {

		($name, $value) = split(/:/, $pair);
		$COOKIE{$name} = $value;
	}

	#--- 入力フォーム画面 --------------------------------#

	# ＣＧＩで出力されたデータをＨＴＭＬとして認識させるヘッダの出力
	print "Content-type: text/html; charset=Shift_JIS\n\n";

	print "<html><head><title>$title</title></head>\n";
	print "$body\n";

	print "<font size=+2><b>$title</b></font><p>\n";

    print "<P ALIGN=RIGHT><FONT SIZE=+2><A HREF=\"../\">トップに戻る</A></FONT></P>\n";
	print "<form method=$method action=\"$reload\">\n";
	print "<input type=hidden name=\"action\" value=\"regist\">\n";
	print "投稿者 <input type=text name=\"name\" size=20 value=\"$COOKIE{'name'}\" maxlength=19><br>";
	print "メール <input type=text name=\"email\" size=30 value=\"$COOKIE{'email'}\"><br>\n";
	print "題名　 <input type=text name=\"subject\" size=30>  \n";
	print "<input type=submit value=\"     投稿     \"><input type=reset value=\"消す\"><p>\n";

	print "内容<i>（記入通りに記録しますので適当に改行を入れてください。\n";

	if (!$tag) { print "タグは使えません。"; }
	print "）</i><br>\n";

	print "<textarea name=\"value\" rows=5 cols=70></textarea><p>\n";
	print "ＵＲＬ（リンクを入れたい場合はここに記入します）<br>\n";
	print "<input type=text name=\"page\" size=70 value=\"http://\"><p></form>\n";

	print "<hr><font size=-1><i>新しい記事から表\示します。最高$max件の記事が記録され、それを超えると古い記事から削除されます。<br>\n";
	print "１回の表\示で$def件を越える場合は、下のボタンを押すことで次の画面の記事を表\示します。</i></font>\n\n";

	#--- 記録記事の出力 ----------------------------------#

	if ($FORM{'page'} eq '') { $page = 0; } else { $page = $FORM{'page'}; }

	$accesses = @lines; $accesses--;
	$page_end = $page + $def - 1;
	if ($page_end > $accesses) { $page_end = $accesses; }

	foreach ($page .. $page_end) {

		# データを各変数に代入する
		($date,$name,$email,$value,$subject,$hpage) = split(/\,/,$lines[$_]);
		$value =~ s/\0/\,/g; # ヌルコードに変換記録した半角カンマを復帰させる
		chop($hpage) if $hpage =~ /\n/;

		print "<hr><font size=+1 color=\"#ff0000\"><b>$subject</b></font>";

		# メールアドレスが記録されているデータにはリンクを付ける
		if ($email ne '') { print "　投稿者：<b><a href=\"mailto:$email\">$name</a></b>\n"; }
		else { print "　投稿者：<font color=\"#555555\"><b>$name</b></font>\n"; }

		print "<font size=-1>　投稿日：$date</font><p>\n";
		print "<blockquote><pre>$value</pre><p>\n\n";

		# ＵＲＬが記録されているデータにはリンクを付ける
		if ($hpage ne '') { print "<a href=\"$hpage\" target=\"_top\">$hpage</a><p>\n"; }

		print "</blockquote>\n";
	}

	#--- 改ページ処理 ------------------------------------#

	print "<hr><p>\n";

	$page_next = $page_end + 1;
	$i = $page + 1; $j = $page_end + 1;

	if ($page_end ne $accesses) {

		print "<font size=-1><i>以上は、現在登録されている新着順$i番目から$j番目までの記事です。</i></font><p>\n";
		print "<form method=$method action=\"$reload\">\n";
		print "<input type=hidden name=\"page\" value=\"$page_next\">\n";
		print "<input type=submit value=\"次のページ\"></form>\n";
	}
	else {

		print "<font size=-1><i>以上は、現在登録されている新着順$i番目から$j番目までの記事です。";
		print "これ以下の記事はありません。</i></font>\n";
	}

	print "<form action=\"$modoru\"><input type=submit value=\"　終　了　\"></form><p>\n";

	print "<form method=$method action=\"$reload\">\n";
	print "<hr><p>\n";
	print "<input type=checkbox name=\"admin\" value=\"change\">管理パスワードの変更<br>";
	print "記事の削除は管理パスワードを入力 <input type=password name=\"pwd\" size=10> ";
	print "<input type=submit value=\"変更/削除\"></form>\n";

	# このスクリプトの著作権表示（かならず表示してください）
	print "<h4 align=right><hr><a href=\"http://www.ask.or.jp/~rescue/\" target=\"_top\">MiniBBS v7.5c</a> is Free.</h4>\n";
	print "</body></html>\n";
	exit;
}

sub regist {

	# 別のページからこのＣＧＩへの投稿を排除する処理
	# ■注：このＣＧＩからの投稿もできないようにする場合は次の3行の#を削除してください

	#$ref = $ENV{'HTTP_REFERER'};
	#$ref_url = $reload; $ref_url =~ s/\~/.*/g;
	#if (!($ref =~ /$ref_url/i)) { &error(form); }

	# 入力されたデータのチェック

	if ($FORM{'name'} eq "") { &error(1); }
	if ($FORM{'value'} eq "") { &error(2); }
	if ($FORM{'email'} =~ /,/) { &error(4); }
	if ($FORM{'email'} ne "") { if (!($FORM{'email'} =~ /(.*)\@(.*)\.(.*)/)) { &error(3); }}
	if ($FORM{'subject'} eq "") { $FORM{'subject'} = '(無題)'; }
	if ($FORM{'page'} eq "" || $FORM{'page'} eq "http://") { $FORM{'page'} = ''; }

	$FORM{'name'} =~ s/<//g; $FORM{'name'} =~ s/>//g;
	$FORM{'subject'} =~ s/</&lt;/g; $FORM{'subject'} =~ s/>/&gt;/g;
	$FORM{'email'} =~ s/<//g; $FORM{'email'} =~ s/>//g;

	#  クッキーの仕様書  http://www.netscape.com/newsref/std/cookie_spec.html

	if ($yearg < 10)  { $yearg = "0$yearg"; }
	if ($secg < 10)   { $secg  = "0$secg";  }
	if ($ming < 10)   { $ming  = "0$ming";  }
	if ($hourg < 10)  { $hourg = "0$hourg"; }
	if ($mdayg < 10)  { $mdayg = "0$mdayg"; }

	$y0="Sunday"; $y1="Monday"; $y2="Tuesday"; $y3="Wednesday"; $y4="Thursday"; $y5="Friday"; $y6="Saturday";
	$youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6) [$wdayg];

	$m0="Jan"; $m1="Feb"; $m2="Mar"; $m3="Apr"; $m4="May"; $m5="Jun";
	$m6="Jul"; $m7="Aug"; $m8="Sep"; $m9="Oct"; $m10="Nov"; $m11="Dec";
	$month = ($m0,$m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9,$m10,$m11) [$mong];

	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";

	#　独自方式のクッキーフォーマット
	#
	#　この簡易ＢＢＳでは名前とメールアドレスを保存の対象にしています。
	#　それぞれを独立したクッキーとしてブラウザに食べさせればとても簡単ですが、
	#　ブラウザがクッキーを格納できる数に制限があるため、できるだけ一つのクッキーに
	#　保存データをまとめて食べさせることが望まれます。そのためにここでは独自の方法で
	#　１つのクッキー内に複数のデータを詰め込み、クッキーの取得時にそれらを展開して利用しています。
	#　
	#　name:<name>,email:<email> という形式にまとめて、これを一つのクッキーとして
	#　cookieという名前でブラウザに送信しています。
	#
	#　独自フォーマット　cookie=name:<name>,email:<email>

	$cook="name\:$FORM{'name'}\,email\:$FORM{'email'}";
	print "Set-Cookie: $reload=$cook; expires=$date_gmt\n";

	# 記入者のリモートホスト名を取得する（これは表示されずＨＴＭＬソースで閲覧できる）
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($host eq $addr) { $host = gethostbyaddr(pack('C4',split(/\./,$host)),2) || $addr; }

	# 記録ファイルを読み出しオープンして、配列<@lines>に格納する
	if (!open(DB,"$file")) { &error(0); }
	@lines = <DB>; $password = shift(@lines);
	close(DB);

	# 最大保持記録数の処理
	$i = 0;
	foreach $line (@lines) {

		$i++;
		if ($i == $max) { last; }
		push(@new,$line);
	}

	$value = "$date_now\,$FORM{'name'}\,$FORM{'email'}\,$FORM{'value'}<!--remote_host：$host-->\,$FORM{'subject'}\,$FORM{'page'}\n";
	unshift(@new,$value);

	# 記録ファイルを上書きオープンして、配列<@new>を書き出す
	if (!open(DB,">$file")) { &error(0); }
	print DB $password;
	print DB @new;
	close(DB);

	# 記録処理後、再読み込みする
	print "Location: $reload" . '?' . "\n\n";
	exit;
}

sub error {

	#  &error(xx); で呼び出されたルーチンは、()内の数字が $error に代入される。

	$error = $_[0];

	if    ($error eq "0") { $error_msg = '記録ファイルの入出力にエラーが発生しました。'; }
	elsif ($error eq "1") {	$error_msg = '投稿者名が記入されていません。'; }
	elsif ($error eq "2") {	$error_msg = '内容が書かれていません。または記録禁止のタグが書かれています。'; }
	elsif ($error eq "3") {	$error_msg = 'メールアドレスが正しく入力されていません。'; }
	elsif ($error eq "4") {	$error_msg = 'メールアドレスは複数指定できません。'; }
	elsif ($error eq "tag") { $error_msg = '利用ができないタグが記述されていますので投稿できません。'; }
	elsif ($error eq "form") { $error_msg = "投稿画面のＵＲＬが<br>$reload<br>" . '以外からの投稿はできません。'; }

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
        print "<h3>$error_msg</h3>\n";
        print "</body></html>\n";
        exit;
}


sub remove1 {

	if (!open(DB,"$file")) { &error(0); }
	@lines = <DB>; $password = shift(@lines);
	close(DB);

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
	print "<font size=+2><b>削除モード</b></font>  [<a href=\"$reload\">戻る</a>]<p>\n";

	print "<form method=$method action=\"$reload\">\n";
	print "<input type=hidden name=\"action\" value=\"remove\">\n";
	print "<pre>";
	print "   登録日                  投稿者               タイトル              内容<hr>\n";

	foreach $line (@lines) {

		($date,$name,$email,$value,$subject) = split(/\,/,$line);

		$value =~ s/\0/\,/g;
		chop($subject) if $subject =~ /\n/;
		$value =~ s/<!--.*-->//ig; $value =~ s/</&lt;/ig; $value =~ s/>/&gt;/ig; $value =~ s/\n/./g; $value =~ s/\r/./g;

		$i1 = length($subject);
		if ($i1 > 20) { $subject = substr($subject,0,18); $subject = $subject . '..'; }
		elsif ($i1 < 20) { $blank = ' ' x (20 - $i1); $subject = $subject . $blank; }

		$i2 = length($name);
		if ($i2 > 20) { $name = substr($name,0,18); $name = $name . '..'; }
		elsif ($i2 < 20) { $blank = ' ' x (20 - $i2); $name = $name . $blank; }

		if (length($value) > 40) { $value = substr($value,0,40); }
		print "<input type=checkbox name=\"target\" value=\"$date\">";
		print "$date $name $subject $value\n";
	}

	print "</pre><p><input type=hidden name=\"pwd\" value=\"$FORM{'pwd'}\">\n";
	print "<input type=submit value=\"     削除     \"><input type=reset value=\"リセット\"></form><p>\n";
	print "</body></html>\n";
}

sub remove2 {

	if (!open(DB,"$file")) { &error(0); }
	@lines = <DB>; $password = shift(@lines);
	close(DB);

	foreach $line (@lines) {

		($date,$name,$email,$value,$subject) = split(/\,/,$line);
		$del = 0;
		foreach $target (@RM) {	if ($target eq $date) { $del = 1; } }
		if ($del == 0) { push(@new,$line); }
	}

	if (!open(DB,">$file")) { &error(0); }
	print DB $password;
	print DB @new;
	close(DB);
}

sub password {

	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
	print "<h1>管理パスワードの設定/変更</h1>\n";

	if ($first && $message eq '') { print "記事を削除するための管理パスワードを登録します。<p>\n"; }
	else { print "$message<p>\n"; }

	print "<form method=$method action=\"$reload\">\n";
	print "<input type=hidden name=\"action\" value=\"password\">\n";
	if ($first != 1) { print "旧パスワード <input type=password name=\"password_old\" size=10><br>\n"; }
	print "新パスワード <input type=password name=\"password\" size=10><br>\n";
	print "新パスワード <input type=password name=\"password2\" size=10>（確認のためもう一度）<p>\n";
	print "<input type=submit value=\"     登録     \"></form><p>\n";
	print "</body></html>\n";
	exit;
}

sub encode {

	if ($header eq 'crypt_password') {

		if (crypt($FORM{'password_old'}, substr($password,0,2)) ne $password) { $message = '旧パスワードが認証されませんでした.'; &password; }
	}
	else {
		if (!open(DB,"$file")) { &error(0); }
		@lines = <DB>;
		close(DB);

		$first = 1;
	}

	if ($FORM{'password'} =~ /\W/ || $FORM{'password'} eq '') { $message = '新パスワードに英数字以外の文字が含まれているか空欄です.'; &password; }
	if ($FORM{'password'} ne $FORM{'password2'}) { $message = '確認のために入力された新パスワードが一致しません.'; &password; }

	$now = time;
	($p1, $p2) = unpack("C2", $now);
	$wk = $now / (60*60*24*7) + $p1 + $p2 - 8;
	@saltset = ('a'..'z','A'..'Z','0'..'9','.','/');
	$nsalt = $saltset[$wk % 64] . $saltset[$now % 64];
	$pwd = crypt($FORM{'password'}, $nsalt);

	if (!open(DB,">$file")) { &error(0); }
	print DB "crypt_password:$pwd\n";
	print DB @lines;
	close(DB);

	&html;
}

#end_of_script

