<?php

class ClientConnector
{
    public $address = null;
    public $service_port = null;
    public $socket = null;
    public function ClientConnector()
    {
        $this->address = "127.0.0.1";
        $this->service_port = 667; //DOOM

        /* Create a TCP/IP socket. */
        $this->socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        if ($this->socket === false) {
            echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
        } else {
            echo "OK.\n";
        }

        echo "Attempting to connect to '$this->address' on port '$this->service_port'...";
        $result = socket_connect($this->socket, $this->address, $this->service_port);
        if ($result === false) {
            echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($this->socket)) . "\n";
        } else {
            echo "OK.\n";
        }
    }

    public function TriggerAlarm($type)
    {
        print("Sending alarm trigger.");
    }


    public function DisarmAlarm()
    {
        print("Alarm is now Disarmed!");
    }

    public function ArmAlarm()
    {
        print("Alarm is now armed!");
    }

    public function BytesToString($bytes)
    {
        $s = "";
        foreach($bytes as $byte)
        {
            $s .= chr($byte);
        }
        return $s;
    }

    public function CheckBarcode($barcode)
    {
        $barcodes = [1719402,1687289,1719406];
        if(in_array($barcode,$barcodes))
        {
            $this->DisarmAlarm();
            return true;            //Valid barcode
        }
        return false;               //Wrong barcode
    }

}




