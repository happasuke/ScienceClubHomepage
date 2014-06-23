#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ DreamCounter
#│ dream.cgi - 2008/03/05
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

# 外部ファイル取込
require './drinit.cgi';
require $gifcat;

# デコード処理
$string = &parse_form;
$in{'id'}  =~ s/\W//g;
$in{'fig'} =~ s/\D//g;
if ($in{'fig'} > $maxfig) { $in{'fig'} = $maxfig; }

# チェックモード
if ($mode eq "check") {	&check; }

# 他サイトからのアクセス排除
if ($base_url) {
	my $ref = $ENV{'HTTP_REFERER'};
	$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if ($ref && $ref !~ /$base_url/i) { &error; }
}

# 画像ディレクトリを定義
if ($in{'gif'}) {
	$in{'gif'} =~ s/\D//g;
	$gifdir =~ s|(.*)\d+/$|$1$in{'gif'}/|g;
}

## ランダムモード
if (!$string || $mode eq 'rand') {

	if (!$in{'fig'}) { $in{'fig'} = 5; }

	srand;
	my $count;
	foreach (1 .. $in{'fig'}) {
		$count .= int(rand(10));
	}

	# 画像表示
	&count_view($count);

## カウンタ処理
} elsif ($in{'id'} ne "") {

	&counter;

## 時間処理
} elsif ($mode eq "time") {

	# 時間取得
	my ($min,$hour,$mday,$mon,$year) = &get_time;

	my $count;
	if ($in{'type'} == 24) {
		$count = $hour . 'c' . $min;
	} else {
		if ($hour >= 12) {
			$hour = sprintf("%02d", $hour-12);
			$head = 'p';
		} else {
			$head = 'a';
		}
		$count = $head . $hour . 'c' . $min;
	}

	# 画像表示
	&count_view($count);

## カレンダ処理
} elsif ($mode eq "date") {

	# 時間取得
	my ($min,$hour,$mday,$mon,$year) = &get_time;

	my $count;
	if ($in{'year'} == 4) {
		$count = $year . 'd' . $mon . 'd' . $mday;
	} else {
		$year = sprintf("%02d", $year-2000);
		$count = $year . 'd' . $mon . 'd' . $mday;
	}

	# 画像表示
	&count_view($count);

## 更新時間表示処理
} elsif ($in{'file'}) {

	# ファイルがなければエラー
	unless (-e $in{'file'}) { &error; }

	# 更新日数を取得
	my ($mtime) = (stat($in{'file'}))[9];

	# 更新時間
	my ($min,$hour,$mday,$mon,$year) = &get_time($mtime);

	# スラッシュ "/" がなければダッシュ "-" で代用
	my $slush = $gifdir . 's.gif';
	if (-e $slush) { $s = 's'; } else { $s = 'd'; }

	# 画像表示
	my $count = $year . $s . $mon . $s . $mday . 'd' . $hour . 'c' . $min;
	&count_view($count);

## ファイルサイズ数表示処理
} elsif ($in{'size'}) {

	# ファイルがなければエラー
	unless (-e $in{'size'}) { &error; }

	# サイズ数を取得 (bytes)
	my ($size) = (stat($in{'size'}))[7];

	# 単位変換（四捨五入）
	if ($in{'p'} eq 'k') {
		$size = int(($size / 1024)+0.5);
	} elsif ($in{'p'} eq 'm') {
		$size = int(($size / 1048576)+0.5);
	}

	# 画像表示
	&count_view($size);

## 強制表示（数字のみ）
} elsif ($in{'num'} ne "") {

	# 画像表示
	$in{'num'} =~ s/\D//g;
	&count_view($in{'num'});

## 他の引数だとエラー
} else {
	&error;
}

