<?php

class ClientConnector
{
    public $address = null;
    public $service_port = null;
    public $socket = null;
    public function ClientConnector()
    {
        $this->address = "192.168.1.66"; //"127.0.0.1";
        $this->service_port = 667; //DOOM

        /* Create a TCP/IP socket. */
        $this->socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        if ($this->socket === false) {
            echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
        } else {
            //echo "OK.\n";
        }

        //echo "Attempting to connect to '$this->address' on port '$this->service_port'...";
        $result = socket_connect($this->socket, $this->address, $this->service_port);
        if ($result === false) {
            echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($this->socket)) . "\n";
        } else {
            //echo "OK.\n";
        }
    }

    public function TriggerAlarm($type)
    {
        $bytes = array();
        $bytes[] = 1;       #TriggerAlarm
        $bytes[] = $type;       #AlarmType

        socket_write($this->socket,$this->BytesToString($bytes));
    }


    public function DisarmAlarm()
    {
        $bytez = array();
        $bytez[] = 2;       #Disarm

        socket_write($this->socket,$this->BytesToString($bytez));
    }

    public function ArmAlarm()
    {
        $bytez = array();
        $bytez[] = 3;       #Disarm

        socket_write($this->socket,$this->BytesToString($bytez));
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

    public function GetStatus()
    {
        $s = chr(4);
        socket_write($this->socket,$s);
        return unpack("s",socket_read($this->socket,1,PHP_BINARY_READ)."\x00")[1];
    }

    public function CheckBarcode($barcode)
    {
        $barcodes = [1719402,1687289,1718549,1717261,"qqqq"];
        if(in_array($barcode,$barcodes))
        {
            $this->DisarmAlarm();
            return true;            //Valid barcode
        }
        return false;               //Wrong barcode
    }

}




