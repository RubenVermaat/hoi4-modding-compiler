using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class MenuManager : MonoBehaviour
{
    [SerializeField] private GameObject menu;
    private CameraManager cameraManager;
    private GameManager gameManager;
    private GameSetupManager gameSetupManager;

    public void Start(){
        cameraManager = FindAnyObjectByType<CameraManager>();
        gameManager = FindAnyObjectByType<GameManager>();
        gameSetupManager = FindAnyObjectByType<GameSetupManager>();
    }
    public void StartFreeMatch()
    {
       gameManager.StartMatch();
       gameSetupManager.SetupPieces();
       cameraManager.SwitchCamera("Gameboard");
    }
}
