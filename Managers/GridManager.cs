using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Tilemaps;

public class GridManager : MonoBehaviour
{
    [SerializeField] private int width, height;
    [SerializeField] private Tile tilePrefab;
    [SerializeField] private GameObject piecePrefab;
    [SerializeField] private GameObject gameBoard;
    private GameObject grid;
    private GameObject pieces;
    [SerializeField] private Transform cam;
    [SerializeField] private Color enemyColor;
    private PiecesManager piecesManager;
    private Dictionary<Vector2, Tile> tiles = new Dictionary<Vector2, Tile>();
    public Dictionary<Vector2, Tile> GetTiles => tiles;

    void Start() {
        grid = gameBoard.transform.Find("Grid").gameObject;
        pieces = gameBoard.transform.Find("Pieces").gameObject;
        piecesManager = FindObjectOfType<PiecesManager>();
    }

    public void GenerateGrid() {
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                //Create tile
                var spawnedTile = Instantiate(tilePrefab, new Vector3(x, y), Quaternion.identity);
                spawnedTile.name = $"Tile (X - {x}, Y - {y})";
                var isOffset = (x % 2 == 0 && y % 2 != 0) || (x % 2 != 0 && y % 2 == 0); //Is even or not
                spawnedTile.Init(isOffset);

                // Set the parent of tileObject to gridObject
                spawnedTile.transform.parent = grid.transform;

                //Add tile to Dictionary list
                tiles[new Vector2(x, y)] = spawnedTile;
            }
        }

        cam.transform.position = new Vector3((width - 1) / 2f, (height - 1) / 2f, -10f);
        piecesManager.LoadPieces();
    }

    public void AddPieceComponent(GameObject spawnedPiece, string id)
    {
        id = char.ToUpper(id[0]) + id.Substring(1);
        // Determine the component type name based on the card type
        string componentTypeName = id + "Piece";

        // Get the type of the component using reflection
        Type componentType = Assembly.GetExecutingAssembly()
                                     .GetTypes()
                                     .FirstOrDefault(t => t.Name == componentTypeName);

        // Add the component to the spawned piece if the type exists
        if (componentType != null && typeof(Component).IsAssignableFrom(componentType))
        {
            spawnedPiece.AddComponent(componentType);
        }
        else
        {
            Debug.LogError($"Component type '{componentTypeName}' not found.");
        }
    }

    public void PlaceStartPiece(Card card, Vector2 pos, int team){
        var spawnedPiece = Instantiate(piecePrefab, pos, Quaternion.identity);
        // Set the parent of spawnedPiece to piecesObject
        spawnedPiece.transform.parent = pieces.transform;
        AddPieceComponent(spawnedPiece, card.id);
        spawnedPiece.GetComponent<Piece>().SetTeam(team);
        spawnedPiece.GetComponent<Piece>().SetID(card.id);
        spawnedPiece.GetComponent<Piece>().SetWave(card.wave);
        if (team == 2){
            spawnedPiece.GetComponent<Piece>().SetDirection("down");
        }
        //Important, this has to be run as last
        spawnedPiece.GetComponent<Piece>().Setup();

        Tile _tile = GetTileAtPosition(pos);
        _tile.AddPiece(spawnedPiece.gameObject);
    }

    public void ResetTiles(){
        foreach (var tile in tiles.Values)
        {
            tile.ResetTile();
        }
    }

    public Tile GetTileAtPosition(Vector2 pos){
        if (tiles.TryGetValue(pos, out var tile)){
            return tile;
        }else{ return null; }
    }

    public GameObject CreateRandomPiece(){
        var spawnedPiece = Instantiate(piecePrefab, Vector3.zero, Quaternion.identity);
        return spawnedPiece.gameObject;
    }
}
