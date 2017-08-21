<!DOCTYPE html>
<html lang="en">
<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
<head><body>
<b align="left"><th>Serial no:</b></th><br>

<form action="excelReport.php" method="POST">
Serial Number:<input type="text" name="serialNo">
<input type="Submit" Name = "Download">
</form>

<form method="get" action="input.html">
<button type="submit" style="float:right;background-color:#4CAF50;border:none;color:white;padding:15px 40px;cursor:pointer;font-weight:bold;">New Test</button></form>
<h3><center>Compressor Test Log</center></h3>


<?php
$serial = $_POST["serialNo"];
echo $serial;
$fp = fopen("file2.json","w")or die("unable to open file");
$input = $serial;

$posts=array('serial'=>$input);
    $response=$posts;
    fwrite($fp,json_encode($response));
    fclose($fp);
?><br>
<style>
table {
    border-collapse: collapse;
}

th,td {
    padding:8px;
    text-align:left;
    border-bottom: 1px solid #ddd;
}
tr:nth-child(even){background-color: #f2f2f2}
</style>
</head>
<?php
$username="root";
$password="root";
$database="temp_database";
mysql_connect(localhost,$username,$password);
@mysql_select_db($database) or die( "Unable to select database");

//$query="SELECT * FROM tempLog ORDER BY Date DESC,Time DESC,SerialNo DESC,Bat_temp DESC, Milk_temp DESC,Aux_temp DESC,Comp_curr DESC, HP DESC, LP DESC temp_database.tempLog WHERE SerialNo='$input'" ;
//$query="SELECT * FROM tempLog WHERE SerialNo='".$serial."' ORDER BY Time DESC";
$query="SELECT * FROM tempLog WHERE SerialNo='".$serial."'";
$result=mysql_query($query);
$num=mysql_numrows($result);
mysql_close();
$tempValues = array();
?>
<table id="dataTbl"  cellspacing="14" cellpadding="10" style="width: 100%">
  
    <tr>
      <!--style="background-color: #00ff00;"-->
      <th><font face="Arial, Helvetica, sans-serif">Date</font></th>
      <th><font face="Arial, Helvetica, sans-serif">Time</font></th>
      <th><font face="Arial, Helvetica, sans-serif">Serial No</font></th>
      <th><font face="Arial, Helvetica, sans-serif">Brine out</font></th>
      <th><font face="Arial, Helvetica, sans-serif">Brine in</font></th>
      <th><font face="Arial, Helvetica, sans-serif">Ambient Temp</font></th>
      <th><font face="Arial, Helvetica, sans-serif">Comp Current</font></th>
      <th><font face="Arial, Helvetica. sans-serif">HP</font></th>
      <th><font face="Arial, Helvetica. sans-serif">LP</font></th>
    </tr>

<?php
$i=0;
while ($i < $num)
{
	$dateAndTemps = array();
	$f1=mysql_result($result,$i,"Date");
	$f2=mysql_result($result,$i,"Time");
        $f3=mysql_result($result,$i,"SerialNo");
	$f4=mysql_result($result,$i,"Bat_temp");
        $f5=mysql_result($result,$i,"Milk_temp");
	$f6=mysql_result($result,$i,"Aux_temp");
	$f7=mysql_result($result,$i,"Comp_curr");
	$f8=mysql_result($result,$i,"HP");
	$f9=mysql_result($result,$i,"LP");
?>
<tr>
<td><b><font face="Arial, Helvetica, sans-serif"><?php echo $f1 ;?></font></b></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $f2; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $f3; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $f4; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $f5; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $f6; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $f7; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $f8; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $f9; ?></font></td>
</td>
</tr>

<?php
$i++;}
?>
</table>
</body>
</html>
