
const firebaseConfig = {
    apiKey: "AIzaSyDEh1_Pk58sTtlgknCyEnUAzTn7UgDWBE8",
    authDomain: "busapp-7d45f.firebaseapp.com",
    databaseURL: "https://busapp-7d45f-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "busapp-7d45f",
    storageBucket: "busapp-7d45f.firebasestorage.app",
    messagingSenderId: "940862242108",
    appId: "1:940862242108:web:e673630f39652c5ce8b239",
    measurementId: "G-CV7D1S329V"
  };

firebase.initializeApp(firebaseConfig);
const db = firebase.database();
const busesRef = db.ref("buses");

// Callback registry for multiple consumers
const busCallbacks = [];

export function onBusesUpdate(callback) {
  busCallbacks.push(callback);
}

// Listen to Firebase
busesRef.on("value", snapshot => {
  const buses = snapshot.val() || {};
  busCallbacks.forEach(cb => cb(buses));
});