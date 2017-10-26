<?php
/**
 * Created by PhpStorm.
 * User: universal
 * Date: 10/26/2017
 * Time: 6:08 PM
 */

include_once('ServerConnector.php');

$server_connection = new ServerConnector(); //connects to alarm client

$data = $server_connection->GetData();

//print_r($data);


$tabledata = "";
foreach($data as $client)
{
    $id = $client['id'];
    $alarm_triggered = $client['alarm_triggered'];
    $breached = $client['breached'];
    $armed = $client['armed'];

    $status = "";
    if($armed==1 && $breached ==1 && $alarm_triggered ==1)
    {
        $status = "<td class = \"danger\"><span>Client Breached!</span></td>";
    }
    else if($armed==1 && $alarm_triggered ==1)
    {
        $status = "<td class = \"warning\"><span>Client Triggered!</span></td>";
    }
    else if($armed==1)
    {
        $status = "<td class = \"success\"><span>Client Armed.</span></td>";
    }
    else if($armed==0)
    {
        $status = "<td class = \"success\"><span>Client Disarmed.</span></td>";
    }

    $tabledata .= "<tr class=\"cID\"><td><span>$id</span></td>$status</tr>";
}



?>




<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="css/custom.css" >
    <title>Server GUI</title>
</head>
<body>
<div class="col-md-4 extrawidth"></div>
<div class = "container col-md-3">
    <table class = "table">
        <thead>
        <tr>
            <th>Client No.</th>
            <th>Client Status</th>
        </tr>
        </thead>
        <tbody>
        <?php print($tabledata); ?>
        </tbody>
    </table>
</div>

<script type="text/javascript">
setTimeout(function(){

window.location.replace("server.php");

}, 2000);

</script>

</body>
</html>