#-------------------------------------------------
#  GIF出力
#-------------------------------------------------
sub count_view {
	my $count = shift;

	my @image;
	foreach ( split(//, $count) ) {
		push(@image,"$gifdir$_.gif");
	}

	# 連結開始
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat::gifcat(@image);
	exit;
}

#-------------------------------------------------
#  カウンタ処理
#-------------------------------------------------
sub counter {
	# ログを定義
	my $logfile = "$datadir$in{'id'}.dat";

	# ログの存在をチェック
	unless(-e $logfile) {

		# ログ生成 [なし] ならプログラムを終了
		if ($id_creat == 0) {

			&error;

		# ログ生成 [あり] ならログを生成
		} else {
			open(OUT,">$logfile") || &error;
			print OUT "0";
			close(OUT);

			# パーミッションを 666 へ
			chmod(0666, $logfile);
		}
	}

	# デフォルト桁数を定義
	if ($in{'fig'} eq "") { $in{'fig'} = 5; }

	# IPアドレスを取得
	my $addr = $ENV{'REMOTE_ADDR'};

	# 記録ファイルから読み込み
	open(DAT,"+< $logfile") || &error;
	eval "flock(DAT, 2);";
	my $data = <DAT>;

	# 記録ファイルを分解
	my ($count, $ip) = split(/:/, $data);

	# IPチェック
	my $flg;
	if ($ip_chk && $addr eq $ip) { $flg = 1; }

	# ログ更新
	if (!$flg) {
		# カウントアップ
		$count++;

		# ファイルをフォーマット
		if ($ip_chk) {
			$data = "$count:$addr";
		} else {
			$data = $count;
		}

		# 記録ファイル更新
		seek(DAT, 0, 0);
		print DAT $data;
		truncate(DAT, tell(DAT));
	}
	close(DAT);

	# 桁数調整
	while ( length($count) < $in{'fig'} ) {
		$count = '0' . $count;
	}

	# 画像表示
	&count_view($count);
}

#-------------------------------------------------
#  時間取得
#-------------------------------------------------
sub get_time {
	my $time = shift;
	$time = time if (!$time);

	$ENV{'TZ'} = "JST-9";
	my ($min,$hour,$mday,$mon,$year) = (localtime($time))[1..5];

	$year += 1900;
	$mon  = sprintf("%02d", $mon+1);
	$hour = sprintf("%02d", $hour);
	$min  = sprintf("%02d", $min);
	$mday = sprintf("%02d", $mday);

	return ($min,$hour,$mday,$mon,$year);
}

#-------------------------------------------------
#  エラー処理
#-------------------------------------------------
sub error {
	# エラー画像
	my @err = (
		'47','49','46','38','39','61','2d','00','0f','00','80','00','00',
		'00','00','00','ff','ff','ff','2c','00','00','00','00','2d','00',
		'0f','00','00','02','49','8c','8f','a9','cb','ed','0f','a3','9c',
		'34','81','7b','03','ce','7a','23','7c','6c','00','c4','19','5c',
		'76','8e','dd','ca','96','8c','9b','b6','63','89','aa','ee','22',
		'ca','3a','3d','db','6a','03','f3','74','40','ac','55','ee','11',
		'dc','f9','42','bd','22','f0','a7','34','2d','63','4e','9c','87',
		'c7','93','fe','b2','95','ae','f7','0b','0e','8b','c7','de','02',
		'00','3b');

	print "Content-type: image/gif\n\n";
	foreach (@err) {
		print pack('C*',hex($_));
	}
	exit;
}

#-------------------------------------------------
#  チェックモード
#-------------------------------------------------
sub check {
	&header;
	print <<EOM;
<h3>Check Mode</h3>
<ul>
EOM

	# データディレクトリ
	my $flg;
	if (-d $datadir) {
		$flg = 1;
		print "<li>データディレクトリのパス：OK\n";

		if (-r $datadir && -w $datadir && -x $datadir) {
			print "<li>データディレクトリのパーミッション：OK\n";
		} else {
			print "<li>データディレクトリのパーミッション：NG → $datadir\n";
		}
	} else {
		print "<li>データディレクトリのパス：NG → $datadir\n";
	}

	# 他サイトからのアクセス制限
	print "<li>他サイトからのアクセス制限：";
	if ($base_url) {
		print "あり → $base_url\n";
	} else {
		print "なし\n";
	}

	# 画像ディレクトリのパス確認
	if (-d $gifdir) {
		print "<li>$gifdir : 画像ディレクトリのパス : OK! \n";
	} else {
		print "<li>$gifdir : 画像ディレクトリがありません\n";
	}

	# 画像チェック
	foreach ("0".."9", "a", "p", "c", "d") {
		if (-e "$gifdir$_.gif") {
			print "<li>$_ : 画像OK \n";
		} else {
			print "<li>$_ : 画像がありません\n";
		}
	}

	# 画像連結
	print "<li>画像連結テスト → <img src=\"$dreamcgi?num=0123456789\">\n";

	# ログファイル検索
	if ($flg) {
		my @file = &datadir;
		foreach (@file) {
			my $datfile = "$datadir$_";

			if (-r $datfile && -w $datfile) {
				print "<li>ログ $_ : パーミッションOK \n";
			} else {
				print "<li>ログ $_ : パーミッション<b>NG</b>\n";
			}
		}
	}

	# 著作権表示：削除改変禁止
	print <<EOM;
<li>バージョン : <a href="http://www.kent-web.com/">$ver</a>
</ul>
</body>
</html>
EOM
	exit;
}


