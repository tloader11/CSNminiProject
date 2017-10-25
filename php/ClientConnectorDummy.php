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

        echo "OK.\n";

        echo "Attempting to connect to '$this->address' on port '$this->service_port'...";
        echo "OK.\n";

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
        $barcodes = [1719402,1687289,1718549];
        if(in_array($barcode,$barcodes))
        {
            $this->DisarmAlarm();
            return true;            //Valid barcode
        }
        return false;               //Wrong barcode
    }

}




