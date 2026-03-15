using UnityEngine;

namespace OpenGestureXR
{
    /// <summary>
    /// Maps gesture events to Unity object actions.
    /// Attach to any interactable GameObject (Cube, Sphere, etc.).
    /// </summary>
    public class ObjectInteractor : MonoBehaviour
    {
        [Tooltip("Hand anchor transform — object attaches here on grab")]
        public Transform handAnchor;

        private bool _isGrabbed;

        private void OnEnable()  => GestureClient.OnGestureReceived += HandleGesture;
        private void OnDisable() => GestureClient.OnGestureReceived -= HandleGesture;

        private void HandleGesture(string gesture, float confidence)
        {
            switch (gesture)
            {
                case "grab":      Grab();      break;  // attach object to hand
                case "open_hand": Release();   break;  // detach object
                case "pinch":     Select();    break;  // select object
                case "point":     Highlight(); break;  // highlight object
            }
        }

        /// <summary>Attach this object to the hand anchor.</summary>
        private void Grab()
        {
            if (_isGrabbed || handAnchor == null) return;
            _isGrabbed = true;
            transform.SetParent(handAnchor, worldPositionStays: true);
            Debug.Log($"[ObjectInteractor] Grabbed: {gameObject.name}");
        }

        /// <summary>Detach this object from the hand anchor.</summary>
        private void Release()
        {
            if (!_isGrabbed) return;
            _isGrabbed = false;
            transform.SetParent(null);
            Debug.Log($"[ObjectInteractor] Released: {gameObject.name}");
        }

        /// <summary>Select this object (extend with UI/highlight logic).</summary>
        private void Select()
        {
            Debug.Log($"[ObjectInteractor] Selected: {gameObject.name}");
        }

        /// <summary>Highlight this object (extend with outline shader).</summary>
        private void Highlight()
        {
            Debug.Log($"[ObjectInteractor] Highlighted: {gameObject.name}");
        }
    }
}
