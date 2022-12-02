// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Noviembre 2022
// Autores: Jose Luis Madrigal, Cesar Emiliano Palome, Christian Parrish y Jorge Blanco
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;
    public bool desaparece;

    public AgentData(string id, float x, float y, float z, bool desaparece)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.desaparece = desaparece;
    }
}

[Serializable]
public class SemaforoData
{
    public string id, orientacion;
    public float x, y, z;
    public bool state;

    public SemaforoData(string id, float x, float y, float z, bool state, string orientacion)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state = state;
        this.orientacion = orientacion;
    }
}

public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

[Serializable]

public class SemaforosData
{
    public List<SemaforoData> positions;

    public SemaforosData() => this.positions = new List<SemaforoData>();
}


public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getObstaclesEndpoint = "/getSemaforos";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData;
    SemaforosData semaforosData;
    Dictionary<string, GameObject> agents, semaforosInstVerde, semaforosInstRojo;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, started = false;

    public GameObject car1, car2, car3,car4, semaforoVerdePrefab, semaforoRojoPrefab;
    public int NAgents, width, height, pasos;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    List<GameObject> cars;

    void Start()
    {
        cars = new List<GameObject> { car1, car2, car3, car4};

        agentsData = new AgentsData();
        semaforosData = new SemaforosData();
        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();
        agents = new Dictionary<string, GameObject>();
        semaforosInstVerde = new Dictionary<string, GameObject>();
        semaforosInstRojo = new Dictionary<string, GameObject>();

        //floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        //floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);

        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if (direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);

            }

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetSemaforosData());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetSemaforosData());
        }
    }

    IEnumerator GetAgentsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            Debug.Log(www.downloadHandler.text);

            foreach (AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, (float) 0, agent.z - 1);

                    if(!started)
                    {
                        prevPositions[agent.id] = newAgentPosition;
                        System.Random rnd = new System.Random();
                        int randIndex = rnd.Next(cars.Count);
                        agents[agent.id] = Instantiate(cars[randIndex], newAgentPosition, Quaternion.identity);
                    }
                    else
                    {
                        if (agent.desaparece is true){
                            Destroy(agents[agent.id]);
                            prevPositions.Remove(agent.id);
                            currPositions.Remove(agent.id);
                        }
                        else{
                            Vector3 currentPosition = new Vector3();
                            if(currPositions.TryGetValue(agent.id, out currentPosition))
                                prevPositions[agent.id] = currentPosition;
                                currPositions[agent.id] = newAgentPosition;
                        }
                    }
            }
        }
    }


    IEnumerator GetSemaforosData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            semaforosData = JsonUtility.FromJson<SemaforosData>(www.downloadHandler.text);

            Debug.Log(semaforosData.positions);

            foreach (SemaforoData semaforo in semaforosData.positions)
            {
                    if(!started)
                    {
                        if (semaforo.orientacion == "vertical"){
                            semaforosInstVerde[semaforo.id] = Instantiate(semaforoVerdePrefab, new Vector3(semaforo.x, semaforo.y -1, semaforo.z - (float).5), Quaternion.identity);
                            Debug.Log(semaforosInstVerde[semaforo.id]);
                            semaforosInstRojo[semaforo.id] = Instantiate(semaforoRojoPrefab, new Vector3(semaforo.x, semaforo.y - 1, semaforo.z - (float).5), Quaternion.identity);
                            Debug.Log(semaforosInstRojo[semaforo.id]);
                        }
                        else{
                        semaforosInstVerde[semaforo.id] = Instantiate(semaforoVerdePrefab, new Vector3(semaforo.x + (float).5, semaforo.y - 1, semaforo.z - (float)1.5), Quaternion.Euler(0, 90, 0));
                        Debug.Log(semaforosInstVerde[semaforo.id]);
                        semaforosInstRojo[semaforo.id] = Instantiate(semaforoRojoPrefab, new Vector3(semaforo.x + (float).5, semaforo.y - 1, semaforo.z - (float)1.5), Quaternion.Euler(0, 90, 0));
                        Debug.Log(semaforosInstRojo[semaforo.id]);
                    }
                }
                    else
                    {
                        if (semaforo.state is false){
                            semaforosInstVerde[semaforo.id].SetActive(false);
                            semaforosInstRojo[semaforo.id].SetActive(true);
                    }
                    else
                    {
                            semaforosInstVerde[semaforo.id].SetActive(true);
                            semaforosInstRojo[semaforo.id].SetActive(false);

                    }
                }
            }
            updated = true;
            if(!started) started = true;
        }
    }


}
