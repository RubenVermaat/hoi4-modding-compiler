using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraManager : MonoBehaviour
{
    public List<Cam> cameras;
    // Start is called before the first frame update
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.P))
        {
            if (!SwitchCamera("asdasdas")){
                SwitchCamera("Gameboard");
            } 
        }
    }


    /// <summary>
    /// Switches the active camera to the one with the specified ID.
    /// </summary>
    /// <param name="id">The ID of the camera to switch to.</param>
    /// <returns>True if the camera was found and switched to, false otherwise.</returns>
    public bool SwitchCamera(string id)
    {
        // Maybe this can be more efficient with a dictionary or something
        // Making sure you don't have to loop through them all
        // Although there won't be that many cameras anyway
        // I hope?
        bool camFound = false;
        foreach (Cam cam in cameras)
        {
            if (cam.id == id)
            {
                cam.camera.enabled = true;
                camFound = true;
            }
            else { cam.camera.enabled = false; }
        }
        return camFound;
    }
}

[System.Serializable]
public class Cam {
    public string id;
    public Camera camera;
}
