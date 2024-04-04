// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: process.env.FB_API,
  authDomain: "gec-spectra.firebaseapp.com",
  databaseURL: "https://gec-spectra-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "gec-spectra",
  storageBucket: "gec-spectra.appspot.com",
  messagingSenderId: "119385456378",
  appId: "1:119385456378:web:6e372f3afca5dc3edcd343"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);