using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/* 
 * 
 * This script aims to use data from the server and client and control truck service to follow best route and 
 * collect waste from bins that is full.  
 * Logic: if any two of the bins are full, then the truck reaches the 

 */


public class ProvideService : MonoBehaviour
{

    public SendDataFromUnity systemData;
    public WaypointMover Truck;
    public int index;

    private bool pathCompleted;
    private bool truckIsMoving;
    private bool ready = true;
    public bool setEmpty = false;


    // Update is called once per frame
    void Update()
    {
        if (systemData.simMode == 1 || systemData.simMode == 0)
        {
            if (!Truck.pathComplete)
            {
                if (systemData.lvl_g > 60 && (systemData.lvl_b >75 || systemData.lvl_r >75) && !Truck.moving)
                {                                 
                   Truck.MoveTruck(index); //Moves the truck along the index path , stops at the bin marker for 2 seconds then continues the travel and stops at the last waypoint.(Does not reset the path)
                }

                else if (Truck.moving)
                {
                    Truck.MoveTruck(index);  // waypoint in each index is the track provied as object in unity 
                    if (Truck.isWaiting)
                    {
                        setEmpty = true;
                        systemData.levelSlider_r.value = 0;
                        systemData.levelSlider_b.value = 0;
                        systemData.levelSlider_g.value = 0; //updating slider to 0 when truck reaches the marker
                    }
                }
                else
                {
                    
                }

            }
            else
            {
                Truck.ResetTruckPath(index);
                Debug.Log("stopped");
            }
            setEmpty = false;

        }
        else
        {
            Truck.ResetTruckPath(index);
        }
        
        Debug.Log("truck is moving: " + Truck.moving + "Path: " + Truck.pathComplete + "lvl_g :"+ systemData.lvl_g );
    }
         
}

