using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using System.Net;
using UnityEngine;
using System.Net.Sockets;
using Newtonsoft.Json;
using WebSocketSharp;
using UnityEngine.UI;


/*
 * This script is to send/receive panel-slider data to server through websocket  
 
*/

public class SendDataFromUnity : MonoBehaviour
{

    private WebSocket ws;
    private string jsonData, time;
    public Text Gt, Bt, Rt, HouseNo, Gl, Bl, Rl, Gh, Bh, Rh, Gwt, Bwt, Rwt, timeText,IP;
    public Slider levelSlider_g, levelSlider_b, levelSlider_r,humiditySlider_g, humiditySlider_r, humiditySlider_b,tempSlider_g, tempSlider_r,tempSlider_b;
    public float temp_g, temp_b, temp_r, lvl_g, lvl_b, lvl_r, hum_g, hum_b, hum_r,simMode =0,test=0;
    public CalculateWeight greenWeight, redWeight, blueWeight;
    public GameObject[] exclamation;
    public bool G_isFull = false, R_isFull=false, B_isFull=false;
    public WaypointMover Mover;
    //public string IP;

    private void Start()
    {
         
        try
        {
            ws = new WebSocket("ws://131.155.186.121:8080"); // (websocket://IP.address.of.server:port_number) 
            ws.OnMessage += OnMessage; //subscribe message event handler
            ws.OnError += OnError;  // Attach error event handler
            ws.OnClose += OnClose;  // Attach close event handler
            ws.Connect();
        }
        catch (Exception e)
        {
            Debug.LogError($"WebSocket connection error: {e}");
        }

        

    }

    //Function to activate Simulation mode - use function as action to button in unity
    public void onClick() 
    {
        simMode = 1;
        ws.Send("Simulation Mode"); //key to Raspbery-pi to stop snding data and start receving data
        ws.OnMessage -= OnMessage; //unscubscribe to message event handler to stop receiving message from server
        AudioManager.Instance.PlaySFX("SimMode");


    }

    // Function to deactivate Simulation mode - use function as action to button in unity
    public void offClick() 
    {

        ws.Send("Physical Mode"); //key to Raspbery-pi to start snding data and stop receving data
        simMode = 0;
        ws.OnMessage += OnMessage; //subscribe again to message event handler when changed from simulation to physical mode
        AudioManager.Instance.PlaySFX("PhysicalMode"); //add audio files in unity screen to game object
        
    }


    // Update is called once per frame
    void Update()
    {

        //System status in Physical mode - receive data from websockets and upate the displays
        if (simMode == 0)
        {
            Debug.Log("Physical " );
            ReceiveDisplay(); // received data sent to display in each house 

        }
        
        //System status in Simulation mode - update data from sliders and send data as JSON package to Raspbery-pi through websocket
        else
        {
            Debug.Log("Simulation  ");
            SendDisplay(); //Send data from simulation sliders to physical world
          
        }

        Debug.Log("full Status GBR" + G_isFull + "," + B_isFull + "," + R_isFull);

    }

    //FUnction create JSON data and send to websocket along with display
    public void SendDisplay() 
    {

        BinData dataToSend = new BinData //Serialized class with required data fromat
        {
            //Simulation slider Values - send to physical actuators
            Distance_Organic = levelSlider_g.value,
            Distance_Paper = levelSlider_b.value,
            Distance_PMD = levelSlider_r.value,

            Temperature_Organic = tempSlider_g.value,
            Temperature_Paper = tempSlider_b.value,
            Temperature_PMD = tempSlider_r.value,


            Humidity_Organic = humiditySlider_g.value,
            Humidity_Paper = humiditySlider_b.value,
            Humidity_PMD = humiditySlider_r.value,

            Organic_isFull = G_isFull,
            PMD_isFull = R_isFull,
            Paper_isFull = B_isFull


        };
        //Convert dictionary data to JSON format
        jsonData = JsonConvert.SerializeObject(dataToSend);
        
        //sendig converted data to Raspberi-pi through websocket
        ws.Send(jsonData);
        Debug.Log("sending data:" + dataToSend);

        //Updating local variables to update displays

        lvl_g = dataToSend.Distance_Organic;
        lvl_b = dataToSend.Distance_Paper;
        lvl_r = dataToSend.Distance_PMD;

        hum_b = dataToSend.Humidity_Organic;
        hum_g = dataToSend.Humidity_Paper;
        hum_r = dataToSend.Humidity_PMD;

        temp_g = dataToSend.Temperature_Organic;
        temp_b = dataToSend.Temperature_Paper;
        temp_r = dataToSend.Temperature_PMD;

        Gl.text = "Level:" + lvl_g.ToString();
        Bl.text = "Level:" + lvl_b.ToString();
        Rl.text = "Level:" + lvl_r.ToString();

        Gh.text = "Hum:" + hum_g.ToString();
        Bh.text = "Hum:" + hum_b.ToString();
        Rh.text = "Hum:" + hum_r.ToString();

        Gt.text = "Temp:" + temp_g.ToString();
        Bt.text = "Temp:" + temp_b.ToString();
        Rt.text = "Temp:" + temp_r.ToString();


        //Sending binFull status 
        if (lvl_g > 75)
        {
            G_isFull = true; // to be set false only when truck reached the spot and collected.
        }
        else
        {
            G_isFull = false;
           // exclamation[0].SetActive(false);
        }

        if (lvl_b > 75)
        {
            B_isFull = true; // to be set false only when truck reached the spot and collected.
           // exclamation[1].SetActive(true);
        }
        else
        {
            B_isFull = false;
           // exclamation[1].SetActive(false);
        }

        if (lvl_r > 75)
        {
            R_isFull = true; // to be set false only when truck reached the spot and collected.
            //exclamation[2].SetActive(true);
        }
        else
        {
            R_isFull = false;
           // exclamation[2].SetActive(false);
        }
        exclamation[0].SetActive(G_isFull);
        exclamation[1].SetActive(B_isFull);
        exclamation[2].SetActive(R_isFull);

    }

