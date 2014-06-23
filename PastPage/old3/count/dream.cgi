#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� DreamCounter
#�� dream.cgi - 2008/03/05
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

# �O���t�@�C���捞
require './drinit.cgi';
require $gifcat;

# �f�R�[�h����
$string = &parse_form;
$in{'id'}  =~ s/\W//g;
$in{'fig'} =~ s/\D//g;
if ($in{'fig'} > $maxfig) { $in{'fig'} = $maxfig; }

# �`�F�b�N���[�h
if ($mode eq "check") {	&check; }

# ���T�C�g����̃A�N�Z�X�r��
if ($base_url) {
	my $ref = $ENV{'HTTP_REFERER'};
	$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	if ($ref && $ref !~ /$base_url/i) { &error; }
}

# �摜�f�B���N�g�����`
if ($in{'gif'}) {
	$in{'gif'} =~ s/\D//g;
	$gifdir =~ s|(.*)\d+/$|$1$in{'gif'}/|g;
}

## �����_�����[�h
if (!$string || $mode eq 'rand') {

	if (!$in{'fig'}) { $in{'fig'} = 5; }

	srand;
	my $count;
	foreach (1 .. $in{'fig'}) {
		$count .= int(rand(10));
	}

	# �摜�\��
	&count_view($count);

## �J�E���^����
} elsif ($in{'id'} ne "") {

	&counter;

## ���ԏ���
} elsif ($mode eq "time") {

	# ���Ԏ擾
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

	# �摜�\��
	&count_view($count);

## �J�����_����
} elsif ($mode eq "date") {

	# ���Ԏ擾
	my ($min,$hour,$mday,$mon,$year) = &get_time;

	my $count;
	if ($in{'year'} == 4) {
		$count = $year . 'd' . $mon . 'd' . $mday;
	} else {
		$year = sprintf("%02d", $year-2000);
		$count = $year . 'd' . $mon . 'd' . $mday;
	}

	# �摜�\��
	&count_view($count);

## �X�V���ԕ\������
} elsif ($in{'file'}) {

	# �t�@�C�����Ȃ���΃G���[
	unless (-e $in{'file'}) { &error; }

	# �X�V�������擾
	my ($mtime) = (stat($in{'file'}))[9];

	# �X�V����
	my ($min,$hour,$mday,$mon,$year) = &get_time($mtime);

	# �X���b�V�� "/" ���Ȃ���΃_�b�V�� "-" �ő�p
	my $slush = $gifdir . 's.gif';
	if (-e $slush) { $s = 's'; } else { $s = 'd'; }

	# �摜�\��
	my $count = $year . $s . $mon . $s . $mday . 'd' . $hour . 'c' . $min;
	&count_view($count);

## �t�@�C���T�C�Y���\������
} elsif ($in{'size'}) {

	# �t�@�C�����Ȃ���΃G���[
	unless (-e $in{'size'}) { &error; }

	# �T�C�Y�����擾 (bytes)
	my ($size) = (stat($in{'size'}))[7];

	# �P�ʕϊ��i�l�̌ܓ��j
	if ($in{'p'} eq 'k') {
		$size = int(($size / 1024)+0.5);
	} elsif ($in{'p'} eq 'm') {
		$size = int(($size / 1048576)+0.5);
	}

	# �摜�\��
	&count_view($size);

## �����\���i�����̂݁j
} elsif ($in{'num'} ne "") {

	# �摜�\��
	$in{'num'} =~ s/\D//g;
	&count_view($in{'num'});

## ���̈������ƃG���[
} else {
	&error;
}

