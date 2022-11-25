using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CityMaker : MonoBehaviour
{
    [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject buildingPrefab;
    [SerializeField] GameObject buildingPrefab2;
    //[SerializeField] GameObject buildingPrefab3;
    [SerializeField] GameObject buildingPrefab4;
    [SerializeField] GameObject buildingPrefab5;
    [SerializeField] GameObject apartmentPrefab;
    [SerializeField] GameObject gasPrefab;
    [SerializeField] GameObject estadioPrefab;
    [SerializeField] GameObject grassPrefab;
    [SerializeField] GameObject treePrefab;
    [SerializeField] GameObject semaphorePrefab;
   

    [SerializeField] int tileSize;

    List<GameObject> prefabs;

    // Start is called before the first frame update
    void Start()
    { 
        prefabs = new List<GameObject> {buildingPrefab, buildingPrefab2, buildingPrefab4, buildingPrefab5, apartmentPrefab, gasPrefab};
        MakeTiles(layout.text);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 2;
        Debug.Log(y);

        Vector3 position;
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == '>' || tiles[i] == '<')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                //tile.transform.parent = transform;
                x += 1;
            }
            else if (tiles[i] == 'v' || tiles[i] == '^')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                //tile.transform.parent = transform;
                x += 1;
            }
            else if (tiles[i] == 'c')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                //tile.transform.parent = transform;
                x += 1;
            }
            else if (tiles[i] == 's')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                tile = Instantiate(semaphorePrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            }
            else if (tiles[i] == 'S')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            }
            else if (tiles[i] == 'D')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(grassPrefab, position, Quaternion.identity);
                tile = Instantiate(buildingPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.GetComponent<Renderer>().materials[0].color = Color.red;
                tile.transform.parent = transform;
                x += 1;
            }
            else if (tiles[i] == '#')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(grassPrefab, position, Quaternion.identity);
                System.Random rnd = new System.Random();
                int randIndex = rnd.Next(prefabs.Count);
                tile = Instantiate(prefabs[randIndex], position, Quaternion.identity);
                //tile.transform.localScale = new Vector3(1, 1, 1);
                tile.transform.parent = transform;
                x += 1;
            }
            else if (tiles[i] == 'E')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(grassPrefab, position, Quaternion.identity);
                tile = Instantiate(estadioPrefab, position, Quaternion.identity);
                //tile.transform.localScale = new Vector3(1, 1, 1);
                tile.transform.parent = transform;
                x += 1;
            }
            else if (tiles[i] == 'e')
            {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(grassPrefab  , position, Quaternion.identity);
                tile = Instantiate(treePrefab, position, Quaternion.identity);
                //tile.transform.localScale = new Vector3(1, 1, 1);
                tile.transform.parent = transform;
                x += 1;
            }else if (tiles[i] == '\n')
            {
                x = 0;
                y -= 1;
            }
        }

    }
}