    //Updates unity display based on physical entity
    public void ReceiveDisplay()
    {
        // updating slider with received data 
        levelSlider_g.value = lvl_g;
        levelSlider_b.value = lvl_b;
        levelSlider_r.value = lvl_r;

        humiditySlider_b.value = hum_b;
        humiditySlider_g.value = hum_g;
        humiditySlider_r.value = hum_r;

        tempSlider_g.value = temp_g;
        tempSlider_b.value = temp_b;
        tempSlider_r.value = temp_r;


        // print text box based on received data
        Gt.text = "Temp:" + temp_g.ToString();
        Bt.text = "Temp:" + temp_b.ToString();
        Rt.text = "Temp:" + temp_r.ToString();

        Gl.text = "Level:" + lvl_g.ToString();
        Bl.text = "Level:" + lvl_b.ToString();
        Rl.text = "Level:" + lvl_r.ToString();

        Gh.text = "Hum:" + hum_g.ToString();
        Bh.text = "Hum:" + hum_b.ToString();
        Rh.text = "Hum:" + hum_r.ToString();

        //update gameobject status to display warning
        exclamation[0].SetActive(G_isFull);
        exclamation[1].SetActive(B_isFull);
        exclamation[2].SetActive(R_isFull);


    }

    private void OnError(object sender, ErrorEventArgs e)
    {
        Debug.LogError($"WebSocket error: {e.Message}");
        // You can add more error handling logic here if needed
    }

    private void OnClose(object sender, CloseEventArgs e)
    {
        Debug.LogWarning($"WebSocket connection closed with code {e.Code}, reason: {e.Reason}");
        // You can add more logic for handling connection closure here
    }


    //Receiving data from Raspbery-pi through websocket
    public void OnMessage(object sender, MessageEventArgs e)
    {

        if (e.IsText)
        {
            //getting JSON data from server
            string sensorDataJson = e.Data;
            BinData sensorData = JsonConvert.DeserializeObject<BinData>(sensorDataJson);
        
            //storing values in global variables in client
            temp_g = sensorData.Temperature_Organic;
            temp_b = sensorData.Temperature_Paper;
            temp_r = sensorData.Temperature_PMD;

            lvl_g = sensorData.Distance_Organic;
            lvl_b = sensorData.Distance_Paper;
            lvl_r = sensorData.Distance_PMD;

            hum_g = sensorData.Humidity_Organic;
            hum_b = sensorData.Humidity_Paper;
            hum_r = sensorData.Humidity_PMD;

            G_isFull = sensorData.Organic_isFull;
            B_isFull = sensorData.Paper_isFull;
            R_isFull = sensorData.PMD_isFull;



        }
                     
        else
        {
            Debug.LogWarning("no data received");
        }
               
    }

    public void OnDestroy()
    {
        if (ws != null && ws.IsAlive)
        {
            ws.Close();
        }
    }
    
}

[Serializable]
public class BinData //data format received from WS-server
{
    public float Temperature_Organic { get; set; }
    public float Humidity_Organic { get; set; }
    public float Distance_Organic { get; set; }
    public float Temperature_Paper { get; set; }
    public float Humidity_Paper { get; set; }
    public float Distance_Paper { get; set; }
    public float Temperature_PMD { get; set; }
    public float Humidity_PMD { get; set; }
    public float Distance_PMD { get; set; }
    public string Timestamp { get; set; }
    public int House { get; set; }
    public bool Organic_isFull { get; set; }
    public bool PMD_isFull { get; set; }
    public bool Paper_isFull { get; set; }


}