#-------------------------------------------------
#  GIF�o��
#-------------------------------------------------
sub count_view {
	my $count = shift;

	my @image;
	foreach ( split(//, $count) ) {
		push(@image,"$gifdir$_.gif");
	}

	# �A���J�n
	print "Content-type: image/gif\n\n";
	binmode(STDOUT);
	print &gifcat::gifcat(@image);
	exit;
}

#-------------------------------------------------
#  �J�E���^����
#-------------------------------------------------
sub counter {
	# ���O���`
	my $logfile = "$datadir$in{'id'}.dat";

	# ���O�̑��݂��`�F�b�N
	unless(-e $logfile) {

		# ���O���� [�Ȃ�] �Ȃ�v���O�������I��
		if ($id_creat == 0) {

			&error;

		# ���O���� [����] �Ȃ烍�O�𐶐�
		} else {
			open(OUT,">$logfile") || &error;
			print OUT "0";
			close(OUT);

			# �p�[�~�b�V������ 666 ��
			chmod(0666, $logfile);
		}
	}

	# �f�t�H���g�������`
	if ($in{'fig'} eq "") { $in{'fig'} = 5; }

	# IP�A�h���X���擾
	my $addr = $ENV{'REMOTE_ADDR'};

	# �L�^�t�@�C������ǂݍ���
	open(DAT,"+< $logfile") || &error;
	eval "flock(DAT, 2);";
	my $data = <DAT>;

	# �L�^�t�@�C���𕪉�
	my ($count, $ip) = split(/:/, $data);

	# IP�`�F�b�N
	my $flg;
	if ($ip_chk && $addr eq $ip) { $flg = 1; }

	# ���O�X�V
	if (!$flg) {
		# �J�E���g�A�b�v
		$count++;

		# �t�@�C�����t�H�[�}�b�g
		if ($ip_chk) {
			$data = "$count:$addr";
		} else {
			$data = $count;
		}

		# �L�^�t�@�C���X�V
		seek(DAT, 0, 0);
		print DAT $data;
		truncate(DAT, tell(DAT));
	}
	close(DAT);

	# ��������
	while ( length($count) < $in{'fig'} ) {
		$count = '0' . $count;
	}

	# �摜�\��
	&count_view($count);
}

#-------------------------------------------------
#  ���Ԏ擾
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
#  �G���[����
#-------------------------------------------------
sub error {
	# �G���[�摜
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
#  �`�F�b�N���[�h
#-------------------------------------------------
sub check {
	&header;
	print <<EOM;
<h3>Check Mode</h3>
<ul>
EOM

	# �f�[�^�f�B���N�g��
	my $flg;
	if (-d $datadir) {
		$flg = 1;
		print "<li>�f�[�^�f�B���N�g���̃p�X�FOK\n";

		if (-r $datadir && -w $datadir && -x $datadir) {
			print "<li>�f�[�^�f�B���N�g���̃p�[�~�b�V�����FOK\n";
		} else {
			print "<li>�f�[�^�f�B���N�g���̃p�[�~�b�V�����FNG �� $datadir\n";
		}
	} else {
		print "<li>�f�[�^�f�B���N�g���̃p�X�FNG �� $datadir\n";
	}

	# ���T�C�g����̃A�N�Z�X����
	print "<li>���T�C�g����̃A�N�Z�X�����F";
	if ($base_url) {
		print "���� �� $base_url\n";
	} else {
		print "�Ȃ�\n";
	}

	# �摜�f�B���N�g���̃p�X�m�F
	if (-d $gifdir) {
		print "<li>$gifdir : �摜�f�B���N�g���̃p�X : OK! \n";
	} else {
		print "<li>$gifdir : �摜�f�B���N�g��������܂���\n";
	}

	# �摜�`�F�b�N
	foreach ("0".."9", "a", "p", "c", "d") {
		if (-e "$gifdir$_.gif") {
			print "<li>$_ : �摜OK \n";
		} else {
			print "<li>$_ : �摜������܂���\n";
		}
	}

	# �摜�A��
	print "<li>�摜�A���e�X�g �� <img src=\"$dreamcgi?num=0123456789\">\n";

	# ���O�t�@�C������
	if ($flg) {
		my @file = &datadir;
		foreach (@file) {
			my $datfile = "$datadir$_";

			if (-r $datfile && -w $datfile) {
				print "<li>���O $_ : �p�[�~�b�V����OK \n";
			} else {
				print "<li>���O $_ : �p�[�~�b�V����<b>NG</b>\n";
			}
		}
	}

	# ���쌠�\���F�폜���ϋ֎~
	print <<EOM;
<li>�o�[�W���� : <a href="http://www.kent-web.com/">$ver</a>
</ul>
</body>
</html>
EOM
	exit;
}


