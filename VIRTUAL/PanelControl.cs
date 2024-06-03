using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using System.Net;
using UnityEngine;
using UnityEngine.UI;
using Newtonsoft.Json;
using System.Net.Sockets;
using System.Text;
using UnityEngine.SceneManagement;
using WebSocketSharp;

/*
 * This is a script for Panel as a gameobject - Displays and updates slider, texts and warning symbols
 * this gameobject instances are used for different houses
 */



public class PanelControl : MonoBehaviour
{

    private WebSocket ws;
    public Slider levelSlider_g, levelSlider_b, levelSlider_r, humiditySlider_g, humiditySlider_r, humiditySlider_b, tempSlider_g, tempSlider_r, tempSlider_b;
    public string jsonData_house;
    public Text Gt, Bt, Rt, HouseNo, Gl, Bl, Rl, Gh, Bh, Rh, Gwt, Bwt, Rwt, timeText;
    public bool G_isFull = false, R_isFull = false, B_isFull = false;
    public float temp_g, temp_b, temp_r, lvl_g, lvl_b, lvl_r, hum_g, hum_b, hum_r, simMode = 0, test = 0;
    [SerializeField] private Text number;
    public GameObject[] excMark;


    void Start()
    {
  

    }


    void Update()
    {       

        //Sending binFull status 
        if (lvl_g > 75)
        {
            G_isFull = true; // to be set false only when truck reached the spot and collected.
        }
        else
        {
            G_isFull = false;

        }

        if (lvl_b > 75)
        {
            B_isFull = true; // to be set false only when truck reached the spot and collected.
        }
        else
        {
            B_isFull = false;
        }

        if (lvl_r > 75)
        {
            R_isFull = true; // to be set false only when truck reached the spot and collected.
        }
        else
        {
            R_isFull = false;
        }

        CollectData();
        excMark[0].SetActive(G_isFull);
        excMark[1].SetActive(B_isFull);
        excMark[2].SetActive(R_isFull);

    }




    public void CollectData()
    {
        //converting the text box text into integer for using in other script
        int.TryParse(number.text, out int floatNumber);

        

        //converting slider values to JSON data
        ControlPanelData HouseDataToSend = new ControlPanelData
        {
            //Simulation slider Values - send to physical actuators
            Distance = new float[] { levelSlider_g.value, levelSlider_b.value, levelSlider_r.value },
            Temperature = new float[] { tempSlider_g.value, tempSlider_b.value, tempSlider_r.value },
            Humidity = new float[] { humiditySlider_g.value, humiditySlider_b.value, humiditySlider_r.value },
            Number = floatNumber,
            Organic_isFull = G_isFull,
            Paper_isFull = B_isFull,
            PMD_isFull = R_isFull
            
        };
        jsonData_house = JsonConvert.SerializeObject(HouseDataToSend);  //converting slider data into JSON format to send through websocket

        //Updating local variables to update displays
        lvl_g = HouseDataToSend.Distance[0];
        lvl_b = HouseDataToSend.Distance[1];
        lvl_r = HouseDataToSend.Distance[2];

        hum_g = HouseDataToSend.Humidity[0];
        hum_b = HouseDataToSend.Humidity[1];
        hum_r = HouseDataToSend.Humidity[2];

        temp_g = HouseDataToSend.Temperature[0];
        temp_b = HouseDataToSend.Temperature[1];
        temp_r = HouseDataToSend.Temperature[2];

        Gl.text = "Level:" + lvl_g.ToString();
        Bl.text = "Level:" + lvl_b.ToString();
        Rl.text = "Level:" + lvl_r.ToString();

        Gh.text = "Hum:" + hum_g.ToString();
        Bh.text = "Hum:" + hum_b.ToString();
        Rh.text = "Hum:" + hum_r.ToString();

        Gt.text = "Temp:" + temp_g.ToString();
        Bt.text = "Temp:" + temp_b.ToString();
        Rt.text = "Temp:" + temp_r.ToString();
        
    }

}

[Serializable]
public class ControlPanelData //data format received from WS-server
{
    public float[] Temperature { get; set; }
    public float[] Humidity { get; set; }
    public float[] Distance { get; set; }
    public int Number { get; set; }
    public bool Organic_isFull { get; set; }
    public bool PMD_isFull { get; set; }
    public bool Paper_isFull { get; set; }

}
