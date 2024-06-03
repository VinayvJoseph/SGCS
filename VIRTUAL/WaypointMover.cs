using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*
 * This script moves the truck on the selected path (path Index) and stops when reaches the bin set, then returns to the treatment plant
*/

public class WaypointMover : MonoBehaviour
{
   

    [SerializeField]  private WayPoints[] waypointScript; // An array to hold multiple waypoint paths
    private int currentPathIndex = 0; // Index of the currently selected path


    [SerializeField] private float moveSpeed = 1000f;

    [Range(1f, 500f)]
    [SerializeField] private float distanceThreshold = 20f;
    [Range(1f, 10f)]
    [SerializeField] private float waitTime = 2.0f;
    [SerializeField] GameObject[] cube;
    //public float dis;
    private float timer = 0f;
    public bool isWaiting = false;
    public float dis;
    public bool pathComplete = false, moving = false;

    private Transform currentWaypoint;
    // Start is called before the first frame update
    void Start()
    {
        currentWaypoint = waypointScript[currentPathIndex].GetNextWayPoint(currentWaypoint); // getting the transform of the first waypoint and moving the truck to starting point
        transform.position = currentWaypoint.position;

        currentWaypoint = waypointScript[currentPathIndex].GetNextWayPoint(currentWaypoint);
        transform.LookAt(currentWaypoint);
        
    }
    //function to move truck to the input path index
    public void MoveTruck(int currentPathIndex)
    {

        pathComplete = false;
        moving = true;
        if (!isWaiting)
        {
            AudioManager.Instance.PlaySFX("TruckDriving");

            transform.position = Vector3.MoveTowards(transform.position, currentWaypoint.position, moveSpeed * Time.deltaTime);

            if (Vector3.Distance(transform.position, currentWaypoint.position) < distanceThreshold)
            {
                currentWaypoint = waypointScript[currentPathIndex].GetNextWayPoint(currentWaypoint);
                transform.LookAt(currentWaypoint);
            }
            //check for the distance of truck against the bin set locator
            dis = Vector3.Distance(transform.position, cube[currentPathIndex].transform.position);

            if (dis < distanceThreshold)
            {
                isWaiting = true;
                timer = 0f;
                
                AudioManager.Instance.StopSFX("TruckDriving");
                AudioManager.Instance.PlaySFX("TruckIdle");
            }


        }

                          
        else
        {

            timer += Time.deltaTime;
            // AudioManager.Instance.PlaySFX("TruckIdle");
            if (timer >= waitTime)
            {
                isWaiting = false;
            }

        } 

        if (waypointScript[currentPathIndex].lastWayPoint)
        {
            pathComplete = true;
            moving = false;
        }


        // Example: Switch to a different path when the player presses a key
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SwitchToPath((currentPathIndex + 1) % waypointScript.Length);
        }

        Debug.Log("path index" + currentPathIndex);
    }

    //setting truck to starting point of the path
    public void ResetTruckPath(int currentPathIndex)
    {
        currentWaypoint = waypointScript[currentPathIndex].GetNextWayPoint(null); // getting the transform of the first waypoint and moving the truck to starting point
        transform.position = currentWaypoint.position;

        currentWaypoint = waypointScript[currentPathIndex].GetNextWayPoint(currentWaypoint);
        transform.LookAt(currentWaypoint);
        moving = false;
        pathComplete = false;
    }
       

    // Function to switch to a different path based on its index
    void SwitchToPath(int newPathIndex)
    {
        if (newPathIndex >= 0 && newPathIndex < waypointScript.Length)
        {
            currentPathIndex = newPathIndex;
            currentWaypoint = waypointScript[currentPathIndex].GetNextWayPoint(null);
            transform.position = currentWaypoint.position;
            currentWaypoint = waypointScript[currentPathIndex].GetNextWayPoint(currentWaypoint);
            transform.LookAt(currentWaypoint);
        }
    }
}
