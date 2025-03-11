using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Diagnostics;
using Unity.Collections.LowLevel.Unsafe;

public class PlayerManager : MonoBehaviour
{
    [SerializeField] private Tile selectedTile;
    [SerializeField] private PlayerMode playerMode;
    private List<Player> players = new List<Player>();
    private GridManager gridManager;
    private GameManager gameManager;
    public PlayerMode GetPlayerMode => players[((gameManager.turnOff-1))].GetPlayerMode;
    public Tile GetTile => selectedTile;
    public List<Player> GetPlayers => players;

    public void Start(){
        var player1 = new Player("Player 1", 1);
        var player2 = new Player("Player 2", 2);
        players.Add(player1);
        players.Add(player2);
        LoadDeck(players[0], "DeckSet1", false);
        LoadDeck(players[1], "DeckSet2", true);
        gridManager = FindObjectOfType<GridManager>();
        gameManager = FindAnyObjectByType<GameManager>();
    }

    public void SelectTile(Tile tile){
        if (players[(gameManager.turnOff-1)].GetPlayerMode != PlayerMode.MovingPiece){
            selectedTile = tile;
        }
    }

    public void DeselectPiece(){
        DeselectTile();
        gridManager.ResetTiles();
    }

    public void MovePiece(GameObject newTile){
        var piece = selectedTile.GetPiece();
        piece.GetComponent<Piece>().Moved();
        newTile.GetComponent<Tile>().AddPiece(piece);
        selectedTile.RemovePiece();
        DeselectTile();
        gridManager.ResetTiles();
    }

    public void DeselectTile(){
        selectedTile = null;
        SwitchPlayerMode(PlayerMode.None);
    }

    public void SwitchPlayerMode(PlayerMode mode){
        players[(gameManager.turnOff-1)].SetPlayerMode(mode);
    }

    public void LoadDeck(Player player, string name, bool reversed){
        string filePath = "Assets/Json/" + name + ".json";
        string json = File.ReadAllText(filePath);
        Deck _deck = JsonUtility.FromJson<Deck>(json);
        if (reversed){
            for (int i = 0; i < _deck.cards.Count; i++)
            {
                _deck.cards[i].y = (7 - int.Parse(_deck.cards[i].y)).ToString();
            }
        }
        player.SetDeck(_deck);
    }
    
}