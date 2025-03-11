using System;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public int turnOff = 1;
    private PlayerManager playerManager;
    private GridManager gridManager;

    public void Start(){
        playerManager = FindObjectOfType<PlayerManager>();
        gridManager = FindObjectOfType<GridManager>();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.L))
        {
            gridManager.ResetTiles();
        }
    }

    public void StartMatch(){
        gridManager.GenerateGrid();
    }

    public void NextTurn()
    {
        CheckCheck();
        if (turnOff == playerManager.GetPlayers.Count){
            turnOff = 1;
        }else{
            turnOff++;
        }
        CheckCheck();
    }

    public void EnemyCover(){
        //Goes through all the tiles with pieces
        //Maps out covered area by enemy pieces
        foreach (var tile in gridManager.GetTiles.Values)
        {
            if (tile.GetPiece() != null)
            {
                var piece = tile.GetPiece();
                if (piece.GetComponent<Piece>().GetTeam != turnOff)
                {
                    if (piece.GetComponent<Piece>() != null)
                    {
                        piece.GetComponent<Piece>().PossibleMoves(MoveCheckType.Cover);
                    }
                }
            }
        }
    }

    public void CheckCheck(){
        EnemyCover();
        //Goes through all the covered tiles
        //Checks if one of those has the king
        foreach (var tile in gridManager.GetTiles.Values)
        {
            if (tile.GetPiece() != null)
            {
                if (tile.Covered){
                    var piece = tile.GetPiece();
                    if (piece.GetComponent<KingPiece>() != null)
                    {
                        Debug.Log("Check! " + turnOff);
                        if (!piece.GetComponent<KingPiece>().CanMove()){
                            Debug.Log("Checkmate! " + turnOff);
                        }
                    }
                }
            }
        }
        gridManager.ResetTiles();
    }

    public void CheckMate(){
        Debug.Log("Checkmate! " + turnOff);
    }
}