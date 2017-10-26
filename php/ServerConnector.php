<?php

class ServerConnector
{
    public $address = null;
    public $service_port = null;
    public $socket = null;
    public function ServerConnector()
    {
        $this->address = "192.168.1.27"; //"127.0.0.1";
        $this->service_port = 666; //DOOM

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

    public function GetData()
    {
        $bytes = array();
        $bytes[] = 1;       #length
        $bytes[] = 60;       #PHP_Get_All

        socket_write($this->socket,$this->BytesToString($bytes));
        $data = socket_read($this->socket,2048);
        socket_close($this->socket);
        return $this->DataToArray($data);
    }

    public function DataToArray($data)
    {
        $i = 0;
        $counter = 0;
        $result = array();
        foreach(str_split($data) as $byte)
        {
            $byteval = unpack("S",$byte."\x00")[1];
            switch($i)
            {
                case 0:
                    $result[$counter] = array();
                    $result[$counter]['id'] = $byteval;
                    $i++;
                    break;
                case 1:
                    $result[$counter]['alarm_triggered'] = $byteval;
                    $i++;
                    break;
                case 2:
                    $result[$counter]['breached'] = $byteval;
                    $i++;
                    break;
                case 3:
                    $result[$counter]['armed'] = $byteval;
                    $i = 0;
                    $counter++;
                    break;
            }
        }
        return $result;
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
}




