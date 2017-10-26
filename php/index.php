<?php
include_once('ClientConnector.php');

$client_connection = new ClientConnector(); //connects to alarm client

if(isset($_GET['q']))
{
    $value = $_GET['q'];
    switch($value)
    {
        case 0:
            $client_connection->ArmAlarm();
            header("Location: index.php");
            break;
        case 1:
            $client_connection->TriggerAlarm(2);
            header("Location: index.php");
            break;
        case 2:
            if(isset($_GET['code']) && $client_connection->CheckBarcode($_GET['code']))
            {
                $client_connection->DisarmAlarm();
            }
            header("Location: index.php");
            break;
        default:
            break;
    }
}


$status = $client_connection->GetStatus();

if($status==0)
{
    $armed = "Het systeem is gearmed.";
}
else if($status==1)
{
    $armed = "Het alarm gaat af!";
}
else if($status==2)
{
    $armed = "Het systeem is disarmed";
}

//include_once('ClientConnectorDummy.php');


//$client_connection->TriggerAlarm(3); //getal = trigger type
//type 1 =

//$client_connection->CheckBarcode(1719402); //returns True and links to Disarm

//$client_connection->CheckBarcode(1719466); //returns False and exits

//$client_connection->DisarmAlarm(); //Disarms the client. System Unlocked.

//$client_connection->ArmAlarm(); //Arms the client. Re-Arms the System. TriggerAlarm will work again after this one.


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
    <title>Client 2</title>
</head>
<body>
<div class="col-md-4 extrawidth"></div>
<div class = "container col-md-3">
    <table class = "table">
        <thead>
        <tr>
            <th>Client Interface</th>
        </tr>
        </thead>
        <tbody>
        <tr class = "success">
            <td><?php print($armed)?></td>
        </tr>
        </tbody>
    </table>
    <button type="button" class="btn btn-warning col-xs-2" id = "arm">Arm</button>
    <button type="button" class="btn btn-success disarm_button" id = "disarm">Disarm</button>
    <button type="button" class="btn btn-danger disarm_button" id = "trigger">Trigger</button>
</div>

</body>
</html>

<script type="text/javascript">

    if(<?php print($status); ?> != 2)
    {
        $(".success").removeClass( "success" ).addClass( "danger" );
    }

    $('#arm').on('click', function (e) {

        if(<?php print($status); ?> == 2){
            window.location.replace("index.php?q=0");
        }
        else{
            alert("Already armed!");
        }
    })
    $('#disarm').on('click', function (e) {

        if(<?php print($status); ?> != 2){

            var person = prompt("Enter your code");
            window.location.replace("index.php?q=2&code="+person);
        }
        else{
            alert("Already disarmed!");
        }
    });
    $('#trigger').on('click', function (e) {
        window.location.replace("index.php?q=1");
    });
    setTimeout(function(){

        window.location.replace("index.php");

    }, 7000);

</script>
<!--
<html style="background-color: red;">
    <body>
        <a href="index.php?q=0">Arm Alarm</a>
        <a href="index.php?q=1">Trigger Alarm</a>
        <a href="index.php?q=2">Disarm Alarm</a>
        <br><br><br>
        <div class="code_venster" style="background-color: white; width:50%;height:50%;margin:auto;">
            <input type="number" class="inputfield" style="margin-left:50px;margin-top:100px;" /><br>
            <span style="margin-left:50px;margin-top:10px;">The system is currently: <span class="status">---</span> </span>
        </div>
    </body>
</html>
-->