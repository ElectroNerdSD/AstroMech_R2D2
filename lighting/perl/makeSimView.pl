#! /usr/bin/perl -w 

use strict;
use Getopt::Long;

my $outfile = "small-ledDisplay.json";
my $style   = "serpentine-top-left";
my $rows    = "5";
my $columns = "8";
my $xSpace  = "2";
my $ySpace  = "2";
my $verbose;

GetOptions (
    "style=s"   => \$style,
    "output=s"  => \$outfile,
    "rows=s"    => \$rows,
    "columns=s" => \$columns,
    "xspace=s"  => \$xSpace,
    "yspace=s"  => \$ySpace,
    "verbose"   => sub { $verbose++ },
) or die("Error in command line arguments :$!\n");

unless($style =~ /(serpentine|justified)-(top|bottom)-(left|right)/) { die "ERROR: The style $style, you are using is not currently supported!\n" }

my $type      = $1;
my $topBottom = $2;
my $leftRight = $3;

print "*INFO: Writting $outfile in, $1 $2 $3 $columns x $rows\n";

open(JSON,">$outfile") || die "ERROR: Unable to open your json $outfile file for write, $!\n";

print JSON "[\n";

if($type eq "serpentine" ) { &createSerpentineLayout($topBottom,$leftRight,$rows,$columns,$xSpace,$ySpace,$verbose); }

print JSON "]\n";

close(JSON);

sub createSerpentineLayout() {

    my $topBottom = shift;
    my $leftRight = shift;
    my $rows      = shift;
    my $columns   = shift;
    my $xSpace    = sprintf("%1.4f",shift);
    my $ySpace    = sprintf("%1.4f",shift);
    my $verbose   = shift;

    if(defined $verbose) { print  "*INFO: Creating a serpentine layout starting at the $topBottom, on the $leftRight side of the board.\n" }
    
    #calculate the end points and spacing based on rows columns 
    my($xStart,$xEnd,$yStart,$yEnd) = &calculatePoints($xSpace,$columns,$ySpace,$rows,$verbose);

    my ($y0,$y1,$yspace) = $topBottom eq "top"  ?  ($yStart,$yEnd,sprintf("%1.4f",-1.0*$ySpace)) : ($yEnd,$yStart,$ySpace) ;
    my @yArray = &buildCoordArray($y0,$y1,$rows,$topBottom,$yspace,$verbose);

    my ($x0,$x1,$xspace) = $leftRight eq "left" ?  ($xEnd,$xStart,$xSpace) : ($xStart,$xEnd,sprintf("%1.4f",-1.0*$xSpace)) ;
    my @xArray = &buildCoordArray($x0,$x1,$columns,$leftRight,$xspace,$verbose);

    my $total_counter = 1;
    my $type_counter  = 0;
    foreach my $yCoord (@yArray) {
        my @tempxArray = $leftRight eq "left" && ${type_counter}%2 || $leftRight eq "right" && ${type_counter}%2 ? reverse(@xArray) : @xArray ;
        foreach my $xCoord (@tempxArray) {
            print JSON sprintf("    { \"point\": [%s,%s,0] }%s\n",$xCoord>=0 ? " $xCoord" : "$xCoord",$yCoord>=0 ? " $yCoord" : "$yCoord",$total_counter<=($rows*$columns)-1 ? "," : ""); 
            $total_counter++;
        }
        $type_counter++;
    }


}

sub buildCoordArray() {

    my $start   = shift;
    my $end     = shift;
    my $count   = shift;
    my $type    = shift;
    my $space   = shift;
    my $verbose = shift;

    my @coords = ();

    if(defined $verbose) { print "*INFO: building $type coords for starting $start, ending $end points, using spacing of $space.\n" } 

    for(my $i=$start; $space<0 ? $i>=$end : $i<=$end ; $i=sprintf("%1.4f",$i+$space)) {
      push(@coords,sprintf("%1.4f",$i));
    }

    if(defined $verbose) { print "*INFO: coordinates @coords\n" } 

    return(@coords);

}

sub calculatePoints() {

    my $xSpace  = shift;
    my $columns = shift;
    my $ySpace  = shift;
    my $rows    = shift;
    my $verbose = shift;

    if(defined $verbose) { print  "*INFO: Calculating points for number of points and space X:$columns,$xSpace : Y:$rows,$ySpace.\n" }

    my $numOfXSpaces = $columns-1;
    my $xStart = sprintf("%1.4f",($numOfXSpaces/2)*$xSpace);
    my $xEnd   = sprintf("%1.4f",$xStart*-1);

    my $numOfYSpaces = $rows-1;
    my $yStart = sprintf("%1.4f",($numOfYSpaces/2)*$ySpace);
    my $yEnd   = sprintf("%1.4f",$yStart*-1);

    if(defined $verbose) { print "*INFO: initial calculated X:$xStart, end point: $xEnd, spacing $xSpace\n"; }
    if(defined $verbose) { print "*INFO: initial calculated Y:$yStart, end point: $yEnd, spacing $ySpace\n"; }

    return($xStart,$xEnd,$yStart,$yEnd);

}
