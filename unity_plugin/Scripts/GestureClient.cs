using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace OpenGestureXR
{
    /// <summary>
    /// Polls the Gesture API and exposes the latest gesture via event.
    /// </summary>
    public class GestureClient : MonoBehaviour
    {
        [Tooltip("Base URL of the Gesture API server")]
        public string apiUrl = "http://localhost:8000/gesture";

        [Tooltip("Polling interval in seconds")]
        public float pollInterval = 0.05f; // ~20 Hz

        public static event Action<string, float> OnGestureReceived;

        [Serializable]
        private class GestureResponse
        {
            public string gesture;
            public float confidence;
        }

        private void Start() => StartCoroutine(PollLoop());

        private IEnumerator PollLoop()
        {
            while (true)
            {
                yield return StartCoroutine(FetchGesture());
                yield return new WaitForSeconds(pollInterval);
            }
        }

        private IEnumerator FetchGesture()
        {
            using var req = UnityWebRequest.Get(apiUrl);
            yield return req.SendWebRequest();

            if (req.result == UnityWebRequest.Result.Success)
            {
                var data = JsonUtility.FromJson<GestureResponse>(req.downloadHandler.text);
                OnGestureReceived?.Invoke(data.gesture, data.confidence);
            }
            else
            {
                Debug.LogWarning($"[GestureClient] Request failed: {req.error}");
            }
        }
    }
}
