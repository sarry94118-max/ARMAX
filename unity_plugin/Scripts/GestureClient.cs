using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

namespace OpenGestureXR
{
    /// <summary>
    /// Polls the Gesture API every 500ms and broadcasts gesture events.
    /// </summary>
    public class GestureClient : MonoBehaviour
    {
        [Tooltip("Gesture API endpoint")]
        public string apiUrl = "http://localhost:8000/gesture";

        // Polling interval: 500ms as required
        private const float PollInterval = 0.5f;

        /// <summary>Fired whenever a gesture response is received.</summary>
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
                yield return FetchGesture();
                yield return new WaitForSeconds(PollInterval);
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
