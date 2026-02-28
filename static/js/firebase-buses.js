

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.9.0/firebase-app.js";
import { getAuth, signInWithCustomToken, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/12.9.0/firebase-auth.js";
import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/12.9.0/firebase-database.js";

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
const app = initializeApp(firebaseConfig);

const auth = getAuth(app);
const db = getDatabase(app);
const busCallbacks = [];

export function onBusesUpdate(callback) {
  busCallbacks.push(callback);
}
function startListening() {
  const busesRef = ref(db, 'buses');
  onValue(busesRef, snapshot => {
    const buses = snapshot.val() || {};
    busCallbacks.forEach(cb => cb(buses));
  });
}

onAuthStateChanged(auth, (user) => {
  if (user) {
    console.log("Firebase remembers you! No need to login again.");
    startListening();
  } else {
    console.log("No Firebase session. Asking Django for a token...");
    
    // Fetch a fresh token from your new endpoint
    fetch('/dashboard/api/firebase-token/')
      .then(response => response.json())
      .then(data => {
        if (data.token) {
          return signInWithCustomToken(auth, data.token);
        } else {
          throw new Error("Django refused to give a token.");
        }
      })
      .then(() => {
        console.log("Successfully logged in with new token!");
        startListening();
      })
      .catch(error => console.error("Auth failed:", error));
  }
});
export async function logoutFirebase() {
  console.log('Signing you out of Firebase...');
  try {
    await signOut(auth);
    console.log('Firebase Sign-out successful.');
  } catch (error) {
    console.error('Firebase Signout failed', error);
  }
}