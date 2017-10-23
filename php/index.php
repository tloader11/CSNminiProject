<?php
//include_once('ClientConnector.php');

include_once('ClientConnectorDummy.php');

$client_connection = new ClientConnector(); //connects to alarm client

$client_connection->TriggerAlarm(3); //getal = trigger type
//type 1 =

$client_connection->CheckBarcode(1719402); //returns True and links to Disarm

$client_connection->CheckBarcode(1719466); //returns False and exits

$client_connection->DisarmAlarm(); //Disarms the client. System Unlocked.

$client_connection->ArmAlarm(); //Arms the client. Re-Arms the System. TriggerAlarm will work again after this one.
