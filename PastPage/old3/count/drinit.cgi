#��������������������������������������������������������������������
#�� DreamCounter v3.41
#�� drinit.cgi - 2008/03/05
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'DreamCounter v3.41';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#��������������������������������������������������������������������
#
# [�^�O�̏������̗�] (*** �̓��O�t�@�C����)
#
#  �E�J�E���^ <img src="http://�`�`/count/dream.cgi?id=***">
#  �E�����\�� <img src="http://�`�`/count/dream.cgi?mode=time">
#  �E�J�����_ <img src="http://�`�`/count/dream.cgi?mode=date">
#  �E�t�@�C���̍X�V����
#             <img src="http://�`�`/count/dream.cgi?file=/home/�`/index.html">
#             [����] --> /home/�`/index.html�̕����̓t���p�X���w��
#
#  * ���p�� (ID���� index �Ɖ���)
#    1.�摜��ύX����Ƃ��F(�ȉ���gif2�f�B���N�g���̉摜�w���)
#      <img src="http://�`�`/count/dream.cgi?id=index&gif=2">
#    2.�����������_���ɕ\������Ƃ��F
#      <img src="http://�`�`/count/dream.cgi?mode=rand">
#    3.�J�E���^�������V���ɂ���Ƃ��F
#      <img src="http://�`�`/count/dream.cgi?id=index&fig=7">
#
#  * �`�F�b�N���[�h (mode=check �Ƃ������������ČĂяo���j
#    http://�`�`/dream.cgi?mode=check
#
# [ �f�B���N�g���\���� (���������̓p�[�~�b�V����) ]
#
#  public_html / index.html(�����ɃJ�E���^����\��)
#       |
#       +-- count / dream.cgi  [755]
#             |     gifcat.pl  [644]
#             |     drinit.cgi [644]
#             |     drmgr.cgi  [755]
#             |
#             +-- data [777] / index.dat [666]
#             |                xxxxx.dat [666}
#             |                   :
#             |                   :
#             |
#             +-- gif1 / 0.gif .. 9.gif, a.gif, p.gif, c.gif, d.gif
#             |
#             +-- gif2 / 0.gif .. 9.gif, a.gif, p.gif, c.gif, d.gif
#                  :

#-------------------------------------------------
#  ����{�ݒ�
#-------------------------------------------------

# �Ǘ��p�X���[�h�i�p�����Ŏw��j
$pass = 'ayashi';

# IP�A�h���X�̃`�F�b�N (0=no 1=yes) 
#   �� yes�̏ꍇ�A������IP�A�h���X�̓J�E���g�A�b�v���Ȃ�
$ip_chk = 1;

# ���O�̎������� (0=no 1=yes)
$id_creat = 0;

# ���O��u���T�[�o�f�B���N�g��
#   �� ���s�f�B���N�g���ł���΂��̂܂܂ł悢
#   �� �Ō�͕K�� / �ŕ���
#   �� �t���p�X�Ȃ� / ����n�߂�ihttp://����ł͂Ȃ��j
$datadir = './data/';

# ���T�C�g����A�N�Z�X��r��
#   �� �r������   : dream.cgi��ݒu����URL�� http://����L�q
#   �� �r�����Ȃ� : �����L�q���Ȃ��i���̂܂܁j
#   ���F�������u�r������v�Ƃ����ꍇ�A�ݒu����T�[�o�◘�p�҂̃u���E�U
#       �ɂ���Ă͎��T�C�g����ł��A�N�Z�X��r������ꍇ������܂��B
$base_url = "";

# �摜�̂���f�t�H���g�i�����l�j�̃f�B���N�g���w��
#   �� �t���p�X�Ȃ� / ����n�߂�ihttp://����ł͂Ȃ��j
#   �� �Ō�͕K�� / �ŕ���
$gifdir = './gif1/';

# �����w��̍ő�l�i�Z�L�����e�B�΍�j
#   �� ����𒴂��錅���͎w�肵�Ă���������܂��B
$maxfig = 12;

# �摜�A�����C�u�����y�T�[�o�p�X�z
$gifcat = './lib/gifcat.pl';

# �{��CGI�yURL�p�X�z
$dreamcgi = './dream.cgi';

# �Ǘ�CGI�yURL�p�X�z
$drmgrcgi = './drmgr.cgi';

#-------------------------------------------------
#  ���ݒ芮��
#-------------------------------------------------

#-------------------------------------------------
#  �t�H�[���f�R�[�h
#-------------------------------------------------
sub parse_form {
	$postflag = 0;
	local($buf);
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$postflag = 1;
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$buf = $ENV{'QUERY_STRING'};
	}
	undef(%in);
	foreach ( split(/&/, $buf) ) {
		local($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;

		$in{$key} = $val;
	}
	$mode = $in{'mode'};
	if ($buf) { return 1; } else { return 0; }
}

#-------------------------------------------------
#  HTML�w�b�_�[
#-------------------------------------------------
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>���J�E���^</title></head>
<body>
EOM
}

#-------------------------------------------------
#  �f�[�^�f�B���N�g������
#-------------------------------------------------
sub datadir {
	my @dir;

	## �f�[�^�f�B���N�g���Ǎ�
	# (1) opendir�֐�
	if (opendir(DIR,"$datadir")) {
		@dir = readdir(DIR);
		closedir(DIR);

	# (2) chdir�֐�
	} else {
		my $dir = $ENV{'SCRIPT_FILENAME'};
		$dir =~ s/[^\\\/]*$//;

		chdir($datadir) || &error("Dir Error : $datadir");
		@dir = <*>;
		if ($dir[0] eq '') {
			my $ls = `ls`;
			@dir = split(/\s+/, $ls);

		}
		chdir($dir);
	}
	# ���O�`�F�b�N
	my @file;
	foreach (@dir) {
		if (/.+\.dat$/) { push(@file,$_); }
	}
	return @file;
}


1;

