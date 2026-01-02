// This file should be in .gitignore - DO NOT commit to GitHub

// Google OAuth Configuration
const OAUTH_CONFIG = {
    google: {
        clientId: '',
        redirectUri: window.location.origin + '/auth/google/callback',
        scope: 'openid email profile'
    }
};

// Firebase Configuration
const FIREBASE_CONFIG = {
    apiKey: "",
    authDomain: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: "",
    measurementId: ""
};
