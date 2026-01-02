// This file should be in .gitignore - DO NOT commit to GitHub

// Google OAuth Configuration
const OAUTH_CONFIG = {
    google: {
        clientId: '923288694940-l5liaa2nc9jih5546dopjeg605berlb0.apps.googleusercontent.com',
        redirectUri: window.location.origin + '/auth/google/callback',
        scope: 'openid email profile'
    }
};

// Firebase Configuration
const FIREBASE_CONFIG = {
    apiKey: "AIzaSyB7qdItzZqtnt-WaDtXnot8RuARmzGJ-o0",
    authDomain: "finance-prepayment-7838d.firebaseapp.com",
    projectId: "finance-prepayment-7838d",
    storageBucket: "finance-prepayment-7838d.firebasestorage.app",
    messagingSenderId: "921714152708",
    appId: "1:921714152708:web:74a758c6a01806fe0a6c51",
    measurementId: "G-137PH0KMCQ"
};