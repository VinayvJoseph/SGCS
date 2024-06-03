using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;


/*
 * This script switches the display screen to physical and simulation screens
 */


public class SwitchScenes : MonoBehaviour
{

    public GameObject SimCanvas, houseCanvas;
    [SerializeField] private Sprite[] buttonSprites;
    [SerializeField] private Image targetButton;
    [SerializeField] private Image Background;
    [SerializeField] private Text buttonText;
    [SerializeField] private Image targetButton1, targetButton2;
    [SerializeField] private Image Background1;
    [SerializeField] private Text buttonText1;
    public bool SimisActive;

    public void toPanel() //load panel scene
    {
        SceneManager.LoadScene(1);
        AudioManager.Instance.PlaySFX("CityView");
    }

    public void toCity() //load main scene
    {
        SceneManager.LoadScene(0);
        AudioManager.Instance.PlaySFX("CityView");
    }

    //Toggle button function to on and off simulation slider screen
    public void ToggleSimScreen() 
    {
        //Check object Sim Canvas in the inspector (Unity->project->window->inspector)
        if (SimCanvas != null)
        {
            SimisActive = SimCanvas.activeSelf; 
            SimCanvas.SetActive(!SimisActive);
            Background.enabled = !SimisActive;
        }

        if(targetButton.sprite == buttonSprites[0])
        {
            targetButton.sprite = buttonSprites[1];
            buttonText.text = "City view";
            AudioManager.Instance.PlaySFX("CityView");
            return;
            
        }

        targetButton.sprite = buttonSprites[0];
        buttonText.text = "Simulation view";
        AudioManager.Instance.PlaySFX("CityView");

    }

    //Toggle button function to on and off simulation slider screen
    public void ToggleHouseScreen() 
    {

        if (houseCanvas != null)
        {
            bool isActive = houseCanvas.activeSelf;
            houseCanvas.SetActive(!isActive);
        }

        if(SimisActive== true)
        {
            if (targetButton1.sprite == buttonSprites[2])
            {
                targetButton1.sprite = buttonSprites[1];
                buttonText1.text = "City view";
                AudioManager.Instance.PlaySFX("CityView");
                return;

            }

            targetButton1.sprite = buttonSprites[2];
            buttonText1.text = "House Panel view";
            AudioManager.Instance.PlaySFX("CityView");

        }

    }
    //Toggle button to on and off simulation slider screen
    public void ToggleSimAndPanel() 
    {

        if ((SimCanvas != null) &&(houseCanvas != null))
        {
            SimisActive = SimCanvas.activeSelf;
            SimCanvas.SetActive(!SimisActive);
            Background.enabled = !SimisActive;

            //bool isActive = houseCanvas.activeSelf;
            houseCanvas.SetActive(SimisActive);
        }

        if (targetButton2.sprite == buttonSprites[0])
        {
            targetButton2.sprite = buttonSprites[2];
            buttonText.text = "City view";
            AudioManager.Instance.PlaySFX("CityView");
            return;

        }

        targetButton2.sprite = buttonSprites[0];
        buttonText.text = "Simulation view";
        AudioManager.Instance.PlaySFX("CityView");

    }

}
