#!/usr/local/bin/perl -T

print "Content-type:text/html\n\n";

&Parse_Form;


$file=$formdata{'name'};
$comments=$formdata{'comments'};

if ($file=~/^(\w+)$/) {
	$file=$1;
	
	open (FILE, ">>$file.txt") || &Error("to write");
	print FILE "$comments\n";
	
	open (FILE, "$file.txt") || &Error("to read");
	@lines = <FILE>;
	close FILE;
	 
	 
	foreach $line (@lines) {
	 	print "<P>$line";
	 }

	 }else {
	print "error with test $file";
	}


		
		
sub Error {
	print "An error occurred on opening file $_[0]";
	exit;
		}
sub Parse_Form {
	if ($ENV{'REQUEST_METHOD'} eq 'GET') {
		@pairs = split(/&/, $ENV{'QUERY_STRING'});
	} elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
		read (STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		@pairs = split(/&/, $buffer);
		
		if ($ENV{'QUERY_STRING'}) {
			@getpairs =split(/&/, $ENV{'QUERY_STRING'});
			push(@pairs,@getpairs);
			}
	} else {
		print "Content-type: text/html\n\n";
		print "<P>Use Post or Get";
	}

	foreach $pair (@pairs) {
		($key, $value) = split (/=/, $pair);
		$key =~ tr/+/ /;
		$key =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	
		$value =~s/<!--(.|\n)*-->//g;
	
		if ($formdata{$key}) {
			$formdata{$key} .= ", $value";
		} else {
			$formdata{$key} = $value;
		}
	}
}	
1;
