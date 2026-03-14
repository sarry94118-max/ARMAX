using UnityEngine;

namespace OpenGestureXR
{
    /// <summary>
    /// Maps gesture events from GestureClient to XR object interactions.
    /// Attach to any interactable object.
    /// </summary>
    public class ObjectInteractor : MonoBehaviour
    {
        [Tooltip("Transform to attach the object to when grabbed (e.g. XR camera or hand anchor)")]
        public Transform handAnchor;

        private bool _isGrabbed;
        private Vector3 _originalPosition;
        private Quaternion _originalRotation;

        private void OnEnable()  => GestureClient.OnGestureReceived += HandleGesture;
        private void OnDisable() => GestureClient.OnGestureReceived -= HandleGesture;

        private void Start()
        {
            _originalPosition = transform.position;
            _originalRotation = transform.rotation;
        }

        private void HandleGesture(string gesture, float confidence)
        {
            switch (gesture)
            {
                case "grab":      Grab();      break;
                case "open_hand": Release();   break;
                case "pinch":     Select();    break;
                case "point":     Highlight(); break;
            }
        }

        private void Grab()
        {
            if (_isGrabbed || handAnchor == null) return;
            _isGrabbed = true;
            transform.SetParent(handAnchor, worldPositionStays: true);
            Debug.Log("[ObjectInteractor] Grabbed");
        }

        private void Release()
        {
            if (!_isGrabbed) return;
            _isGrabbed = false;
            transform.SetParent(null);
            Debug.Log("[ObjectInteractor] Released");
        }

        private void Select()
        {
            Debug.Log($"[ObjectInteractor] Selected: {gameObject.name}");
            // Extend: trigger selection highlight, UI, etc.
        }

        private void Highlight()
        {
            Debug.Log($"[ObjectInteractor] Highlighted: {gameObject.name}");
            // Extend: outline shader, tooltip, etc.
        }
    }
}
