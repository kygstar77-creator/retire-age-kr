import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './fm-base.css';
import './ui/fm-ds.css';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
