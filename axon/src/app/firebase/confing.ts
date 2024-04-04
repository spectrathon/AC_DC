// Import the functions you need from the SDKs you need
import { initializeApp, getApps, getApp } from "firebase/app";
import {getFirestore} from 'firebase/firestore'
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDD9Qhfd0pwTvNWEEIS_tR--pqc4p2MW0o",
  authDomain: "gec-spectra.firebaseapp.com",
  databaseURL: "https://gec-spectra-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "gec-spectra",
  storageBucket: "gec-spectra.appspot.com",
  messagingSenderId: "119385456378",
  appId: "1:119385456378:web:6e372f3afca5dc3edcd343"
};

// Initialize Firebase
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp()

const db = getFirestore(app);

export {db}