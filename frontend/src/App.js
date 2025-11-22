import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Dashboard from './components/Dashboard';
import ChatInterface from './components/ChatInterface';
import ThemeToggle from './components/ThemeToggle';
import { ThemeProvider } from './context/ThemeContext';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <div className="app">
        <ThemeToggle />
        <div className="app-container">
          <Dashboard />
          <ChatInterface />
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;

