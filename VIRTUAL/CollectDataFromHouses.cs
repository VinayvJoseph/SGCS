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
 * This script is to show the possible service that can be provided with the data collected from all houses in the vicinty
 * Service: Truck call to collect the trash to the speified house
 */

public class CollectDataFromHouses : MonoBehaviour
{

    public PanelControl[] House; //list of house panel in the city
    public ProvideService pathSelector; //variable to select the route 
    public string[] H1 ;
    public float[][] house1Temp;
    public float[][] house1Hum;
    public float[][] house1Lvl;
   
    // Start is called before the first frame update
    void Start()
    {

       
    }

    // Update is called once per frame
    void Update()
    {
        
        H1 = new string[House.Length];
        house1Temp = new float[House.Length][];
        house1Lvl = new float[House.Length][];
        house1Hum = new float[House.Length][];

        for (int i =0; i< House.Length;i++)
        {
            H1[i] = House[i].jsonData_house;
            ControlPanelData houseData = JsonConvert.DeserializeObject<ControlPanelData>(H1[i]);
            
            if (houseData != null)
            {

                if (i==houseData.Number) //storing temp , lvl and hum values from single couse in a single list
                {
                    house1Temp[houseData.Number] = houseData.Temperature;
                    house1Lvl[houseData.Number] = houseData.Distance;
                    house1Hum[houseData.Number] = houseData.Humidity;

                }
            }

            //Service implementation
            //setting path number for the truck to choose appropriate path from the waypoints laid- to travel and collect the waste from the bins
            if ((GetValueOf(houseData.Number, "Lvl", "Organic") > 75) && (GetValueOf(houseData.Number, "Lvl", "Paper") > 75 || GetValueOf(houseData.Number, "Lvl", "PMD") > 75))
            {
                pathSelector.index = houseData.Number; //List of path is set according to the house number in unity environment
            }
            if (pathSelector.setEmpty)
            {
                House[houseData.Number].levelSlider_g.value = 0;
                House[houseData.Number].levelSlider_b.value = 0;
                House[houseData.Number].levelSlider_r.value = 0;
            }
        }


        Debug.Log(GetValueOf(2,"Lvl" ,"Paper"));
      
    }

    //Function to get specific parameter value form the specified house number - useful for creating new service based on analysed data
    private float GetValueOf(int houseNumber,string parameter, string binType)
    {

        float requestedValue = 0;
        int count = 0;
        if (string.Equals(parameter, "Temp"))
        {

            if (string.Equals(binType, "Organic"))
            {
                count = 0;
            }
            if (string.Equals(binType, "Paper"))
            {
                count = 1;
            }
            if (string.Equals(binType, "PMD"))
            {
                count = 2;
            }
            requestedValue = house1Temp[houseNumber][count];
        }
        if (string.Equals(parameter, "Lvl"))
        {

            if (string.Equals(binType, "Organic"))
            {
                count = 0;
            }
            if (string.Equals(binType, "Paper"))
            {
                count = 1;
            }
            if (string.Equals(binType, "PMD"))
            {
                count = 2;
            }
            requestedValue = house1Lvl[houseNumber][count];
        }
        if (string.Equals(parameter, "Hum"))
        {

            if (string.Equals(binType, "Organic"))
            {
                count = 0;
            }
            if (string.Equals(binType, "Paper"))
            {
                count = 1;
            }
            if (string.Equals(binType, "PMD"))
            {
                count = 2;
            }
            requestedValue = house1Hum[houseNumber][count];
        }

        return requestedValue;
    }

   
}
