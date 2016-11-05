#! /usr/bin/perl -w 

use strict;
use Getopt::Long;

my $outfile = "small-ledDisplay.json";
my $style   = "serpentine-top-left";
my $row     = "5";
my $column  = "8";
my $xRange  = "16";
my $yRange  = "10";
my $verbose;

GetOptions (
    "style=s"   => \$style,
    "output=s"  => \$outfile,
    "row=s"     => \$row,
    "column=s"  => \$column,
    "xrange=s"  => \$xRange,
    "yrange=s"  => \$yRange,
    "verbose"   => sub { $verbose++ },
) or die("Error in command line arguments :$!\n");

unless($style =~ /(serpentine|justified)-(top|bottom)-(left|right)/) { die "ERROR: The style $style, you are using is not currently supported!\n" }

my $type      = $1;
my $topBottom = $2;
my $leftRight = $3;

print "*INFO: Writting $outfile in, $1 $2 $3 $column x $row\n";

open(JSON,">$outfile") || die "ERROR: Unable to open your json $outfile file for write, $!\n";

if($type eq "serpentine" ) { &createSerpentineLayout($topBottom,$leftRight,$row,$column,$xRange,$yRange,$verbose); }

close(JSON);

sub createSerpentineLayout() {

    my $topBottom = shift;
    my $leftRight = shift;
    my $row       = shift;
    my $column    = shift;
    my $xRange    = shift;
    my $yRange    = shift;
    my $verbose   = shift;

    if(defined $verbose) { print  "*INFO: Creating a serpentine layout starting at the $topBottom, on the $leftRight side of the board.\n" }
    
    #calculate the end points and spacing based on row column 
    my($xStart,$xEnd,$xSpace,$yStart,$yEnd,$ySpace) = &calculateEndPointsAndSpace($row,$xRange,$column,$yRange,$verbose);

    my ($y0,$y1,$ySpace) = $topBottom eq "top"  ?  ($yEnd,$yStart,sprintf("%1.4f",-1.0*$ySpace)) : ($yStart,$yEnd,$ySpace) ;
    my ($x0,$x1,$xSpace) = $leftRight eq "left" ?  ($xStart,$xEnd,$xSpace) : ($xEnd,$xStart,sprintf("%1.4f",-1.0*$xSpace)) ;

    my @yArray = &buildCoordArray($y0,$y1,$topBottom,$ySpace,$verbose);
    my @xArray = &buildCoordArray($x0,$x1,$leftRight,$xSpace,$verbose);


}
sub buildCoordArray() {

    my $start   = shift;
    my $end     = shift;
    my $type    = shift;
    my $space   = shift;
    my $verbose = shift;

    if(defined $verbose) { print "*INFO: building $type coords for starting $start, ending $end points, using spacing of $space.\n" } 

    for(my $i=$start; $i!=$end; $i=$i+$space) {
      print  sprintf("i %1.4f\n",$i);
    }

}

sub calculateEndPointsAndSpace() {

    my $row     = shift;
    my $xRange  = shift;
    my $column  = shift;
    my $yRange  = shift;
    my $verbose = shift;

    if(defined $verbose) { print  "*INFO: Calculating max ranges and spaces for X:$column,$xRange : Y:$row,$yRange.\n" }

    my $xSpace = sprintf("%1.4f",($xRange*1.0)/($column*1.0));
    my $xEnd   = sprintf("%1.4f",($xRange*1.0)/2);
    my $xStart = sprintf("%1.4f",$xEnd*-1);

    my $ySpace = sprintf("%1.4f",($yRange*1.0)/($row*1.0));
    my $yEnd   = sprintf("%1.4f",($yRange*1.0)/2);
    my $yStart = sprintf("%1.4f",$yEnd*-1);

    if(defined $verbose) { print "*INFO: initial calculated X:$xStart, end point: $xEnd, spacing $xSpace\n"; }
    if(defined $verbose) { print "*INFO: initial calculated Y:$yStart, end point: $yEnd, spacing $ySpace\n"; }

    return($xStart,$xEnd,$xSpace,$yStart,$yEnd,$ySpace);

}
